"""Higher-order corner hierarchy for the linearized GH metric wave system.

For reduced wave solutions, J_0=f, J_1=g and
J_(r+2)=Delta J_r. At order r>=0, the six Sommerfeld
corner residuals are (J_(r+1)-partial_x J_r)|x=0.
The four constraint boundary residuals are
(-J_(r+1,t nu)+partial_i J_(r,i nu))|x=0.

These identities are NECESSARY temporal compatibility conditions
for smooth solutions; passing finitely many orders does not imply
existence or that ALL higher-order compatibility holds.
"""
from __future__ import annotations
from hashlib import sha256
import json
import sympy as S
from .gh_boundary_map import (
    COORDS,SPACE,ORDER,TANGENT,I,t,x,tensor,_zero,zero_metric)

def _laplace_spatial(a):
    return S.expand(sum(S.diff(a,v,2) for v in SPACE))

def _matrix_data(m):
    return {name:S.expand(m[I[name[0]],I[name[1]]]) for name in ORDER}

def initial_jet_hierarchy(initial,velocity,max_order=5):
    if type(max_order) is not int or not (0<=max_order<=8):
        raise ValueError("0<=max_order<=8 required")
    f=tensor(initial)
    g=tensor(velocity)
    if any(t in v.free_symbols for v in list(f)+list(g)):
        raise ValueError("initial f and velocity g must not depend on time")
    jets=[f,g]
    for r in range(max_order):
        jets.append(jets[r].applyfunc(_laplace_spatial))
    corner_metric=[]
    corner_constraint=[]
    for r in range(max_order+1):
        j0=jets[r];j1=jets[r+1]
        metric=[S.expand((j1[I[ab[0]],I[ab[1]]]
                    -S.diff(j0[I[ab[0]],I[ab[1]]],x)).subs(x,0))
                for ab in TANGENT]
        cons=[S.expand((-j1[0,nu]+sum(
                  S.diff(j0[i,nu],COORDS[i])
                  for i in (1,2,3))).subs(x,0)) for nu in range(4)]
        corner_metric.append({"order":r,"passed":all(_zero(v) for v in metric),
              "residuals":[str(v) for v in metric]})
        corner_constraint.append({"order":r,"passed":all(_zero(v) for v in cons),
              "residuals":[str(v) for v in cons]})
    whole_initial_C=[
       S.expand(-jets[1][0,nu]+sum(
             S.diff(jets[0][i,nu],COORDS[i]) for i in (1,2,3)))
       for nu in range(4)]
    whole_initial_Ct=[
       S.expand(-jets[2][0,nu]+sum(
             S.diff(jets[1][i,nu],COORDS[i]) for i in (1,2,3)))
       for nu in range(4)] if len(jets)>2 else [
          S.expand(-_laplace_spatial(jets[0][0,nu])+sum(
               S.diff(jets[1][i,nu],COORDS[i]) for i in (1,2,3)))
          for nu in range(4)]
    passed=(all(_zero(v) for v in whole_initial_C+whole_initial_Ct)
        and all(v["passed"] for v in corner_metric+corner_constraint))
    result={"schema":"physqed.gh-higher-corners.v1",
      "status":("PASS_FINITE_ORDER_GH_CORNER_HIERARCHY" if passed else
                "FAILED_FINITE_ORDER_GH_CORNER_HIERARCHY"),
      "through_temporal_order":max_order,
      "initial_C_zero":all(_zero(v) for v in whole_initial_C),
      "initial_dt_C_zero":all(_zero(v) for v in whole_initial_Ct),
      "initial_C_residuals":[str(v) for v in whole_initial_C],
      "initial_dt_C_residuals":[str(v) for v in whole_initial_Ct],
      "six_Sommerfeld_corner_rows":corner_metric,
      "four_harmonic_constraint_corner_rows":corner_constraint,
      "all_temporal_orders_passed":passed,
      "all_orders_infinite_hierarchy_proven":False,
      "existence_of_smooth_boundary_solution_proven":False,
      "first_failure":{
          "sommerfeld":next((v["order"] for v in corner_metric
                 if not v["passed"]),None),
          "harmonic":next((v["order"] for v in corner_constraint
                 if not v["passed"]),None)},
      "reduced_wave_jet_recursion":"J_(r+2)=Delta J_r, J_0=f,J_1=g"}
    result["receipt_sha256"]=sha256(json.dumps(
        result,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return result

def certify_metric_corners(entries,max_order=5):
    """Use explicit time-dependent metric as source of Cauchy f,g."""
    metric=tensor(entries)
    f=_matrix_data(metric.applyfunc(lambda v:v.subs(t,0)))
    g=_matrix_data(metric.applyfunc(lambda v:S.diff(v,t).subs(t,0)))
    # Refuse a field that does not satisfy the reduced wave equations.
    if any(not _zero(-S.diff(v,t,2)+_laplace_spatial(v)) for v in metric):
        raise ValueError("provided explicit metric is not a reduced-wave solution")
    return initial_jet_hierarchy(f,g,max_order)

def replay_metric_corners(entries,stored,max_order=5):
    return isinstance(stored,dict) and stored==certify_metric_corners(entries,max_order)
