"""Independent SymPy rank, ideal essentiality, grammar and SI dimensional oracle.
Imports the case generator ONLY, not the PHYSQED v1.0 certificate verifier.
Gold labels are synthetic and internally generated, NOT external expert labels.
"""
import ast,json,sys
from pathlib import Path
from sympy import Symbol,Rational,Poly,Matrix,expand,groebner,QQ
ROOT=Path(__file__).resolve().parents[2]/"projects"/"physqed"
sys.path.insert(0,str(ROOT))
from benchmarks.multi_premise_v10 import cases

BASE=("M","L","T","I","Theta","N","J")
TAIL=" This checks only a conditional polynomial consequence; no physical law is established."

def formal(expr, names):
    if set(expr)=={"var"}:return names[expr["var"]]
    if set(expr)=={"const"}:return Rational(expr["const"])
    if expr.get("op")=="pow":return formal(expr["arg"],names)**expr["exp"]
    if expr.get("op")=="add":return sum(formal(x,names) for x in expr["args"])
    if expr.get("op")=="mul":
        out=Rational(1)
        for v in expr["args"]:out*=formal(v,names)
        return out
    raise ValueError("bad formal")

def parse(text,names):
    def go(n):
        if isinstance(n,ast.Name):return names[n.id]
        if isinstance(n,ast.Constant) and type(n.value) is int:return Rational(n.value)
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -go(n.operand)
        if isinstance(n,ast.BinOp):
            if isinstance(n.op,ast.Pow) and type(n.right.value) is int:
                return go(n.left)**n.right.value
            a,b=go(n.left),go(n.right)
            if isinstance(n.op,ast.Add):return a+b
            if isinstance(n.op,ast.Sub):return a-b
            if isinstance(n.op,ast.Mult):return a*b
        raise ValueError("uncontrolled text")
    return go(ast.parse(text,mode="eval").body)

def dim(n,types):
    if set(n)=={"var"}:return tuple(types[n["var"]].get(d,0) for d in BASE)
    if set(n)=={"const"}:return (0,)*len(BASE)
    if n.get("op")=="pow":return tuple(i*n["exp"] for i in dim(n["arg"],types))
    if n.get("op")=="mul":
        ds=[dim(x,types) for x in n["args"]]
        return tuple(sum(v) for v in zip(*ds))
    if n.get("op")=="add":
        ds=[dim(x,types) for x in n["args"]]
        if not all(x==ds[0] for x in ds):raise ValueError("mismatched units")
        return ds[0]
    raise ValueError("untyped expression")

def equality_dim(p,types,names):
    u=dim(p["lhs"],types);v=dim(p["rhs"],types)
    if expand(formal(p["lhs"],names))==0:u=v
    if expand(formal(p["rhs"],names))==0:v=u
    if u!=v:raise ValueError("equation is dimensionally inconsistent")
    return u

def check(c):
    if set(c)!={"schema","statement","variables","dimensions","premises","conclusion","witnesses","provenance"}:return False
    if c["schema"]!="physqed-multi-premise-v1.0" or c["provenance"]!="SYNTHETIC_SCOPED":return False
    vars=c["variables"];k=len(c["premises"])
    if not (2<=k<=4 and k<=len(vars)<=8 and len(c["witnesses"])==k):return False
    if set(c["dimensions"])!=set(vars):return False
    symbols={v:Symbol(v) for v in vars}
    pref="For all real scalars "+", ".join(vars)+", if "
    raw=c["statement"]
    if not raw.startswith(pref) or not raw.endswith(TAIL):return False
    body=raw[len(pref):-len(TAIL)]
    if body.count(", then ")!=1:return False
    antecedent,conclusion=body.split(", then ")
    if not conclusion.endswith(" holds."):return False
    segments=antecedent.split(" and ")+[conclusion[:-len(" holds.")]]
    if len(segments)!=k+1:return False
    equations=c["premises"]+[c["conclusion"]]
    for text,eq in zip(segments,equations):
        if text.count(" == ")!=1:return False
        lhs,rhs=text.split(" == ")
        if expand(parse(lhs,symbols)-formal(eq["lhs"],symbols))!=0:return False
        if expand(parse(rhs,symbols)-formal(eq["rhs"],symbols))!=0:return False
    gens=[expand(formal(p["lhs"],symbols)-formal(p["rhs"],symbols)) for p in c["premises"]]
    X=list(symbols.values())
    if any(Poly(p,*X).total_degree()>1 for p in gens):return False
    rows=[[p.diff(x) for x in X] for p in gens]
    if Matrix(rows).rank()!=k:return False
    target=expand(formal(c["conclusion"]["lhs"],symbols)-formal(c["conclusion"]["rhs"],symbols))
    witness=[formal(w,symbols) for w in c["witnesses"]]
    if expand(target-sum(w*p for w,p in zip(witness,gens)))!=0:return False
    premDims=[equality_dim(e,c["dimensions"],symbols) for e in c["premises"]]
    outDims=equality_dim(c["conclusion"],c["dimensions"],symbols)
    for wt,pd in zip(c["witnesses"],premDims):
        if tuple(a+b for a,b in zip(pd,dim(wt,c["dimensions"])))!=outDims:return False
    # This is the stronger, claim-specific requirement: each hypothesis
    # is needed, not merely that the affine rows are linearly independent.
    for i in range(k):
        GB=groebner([p for j,p in enumerate(gens) if j!=i],*X,order="lex",domain=QQ)
        if expand(GB.reduce(target)[1])==0:return False
    return True

def run():
    rows=[]
    for i,(label,c) in enumerate(cases()):
        try:actual=bool(check(c))
        except (ValueError,TypeError,KeyError,IndexError,AttributeError,ZeroDivisionError,OverflowError):
            actual=False
        expected=label=="ACCEPT_EXACT"
        rows.append({"case":i,"label":label,"oracle_accept":actual,"expected_accept":expected,
                     "correct":actual==expected})
    return {"suite":"SymPy independently evaluated polynomial identities, affine ideals, SI units, controlled AST",
            "total":len(rows),"correct":sum(r["correct"] for r in rows),
            "positives":sum(r["oracle_accept"] for r in rows),
            "source_labels":"internally generated synthetic tasks, not blinded human annotations",
            "physical_truth_certified":False,"lean_kernel_verified":False,
            "rows":rows}

if __name__=="__main__":
    r=run()
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+"\n")
    print(json.dumps({k:v for k,v in r.items() if k!="rows"},indent=2))
    raise SystemExit(0 if r["total"]==r["correct"]==880 else 2)
