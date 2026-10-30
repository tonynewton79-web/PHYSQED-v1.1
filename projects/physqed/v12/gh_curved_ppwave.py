"""Exact curved Ricci-flat pp-wave GH bulk-intertwiner benchmark.

Brinkmann ds²=-2 du dv+dx²+dy²+(x²-y²) du² is Ricci flat
and genuinely curved. For an explicit nontrivial trace-reversed metric
perturbation, independently build delta-G from delta-Gamma and
delta-Ricci, check covariant linearized Bianchi and gauge-wave identity.
No curved boundary estimate, glancing theorem or nonlinear IBVP.
"""
from __future__ import annotations
import sympy as S
from hashlib import sha256
import json

u,v,x,y=S.symbols("u v x y",real=True)
COORDS=(u,v,x,y)


def verify_curved_ppwave():
    co=COORDS
    n=4
    g=S.Matrix([[x*x-y*y,-1,0,0],[-1,0,0,0],
                [0,0,1,0],[0,0,0,1]])
    gi=g.inv()
    ga=[[[S.simplify(sum(gi[a,d]*(S.diff(g[d,b],co[c])+
         S.diff(g[d,c],co[b])-S.diff(g[b,c],co[d])) for d in range(n))/2)
         for c in range(n)] for b in range(n)] for a in range(n)]
    ri=[[[[S.expand(S.diff(ga[a][b][d],co[c])-
         S.diff(ga[a][b][c],co[d])+sum(
         ga[a][c][k]*ga[k][b][d]-ga[a][d][k]*ga[k][b][c]
         for k in range(n))) for d in range(n)] for c in range(n)]
         for b in range(n)] for a in range(n)]
    ric=S.Matrix(n,n,lambda b,d:S.expand(sum(
        ri[a][b][a][d] for a in range(n))))
    contracted=[S.expand(sum(gi[b,c]*ga[a][b][c]
                  for b in range(n) for c in range(n))) for a in range(n)]
    def Dc1(C,k):
        return S.Matrix([S.expand(S.diff(C[b],co[k])-
            sum(ga[a][k][b]*C[a] for a in range(n))) for b in range(n)])
    def Dc2(T,k):
        return S.Matrix(n,n,lambda a,b:S.expand(S.diff(T[a,b],co[k])-
            sum(ga[c][k][a]*T[c,b]+ga[c][k][b]*T[a,c]
                for c in range(n))))
    def div2(T):
        return S.Matrix([S.expand(sum(gi[a,k]*Dc2(T,k)[a,b]
            for a in range(n) for k in range(n))) for b in range(n)])
    def div1(C):
        return S.expand(sum(gi[a,k]*Dc1(C,k)[a]
                 for a in range(n) for k in range(n)))
    def lap1(C):
        return S.Matrix([S.expand(sum(gi[a,k]*(
            S.diff(Dc1(C,a)[b],co[k])-sum(
            ga[c][k][a]*Dc1(C,c)[b]+ga[c][k][b]*Dc1(C,a)[c]
            for c in range(n))) for a in range(n) for k in range(n)))
            for b in range(n)])
    bar=S.zeros(n)
    bar[1,1]=u*x
    bar[0,2]=bar[2,0]=v*y
    bar[2,3]=bar[3,2]=x*y
    C=div2(bar)
    Q=S.Matrix(n,n,lambda a,b:S.expand(
        Dc1(C,a)[b]+Dc1(C,b)[a]-g[a,b]*div1(C)))
    trace=S.expand(sum(gi[a,b]*bar[a,b]
        for a in range(n) for b in range(n)))
    h=(bar-g*trace/2).applyfunc(S.expand)
    dga=[[[S.expand(sum(gi[a,d]*(Dc2(h,b)[d,c]+
         Dc2(h,c)[d,b]-Dc2(h,d)[b,c]) for d in range(n))/2)
         for c in range(n)] for b in range(n)] for a in range(n)]
    def Dmixed(A,k):
        return [[[S.expand(S.diff(A[a][b][c],co[k])+
            sum(ga[a][k][d]*A[d][b][c]-ga[d][k][b]*A[a][d][c]-
                ga[d][k][c]*A[a][b][d] for d in range(n)))
                for c in range(n)] for b in range(n)] for a in range(n)]
    diffs=[Dmixed(dga,k) for k in range(n)]
    dRic=S.Matrix(n,n,lambda a,b:S.expand(sum(
        diffs[c][c][a][b]-diffs[b][c][a][c] for c in range(n))))
    scalar=S.expand(sum(gi[a,b]*dRic[a,b]
                   for a in range(n) for b in range(n)))
    dG=(dRic-g*scalar/2).applyfunc(S.expand)
    reduced=(dG-Q/2).applyfunc(S.expand)
    qdiv=div2(Q)
    cwave=lap1(C)
    result={
        "schema":"physqed.curved-ppwave-intertwiner.v1",
        "background_metric":"ds^2=-2 du dv+dx^2+dy^2+(x^2-y^2)du^2",
        "Ricci_tensor_zero":bool(ric==S.zeros(n)),
        "harmonic_coordinates":all(a==0 for a in contracted),
        "curvature_R_x_u_x_u":str(ri[2][0][2][0]),
        "curvature_R_y_u_y_u":str(ri[3][0][3][0]),
        "nonflat_background":ri[2][0][2][0]!=0 and ri[3][0][3][0]!=0,
        "perturbation":"bar_h_vv=u*x; bar_h_ux=bar_h_xu=v*y; bar_h_xy=bar_h_yx=x*y",
        "linearized_harmonic_constraint":[str(a) for a in C],
        "linearized_Bianchi_div_dG_zero":bool(div2(dG)==S.zeros(n,1)),
        "curved_gauge_divergence_identity":bool(qdiv==cwave),
        "reduced_divergence_equals_minus_half_constraint_wave":
            bool(div2(reduced)==-cwave/2),
        "linearized_Einstein_residual_nonzero":dG!=S.zeros(n),
        "Ricci_coupling_in_general_constraint_wave":
            "box_g C_b+R_b^a C_a; Ricci=0 in this background",
        "curved_boundary_spectrum_proven":False,
        "curved_background_uniform_energy_proven":False,
        "curved_Einstein_IBVP_wellposedness_proven":False}
    good=all(result[k] for k in (
        "Ricci_tensor_zero","harmonic_coordinates","nonflat_background",
        "linearized_Bianchi_div_dG_zero",
        "curved_gauge_divergence_identity",
        "reduced_divergence_equals_minus_half_constraint_wave",
        "linearized_Einstein_residual_nonzero"))
    result["status"]=("PASS_EXACT_CURVED_BULK_GH_INTERTWINER" if good
                      else "REJECTED_CURVED_BULK_GH_INTERTWINER")
    result["receipt_sha256"]=sha256(json.dumps(
        result,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return result


def replay_curved_ppwave(stored):
    return isinstance(stored,dict) and stored==verify_curved_ppwave()
