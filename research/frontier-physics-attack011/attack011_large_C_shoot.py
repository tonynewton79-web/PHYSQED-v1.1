"""Attack011 high-amplitude exterior shooting — NONRIGOROUS diagnostic.

Start from a high-order FORMAL zero-mass inverse-radius tail at r=2000,
4000 and integrate exact radial ODE inward with DOP853 (plus Radau).
A root in the finite-radius Killing norm does NOT prove matching at
infinity, exact exterior existence, or a physical black hole.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
EPS=.001

def rhs(r,y):
    N,A,V,K=y
    S=-A*A*r*(N*N-1)/(2*N**4)
    NP=N*(A*A-1)/(2*r)+A*A*(EPS*N*K*K*r/4+K*V-3*V*V/(2*N*r))+A*A*N*r*(N**-2-1)**2/8
    AP=A*(S-NP/N); VP=N*K-2*V/r-AP*V/A; KP=2*V*S/(EPS*N*r)
    return (NP,AP,VP,KP)

def tail(C,R):
    e=EPS;c=float(C)
    a4=1.5*c*c;a6=-36*c*c
    a8=-3*c*c*(3*c*c*e+8*c*c-3840*e)/(8*e)
    n6=6*c*c;n8=-180*c*c
    n10=-12*c*c*(3*c*c*e+2*c*c-840*e)/e
    v6=-3*c**3*(7*e+2)/(14*e)
    v8=4*c**3*(27*e+5)/(3*e)
    v10=3*c**3*(693*c*c*e*e+808*c*c*e+124*c*c-295680*e*e-47040*e)/(616*e*e)
    k7=12*c**3/(7*e);k9=-40*c**3/e
    k11=-6*c**3*(63*c*c*e+62*c*c-23520*e)/(77*e*e)
    return [
       1+n6/R**6+n8/R**8+n10/R**10,
       1+a4/R**4+a6/R**6+a8/R**8,
       c/R**2+v6/R**6+v8/R**8+v10/R**10,
       k7/R**7+k9/R**9+k11/R**11]

def shoot(C,R,method="DOP853"):
    sol=solve_ivp(rhs,(R,2),tail(C,R),method=method,
                  rtol=2e-10,atol=2e-12,max_step=8)
    assert sol.success and sol.t[-1]==2
    y=sol.y[:,-1]
    N,A,V,K=y
    return y, -N*N+A*A*V*V

def main():
    for R in (2000.,4000.):
        low=shoot(7000.,R)[1];high=shoot(7500.,R)[1]
        assert low<-.01 and high>.02
        root=brentq(lambda C:shoot(C,R)[1],7000.,7500.,xtol=5e-6)
        y,g=shoot(root,R)
        assert abs(g)<1e-7 and 7000<root<7500
        assert y[1]>1.006 and y[2]>.99 and y[3]>.73
        # Exact Attack007 local BVP has A(2) in [0.999,1.001];
        # these are disjoint at the level of this NUMERICAL shoot.
        assert y[1]-1.001>.005
        print("R",R,"C_root",format(root,'.7f'),"y(2)",[round(v,9) for v in y])
        print("gtt2 at C=7000,7500",low,high)
    yD,gD=shoot(7500.,2000.,'DOP853')
    yR,gR=shoot(7500.,2000.,'Radau')
    assert np.max(np.abs(yD-yR))<2e-6
    print("PASS DOP853/Radau agreement at C=7500, r=2 within 2e-6")
    print("DIAGNOSTIC ONLY: R->infinity boundary was truncated, not interval-proved")
    print("NO certified large-C matching or globally physical massless horizon")

if __name__=="__main__":main()
