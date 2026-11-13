"""NONRIGOROUS outer-radius continuation diagnostic for exact local BVP.

DOP853 and Radau cross-check, NOT a validated global solution,
asymptotic theorem, or physical stability test. Requires NumPy/SciPy.
"""
import numpy as np
from scipy.integrate import solve_bvp,solve_ivp
from scipy.optimize import brentq
EPS=0.001

def rhs(r,y):
    N,A,V,K=y
    S=-A*A*r*(N*N-1)/(2*N**4)
    NP=N*(A*A-1)/(2*r)+A*A*(EPS*N*K*K*r/4+K*V-3*V*V/(2*N*r))+A*A*N*r*(N**-2-1)**2/8
    AP=A*(S-NP/N)
    VP=N*K-2*V/r-AP*V/A
    KP=2*V*S/(EPS*N*r)
    return np.array([NP,AP,VP,KP])

def bc(ya,yb):
    return np.array([ya[0]-32009/32000,ya[2]-1251/1250,yb[1]-1,yb[3]-3/4])

def main():
    x=np.linspace(1.997,2.003,19)
    initial=np.array([np.full_like(x,32009/32000),np.ones_like(x),
                      np.full_like(x,1251/1250),np.full_like(x,.75)])
    bvp=solve_bvp(rhs,bc,x,initial,tol=1e-10,max_nodes=15000)
    assert bvp.success and np.max(bvp.rms_residuals)<1e-8
    g=lambda r: -bvp.sol(r)[0]**2+bvp.sol(r)[1]**2*bvp.sol(r)[2]**2
    rh=brentq(g,1.997,2.003,xtol=1e-12)
    assert 1.9988<rh<1.9995
    vals=bvp.sol(2.003);samples=[4,10,20,40,80];outs={}
    for method in ('DOP853','Radau'):
        ivp=solve_ivp(rhs,(2.003,80),vals,t_eval=samples,method=method,
                      rtol=2e-10,atol=2e-12,max_step=1)
        assert ivp.success
        outs[method]=ivp.y
    err=np.max(np.abs(outs['DOP853']-outs['Radau']))
    assert err<2e-6
    print('PASS two independent ODE methods, max state difference',err)
    print('NUMERICAL (nonrigorous) horizon root:',rh)
    for i,r in enumerate(samples):
        N,A,V,K=outs['DOP853'][:,i]
        mass_slice=r*(1-A**-2)/2
        print('r=%d  N=%.9f A=%.9f V=%.9f K=%.9f m_slice=%.9f'%
              (r,N,A,V,K,mass_slice))
    print('WARNING finite-radius numerical data do not certify asymptotic behavior')
if __name__=='__main__':main()
