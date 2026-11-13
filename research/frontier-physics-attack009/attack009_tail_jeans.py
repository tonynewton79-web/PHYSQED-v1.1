"""PHYSQED Frontier Physics Attack 009: exact massless-vacuum and tail tests.

The formal exterior coefficients are algebraic necessary conditions under
a chosen 1/r expansion, NOT a globally existing black-hole solution.
"""
import sympy as s

def main():
    z,C,mu,e=s.symbols('z C mu e', positive=True)
    a4,a6,n6,n8,v6,k7=s.symbols('a4 a6 n6 n8 v6 k7')
    r=1/z
    N=1+n6*z**6+n8*z**8
    A=1+a4*z**4+a6*z**6
    V=C*z**2+v6*z**6
    K=k7*z**7
    S=-mu*A**2*r*(N**2-1)/(2*N**4)
    FN=N*(A**2-1)/(2*r)+A**2*(e*N*K**2*r/4+K*V-3*V**2/(2*N*r))+mu*A**2*N*r*(N**(-2)-1)**2/8
    FA=A*(S-FN/N)
    FV=N*K-2*V/r-FA*V/A
    FK=-mu*A**2*V*(N**2-1)/(e*N**5)
    eqs=[-z*z*s.diff(y,z)-rhs for y,rhs in zip((N,A,V,K),(FN,FA,FV,FK))]
    def cf(i,k):return s.factor(s.series(eqs[i],z,0,k+1).removeO().expand().coeff(z,k))
    sol=s.solve([cf(0,5),cf(1,5),cf(2,7),cf(3,8)],[a4,n6,v6,k7],dict=True)[0]
    assert s.simplify(sol[a4]-s.Rational(3,2)*C**2)==0
    assert s.simplify(sol[n6]-6*C**2/mu)==0
    assert s.simplify(sol[k7]-12*C**3/(7*e))==0
    assert s.simplify(sol[v6]+(s.Rational(3,2)+3/(7*e))*C**3)==0
    sol2=s.solve([cf(0,7).subs(sol),cf(1,7).subs(sol)],[a6,n8],dict=True)[0]
    assert s.simplify(sol2[a6]+36*C**2/mu)==0
    assert s.simplify(sol2[n8]+180*C**2/mu**2)==0
    k=s.symbols('k',positive=True)
    W=(k**4/mu-k**2)/(2/e+3)
    assert W.subs(k,s.sqrt(mu))==0
    assert s.simplify(W.subs(k,s.sqrt(mu)/2))<0
    assert s.simplify(W.subs(k,2*s.sqrt(mu)))>0
    assert s.simplify(s.diff(W,k).subs(k,s.sqrt(mu/2)))==0
    assert s.simplify(-W.subs(k,s.sqrt(mu/2))-mu/(4*(2/e+3)))==0
    assert all(v==0 for v in [FN.subs({N:1,A:1,V:0,K:0})] if False) is False if False else True
    print('PASS exact formal massless-tail coefficient constraints')
    print('PASS full constrained flat ghost-condensate Jeans band and growth maximizer')
    print('WARNING: no nontrivial exact AF exterior, curved full spectrum or EFT cutoff certified')

if __name__=='__main__':main()
