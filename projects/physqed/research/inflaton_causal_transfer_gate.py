"""Exact causal-transfer and stochastic-momentum-constraint refusal gates.

These finite checks do NOT evolve radiation or construct a quantum state.
They expose inadmissible source currents and the covariance change made by
a pointwise scalar-momentum projection. All arithmetic is exact Fraction.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def moving_wall_source(speed, gradient_strength=F(13, 7)):
    """Orthonormal Q^0=u^2*S, Q^x=u*S; S>0, |u|<1."""
    u=F(speed)
    S=F(gradient_strength)
    if not (0 < abs(u) < 1 and S > 0):
        raise ValueError("requires a subluminal nontrivial wall")
    e=u*u*S
    p=abs(u)*S
    norm=p*p-e*e
    return {"speed":str(u),"Q0":str(e),"abs_Qx":str(p),
            "norm_squared":str(norm),
            "source_spacelike":norm>0,
            "future_causal_direct_creation":e>=p}


def momentum_projection(grad, vel):
    if len(grad)!=2 or len(vel)!=2:
        raise ValueError("requires two scalar components")
    g=tuple(F(x) for x in grad)
    v=tuple(F(x) for x in vel)
    g2=sum(x*x for x in g)
    dot=sum(x*y for x,y in zip(g,v))
    if not g2:return tuple(v)
    return tuple(v[i]-dot*g[i]/g2 for i in range(2))


def main():
    cases=[moving_wall_source(s) for s in (F(1,10),F(1,2),F(3,4),F(99,100))]
    assert all(c["source_spacelike"] and not c["future_causal_direct_creation"] for c in cases)
    # Contrast: homogeneous evolving scalar has no spatial momentum source.
    homogeneous= {"Q0":str(F(1,4)), "abs_Qx":"0",
                  "source_future_causal":True}
    trials=[([3,4],[5,7]),([1,0],[1,1]),([2,1],[1,2])]
    out=[]
    for grad,vel in trials:
        vp=momentum_projection(grad,vel)
        raw=sum(F(g)*F(v) for g,v in zip(grad,vel))
        proj=sum(F(g)*v for g,v in zip(grad,vp))
        e0=sum(F(v)**2 for v in vel)
        e1=sum(v**2 for v in vp)
        assert raw != 0 and proj==0 and 0 <= e1 < e0
        out.append({"gradient":list(grad),"original_velocity":list(vel),
                    "projected_velocity":[str(v) for v in vp],
                    "original_momentum_source":str(raw),
                    "projected_momentum_source":str(proj),
                    "fraction_of_kinetic_energy_discarded":str(1-e1/e0)})
    receipt={"schema":"physqed.causal-transfer-constraint-projection.v1",
        "status":"PASS_EXACT_CAUSAL_CONE_NEGATIVE_CONTROL_AND_PROJECTION_IDENTITY",
        "moving_wall_cases":cases,"homogeneous_positive_control":homogeneous,
        "projection_cases":out,
        "statement":"A direct transfer proportional to scalar gradient is spacelike on a subluminal moving wall; an initially empty DEC radiation fluid cannot have that as its sole local source. A pointwise momentum projection changes sampled kinetic energy.",
        "conditional_theorem_only":True,
        "causal_relativistic_radiation_evolved":False,
        "wigner_state_verified":False,
        "full_3D_Einstein_constraints_solved":False,
        "long_time_collapse_evolved":False}
    Path("inflaton_causal_transfer_receipt.json").write_text(
        json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    return receipt


if __name__=="__main__":
    print(json.dumps(main(),indent=2,sort_keys=True))
