"""Exact SymPy crosscheck of standard-library Fraction interval Jacobian AD."""
from fractions import Fraction as Q
import sympy as s
from attack007_bvp_certificate import I,D,rhs

def main():
    r,N,A,V,K,e,mu=s.symbols('r N A V K e mu')
    S=-mu*A**2*r*(N**2-1)/(2*N**4)
    FN=N*(A**2-1)/(2*r)+A**2*(e*N*K**2*r/4+K*V-3*V**2/(2*N*r))+mu*A**2*N*r*(N**-2-1)**2/8
    FA=A*(S-FN/N)
    FV=N*K-2*V/r-FA*V/A
    FK=-mu*A**2*V*(N**2-1)/(e*N**5)
    vars=(N,A,V,K)
    tests=[
        (Q(2),Q(32009,32000),Q(1),Q(1251,1250),Q(3,4)),
        (Q(1999,1000),Q(10003,10000),Q(10001,10000),Q(1),Q(751,1000))
    ]
    for r0,*x in tests:
        subst={r:s.Rational(r0.numerator,r0.denominator),
               e:s.Rational(1,1000),mu:1}
        subst.update({v:s.Rational(a.numerator,a.denominator) for v,a in zip(vars,x)})
        vals=rhs(D(I(r0)),[D.var(I(a),j) for j,a in enumerate(x)])
        for i,f in enumerate((FN,FA,FV,FK)):
            value=Q(s.cancel(f.subs(subst)))
            assert vals[i].v.lo==vals[i].v.hi==value
            for j,v in enumerate(vars):
                d=Q(s.cancel(s.diff(f,v).subs(subst)))
                assert vals[i].g[j].lo==vals[i].g[j].hi==d,(i,j)
    print('PASS 8 exact vector components and 32 exact Jacobian entries')

if __name__=='__main__':main()
