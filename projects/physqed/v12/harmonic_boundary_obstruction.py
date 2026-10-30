"""Exact negative control for naive harmonic Einstein boundary claims.

On Minkowski, the trace-reversed linearized metric perturbation
bar_h_xx=t*x (all others zero) solves box bar_h_ab=0 and has
homogeneous Dirichlet data at x=0. But its harmonic constraint
C_mu=partial^nu bar_h_munu has C_x=t at that boundary, nonzero.
This is NOT an example with vanishing initial time derivative of C
and not a counterexample to proper constraint-preserving BCs.
"""
import sympy as S
import json
from hashlib import sha256


def verify_harmonic_boundary_obstruction():
    t,x,y,z=S.symbols("t x y z",real=True)
    coords=(t,x,y,z)
    eta=S.diag(-1,1,1,1)
    bar=S.zeros(4)
    bar[1,1]=t*x
    wave=bar.applyfunc(lambda f:S.simplify(-S.diff(f,t,2)+sum(
        S.diff(f,c,2) for c in (x,y,z))))
    boundary=bar.subs(x,0)
    C=S.Matrix([sum(eta[k,k]*S.diff(bar[i,k],coords[k])
        for k in range(4)) for i in range(4)])
    C_boundary=C.subs(x,0)
    wave_C=C.applyfunc(lambda f:S.simplify(-S.diff(f,t,2)+sum(
        S.diff(f,c,2) for c in (x,y,z))))
    result={
        "schema":"physqed.harmonic-boundary-obstruction.v1",
        "linearized_trace_reversed_metric":"bar_h_xx=t*x, all other components zero",
        "reduced_wave_equations_zero":bool(wave==S.zeros(4)),
        "homogeneous_Dirichlet_metric_at_x0":bool(boundary==S.zeros(4)),
        "harmonic_constraints":[str(v) for v in C],
        "harmonic_constraints_at_x0":[str(v) for v in C_boundary],
        "constraint_wave_equations_zero":bool(wave_C==S.zeros(4,1)),
        "nonzero_boundary_constraint":bool(C_boundary[1]!=0),
        "initial_constraint_field_zero":bool(C.subs(t,0)==S.zeros(4,1)),
        "initial_constraint_time_derivative_zero":bool(
            C.diff(t).subs(t,0)==S.zeros(4,1)),
        "Dirichlet_implies_harmonic_constraint_preservation":False,
        "full_linearized_Einstein_equations_verified":False,
        "nonlinear_Einstein_boundary_well_posedness_proven":False}
    passed=(result["reduced_wave_equations_zero"] and
            result["homogeneous_Dirichlet_metric_at_x0"] and
            result["constraint_wave_equations_zero"] and
            result["nonzero_boundary_constraint"])
    result["status"]=("PASS_EXACT_BOUNDARY_TO_CONSTRAINT_OBSTRUCTION"
                      if passed else "REJECTED_OBSTRUCTION_CHECK")
    result["receipt_sha256"]=sha256(json.dumps(
        result,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return result


def replay_harmonic_boundary_obstruction(stored):
    return isinstance(stored,dict) and stored==verify_harmonic_boundary_obstruction()
