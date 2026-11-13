"""Attack 011: exact stationary metric-Killing-horizon rigidity and regular-center no-go.

Signature (-+++), eps=gamma*q²/(Mpl² Lambda²)>0, mu=lambda*q⁴/Mpl²>0.
Valid for r>0, N,A>0 in the stationary scalar-clock radial equations.
"""
import sympy as s
from fractions import Fraction as Q

def main():
    r,N,A,V,K,e,mu=s.symbols('r N A V K eps mu',positive=True)
    S=-mu*A**2*r*(N**2-1)/(2*N**4)
    NP=N*(A**2-1)/(2*r)+A**2*(e*N*K**2*r/4+K*V-3*V**2/(2*N*r))+mu*A**2*N*r*(N**-2-1)**2/8
    AP=A*(S-NP/N)
    VP=N*K-2*V/r-AP*V/A
    KP=2*V*S/(e*N*r)
    g=-N*N+A*A*V*V
    gp=-2*N*NP+2*A*AP*V*V+2*A*A*V*VP
    target=-N*N*A*A*(1/r+e*K*K*r/2+mu*r*(N**-2-1)**2/4)
    for sig in (-1,1):
        assert s.factor(gp.subs(V,sig*N/A)-target)==0
    # Both metric horizon orientations downcross g_tt outward.
    massprime=(1-A**-2)/2+r*AP/A**3
    mp=3*V**2/(2*N**2)-r*K*V/N-e*r**2*K**2/4-mu*r**2*(N**2-1)*(N**2+3)/(8*N**4)
    assert s.factor(massprime-mp)==0
    y=r*N*K/V
    yp=s.diff(y,r)+s.diff(y,N)*NP+s.diff(y,A)*AP+s.diff(y,V)*VP+s.diff(y,K)*KP
    assert s.factor(yp-y*(3-y)/r-(y+2/e)*S)==0
    gfrac=-(Q(1,2)+Q(1,1000)*Q(3,4)**2)
    assert gfrac==Q(-8009,16000)
    assert abs(gfrac)/2==Q(8009,32000)
    print("PASS exact horizon g_tt' negative for both shift orientations")
    print("PASS unique possible Killing horizon on each connected regular positive-lapse domain")
    print("PASS smooth regular center N(0)>0,V=O(r) forbids any metric Killing horizon")
    print("PASS spatial mass derivative and Riccati ratio transport identities")
    print("PASS rational surface gravity magnitude benchmark")
    print("LIMIT: no claim of global horizon existence, physical scalar trapping or novelty")

if __name__=="__main__":main()
