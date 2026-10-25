"""PHYSQED v1.0 synthetic 2-4-premise challenge generator (not external gold)."""
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from benchmarks.two_premise_v09 import expr
from multi_premise_v10 import VERSION,verify,MultiPremiseRefusal
from two_premise_claims import TAIL

def specimen(i):
    k = 3 if i%2==0 else 4
    t = i//4+1
    if i%4 < 2:
        names=sum(([f"x{j}",f"y{j}"] for j in range(k)),[])
        dims={name:{} for name in names}
        pairs=[(f"x{j}",f"y{j}") for j in range(k)]
        goal=( " + ".join(f"{t}*(x{j}**2-y{j}**2)" for j in range(k)), "0")
        witnesses=[f"{t}*(x{j}+y{j})" for j in range(k)]
    else:
        names=["v","u","a","b","t","s"]+(["m","n"] if k==4 else [])
        dims={"v":{"L":1,"T":-1},"u":{"L":1,"T":-1},
              "a":{"L":1,"T":-2},"b":{"L":1,"T":-2},
              "t":{"T":1},"s":{"T":1}}
        if k==3:
            pairs=[("v","u"),("a","b"),("t","s")]
            goal=(f"{t}*v*a*t",f"{t}*u*b*s")
            witnesses=[f"{t}*a*t",f"{t}*u*t",f"{t}*u*b"]
        else:
            dims.update({"m":{"M":1},"n":{"M":1}})
            pairs=[("m","n"),("v","u"),("a","b"),("t","s")]
            goal=(f"{t}*m*v*a*t",f"{t}*n*u*b*s")
            witnesses=[f"{t}*v*a*t",f"{t}*n*a*t",f"{t}*n*u*t",f"{t}*n*u*b"]
    statement=("For all real scalars "+", ".join(names)+", if "+
               " and ".join(a+" == "+b for a,b in pairs)+
               ", then "+goal[0]+" == "+goal[1]+" holds."+TAIL)
    return {"schema":VERSION,"statement":statement,"variables":names,
        "dimensions":dims,"premises":[{"lhs":expr(a),"rhs":expr(b)} for a,b in pairs],
        "conclusion":{"lhs":expr(goal[0]),"rhs":expr(goal[1])},
        "witnesses":[expr(w) for w in witnesses],"provenance":"SYNTHETIC_SCOPED"}

def cases():
    all_cases=[]
    for i in range(80):
        good=specimen(i)
        all_cases.append(("ACCEPT_EXACT",good))
        def add(label,mut):
            c=copy.deepcopy(good);mut(c);all_cases.append((label,c))
        add("FIRST_WITNESS_ZERO",lambda c:c["witnesses"].__setitem__(0,expr("0")))
        add("LAST_WITNESS_ZERO",lambda c:c["witnesses"].__setitem__(-1,expr("0")))
        add("BAD_CONCLUSION",lambda c:c["conclusion"].__setitem__("rhs",expr("0" if i%4>=2 else "1")))
        add("TEXT_PREMISE_DRIFT",lambda c:c.__setitem__("statement",c["statement"].replace(" == "," + 1 == ",1)))
        add("DEPENDENT_AFFINE",lambda c:c["premises"].__setitem__(-1,copy.deepcopy(c["premises"][0])))
        add("WRONG_UNITS",lambda c:c["dimensions"].__setitem__(c["variables"][0],{"T":15}))
        add("WRONG_QUANTIFIER",lambda c:c.__setitem__("statement",c["statement"].replace("For all real","There exist real",1)))
        add("FALSE_PHYSICAL_CLAIM",lambda c:c.__setitem__("statement",c["statement"]+" All stars are antimatter."))
        add("FALSE_PROVENANCE",lambda c:c.__setitem__("provenance","PHYSICAL_EXPERIMENT_CONFIRMED"))
        if i%4<2:
            def unnecessary(c):
                first=c["premises"][0]
                c["conclusion"]=copy.deepcopy(first)
                c["witnesses"]=[expr("1")]+[expr("0")]*(len(c["premises"])-1)
                c["statement"]=c["statement"].split(", then ")[0]+", then "+f"x0 == y0 holds."+TAIL
            add("UNNECESSARY_PREMISES",unnecessary)
        else:
            add("UNCONTROLLED_STATEMENT",lambda c:c.__setitem__("statement",c["statement"].replace(" holds."," is empirically validated.",1)))
    # 80 positive + 800 negative = 880.
    assert len(all_cases)==880
    return all_cases

def run():
    rows=[]
    for idx,(label,contract) in enumerate(cases()):
        try:
            certificate=verify(contract)
            accepted=True
            if certificate["physical_law_proven"] or certificate["lean_kernel_verified"]:
                raise AssertionError("dangerous proof promotion")
        except MultiPremiseRefusal:
            accepted=False
        expected=(label=="ACCEPT_EXACT")
        rows.append({"index":idx,"label":label,"expected_accept":expected,
                     "actual_accept":accepted,"correct":accepted==expected})
    return {"suite":"PHYSQED v1.0 2-4 exact affine premises and essentiality",
        "total":len(rows),"correct":sum(x["correct"] for x in rows),
        "positives":sum(x["expected_accept"] for x in rows),
        "false_accepts":sum(x["actual_accept"] and not x["expected_accept"] for x in rows),
        "false_refusals":sum(not x["actual_accept"] and x["expected_accept"] for x in rows),
        "external_gold_labels":False,"lean_kernel_confirmed":False,
        "empirical_physics_verified":False,
        "rows_sha256":hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),
        "rows":rows}

if __name__=="__main__":
    result=run()
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="rows"},indent=2))
    raise SystemExit(0 if result["correct"]==result["total"]==880 else 2)
