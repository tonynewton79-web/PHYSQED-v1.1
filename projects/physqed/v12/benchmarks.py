"""Run PHYSQED v1.2 against textbook physics and write JSON receipts.

Usage: PYTHONPATH=projects/physqed python -m v12.benchmarks --out-dir receipts
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sympy as S
from sympy.physics.matrices import msigma
from . import (Geometry, GaugeField, LieAlgebra, euler_lagrange,
               poisson_bracket, first_order_phi4_two_point,
               certify, save_certificate)


def textbook_receipts():
    t,x,y,z=S.symbols("t x y z")
    r,theta,phi=S.symbols("r theta phi",positive=True)
    a=S.Function("a")(t)
    flat=Geometry((t,x,y,z),S.diag(-1,1,1,1))
    sphere=Geometry((theta,phi),S.diag(r**2,r**2*S.sin(theta)**2))
    flrw=Geometry((t,x,y,z),S.diag(-1,a**2,a**2,a**2))
    E=S.Symbol("E",real=True)
    maxwell=GaugeField(LieAlgebra.u1(),(t,x),[[0],[E*t]])
    so3=LieAlgebra.so3()
    sx,sy,sz=(msigma(i) for i in range(1,4))
    m=S.Symbol("m",real=True)
    field=S.Function("field")(t,x)
    L=(S.diff(field,t)**2-S.diff(field,x)**2-m*m*field**2)/2
    q,p=S.symbols("q p")
    cases=[
        ("STD-GR-001","einstein",[(flat.einstein,S.zeros(4))],
         "4D Cartesian Minkowski metric"),
        ("STD-GR-002","tensor",[(sphere.scalar,2/r**2)],
         "radius-r round two-sphere"),
        ("STD-GR-003","einstein",
         [(flrw.einstein[0,0],3*(S.diff(a,t)/a)**2)],
         "spatially flat FLRW with lapse one"),
        ("STD-YM-001","gauge",[(maxwell.field[0][1],S.Matrix([E]))],
         "constant U(1) electric field in 1+1"),
        ("STD-YM-002","gauge",
         [(so3.bracket([1,0,0],[0,1,0]),S.Matrix([0,0,1]))],
         "standard so(3) generator convention"),
        ("STD-QM-001","quantum",
         [(sx*sy-sy*sx,2*S.I*sz)],
         "Pauli spin matrices"),
        ("STD-QFT-001","field",
         [(euler_lagrange(L,[field],[t,x])[0],
           -S.diff(field,t,2)+S.diff(field,x,2)-m*m*field)],
         "free massive Klein-Gordon in (+,-) convention"),
        ("STD-CAN-001","canonical",[(poisson_bracket(q,p,[q],[p]),1)],
         "single classical canonical pair"),
        ("STD-QFT-002","field",
         [(first_order_phi4_two_point(S.Matrix([[1]]),0,0,[1]),
           -S.Rational(1,2))],
         "first order Euclidean zero-dimensional phi^4 two-point"),
    ]
    for claim_id,domain,eqs,source in cases:
        yield certify(claim_id,domain,eqs,assumptions=(source,),source=source)
    yield certify("STD-NEG-001","quantum",
                  [(sx*sy-sy*sx,-2*S.I*sz)],
                  assumptions=("intentional Pauli wrong-sign target",),
                  source="adversarial negative control")


def run(out_dir=None):
    receipts=list(textbook_receipts())
    passed=sum(r["status"].startswith("EXACT_") for r in receipts)
    refused=sum(r["status"]=="REJECTED" for r in receipts)
    if (passed,refused)!=(9,1):
        raise AssertionError(f"expected 9 exact components and 1 refusal: {passed=} {refused=}")
    if out_dir is not None:
        d=Path(out_dir)
        d.mkdir(parents=True,exist_ok=True)
        for receipt in receipts:
            save_certificate(receipt,d/(receipt["claim_id"]+".json"))
        (d/"summary.json").write_text(json.dumps({
            "schema":"physqed-v1.2-standard-benchmarks",
            "exact_symbolic_receipts":passed,
            "intentional_refusals":refused,
            "physics_certified":False,
            "lean_kernel_verified":False,
            "independent_engine_verified":False
        },indent=2)+"\n",encoding="utf-8")
    return passed,refused


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir",type=Path,default=None)
    args=parser.parse_args()
    passed,refused=run(args.out_dir)
    print(f"PHYSQED_V12_STANDARD_COMPONENTS={passed} ADVERSARIAL_REFUSALS={refused}; PHYSICS_UNVERIFIED")


if __name__=="__main__":
    main()
