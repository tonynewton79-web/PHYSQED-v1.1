"""Independent scoped exact gate for dynamical wall-mediator-to-radiation transfer.

This certifies only the polynomial completion and positive six-axis null-stream
source algebra. The 3D finite-volume simulations are in a separate research
reproducibility package, not replayed by this symbolic CI gate.
"""
from __future__ import annotations
import json
from fractions import Fraction as F
from pathlib import Path
import sympy as S

def run():
    X,Y,s,c,lam,k,g,ms=S.symbols('X Y s c lam k g ms',positive=True)
    AA=c+k*k/(4*lam)
    D=c*lam*lam/(4*c*lam+k*k)
    U=c*X**2+lam*(Y-k*X/lam)**2/4+ms**2*s**2/2+g*s*Y
    completed=(ms**2/2)*(s+g*Y/ms**2)**2+AA*(X-k*Y/(4*AA))**2+(D-g*g/(2*ms**2))*Y**2
    assert S.cancel(U-completed)==0
    delta=F('0.016202803686105016')
    a=(4+delta)/2
    v=3-a*a/2
    yc=F('0.81')
    beta=v/((a-yc)**2+2*v)
    kappa=F(10000)
    lamnum=kappa*kappa/(4*beta)
    cnum=F(1,2)-beta
    Dnum=cnum*lamnum**2/(4*cnum*lamnum+kappa**2)
    d=F(12000**2,2*600**2)
    assert Dnum > F(9119000) > d
    assert d==200
    examples=[]
    for E,p in [(F(3,5),(F(1,10),F(-1,6),F(1,8))),
                (F(6,5),(F(2,5),F(-1,5),F(1,10))),
                (F(3,5),(F(1,3),F(-1,3),F(1,3)))]:
        excess=E-sum(abs(x) for x in p)
        if excess<0:
            examples.append({"admitted":False,"energy":str(E),"reason":"outside the six-ray positive cone"})
            continue
        plus=[max(p[i],F(0))+excess/6 for i in range(3)]
        minus=[max(-p[i],F(0))+excess/6 for i in range(3)]
        assert all(x>=0 for x in plus+minus)
        assert sum(plus+minus)==E
        assert all(plus[i]-minus[i]==p[i] for i in range(3))
        examples.append({"admitted":True,"energy":str(E),"sources":[str(x) for x in plus+minus]})
    assert sum(e["admitted"] for e in examples)==2
    # Old moving-wall friction is spacelike: Q0~u^2, |Qx|~u.
    for u in [F(1,10),F(1,2),F(99,100)]:
        assert u*u<abs(u)
    receipt={"schema":"physqed.exact-mediator-nullstream.v1",
      "status":"PASS_SCOPED_POLYNOMIAL_AND_POSITIVE_SIX_STREAM_ALGEBRA",
      "three_field_positive_SOS_identity":True,
      "global_unbiased_vacuum_stability_condition_verified":True,
      "stability_margin_D_approx":float(Dnum),
      "mediator_negative_quadratic_coefficient":str(d),
      "rational_positive_source_and_refusal_cases":examples,
      "old_direct_rigid_wall_friction_refused":True,
      "full_3p1_numerical_replay":False,
      "dynamical_AMR":False,"stochastic_quantum_state":False,
      "reheating_thermalization":False,"wall_annihilation_proven":False}
    Path("inflaton_mediator_exact_receipt.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print(json.dumps(receipt,indent=2,sort_keys=True))
    return receipt

if __name__=="__main__":
    run()
