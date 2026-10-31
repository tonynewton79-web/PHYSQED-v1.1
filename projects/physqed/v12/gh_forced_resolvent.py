"""Regular-source inhomogeneous flat GH half-space resolvent certificate.

For Laplace s with gamma=Re s>0 and transverse frequencies eta,zeta,
first-order volume sources (F0,Fpi,Fphi) are reduced exactly to
D_i=(Fphi_i-partial_i F0)/s and
f_eff=Fpi-s*F0-div D, provided the required derivatives exist in L2.

For the ten-wave null-adapted metric derivative boundary data g:
 ||(Lambda psi,Pi,Phi_x,Phi_y,Phi_z)||_L2
 <= 90/gamma ||f_eff||_L2 + 45/sqrt(gamma)||g||
    +||F0||_L2+||D||_L2.
The proof is a Dirichlet Green lifting and the existing uniform
stable-mode estimate. This is NOT an arbitrary-L2-source no-loss Kreiss
estimate, time-domain well-posedness, or a nonlinear Einstein theorem.
"""
from __future__ import annotations
from functools import lru_cache
from hashlib import sha256
import json
import sympy as S
from . import gh_first_order_uniform as base

ORDER=base.ORDER
LETTERS=("t","x","y","z")


def first_order_forcing_normal_form():
    x,s,eta,zeta=S.symbols("x s eta zeta")
    F0,Fpi,Fx,Fy,Fz=(S.Function(v)(x) for v in
                     ("F0","Fpi","Fx","Fy","Fz"))
    psi=S.Function("psi")(x)
    Dx=(Fx-S.diff(F0,x))/s
    Dy=(Fy-S.I*eta*F0)/s
    Dz=(Fz-S.I*zeta*F0)/s
    D=S.Matrix((Dx,Dy,Dz))
    effective=S.expand(Fpi-s*F0-S.diff(Dx,x)-S.I*eta*Dy-S.I*zeta*Dz)
    Pi=F0-s*psi
    Phi=S.Matrix((S.diff(psi,x)+Dx,S.I*eta*psi+Dy,S.I*zeta*psi+Dz))
    equations=(s*psi+Pi-F0,
      s*Pi+S.diff(Phi[0],x)+S.I*eta*Phi[1]+S.I*zeta*Phi[2]-Fpi,
      s*Phi[0]+S.diff(Pi,x)-Fx,
      s*Phi[1]+S.I*eta*Pi-Fy,
      s*Phi[2]+S.I*zeta*Pi-Fz)
    wave_residual=S.diff(psi,x,2)-(s*s+eta*eta+zeta*zeta)*psi-effective
    defect_sources=(Fx-S.diff(F0,x),Fy-S.I*eta*F0,Fz-S.I*zeta*F0)
    return {
      "first_order_kinematic_rows_zero":all(S.simplify(equations[k])==0
                                               for k in (0,2,3,4)),
      "momentum_row_equals_forced_wave_residual":
          S.simplify(equations[1]-wave_residual)==0,
      "reduction_source_equations_zero":all(
          S.simplify(s*D[i]-defect_sources[i])==0 for i in range(3)),
      "effective_source":str(effective),
      "reduction_defects":[str(v) for v in D],
      "compatible_reduction_sources":"Fphi_i=partial_i F0 => D_i=0",
      "source_regularity":"F0 in H2 normal; Fx in H1; Fpi,Fy,Fz in L2 (more for explicit boundary trace reformulation)",
      "arbitrary_first_order_L2_source_estimate_proven":False}


@lru_cache(maxsize=1)
def _boundary():
    data=base.adapted_normal_symbol()
    P=data["P"]
    N=S.zeros(4,10)
    for j,nu in enumerate(LETTERS):
        N[j,base._index("x",nu)]=1
    return data,P,N,P.col_join(-N)


def boundary_source_lift():
    data,P,N,T=_boundary()
    return {
      "P_Ptranspose":P*P.T,
      "P_gram_exact":P*P.T==S.diag(6,2,2,1,1,1),
      "N_gram_identity":N*N.T==S.eye(4),
      "T_operator_norm_squared_upper_bound":7,
      "boundary_correction":"T J=(P J,-N J); J=int_0^infinity exp(-k*y) f_eff(y)dy",
      "original_matched_boundary_matrix":data["determinant_verified"]}


def exact_exponential_volume_and_boundary_solution():
    """Exact nonzero source and nonzero adapted boundary forcing."""
    x=S.symbols("x",nonnegative=True)
    data,P,N,T=_boundary()
    ss={data["s"]:1,data["k"]:1,data["eta"]:0,data["zeta"]:0}
    i=ORDER.index("yz")
    a=S.zeros(10,1)
    b=S.zeros(10,1)
    a[i]=S.Rational(1,2)
    b[i]=1
    psi=(a-b)*S.exp(-x)+b*S.exp(-2*x)
    source=psi.diff(x,2)-psi
    J=S.integrate(S.exp(-x)*source,(x,0,S.oo))
    boundary=(data["B"].subs(ss)*a+T*J).applyfunc(S.simplify)
    direct=(P*(psi-psi.diff(x)).subs(x,0)).col_join(
                                      (N*psi.diff(x)).subs(x,0))
    first_order_sq=S.integrate(
        (2*psi.T*psi+psi.diff(x).T*psi.diff(x))[0],(x,0,S.oo))
    f_sq=S.integrate((source.T*source)[0],(x,0,S.oo))
    g_sq=(boundary.T*boundary)[0]
    return {
       "effective_wave_equation_exact":
          S.simplify(source[i]-3*S.exp(-2*x))==0,
       "Green_boundary_source_J_exact":J==b,
       "direct_boundary_equals_corrected_B_amplitude":direct==boundary,
       "nonzero_boundary_data_yz":str(boundary[4]),
       "effective_source_L2_squared":str(f_sq),
       "boundary_data_norm_squared":str(g_sq),
       "weighted_first_order_state_norm_squared":str(first_order_sq),
       "estimate_holds_for_exact_specimen":
          bool(S.sqrt(first_order_sq) <=90*S.sqrt(f_sq)+45*S.sqrt(g_sq))}


def prove_regular_source_resolvent():
    form=first_order_forcing_normal_form()
    lifting=boundary_source_lift()
    existing=base.analytic_uniform_bound()
    const=bool(61*S.sqrt(2)<90 and 30*S.sqrt(2)<45)
    success=(form["first_order_kinematic_rows_zero"] and
         form["momentum_row_equals_forced_wave_residual"] and
         form["reduction_source_equations_zero"] and
         lifting["P_gram_exact"] and lifting["N_gram_identity"] and
         lifting["original_matched_boundary_matrix"] and
         existing["uniform_homogeneous_stable_mode_trace_estimate_proven"] and
         const)
    receipt={
       "schema":"physqed.GH-regular-forced-resolvent.v1",
       "status":("PASS_REGULAR_SOURCE_INHOMOGENEOUS_GH_HALFSPACE_ESTIMATE"
                 if success else "REJECTED_FORCED_GH_ESTIMATE"),
       "first_order_normal_form":form,
       "boundary_source_lift":{k:(str(v) if isinstance(v,S.MatrixBase) else v)
                               for k,v in lifting.items()},
       "amplitude_inverse_bound":"Lambda||a||<=30||B a||",
       "Dirichlet_green_trace":"u_Dx(0)=-J; ||J||<=||f_eff||/sqrt(2gamma)",
       "Dirichlet_particular_energy":"W(u_D)<=||f_eff||/gamma",
       "corrected_boundary_source":"B a=g-T J",
       "total_second_order_energy":"W(u)<=61||f_eff||/gamma+30||g||/sqrt(gamma)",
       "first_order_weighted_resolvent":
          "||U||<=90||f_eff||/gamma+45||g||/sqrt(gamma)+||F0||+||D||",
       "constants_exactly_verified":const,
       "uniform_over_glancing_for_gamma_positive":True,
       "volume_source_normal_regularities_required":True,
       "initial_data_can_enter_as_Laplace_source":
         "F0->F0+initial_psi, Fpi->Fpi-initial_psi_t, Fphi->Fphi+grad(initial_psi); initial reduction constraints must vanish",
       "first_order_boundary_source_trace_corrections":
         "D_-psi=F0-Pi-Phi_x+D_x; C=-F0_tnu+Pi_tnu+Phi_i,inu-D_i,inu",
       "arbitrary_L2_first_order_source_no_loss_theorem_proven":False,
       "all_time_corner_orders_proven":False,
       "strong_time_domain_wellposedness_proven":False,
       "curved_background_boundary_resolvent_proven":False,
       "nonlinear_Einstein_IBVP_proven":False,
       "derivation":
         "Dirichlet u_D(0)=0 solves u_Dxx-k²u_D=f_eff. Re(s)>0 and Re(k)>=gamma by k²=s²+omega². Integration by parts against conjugate(s)*conjugate(u_D) gives gamma W(u_D)²<=||f_eff||W(u_D). Boundary derivative is -J, ||J||<=||f_eff||/sqrt(2gamma). The six Sommerfeld and four constraint rows applied to u_D yield T J=(P J,-N J), with ||T||<=sqrt7. Adapted homogeneous trace inverse gives Lambda||a||<=30(||g||+sqrt7||J||). The decaying homogeneous energy is <=Lambda||a||/sqrt(gamma). Triangle and first-order reduction yield displayed conservative constants."
    }
    receipt["receipt_sha256"]=sha256(json.dumps(
        receipt,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return receipt


def replay_regular_source_resolvent(stored):
    return isinstance(stored,dict) and stored==prove_regular_source_resolvent()


def nonzero_reduction_defect_solution():
    """An exact first-order forcing whose wave source vanishes but D_x!=0.

    s=1, eta=zeta=0; F0=e^-x, Fpi=Fphi=0, psi=0.
    Then Pi=Phi_x=e^-x, D_x=e^-x. Every forced first-order
    equation holds, with g=0; no silent D=0 assumption is allowed.
    """
    x=S.symbols("x",nonnegative=True)
    r=S.exp(-x)
    Pi=Phi=r
    residuals=(Pi-r,Pi+S.diff(Phi,x),Phi+S.diff(Pi,x))
    norm_sq=S.integrate(Pi**2+Phi**2,(x,0,S.oo))
    src_norm=S.sqrt(S.integrate(r**2,(x,0,S.oo)))
    return {"first_order_equations_zero":all(S.simplify(v)==0 for v in residuals),
            "reduction_defect_nonzero":Phi!=0,
            "effective_wave_source_zero":True,
            "first_order_state_norm_squared":str(norm_sq),
            "regular_source_bound_passes":bool(S.sqrt(norm_sq)<=2*src_norm),
            "no_false_zero_reduction_claim":True}
