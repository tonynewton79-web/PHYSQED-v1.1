"""PHYSQED independently-derived v1.3 mathematical regression probes.
NOT a blinded third-party benchmark or evidence of a physical theorem.
Reproducibility: fixed exact arithmetic, deterministic case order, no RNG.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "projects" / "physqed"))

import sympy as S
from v12.fields import wick, first_order_phi4_two_point
from v12.geometry import zero
from benchmarks.multi_premise_v10 import specimen
from multi_premise_v10 import MultiPremiseRefusal, verify
from constructive_essentiality_v11 import verify_and_construct

rows = []

def check(label, pred, detail=""):
    rows.append({"id": label, "pass": bool(pred), "detail": str(detail)[:300]})

def attempt(label, fun):
    try:
        fun()
    except Exception as exc:
        check(label, False, "%s: %s" % (type(exc).__name__, exc))

def independent_formal_eval(node, values):
    """Direct Fraction evaluation, independent of the polynomial backend."""
    if "const" in node:
        return F(node["const"])
    if "var" in node:
        return values[node["var"]]
    op = node["op"]
    if op == "add":
        return sum((independent_formal_eval(v, values) for v in node["args"]), F(0))
    if op == "mul":
        result = F(1)
        for v in node["args"]:
            result *= independent_formal_eval(v, values)
        return result
    if op == "pow":
        return independent_formal_eval(node["arg"], values) ** node["exp"]
    raise AssertionError("unsupported test oracle AST")

def gap(equation, values):
    return independent_formal_eval(equation["lhs"], values) - independent_formal_eval(equation["rhs"], values)

# An exact closed-form consequence of connected Wick pairings:
# delta C_ij = -1/2 * SUM_k lambda_k C_ik C_jk C_kk.
# This is a finite zero-dimensional Gaussian integral identity.
for a in (1,2,3,5):
    for b in (2,3,7):
        for lam in (1,2,5):
            tag = f"phi4-scalar-a{a}-b{b}-l{lam}"
            def scalar(a=a,b=b,lam=lam,tag=tag):
                c=S.Rational(a,b)
                got=first_order_phi4_two_point([[c]],0,0,[lam])
                expected=-S.Rational(lam,2)*c**3
                check(tag, got == expected and bool(got.is_Rational),
                      "actual=%s expected=%s exact=%s" %(got,expected,got.is_Rational))
            attempt(tag, scalar)

C = S.Matrix([[S.Rational(3,4), S.Rational(1,5)],
              [S.Rational(1,5), S.Rational(2,3)]])
for couplings in ((1,2),(3,0),(0,5)):
    for left,right in ((0,0),(0,1),(1,1)):
        tag=f"phi4-mixed-{couplings}-{left}{right}"
        def mixed(couplings=couplings,left=left,right=right,tag=tag):
            expected=-S.Rational(1,2)*sum(
                couplings[k]*C[left,k]*C[right,k]*C[k,k] for k in (0,1))
            got=first_order_phi4_two_point(C,left,right,couplings)
            check(tag, got == expected and bool(got.is_Rational),
                  "actual=%s expected=%s exact=%s" %(got,expected,got.is_Rational))
        attempt(tag,mixed)

for order in (0,2,4,6,8,10,12):
    tag=f"wick-univariate-order-{order}"
    def moments(order=order,tag=tag):
        actual=wick([0]*order,[[S.Rational(2,3)]])
        double_factorial=math.prod(range(1,order,2))
        expected=S.Integer(double_factorial)*S.Rational(2,3)**(order//2)
        check(tag,actual==expected,str(actual)+" vs "+str(expected))
    attempt(tag,moments)

for number,entries,expected in (
    (0,[[0,0],[0,0]],True),
    (1,[[0,0],[0,1]],False),
    (2,[[S.sin(S.Symbol("u"))**2+S.cos(S.Symbol("u"))**2-1,0],[0,0]],True),
):
    tag=f"tensor-zero-componentwise-{number}"
    def tensor(entries=entries,expected=expected,tag=tag):
        value=S.ImmutableDenseNDimArray(entries)
        result=zero(value)
        check(tag,result is expected,f"got={result!r} expected={expected!r}")
    attempt(tag,tensor)

# Existing specimen generators are used only to construct controlled inputs.
# Independent Fraction evaluation checks every returned counterexample point.
for idx in range(24):
    contract=specimen(idx+80)
    tag=f"affine-constructive-{idx}"
    def constructive(contract=contract,tag=tag):
        result=verify_and_construct(contract)
        flags=(result["physical_law_proven"] is False and
               result["lean_kernel_verified"] is False)
        for rec in result["counterexamples"]:
            values={k:F(v) for k,v in rec["assignment"].items()}
            omit=rec["dropped_premise"]-1
            flags &= all(gap(p,values)==0 for i,p in enumerate(contract["premises"]) if i!=omit)
            flags &= gap(contract["premises"][omit],values)!=0
            flags &= gap(contract["conclusion"],values)!=0
            flags &= str(gap(contract["premises"][omit],values))==rec["dropped_premise_residual"]
            flags &= str(gap(contract["conclusion"],values))==rec["conclusion_residual"]
        flags &= len(result["counterexamples"])==len(contract["premises"])
        check(tag,flags)
    attempt(tag,constructive)
    changed=copy.deepcopy(contract)
    changed["witnesses"][0]={"const":"0"}
    tag=f"affine-witness-tamper-rejected-{idx}"
    def reject(changed=changed,tag=tag):
        try:
            verify(changed)
        except MultiPremiseRefusal:
            check(tag,True)
        else:
            check(tag,False,"invalid witness wrongly accepted")
    attempt(tag,reject)

# Test an actual typed Einstein-Maxwell contract, not merely disconnected utilities.
from v12.typed_input import execute_physics_input
modelpath=ROOT/"projects"/"physqed"/"examples"/"typed"/"einstein_maxwell_flat.json"
def em_positive():
    data=json.loads(modelpath.read_text())
    result=execute_physics_input(data)
    ok=(result["status"]=="PASS_TYPED_EINSTEIN_MAXWELL_ADM__SCOPED"
        and len(result["coupled_contract"]["nodes"])==16
        and all(n["passed"] for n in result["coupled_contract"]["nodes"])
        and result["physical_truth_proven"] is False
        and result["global_theorem_proven"] is False)
    check("einstein-maxwell-flat-16-linked",ok,result.get("status"))
attempt("einstein-maxwell-flat-16-linked",em_positive)

def em_negative():
    data=json.loads(modelpath.read_text())
    data["tensor_types"]["stress"]["variance"]="uu"
    try:
        execute_physics_input(data)
    except ValueError:
        check("einstein-maxwell-wrong-index-refusal",True)
    else:
        check("einstein-maxwell-wrong-index-refusal",False,"invalid type accepted")
attempt("einstein-maxwell-wrong-index-refusal",em_negative)

summary={
    "suite":"PHYSQED-v1.3 independent-exact regression probes",
    "source_branch":"benchmark/independent-20261110",
    "scope":"finite symbolic, algebraic, controlled-input and receipt checks",
    "external_blind_gold":False,
    "competitor_benchmark":False,
    "empirical_physics_validated":False,
    "global_theorem_proven":False,
    "total":len(rows),
    "passed":sum(r["pass"] for r in rows),
    "failed":sum(not r["pass"] for r in rows),
    "rows_sha256":hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),
    "failures":[r for r in rows if not r["pass"]],
}
Path("benchmark_receipt.json").write_text(json.dumps({"summary":summary,"rows":rows},indent=2)+"\n")
print(json.dumps(summary,indent=2))
sys.exit(0 if summary["failed"]==0 else 1)
