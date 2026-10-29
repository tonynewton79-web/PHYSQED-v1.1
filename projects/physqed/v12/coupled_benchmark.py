"""Reproducible textbook Reissner–Nordstrom Einstein–Maxwell receipt.

Execute: PYTHONPATH=projects/physqed python -m v12.coupled_benchmark \
    --output /tmp/physqed-v12-rn.json

This checks local tensor equations for an exact electrovacuum with a fixed
action normalization. It does not prove global black-hole or QFT properties.
"""
import argparse
import sympy as S
from .geometry import Geometry
from .coupled import (maxwell_from_potential,maxwell_bianchi,maxwell_equations,
                      maxwell_stress,covariant_divergence_stress,
                      einstein_maxwell_residual)
from .receipts import certify,save_certificate


def build_receipt():
    t,r,theta,phi=S.symbols("t r theta phi",real=True)
    Q=S.Rational(1,2)
    f=1-2/r+Q**2/r**2
    chart=(t,r,theta,phi)
    geometry=Geometry(chart,S.diag(-f,1/f,r*r,r*r*S.sin(theta)**2))
    F=maxwell_from_potential(chart,(Q/r,0,0,0))
    T=maxwell_stress(geometry,F)
    equations=[
        (einstein_maxwell_residual(geometry,F),S.zeros(4)),
        (maxwell_equations(geometry,F),(0,0,0,0)),
        (maxwell_bianchi(F,chart),tuple(0 for _ in range(4**3))),
        (covariant_divergence_stress(geometry,T),(0,0,0,0)),
        (S.trace(geometry.g_inv*T),0),
        (geometry.scalar,0),
    ]
    receipt=certify(
        "STD-GR-EM-RN-001","einstein",equations,
        source="Reissner-Nordstrom textbook solution, not a research-paper case",
        assumptions=("signature (-,+,+,+)",
                     "action normalization S=int sqrt(-g) (R-F_ab F^ab)",
                     "M=1, Q=1/2", "r outside outer horizon",
                     "coordinate patch 0<theta<pi", "Levi-Civita connection"))
    if not receipt["status"].startswith("EXACT_"):
        raise AssertionError("Reissner-Nordstrom exact component receipt rejected")
    # The scaled-field bad control must fail the coupled Einstein equation.
    bad=certify(
        "STD-GR-EM-RN-NEG","einstein",
        [(einstein_maxwell_residual(geometry,2*F),S.zeros(4))],
        source="intentionally incorrect electromagnetic amplitude",
        assumptions=("same RN metric","field scaled by factor 2"))
    if bad["status"]!="REJECTED" or not any(
        v["counterexample"] is not None for v in bad["checks"] if not v["passed"]
    ):
        raise AssertionError("scaled-field negative control not refused")
    return receipt,bad


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",required=True)
    parser.add_argument("--negative-output",default=None)
    args=parser.parse_args()
    positive,negative=build_receipt()
    save_certificate(positive,args.output)
    if args.negative_output:
        save_certificate(negative,args.negative_output)
    print("PASS: RN Einstein/Maxwell/Bianchi/stress + scaled-field refusal"
          " (symbolic components only; physical law unverified)")


if __name__=="__main__":
    main()
