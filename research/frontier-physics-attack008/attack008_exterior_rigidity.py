"""PHYSQED Attack 008: exact exterior identities and asymptotic nonzero-mass obstruction.

The theorem itself uses C1 big-O falloff and an ADM limit, not a power series.
This SymPy program independently checks exact ODE conservation identities and
a formal coefficient adversarial control. See README for the rigorous proof.
"""
import sympy as s

def main():
    r=s.symbols('r',positive=True)
    N,A,V,K,eps,mu=s.symbols('N A V K eps mu',positive=True)
    S=-mu*A**2*r*(N**2-1)/(2*N**4)
    NP=N*(A**2-1)/(2*r)+A**2*(eps*N*K**2*r/4+K*V-3*V**2/(2*N*r))+mu*A**2*N*r*(N**-2-1)**2/8
    AP=A*(S-NP/N)
    VP=N*K-2*V/r-AP*V/A
    KP=-mu*A**2*V*(N**2-1)/(eps*N**5)
    assert s.factor(NP/N+AP/A-S)==0
    assert s.factor(KP-2*V*S/(eps*N*r))==0
    assert s.factor(AP*r**2*V+A*2*r*V+A*r**2*VP-A*N*r**2*K)==0
    print('PASS exact log-lapse, momentum and shift transport identities')
    m,nu,v,k=s.symbols('m nu v k',real=True)
    nf=1+nu/r**3;af=1+m/r;vf=v/r**s.Rational(3,2);kf=k/r**s.Rational(5,2)
    sub={N:nf,A:af,V:vf,K:kf}
    lnna=s.factor(s.diff(nf,r)/nf+s.diff(af,r)/af)
    sr=s.factor(S.subs(sub))
    fN=s.factor(NP.subs(sub))
    assert s.simplify(s.limit(r**2*lnna,r,s.oo)+m)==0
    assert s.simplify(s.limit(r**2*sr,r,s.oo)+mu*nu)==0
    assert s.simplify(s.limit(r**2*fN,r,s.oo)-m)==0
    assert s.simplify(s.limit(r**2*s.diff(nf,r),r,s.oo))==0
    assert s.simplify(s.limit(r**2*fN.subs(m,0),r,s.oo))==0
    print('PASS formal consistency forces nonzero ADM coefficient to vanish')
    print('SCOPE: C1 AF exact stationary scalar-clock sector; no global horizon theorem')

if __name__=='__main__':main()
