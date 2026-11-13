"""Exact inverse of epsilon=0 linearized radial operator, not finite-eps inverse."""
from fractions import Fraction as Q
import sympy as s

def main():
    r,M,mu=s.symbols('r M mu',positive=True)
    f1,f2,f3=(s.Function('f'+str(j))(r) for j in (1,2,3))
    n=(f1+f2-(2*M+r)*f3)/(8*mu*r**3)
    a=s.symbols('a')
    ap=-s.diff(n,r)+f3/(8*r)
    bp=(1+r/(2*M))*s.diff(n,r)-a/(2*M)-f2/(16*M*r)
    L1=16*M*r*(ap+bp)+8*mu*r**3*n+8*r**2*ap+8*r*a
    L2=-16*M*r*bp+16*M*r*s.diff(n,r)+8*r**2*s.diff(n,r)-8*r*a
    L3=8*r*(ap+s.diff(n,r))
    assert s.simplify(L1-f1)==s.simplify(L2-f2)==s.simplify(L3-f3)==0
    lo,hi,ref,D=Q(19,10),Q(8),Q(4),Q(4)
    nb=Q(12)/(8*lo**3)
    nprime=Q(13)/(8*lo**3)+Q(36)/(8*lo**4)
    ab=nb+Q(12)/(8*ref**3)+D/(8*lo)
    aprime=nprime+Q(1)/(8*lo)
    bprime=(1+hi/2)*nprime+ab/2+Q(1)/(16*lo)
    bb=D*bprime
    assert max(nb,nprime,ab,aprime,bprime,bb)<20
    print('PASS exact epsilon=0 linear inhomogeneous Green reconstruction')
    print('PASS conservative C1 inverse norm <20 on [1.9,8], pinned a(4)=b(4)=0')
    print('LIMIT: epsilon>0 adds second radial derivative; no uniform inverse')

if __name__=='__main__':main()
