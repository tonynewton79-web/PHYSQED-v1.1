"""Exact, conditional causal-cone gate for direct scalar-friction transfer.

The obstruction applies only to creating an initially empty DEC-compliant
radiation fluid from a rigid moving-wall scalar source alone; not a theorem
against microscopic reheating, a pre-existing bath or mediator particles.
"""
from fractions import Fraction as F
from pathlib import Path
import json
if __name__=="__main__":
    cases=[]
    for u in (F(1,10),F(1,2),F(3,4),F(99,100)):
        Q0=u*u;Qx=u
        norm=Qx*Qx-Q0*Q0
        assert norm>0 and Q0<abs(Qx)
        cases.append(dict(u=str(u),Q0=str(Q0),abs_Qx=str(Qx),
                          Lorentz_norm_squared=str(norm),spacelike=True))
    r=dict(schema="physqed.causal-scalar-radiation-gate.v1",
     status="PASS_EXACT_SPACELIKE_WALL_CURRENT__REHEATING_UNPROVEN",
     cases=cases,
     assumptions="single/comoving canonical scalar gradient source; 0<|u|<1; positive friction; radiation stress initially zero throughout a neighborhood; dominant energy condition; no mediator",
     physical_reheating_no_go=False, fluid_evolved=False)
    Path("inflaton_causal_radiation_receipt.json").write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print(json.dumps(r,indent=2,sort_keys=True))
