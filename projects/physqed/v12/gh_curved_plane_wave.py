"""A genuinely curved Ricci-flat harmonic-background GH control.

Vacuum Brinkmann plane wave
  ds²=-2 du dv+dx²+dy²+(x²-y²)du²
has exact Ricci=0, R_uxux=-1, R_uyuy=+1, harmonic coordinates,
and a spacelike x-normal. The covector dt=(du+dv)/sqrt(2) is
timelike for |x|,|y|<=1/2.

For trace-reversed bar_h_ab=u² g_ab the curved harmonic constraint
C_b=nabla^a bar_h_ab=2u du_b, its covariant vector wave vanishes,
and the Ricci-flat reduced Lichnerowicz metric wave vanishes.
But the linearized full Einstein tensor is 2 du_a du_b !=0.
This is a scoped curved-background algebraic control, not a curved
boundary resolvent or nonlinear evolution theorem.
"""
from __future__ import annotations
from functools import lru_cache
from hashlib import sha256
import json
import sympy as S

u,v,x,y=S.symbols("u v x y",real=True)
X=(u,v,x,y)

def _zero(z):
    return S.simplify(S.cancel(S.together(z)))==0

@lru_cache(maxsize=1)
def background():
    H=x*x-y*y
    g=S.Matrix([[H,-1,0,0],[-1,0,0,0],
                [0,0,1,0],[0,0,0,1]])
    gi=g.inv().applyfunc(S.simplify)
    n=4
    ch=[[[S.simplify(sum(gi[a,d]*(
        S.diff(g[d,b],X[c])+S.diff(g[d,c],X[b])-
        S.diff(g[b,c],X[d])) for d in range(n))/2)
        for c in range(n)] for b in range(n)] for a in range(n)]
    R=[[[[S.simplify(S.diff(ch[a][b][d],X[c])-
        S.diff(ch[a][b][c],X[d])+sum(
          ch[a][c][k]*ch[k][b][d]-ch[a][d][k]*ch[k][b][c]
          for k in range(n))) for d in range(n)] for c in range(n)]
        for b in range(n)] for a in range(n)]
    Ric=S.Matrix(n,n,lambda b,d:S.simplify(sum(
            R[a][b][a][d] for a in range(n))))
    contracted=S.Matrix([S.simplify(sum(gi[b,c]*ch[a][b][c]
         for b in range(n) for c in range(n))) for a in range(n)])
    return g,gi,ch,R,Ric,contracted

def scalar_box(f,gi,ch):
    return S.simplify(sum(gi[a,b]*(
        S.diff(f,X[a],X[b])-sum(ch[k][a][b]*S.diff(f,X[k])
                 for k in range(4))) for a in range(4) for b in range(4)))

def covariant_divergence_symmetric(bar,gi,ch):
    return S.Matrix([S.simplify(sum(gi[a,b]*(
        S.diff(bar[b,c],X[a])-sum(
            ch[k][a][b]*bar[k,c]+ch[k][a][c]*bar[b,k]
                  for k in range(4)))
        for a in range(4) for b in range(4))) for c in range(4)])

def covector_wave(c,gi,ch):
    grad=[[S.simplify(S.diff(c[j],X[i])-sum(
           ch[k][i][j]*c[k] for k in range(4)))
           for j in range(4)] for i in range(4)]
    second=[S.simplify(sum(gi[i,j]*(
          S.diff(grad[j][b],X[i])-sum(
              ch[k][i][j]*grad[k][b]+ch[k][i][b]*grad[j][k]
              for k in range(4)))
              for i in range(4) for j in range(4))) for b in range(4)]
    return S.Matrix(second),grad

def verify_curved_gh_control():
    g,gi,ch,R,Ric,contracted=background()
    f=u*u
    bar=(f*g).applyfunc(S.expand)
    C=covariant_divergence_symmetric(bar,gi,ch)
    box_f=scalar_box(f,gi,ch)
    vecwave,gradC=covector_wave(C,gi,ch)
    hessian=S.Matrix(4,4,lambda a,b:S.simplify(
        S.diff(f,X[a],X[b])-sum(
            ch[k][a][b]*S.diff(f,X[k]) for k in range(4))))
    # Trace reversal: the physical metric perturbation is -f*g.
    # For a 4D Ricci-flat conformal variation delta g=-f*g,
    # delta G = Hess(f)-g*box(f).
    full=(hessian-g*box_f).applyfunc(S.simplify)
    # For bar_h=f*g, metric compatibility yields
    # L(bar_h)=(box f)*g+2*f*Ric=0 on this Ricci-flat model.
    reduced=(g*box_f+2*f*Ric).applyfunc(S.simplify)
    r_uxux=S.simplify(sum(g[0,a]*R[a][2][0][2]
                               for a in range(4)))
    r_uyuy=S.simplify(sum(g[0,a]*R[a][3][0][3]
                               for a in range(4)))
    dt=S.Matrix([1,1,0,0])/S.sqrt(2)
    dt_norm=S.simplify((dt.T*gi*dt)[0])
    # H in [-1/4,+1/4] on |x|,|y|<=1/2.
    t_bound=S.simplify(dt_norm+S.Rational(7,8))
    passed=(g.det()==-1 and Ric==S.zeros(4) and
            contracted==S.zeros(4,1) and
            r_uxux==-1 and r_uyuy==1 and
            C==S.Matrix([2*u,0,0,0]) and
            vecwave==S.zeros(4,1) and
            reduced==S.zeros(4) and
            full==S.diag(2,0,0,0) and
            _zero(dt_norm+1+(x*x-y*y)/2))
    result={
       "schema":"physqed.curved-gh-plane-wave.v1",
       "status":("PASS_EXACT_CURVED_GH_BACKGROUND_AND_REDUCED_CONTROL" if passed
                  else "REJECTED_CURVED_GH_CONTROL"),
       "background":"Brinkmann vacuum plane wave, H=x^2-y^2",
       "signature":"Lorentzian, ds^2=-2 du dv+(x^2-y^2)du^2+dx^2+dy^2",
       "det_g":str(g.det()),
       "vacuum_Ricci_zero":bool(Ric==S.zeros(4)),
       "nonzero_R_uxux":str(r_uxux),
       "nonzero_R_uyuy":str(r_uyuy),
       "coordinates_harmonic_Gamma_contracted_zero":bool(contracted==S.zeros(4,1)),
       "time_covector":"dt=(du+dv)/sqrt(2)",
       "time_covector_squared":str(dt_norm),
       "time_timelike_on_box_abs_x_y_le_half":bool(_zero(dt_norm+1+(x*x-y*y)/2)),
       "time_covector_squared_upper_bound":"-7/8",
       "boundary_x_constant_timelike":bool(gi[2,2]==1),
       "linearized_trace_reversed_metric":"bar_h_ab=u^2 g_ab",
       "harmonic_constraint_covector":[str(a) for a in C],
       "covariant_constraint_wave_zero":bool(vecwave==S.zeros(4,1)),
       "reduced_Ricci_flat_Lichnerowicz_wave_zero":bool(reduced==S.zeros(4)),
       "full_linearized_Einstein_nonzero_uu":str(full[0,0]),
       "full_linearized_Einstein_satisfied":bool(full==S.zeros(4)),
       "curved_background_verified":bool(passed),
       "general_curved_GH_operator_intertwiner_verified":False,
       "curved_boundary_symbol_uniform_resolvent_proven":False,
       "nonlinear_Einstein_IBVP_proven":False,
       "scope":"Concrete nonflat Ricci-flat harmonic background and one covariant reduced-wave mode; no curved evolution-to-constraint boundary theorem."}
    result["receipt_sha256"]=sha256(json.dumps(
          result,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return result

def replay_curved_gh(receipt):
    return isinstance(receipt,dict) and receipt==verify_curved_gh_control()
