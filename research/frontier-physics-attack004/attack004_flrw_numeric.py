"""Numerical local flat-FLRW bounce diagnostic; NOT observational data.

P(X)=X^2-3X/2, reduced Mpl=1, X=dot(phi)^2/2.
Shows a mathematically consistent but scalar gradient-unstable bounce.
"""
import numpy as np
from scipy.integrate import solve_ivp

def rhs(t,y):
    a,H,X=y
    PX=2*X-1.5
    K=6*X-1.5
    return [a*H,-X*PX,-6*H*X*PX/K]

def rho(X):
    return 3*X*X-1.5*X

def main():
    Y=[]
    for tf in (0.5,-0.5):
        sol=solve_ivp(rhs,(0,tf),[1.,0.,0.5],method="DOP853",rtol=1e-12,atol=1e-14,dense_output=True)
        assert sol.success
        Y.append(sol.sol(np.linspace(0,tf,151)))
    a,H,X=np.hstack(Y)
    K=6*X-1.5
    cs2=(2*X-1.5)/K
    res=np.max(np.abs(3*H**2-rho(X)))
    assert res<1e-10
    assert np.min(K)>0 and np.max(cs2)<0 and np.min(a)>=1-1e-10
    print("PASS: 301 sampled points t in [-0.5,0.5], constraint residual",res)
    print("PASS: positive kinetic K and negative sound speed squared throughout")
    print("This does not represent a stable cosmology or observational fit.")

if __name__=="__main__":
    main()
