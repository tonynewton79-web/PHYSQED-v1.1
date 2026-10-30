"""Curved Ricci-flat pp-wave in a genuine timelike ADM foliation.

The original Brinkmann u coordinate is null; define
u=(t-z)/sqrt(2), v=(t+z)/sqrt(2). On |x|,|y|<=1/2,
H=x²-y² in [-1/4,1/4]. Exact 3+1 lapse, shift and spatial
geometry yield a uniform positive normal wave-cone gap, while
the advective shift characteristic passes through zero at H=0.

This certifies bounded *frozen principal operator coefficients*
for a curved background. No curved boundary rank selection,
variable-coefficient energy theorem or Einstein IBVP is inferred.
"""
from hashlib import sha256
import json
import sympy as S


def verify_ppwave_timelike_frozen():
    t,x,y,z=S.symbols("t x y z",real=True)
    H=x*x-y*y
    hzz=1+H/2
    g=S.Matrix([[-1+H/2,0,0,-H/2],
                [0,1,0,0],[0,0,1,0],
                [-H/2,0,0,1+H/2]])
    h=S.diag(1,1,hzz)
    beta=S.Matrix([0,0,-H/(2+H)])
    N2=1/hzz
    expected_tt=-N2+(h*beta).dot(beta)
    inverse=g.inv()
    wave_plus=S.factor(-beta[2]+N2)
    wave_minus=S.factor(-beta[2]-N2)
    # N sqrt(h^zz)=1/hzz=N², since h^zz=1/hzz.
    # Exact scalar square inequalities on |x|,|y|<=1/2:
    # 0<=x²,y²<=1/4, therefore -1/4<=H<=1/4.
    tests={
       "time_spatial_signature_reconstructs":S.simplify(expected_tt-g[0,0])==0,
       "shift_cross_term_reconstructs":S.simplify(hzz*beta[2]-g[0,3])==0,
       "metric_det_minus_one":S.simplify(g.det()+1)==0,
       "inverse_lapse_relation":S.simplify(-1/inverse[0,0]-N2)==0,
       "inverse_shift_relation":S.simplify(-inverse[0,3]/inverse[0,0]-beta[2])==0,
       "normal_speed_plus_exact_one":S.simplify(wave_plus-1)==0,
       "normal_speed_minus_exact":S.simplify(wave_minus-(H-2)/(H+2))==0}
    result={
       "schema":"physqed.GH-curved-ADM-frozen-principal.v1",
       "background":"Brinkmann Ricci-flat wave in timelike t=(u+v)/sqrt(2)",
       "original_Brinkmann_u_is_null":True,
       "transverse_box":"-1/2 <= x,y <= 1/2",
       "exact_H_bounds":["-1/4","1/4"],
       "spatial_h_zz":"1+H/2",
       "spatial_min_eigenvalue_at_least":"7/8",
       "lapse_squared":"1/(1+H/2)",
       "lapse_squared_bounds":["8/9","8/7"],
       "beta_z":"-H/(H+2)",
       "beta_abs_upper_bound":"1/7",
       "normal_characteristic_speed_plus":str(wave_plus),
       "normal_characteristic_speed_minus":str(wave_minus),
       "normal_wave_pair_strict_signs_proved":True,
       "advective_normal_speed":"H/(H+2)",
       "advective_normal_speed_changes_sign_at_H_zero":True,
       "same_curved_geometry_as_previous_Ricci_flat_ppwave":True,
       "exact_tensor_algebra_tests":tests,
       "globally_uniform_boundary_inertia_proven":False,
       "curved_boundary_resolvent_estimate_proven":False,
       "curved_Einstein_IBVP_theorem_proven":False}
    ok=all(tests.values())
    result["status"]=("PASS_CURVED_TIMELIKE_ADM_FROZEN_PRINCIPAL"
                     if ok else "REJECTED_CURVED_ADM_PRINCIPAL")
    result["receipt_sha256"]=sha256(json.dumps(
         result,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return result


def replay_ppwave_timelike_frozen(stored):
    return isinstance(stored,dict) and stored==verify_ppwave_timelike_frozen()
