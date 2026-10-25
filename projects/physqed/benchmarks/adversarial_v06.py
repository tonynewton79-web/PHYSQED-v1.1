#!/usr/bin/env python3
"""120 deterministic synthetic checks; this is NOT a head-to-head competitor score."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from engine import certify
V=lambda x:{"var":x}
C=lambda x:{"const":str(x)}
A=lambda *x:{"op":"add","args":list(x)}
M=lambda *x:{"op":"mul","args":list(x)}
P=lambda x,n:{"op":"pow","arg":x,"exp":n}

def algebra(k,p,bad):
    x,y,z=V("x"),V("y"),V("z")
    neg=lambda q:M(C(-1),q)
    if p==0:
        return M(C(k),P(A(x,y),2)),A(M(C(k),P(x,2)),M(C(2*k if not bad else 3*k),x,y),M(C(k),P(y,2)))
    if p==1:
        return M(C(k),P(A(x,neg(y)),2)),A(M(C(k),P(x,2)),M(C(-2*k if not bad else -k),x,y),M(C(k),P(y,2)))
    if p==2:
        return M(C(k),x,A(y,z)),A(M(C(k),x,y),M(C(k if not bad else -k),x,z))
    return M(C(k),A(x,y),A(x,neg(y))),A(M(C(k),P(x,2)),M(C(-k if not bad else k),P(y,2)))

def claim(i,statement,kind,lhs,rhs,variables):
    return {"schema_version":"physqed-0.1","id":i,"statement":statement,
       "source":"synthetic-adversarial-v06; no independent published tasks",
       "assumptions":["Only the declared mathematical component is checked"],
       "checks":[{"kind":kind,"variables":variables,"lhs":lhs,"rhs":rhs}]}

def cases():
    out=[]
    for pattern in range(4):
        for k in range(1,11):
            for bad in (False,True):
                l,r=algebra(k,pattern,bad)
                out.append(("false_algebra" if bad else "valid_algebra",
                   claim(f"alg_{pattern}_{k}_{int(bad)}","Polynomial component test",
                         "algebra_identity",l,r,["x","y","z"])))
    dims={"F":{"M":1,"L":1,"T":-2},"m":{"M":1},
          "a":{"L":1,"T":-2},"v":{"L":1,"T":-1}}
    for i in range(20):
        bad=bool(i%2)
        out.append(("false_dimensions" if bad else "valid_dimensions",
              claim(f"dim_{i}","Declared dimension comparison",
                   "dimension_equality",V("F"),M(V("m"),V("v" if bad else "a")),dims)))
    for i in range(20):
        l,r=algebra(i+1,i%4,False)
        out.append(("semantic_drift",
              claim(f"semantic_{i}",
                  "This identity proves all black holes must evaporate instantly.",
                  "algebra_identity",l,r,["x","y","z"])))
    assert len(out)==120
    return out

def run():
    rows=[]
    for label,case in cases():
        result=certify(case)
        want="REJECTED" if label.startswith("false_") else (
             "CONSISTENCY_CHECKS_PASSED" if label=="valid_dimensions" else
             "MATHEMATICAL_COMPONENTS_VERIFIED")
        scoped= result["status"]==want and result["physical_law_proven"] is False and result["lean_kernel_verified"] is False
        rows.append({"id":case["id"],"class":label,"status":result["status"],
                     "expected":want,"scope_correct":scoped})
    classes=sorted(set(v["class"] for v in rows))
    return {"suite":"PHYSQED-v06 deterministic adversarial",
          "total":len(rows),"scope_correct":sum(v["scope_correct"] for v in rows),
          "per_class":{n:{"total":sum(v["class"]==n for v in rows),
                          "scope_correct":sum(v["class"]==n and v["scope_correct"] for v in rows)} for n in classes},
          "semantic_drift_detected":0,
          "semantic_note":"20 false English claims were NOT automatically detected as semantic drift; no physical proof credit was awarded.",
          "competing_systems_run":False,"lean_proof_established":False,
          "cases_digest":hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),
          "rows":rows}

if __name__=="__main__":
    output=run()
    output_file=Path(sys.argv[1]) if len(sys.argv)>1 else None
    if output_file:output_file.write_text(json.dumps(output,sort_keys=True,indent=2)+"\n")
    print(json.dumps({k:v for k,v in output.items() if k!="rows"},indent=2,sort_keys=True))
    raise SystemExit(0 if output["total"]==120 and output["scope_correct"]==120 else 2)
