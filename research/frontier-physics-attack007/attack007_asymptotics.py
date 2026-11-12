"""Asymptotic conditional rigidity of standard power-law stationary scalar clock."""
import sympy as s
r=s.symbols('r',positive=True)
mu,e,c,n1,n2,n3,a1=s.symbols('mu e c n1 n2 n3 a1',positive=True)

def main():
    N=1+n1/r+n2/r**2+n3/r**3
    A=1+a1/r
    lhs=s.diff(N,r)/N+s.diff(A,r)/A
    rhs=-mu*A**2*r*(N**2-1)/(2*N**4)
    assert s.simplify(s.limit(rhs,r,s.oo)+mu*n1)==0
    assert s.simplify(s.limit(r*rhs.subs(n1,0),r,s.oo)+mu*n2)==0
    assert s.simplify(s.limit(r**2*(lhs-rhs).subs({n1:0,n2:0}),r,s.oo)-(-a1+mu*n3))==0
    for p in (s.Rational(1,2),s.Integer(1),s.Integer(3)):
        V=c/r**p
        K=(s.diff(V,r)+s.diff(A,r)*V/A+2*V/r)/N
        mom=2*V/(N*r)*lhs-e*s.diff(K,r)
        assert s.simplify(s.limit(mom*r**(p+2),r,s.oo)-e*(p+1)*(2-p)*c)==0
    Nc=1+n3/r**3;Ac=1+a1/r;V=c/r**2
    K=(s.diff(V,r)+s.diff(Ac,r)*V/Ac+2*V/r)/Nc
    FN=Nc*(Ac**2-1)/(2*r)+Ac**2*(e*Nc*K**2*r/4+K*V-3*V**2/(2*Nc*r))+mu*Ac**2*Nc*r*(Nc**(-2)-1)**2/8
    assert s.factor(s.limit(r**2*(FN-s.diff(Nc,r)),r,s.oo))==a1
    print('PASS conditional power-law shift exponent p=2 necessary')
    print('PASS conventional 1/r expansions force zero spatial ADM mass a1=0')
    print('LIMIT: no proof for non-power, polyhomogeneous, oscillatory clock asymptotics')

if __name__=='__main__':main()
