"""Shifted Minkowski Maxwell IBVP positive control (exact algebra).

X=x+v*t. Physical fixed-X walls have shifted-coordinate velocity
(-v,0,0). For U=(E_i,B_i), the Maxwell principal matrices are
A^j_EB=-epsilon_ijk, A^j_BE=epsilon_ijk, A^x -= v I.
Gauss constraints are transported by (dt-v dx), since div curl=0.
The corrected moving-boundary flux has principal form
A(n)-V_n I, and perfect conductor n cross E=0 provides a
four-dimensional maximal nonnegative trace space on every face.

This is a Maxwell positive control, not a proof of nonlinear
Einstein boundary-to-constraint compatibility or arbitrary-data
Maxwell IBVP existence.
"""
from __future__ import annotations
from hashlib import sha256
import json
import sympy as S


def _eps(i,j,k):
    if len({i,j,k})<3:
        return 0
    return 1 if (i,j,k) in ((0,1,2),(1,2,0),(2,0,1)) else -1


def verify_maxwell_shifted_boundary(shift="1/5",boundary_velocity=None,
                                     *,undercomplete=False):
    if isinstance(shift,float):
        raise ValueError("exact rational shift required")
    try:
        v=S.Rational(str(shift))
    except (TypeError,ValueError) as exc:
        raise ValueError("exact rational shift required") from exc
    if abs(v)>=1:
        raise ValueError("positive-control regime requires |shift|<1")
    if boundary_velocity is None:
        boundary_velocity=-v
    elif isinstance(boundary_velocity,float):
        raise ValueError("exact boundary velocity required")
    else:
        boundary_velocity=S.Rational(str(boundary_velocity))
    matrices=[]
    for j in range(3):
        a=S.zeros(6)
        for i in range(3):
            for k in range(3):
                a[i,k+3]=-_eps(i,j,k)
                a[i+3,k]=_eps(i,j,k)
        if j==0:
            a-=v*S.eye(6)
        if a!=a.T:
            raise AssertionError("Maxwell principal symbol not symmetric")
        matrices.append(a)
    lam=S.symbols("lambda")
    charpoly=S.factor((lam*S.eye(6)-(matrices[0]+v*S.eye(6))).det())
    expected=lam**2*(lam**2-1)**2
    if S.simplify(charpoly-expected):
        raise AssertionError("incorrect Maxwell normal characteristic")
    faces=[]
    for j in range(3):
        for side,sign in (("lower",-1),("upper",1)):
            wall_normal=sign*boundary_velocity if j==0 else S.S.Zero
            flux=sign*matrices[j]-wall_normal*S.eye(6)
            frame=S.zeros(6,4)
            frame[j,0]=1
            for k in range(3):
                frame[3+k,k+1]=1
            if undercomplete:
                frame=frame[:,:3]
            restricted=(frame.T*flux*frame).applyfunc(S.simplify)
            characteristic=S.factor((lam*S.eye(6)-flux).det())
            inertia_ok=bool(S.simplify(characteristic-expected)==0)
            rank_ok=frame.rank()==frame.cols
            maximal=frame.cols==4
            zero_flux=bool(restricted==S.zeros(frame.cols))
            faces.append({
                "name":("x","y","z")[j]+"_"+side,
                "moving_wall_normal_velocity":str(wall_normal),
                "characteristic_polynomial":str(characteristic),
                "two_positive_two_negative_two_zero":inertia_ok,
                "frame_rank":int(frame.rank()),
                "frame_columns":frame.cols,
                "maximal_nonnegative_dimension":4,
                "restricted_flux":[[str(z) for z in row]
                                   for row in restricted.tolist()],
                "flux_zero":zero_flux,
                "passed":inertia_ok and rank_ok and maximal and zero_flux})
    t,x,y,z=S.symbols("t x y z")
    space=(x,y,z)
    E=S.Matrix([S.Function("E"+str(i))(t,x,y,z) for i in range(3)])
    B=S.Matrix([S.Function("B"+str(i))(t,x,y,z) for i in range(3)])
    def curl(V):
        return S.Matrix([sum(_eps(i,j,k)*S.diff(V[k],space[j])
            for j in range(3) for k in range(3)) for i in range(3)])
    def div(V):
        return sum(S.diff(V[j],space[j]) for j in range(3))
    curl_div_E=S.expand(div(curl(E)))
    curl_div_B=S.expand(div(curl(B)))
    if curl_div_E or curl_div_B:
        raise AssertionError("div curl identity failed")
    result={
        "schema":"physqed.shifted-maxwell-ibvp-control.v1",
        "shift":str(v),
        "boundary_coordinate_velocity":str(boundary_velocity),
        "coordinate_map":"X=x+v*t; fixed inertial-X box moves in x",
        "principal_characteristic_polynomial":str(charpoly),
        "boundary_faces":faces,
        "all_six_maximal_nonnegative":all(f["passed"] for f in faces),
        "electric_gauss_propagation_verified":bool(curl_div_B==0),
        "magnetic_gauss_propagation_verified":bool(curl_div_E==0),
        "gauss_transport_equations":"(dt-v dx) div(E)=(dt-v dx) div(B)=0",
        "energy_flux_identity":"d/dt int_moving_box e = -int_boundary n.(E cross B)",
        "perfect_conductor_trace":"n cross E=0; normal E and all B allowed",
        "nonlinear_Einstein_boundary_to_constraint_map_proven":False,
        "physical_Einstein_evolution_boundary_conditions_verified":False,
        "smooth_Maxwell_IBVP_existence_proven":False,
        "status":("PASS_EXACT_SHIFTED_MAXWELL_BOUNDARY_ALGEBRA"
                  if all(f["passed"] for f in faces)
                  else "REJECTED_OR_INCONCLUSIVE_MAXWELL_BOUNDARY")}
    result["receipt_sha256"]=sha256(json.dumps(
        result,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return result


def replay_maxwell_shifted_boundary(shift,stored,
                                     boundary_velocity=None,*,undercomplete=False):
    return isinstance(stored,dict) and stored==verify_maxwell_shifted_boundary(
        shift,boundary_velocity,undercomplete=undercomplete)
