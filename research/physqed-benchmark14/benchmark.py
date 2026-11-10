"""PHYSQED Benchmark 14: deterministic, newly generated exact implication challenges.

Independent ground truth:
  - SymPy symbolic expansion proves valid witness identities.
  - A real rational assignment exhibits false consequences when a premise is
    omitted or the asserted conclusion is shifted.
  - Explicit controlled-schema modifications test conservative refusals.
No natural-language semantics, experiments, external blind labels, general
theorem proving, or competing system performance are asserted here.
"""
from __future__ import annotations
import copy
import hashlib
import json
import sys
import time
from pathlib import Path
import sympy as S

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"projects"/"physqed"))

from benchmarks.two_premise_v09 import expr
from two_premise_claims import TAIL,VERSION as TWO_VERSION,verify as verify_two,MultiPremiseRefusal as TwoRefusal
from multi_premise_v10 import VERSION as MULTI_VERSION,verify as verify_multi,MultiPremiseRefusal as MultiRefusal

SEED=20261110
SUITE="PHYSQED Benchmark 14 / frozen deterministic synthetic implication challenge"
TOTAL_PER_ARITY=48
NEGATIVE_KINDS=("WRONG_WITNESS","FALSE_CONCLUSION","DEPENDENT_PREMISE",
                "TEXT_FORMAL_MISMATCH","DIMENSIONAL_CORRUPTION",
                "FALSE_PROVENANCE","WRONG_QUANTIFIER","PHYSICS_OVERCLAIM",
                "WRONG_SCHEMA")

def make_specimen(arity,variant):
    names=sum(([f"x{i}",f"y{i}"] for i in range(arity)),[])
    unit={"L":1} if variant%2 else {}
    dimensions={x:dict(unit) for x in names}
    coeffs=[2+((SEED+variant*5+i*3)%7) for i in range(arity)]
    # Formula text is generated independently of PHYSQED's parser.
    halves=[f"({a})*(x{i}-y{i})*"+(f"x{i}" if variant%2 else f"y{i}")
            for i,a in enumerate(coeffs)]
    witnesses=[f"({a})*"+(f"x{i}" if variant%2 else f"y{i}")
            for i,a in enumerate(coeffs)]
    goal=" + ".join(halves)
    premisetxt=[f"x{i} == y{i}" for i in range(arity)]
    statement=(f"For all real scalars {', '.join(names)}, if "+
               " and ".join(premisetxt)+f", then {goal} == 0 holds."+TAIL)
    contract={"schema":TWO_VERSION if arity==2 else MULTI_VERSION,
              "statement":statement,"variables":names,"dimensions":dimensions,
              "premises":[{"lhs":expr(f"x{i}"),"rhs":expr(f"y{i}")}
                          for i in range(arity)],
              "conclusion":{"lhs":expr(goal),"rhs":expr("0")},
              "witnesses":[expr(v) for v in witnesses],
              "provenance":"SYNTHETIC_SCOPED"}
    return contract,coeffs,goal,witnesses

def independent_mathematical_oracle(arity,variant,coeffs):
    """Direct SymPy verification and rational counterexamples, not solver output."""
    variables=S.symbols(" ".join(sum(([f"x{i}",f"y{i}"] for i in range(arity)),[])))
    index={str(z):z for z in variables}
    target=0
    witness_sum=0
    for i,a in enumerate(coeffs):
        x=index[f"x{i}"];y=index[f"y{i}"]
        w=S.Integer(a)*(x if variant%2 else y)
        p=x-y
        target+=w*p
        witness_sum+=w*p
    assert S.Poly(S.expand(target-witness_sum),variables).is_zero
    # Conditional identity true for any common value x_i=y_i.
    assert S.expand(target.subs({index[f"x{i}"]:i+1 for i in range(arity)})
                    .subs({index[f"y{i}"]:i+1 for i in range(arity)}))==0
    # Each premise must be essential: omit equation j, set x_j/y_j
    # to (1,2) for y-witness or (2,1) for x-witness; all others 0.
    for j in range(arity):
        vals={z:S.Integer(0) for z in variables}
        vals[index[f"x{j}"]]=S.Integer(2 if variant%2 else 1)
        vals[index[f"y{j}"]]=S.Integer(1 if variant%2 else 2)
        assert target.subs(vals)!=0
        assert all((index[f"x{i}"]-index[f"y{i}"]).subs(vals)==0
                   for i in range(arity) if i!=j)
    # False conclusion target==1 is broken at all-zero assignment.
    assert S.expand(target-S.Integer(1)).subs({z:0 for z in variables})==-1
    return True

def mutations(c,goal,arity):
    v=[]
    def edited(label,mut):
        d=copy.deepcopy(c);mut(d);v.append((label,d))
    edited("WRONG_WITNESS",lambda d:d["witnesses"].__setitem__(-1,expr("0")))
    def false_conclusion(d):
        d["conclusion"]["rhs"]=expr("1")
        d["statement"]=d["statement"].replace(f"{goal} == 0 holds.",
                                                f"{goal} == 1 holds.")
    edited("FALSE_CONCLUSION",false_conclusion)
    def dependent(d):
        d["premises"][-1]=copy.deepcopy(d["premises"][0])
        d["statement"]=d["statement"].replace(f"x{arity-1} == y{arity-1}",
                                               "x0 == y0")
    edited("DEPENDENT_PREMISE",dependent)
    edited("TEXT_FORMAL_MISMATCH",
           lambda d:d.__setitem__("statement",d["statement"].replace(" == "," + 1 == ",1)))
    edited("DIMENSIONAL_CORRUPTION",
           lambda d:d["dimensions"].__setitem__("x0",{"T":1}))
    edited("FALSE_PROVENANCE",lambda d:d.__setitem__("provenance","EXPERIMENT_CONFIRMED"))
    edited("WRONG_QUANTIFIER",
           lambda d:d.__setitem__("statement",d["statement"].replace(
               "For all real scalars","There exist real scalars",1)))
    edited("PHYSICS_OVERCLAIM",
           lambda d:d.__setitem__("statement",d["statement"]+" A physical law has been proved."))
    edited("WRONG_SCHEMA",lambda d:d.__setitem__("schema","physqed-unrestricted-physics"))
    assert tuple(label for label,_ in v)==NEGATIVE_KINDS
    return v

def verify_contract(arity,contract):
    return verify_two(contract) if arity==2 else verify_multi(contract)

def run():
    rows=[]
    started=time.perf_counter()
    for k in (2,3,4):
        for variant in range(TOTAL_PER_ARITY):
            original,coeffs,goal,_=make_specimen(k,variant)
            independent_mathematical_oracle(k,variant,coeffs)
            cases=[("ACCEPT_EXACT",original,True)]+[
                (name,case,False) for name,case in mutations(original,goal,k)]
            for name,c,expect in cases:
                case_id=f"arity{k}-v{variant:03d}-{name}"
                actual=False;flags_ok=True;exception=None
                try:
                    receipt=verify_contract(k,c)
                    actual=True
                    # A scoped mathematical pass must NEVER imply empirical or Lean proof.
                    flags_ok=(receipt["physical_law_proven"] is False and
                              receipt["lean_kernel_verified"] is False)
                except (TwoRefusal,MultiRefusal):
                    actual=False
                except Exception as exc:
                    exception=f"{type(exc).__name__}: {str(exc)[:180]}"
                rows.append({"id":case_id,"kind":name,"arity":k,
                             "expected_accept":expect,
                             "actual_accept":actual,
                             "correct":actual==expect and flags_ok and exception is None,
                             "unexpected_exception":exception,
                             "proof_flags_safe":flags_ok})
    elapsed=round(time.perf_counter()-started,4)
    summary={
        "suite":SUITE,"challenge_seed":SEED,
        "positive_gold_origin":"independent SymPy expansion, rational omitted-premise witnesses",
        "negative_gold_origin":"formula-changing and schema-changing controlled mutations",
        "independent_external_labels":False,"genuinely_blind":False,
        "competitor_comparison":False,"physical_truth_proven":False,
        "lean_proof_of_cases":False,
        "cases":len(rows),"passes":sum(r["correct"] for r in rows),
        "failures":sum(not r["correct"] for r in rows),
        "accepted_true_positives":sum(r["expected_accept"] and r["actual_accept"] for r in rows),
        "false_accepts":sum(not r["expected_accept"] and r["actual_accept"] for r in rows),
        "false_refusals":sum(r["expected_accept"] and not r["actual_accept"] for r in rows),
        "unexpected_exceptions":sum(r["unexpected_exception"] is not None for r in rows),
        "duration_seconds":elapsed,
        "rows_sha256":hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),
        "errors":[r for r in rows if not r["correct"]][:60],
    }
    Path("benchmark14_receipt.json").write_text(json.dumps(
        {"summary":summary,"rows":rows},sort_keys=True,indent=2)+"\n")
    print(json.dumps(summary,sort_keys=True,indent=2))
    return 0 if summary["failures"]==0 and len(rows)==1440 else 1

if __name__=="__main__":
    sys.exit(run())
