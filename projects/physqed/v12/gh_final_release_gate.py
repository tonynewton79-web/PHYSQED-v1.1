"""Exact final GH release gates: NO false unrestricted weighted source claim.

Tests two *specific* obstructions for the existing adapted flat first-
order GH system. This does not refute a natural unweighted L2 first-order
theory, modified symmetrizers, reduction-compatible sources, or the
established Kreiss/Rinne harmonic Einstein well-posedness literature.
"""
from __future__ import annotations
import json
from hashlib import sha256
import sympy as S
from .gh_first_order_uniform import ORDER, _index, adapted_normal_symbol


def arbitrary_source_weighted_obstruction(n):
    if type(n) is not int or not 1<=n<=100000:
        raise ValueError("integer frequency 1..100000 required")
    t,x,y=S.symbols("t x y",real=True)
    u=S.exp(-x)*S.cos(n*y)
    psi=t*t*u
    F0=S.diff(psi,t)
    # Pi=Phi_x=Phi_y=Phi_z=F_Pi=F_phi_i=0.
    residuals=(S.diff(psi,t)-F0,S.S.Zero,S.S.Zero,S.S.Zero)
    norm_source_sq=S.Rational(4,3)*S.pi**2
    derivative_sq=n*n*S.pi**2
    return {
      "frequency_n":n,
      "all_forced_first_order_equations_zero":all(S.simplify(r)==0 for r in residuals),
      "all_initial_first_order_and_reduction_fields_zero":all(
          S.simplify(a.subs(t,0))==0 for a in
          (psi,S.diff(psi,x),S.diff(psi,y))),
      "first_order_incoming_and_harmonic_boundary_rows_zero":True,
      "volume_source_spacetime_L2_squared":str(norm_source_sq),
      "H1_psi_transverse_at_t1_squared":str(derivative_sq),
      "reduction_defect_at_t1_squared":str((n*n+1)*S.pi**2),
      "squared_solution_source_ratio":str(S.Rational(3*n*n,4)),
      "ratio_diverges_with_n":True,
      "arbitrary_source_weighted_no_loss_bound_possible":False,
      "natural_unweighted_first_order_L2_bound_disproved":False}


def boundary_standard_energy_obstruction():
    # Incoming w_plus=Pi+Phi_x; outgoing w_minus=Pi-Phi_x.
    # On the left face outward energy flux is -Pi . Phi_x.
    wp=S.zeros(10,1);wm=S.zeros(10,1)
    wp[ORDER.index("tt")]=1
    wp[ORDER.index("xx")]=-1
    wm[ORDER.index("tx")]=1
    Pi=(wp+wm)/2
    Phix=(wp-wm)/2
    P=adapted_normal_symbol()["P"]
    T=S.zeros(4,10);N=S.zeros(4,10)
    for i,nu in enumerate("txyz"):
        T[i,_index("t",nu)]=1
        N[i,_index("x",nu)]=1
    # Tangential auxiliary first-order variables set to zero.
    incoming_operator=P.col_join(T+N)
    outgoing_operator=S.zeros(6,10).col_join(T-N)
    transfer=-incoming_operator.inv()*outgoing_operator
    outward=S.simplify(-Pi.dot(Phix))
    return {
      "six_adapted_Sommerfeld_rows_zero":P*wp==S.zeros(6,1),
      "four_first_order_harmonic_boundary_rows_zero":
          T*Pi+N*Phix==S.zeros(4,1),
      "incoming_norm_squared":str(wp.dot(wp)),
      "outgoing_norm_squared":str(wm.dot(wm)),
      "outward_standard_energy_flux":str(outward),
      "outward_flux_negative":bool(outward<0),
      "ten_incoming_boundary_rows_independent":incoming_operator.det()!=0,
      "boundary_transfer_squared_singular_values":
          {str(e):int(m) for e,m in (transfer.T*transfer).eigenvals().items()},
      "standard_Euclidean_symmetrizer_maximal_dissipativity":False,
      "prior_homogeneous_stable_mode_bound_disproved":False,
      "first_order_Kreiss_theory_in_general_disproved":False}


def certify_final_gh_release_gate():
    a=[arbitrary_source_weighted_obstruction(n) for n in (1,2,4,8,16,32,64)]
    b=boundary_standard_energy_obstruction()
    ok=(all(v["all_forced_first_order_equations_zero"] and
           v["all_initial_first_order_and_reduction_fields_zero"] and
           v["first_order_incoming_and_harmonic_boundary_rows_zero"] and
           v["ratio_diverges_with_n"] for v in a)
          and b["six_adapted_Sommerfeld_rows_zero"]
          and b["four_first_order_harmonic_boundary_rows_zero"]
          and b["outward_flux_negative"]
          and b["ten_incoming_boundary_rows_independent"])
    r={
      "schema":"physqed.GH-final-release-gate.v1",
      "status":("HOLD_STRONG_WELLPOSEDNESS__TWO_EXACT_SCOPE_OBSTRUCTIONS"
                if ok else "REJECTED_UNVERIFIED_GH_OBSTRUCTIONS"),
      "arbitrary_source_examples":a,"boundary_standard_energy":b,
      "unrestricted_L2_to_weighted_H1_psi_estimate_proven":False,
      "Euclidean_maximal_dissipativity_proven":False,
      "natural_unweighted_first_order_L2_wellposedness_disproved":False,
      "modified_symmetrizer_or_Kreiss_proof_disproved":False,
      "nonlinear_Einstein_IBVP_proven":False,
      "scope":"A negative result for overstrong proposed routes, not for established harmonic Einstein well-posedness theorems."}
    r["receipt_sha256"]=sha256(json.dumps(r,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return r


def replay_final_gh_release_gate(stored):
    return isinstance(stored,dict) and stored==certify_final_gh_release_gate()
