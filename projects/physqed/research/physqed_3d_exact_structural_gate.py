"""Exact 3D momentum-curl and causal six-stream structural gates.

Restricted analytic identities. Not the full 3+1 numerical ADM simulator,
not a physically derived stochastic vacuum, and not radiative reheating.
"""
import json
from pathlib import Path
import sympy as S

def main():
    x,y,z=S.symbols("x y z", real=True)
    eps=S.symbols("eps", real=True, nonzero=True)
    coords=(x,y,z)
    f=eps*S.sin(x)
    pi=eps*S.sin(y)
    J=S.Matrix([-pi*S.diff(f,coord) for coord in coords])
    curl=S.Matrix([S.diff(J[2],y)-S.diff(J[1],z),
                   S.diff(J[0],z)-S.diff(J[2],x),
                   S.diff(J[1],x)-S.diff(J[0],y)])
    assert S.simplify(curl[2]-eps**2*S.cos(x)*S.cos(y))==0
    assert curl[2].subs({x:0,y:0,eps:1})==1
    W=S.Matrix([S.Rational(7,16)*eps**2*S.cos(x)*S.sin(y),
                -S.Rational(1,16)*eps**2*S.sin(x)*S.cos(y),0])
    divW=sum(S.diff(W[i],coords[i]) for i in range(3))
    operator=S.Matrix([sum(S.diff(W[i],v,2) for v in coords)
           +S.diff(divW,coords[i])/3 for i in range(3)])
    assert all(S.trigsimp(operator[i]-J[i])==0 for i in range(3))
    # Six nonnegative null streams: E >= |P| by the triangle inequality.
    e=[S.Integer(v) for v in [1,2,3,4,5,6]]
    E=sum(e)
    P=S.Matrix([e[0]-e[1],e[2]-e[3],e[4]-e[5]])
    assert E*E-P.dot(P)==438>0
    q=[S.Rational(1,6)]*6
    assert sum(q)==1
    assert S.Matrix([q[0]-q[1],q[2]-q[3],q[4]-q[5]])==S.zeros(3,1)
    u=S.Rational(1,2)
    assert u*u*(1-u*u)==S.Rational(3,16)>0
    r={"schema":"physqed.3p1.structural-exact-gate.v1",
       "status":"PASS_EXACT_VECTOR_MOMENTUM_AND_CAUSAL_SIX_STREAM_ALGEBRA",
       "nonzero_curl_witness_at_origin":"1",
       "vector_potential_exact_operator_solution":True,
       "dominant_energy_quadratic_margin":"438",
       "balanced_source_timelike":True,
       "old_wall_friction_spacelike_norm_at_half_speed":"3/16",
       "full_nonlinear_3p1_simulation_replayed":False,
       "stochastic_quantum_initial_conditions_proven":False,
       "radiation_thermalization_derived":False,
       "wall_collapse_proven":False}
    Path("physqed_3d_exact_structural_receipt.json").write_text(
        json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(r,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
