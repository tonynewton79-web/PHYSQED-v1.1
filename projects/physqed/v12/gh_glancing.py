"""Exact glancing obstruction and off-glancing boundary-symbol bound.

The existing ten-row boundary matrix is invertible at every strict
Re(s)>0 decaying mode, but fails the UNWEIGHTED normalized uniform
Kreiss/Lopatinski lower bound at glancing. The explicit amplitude
(H_tx,H_xx)=(k,-s) yields boundary residual -k^2.

Away from glancing, |k|>=delta*p, a direct triangular estimate
supplies a quantitative normalized inverse bound. Neither statement
by itself proves a full PDE well-posedness theorem.
"""
from __future__ import annotations
import cmath
import math
from hashlib import sha256
import json
import sympy as S
from .gh_boundary_map import normal_mode_symbol

def _algebraic_zero(expr):
    return S.simplify(S.expand(expr))==0

def symbolic_glancing_obstruction():
    result=normal_mode_symbol()
    B=result["ten_by_ten_boundary_symbol"]
    s,k,eta,zeta=S.symbols("s k eta zeta")
    h=S.zeros(10,1)
    h[6]=k       # trace-reversed h_tx
    h[9]=-s      # trace-reversed h_xx
    residual=B*h
    desired=S.zeros(10,1)
    desired[6]=-k*k     # C_t; every other row cancels
    return {
      "exact_boundary_symbol_factorization":bool(result["factorization_verified"]),
      "explicit_glancing_amplitude_verified":all(_algebraic_zero(residual[i]-desired[i]) for i in range(10)),
      "amplitude_nonzero_for_glancing_sequence":True,
      "metric_amplitude_indices":["tx","xx"],
      "metric_amplitude":["k","-s"],
      "only_nonzero_boundary_row":"C_t=-k^2",
      "glancing_sequence":"s=epsilon+i, eta=1, zeta=0, k=sqrt(epsilon^2+2*i*epsilon), epsilon>0",
      "frequency_normalization":"p=sqrt(|s|^2+eta^2+zeta^2)",
      "boundary_to_amplitude_normalized_upper_bound":
          "||B H||/(p||H||) <= sqrt(5/2)*epsilon for 0<epsilon<=1",
      "uniform_unweighted_normalized_lopatinski_bound_proven":False,
      "uniform_unweighted_normalized_lopatinski_bound_refuted":True,
      "uniform_weighted_resolvent_estimate_proven":False,
      "nonlinear_Einstein_IBVP_proven":False,
    }

def off_glancing_constant(delta):
    """Explicit C(delta) in ||H||<=C(delta) ||B H||/p.

    If |k|>=delta*p with p=sqrt(|s|^2+eta^2+zeta^2),
    Re(s)>0, Re(k)>0 and k^2=s^2+eta^2+zeta^2, then

       |s+k|>=p/sqrt(2);
       ||C_tangent||<=sqrt(3)*p<=2p;
       ||D_normal^-1||<= (1/delta+1/delta^2)/p.

    The remaining 4x4 normal block equals -k I+N, N^2=0
    with ||N||<=p. The combined bound is conservative.
    """
    if not isinstance(delta,(int,float)) or isinstance(delta,bool) or not (0<delta<=1):
        raise ValueError("0<delta<=1 required")
    d=float(delta)
    return math.sqrt(2)+(1/d+1/(d*d))*(1+2*math.sqrt(2))

def glancing_trials():
    values=[]
    for eps in (0.1,0.01,0.001,0.0001):
        s=eps+1j
        k=cmath.sqrt(s*s+1)
        p=math.sqrt(abs(s)**2+1)
        amplitude=math.sqrt(abs(k)**2+abs(s)**2)
        ratio=(abs(k)**2)/(p*amplitude)
        bound=math.sqrt(5/2)*eps
        values.append({"epsilon":eps,"normalized_residual_ratio":ratio,
                       "analytic_upper_bound":bound,"bound_satisfied":ratio<=bound,
                       "strictly_decaying":k.real>0})
    return values

def certify_glancing_gate():
    algebra=symbolic_glancing_obstruction()
    samples=glancing_trials()
    ok=(algebra["exact_boundary_symbol_factorization"]
        and algebra["explicit_glancing_amplitude_verified"]
        and all(x["bound_satisfied"] and x["strictly_decaying"] for x in samples))
    result={"schema":"physqed.gh-glancing-audit.v1",
            "status":("PASS_EXACT_UNIFORM_BOUND_OBSTRUCTION" if ok
                      else "REJECTED_GLANCING_AUDIT"),
            "algebra":algebra,
            "numerical_sanity_checks":samples,
            "off_glancing_normalized_inverse_constant_at_delta_1_over_4":
                off_glancing_constant(0.25),
            "off_glancing_assumption":"|k|>=delta*p; Re(s)>0; Re(k)>0",
            "claim_boundary":"The specific 6 Sommerfeld plus 4 Dirichlet harmonic constraints has no UNWEIGHTED uniform boundary inverse near glancing. An away-from-glancing bound is algebraic; no global PDE stability or weighted estimate."}
    result["receipt_sha256"]=sha256(json.dumps(
          result,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return result

def replay_glancing_gate(receipt):
    return isinstance(receipt,dict) and receipt==certify_glancing_gate()
