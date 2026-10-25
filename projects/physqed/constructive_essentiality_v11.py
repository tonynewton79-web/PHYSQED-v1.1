"""PHYSQED v1.1: exact rational counterexample for every essential premise.

A conditional extension of v1.0; accepts only already-verified contracts,
returns pointwise arithmetic witnesses, and NEVER upgrades physical/Lean claims.
"""
from __future__ import annotations
from fractions import Fraction

class WitnessRefusal(ValueError):
    pass

def add(a, b):
    out=dict(a)
    for m,coef in b.items():out[m]=out.get(m,Fraction(0))+coef
    return {m:coef for m,coef in out.items() if coef}

def mul(a,b,limit=512):
    out={}
    for x,coef in a.items():
        for y,c in b.items():
            exp=tuple(i+j for i,j in zip(x,y))
            out[exp]=out.get(exp,Fraction(0))+coef*c
            if len(out)>limit:raise WitnessRefusal("substitution term budget")
    return {m:c for m,c in out.items() if c}

def at(poly,x):
    result=Fraction(0)
    for mon,coef in poly.items():
        item=coef
        for a,p in zip(x,mon):item*=a**p
        result+=item
    return result

def affine_rref(gens,n):
    zero=(0,)*n; rows=[]
    for gen in gens:
        if any(sum(mon)>1 for mon in gen):raise WitnessRefusal("non-affine premise")
        normal=[gen.get(tuple(int(i==j) for i in range(n)),Fraction(0)) for j in range(n)]
        if not any(normal):raise WitnessRefusal("constant or zero premise")
        rows.append(normal+[-gen.get(zero,Fraction(0))])
    pivot_cols=[]; lead=0
    for col in range(n):
        pos=next((j for j in range(lead,len(rows)) if rows[j][col]),None)
        if pos is None:continue
        rows[lead],rows[pos]=rows[pos],rows[lead]
        q=rows[lead][col];rows[lead]=[c/q for c in rows[lead]]
        for j in range(len(rows)):
            if j!=lead and rows[j][col]:
                c=rows[j][col]
                rows[j]=[v-c*w for v,w in zip(rows[j],rows[lead])]
        pivot_cols.append(col)
        lead+=1
        if lead==len(rows):break
    if lead!=len(rows):raise WitnessRefusal("dependent remaining premises")
    return rows,pivot_cols

def restrict_target(target,rows,pivots,n):
    free=[i for i in range(n) if i not in pivots]
    d=len(free); zero=(0,)*d; substitute=[None]*n
    for pivot,row in zip(pivots,rows):
        expr={zero:row[-1]} if row[-1] else {}
        for j,idx in enumerate(free):
            if row[idx]:
                mon=tuple(int(v==j) for v in range(d))
                expr=add(expr,{mon:-row[idx]})
        substitute[pivot]=expr
    for j,idx in enumerate(free):
        substitute[idx]={tuple(int(v==j) for v in range(d)):Fraction(1)}
    ans={}
    for mon,coef in target.items():
        term={zero:coef}
        for idx,exp in enumerate(mon):
            for _ in range(exp):term=mul(term,substitute[idx])
        ans=add(ans,term)
        if len(ans)>512:raise WitnessRefusal("polynomial reduction term budget")
    return ans,free

def specialize(poly,i,value):
    out={}
    for m,c in poly.items():
        mon=m[:i]+(0,)+m[i+1:]
        out[mon]=out.get(mon,Fraction(0))+c*value**m[i]
    return {m:c for m,c in out.items() if c}

def rational_free_point(poly,d):
    if not poly:raise WitnessRefusal("not essential: restriction vanishes")
    remaining=dict(poly); point=[]
    for i in range(d):
        degree=max((m[i] for m in remaining),default=0)
        for v in range(degree+1):
            replacement=specialize(remaining,i,Fraction(v))
            if replacement:
                remaining=replacement;point.append(Fraction(v));break
        else:raise WitnessRefusal("finite-grid interpolation failure")
    if at(poly,point)==0:raise WitnessRefusal("proposed point not a counterexample")
    return point

def constructive_witnesses(names,gens,target):
    n=len(names)
    if len(set(names))!=n or not 2<=len(gens)<=4 or n<len(gens):
        raise WitnessRefusal("unsupported witness domain")
    records=[]
    for omit in range(len(gens)):
        rows,pivots=affine_rref([p for j,p in enumerate(gens) if j!=omit],n)
        reduced,free=restrict_target(target,rows,pivots,n)
        free_values=rational_free_point(reduced,len(free))
        point=[Fraction(0)]*n
        for idx,v in zip(free,free_values):point[idx]=v
        for pivot,row in zip(pivots,rows):
            point[pivot]=row[-1]-sum((row[j]*point[j] for j in free),Fraction(0))
        if any(at(p,point)!=0 for j,p in enumerate(gens) if j!=omit):
            raise WitnessRefusal("retained assumption fails at counterexample")
        omitted_residual=at(gens[omit],point)
        conclusion_residual=at(target,point)
        if not omitted_residual or not conclusion_residual:
            raise WitnessRefusal("counterexample fails to falsify conclusion")
        records.append({"dropped_premise":omit+1,
                        "assignment":{name:str(v) for name,v in zip(names,point)},
                        "dropped_premise_residual":str(omitted_residual),
                        "conclusion_residual":str(conclusion_residual),
                        "all_remaining_premises_satisfied":True})
    return records

def verify_and_construct(contract):
    """v1.0 scope and essentiality must be certified BEFORE witness extraction."""
    from multi_premise_v10 import verify
    from two_premise_claims import _read_formal
    from multi_premise_v10 import _add,_neg
    status=verify(contract)
    names=contract["variables"]
    gens=[_add(_read_formal(p["lhs"],names),_neg(_read_formal(p["rhs"],names)))
          for p in contract["premises"]]
    c=contract["conclusion"]
    target=_add(_read_formal(c["lhs"],names),_neg(_read_formal(c["rhs"],names)))
    records=constructive_witnesses(names,gens,target)
    return {"status":"CONSTRUCTIVE_AFFINE_ESSENTIALITY__PHYSICS_UNVERIFIED",
            "inherited_v10_contract_sha256":status["contract_sha256"],
            "premise_count":len(gens),"counterexamples":records,
            "lean_kernel_verified":False,"physical_law_proven":False,
            "independent_expert_semantics_verified":False}
