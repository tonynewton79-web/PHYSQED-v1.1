"""Attack 010: independent SymPy replay of exact Green source identities.

Exact algebra, no numerical sampling. Also derives the quadratic-amplitude
forced radial Helmholtz equation and factorial coefficient recurrence.
"""
import sympy as s

def main():
    r,t,u,h,V,K,c,eps,mu,U,H,P,Z=s.symbols(
        'r t u h V K c eps mu U H P Z',nonzero=True)
    N=1+u/r;T=1+h;A=T/N
    S=-mu*A*A*r*(N*N-1)/(2*N**4)
    FN=(N*(A*A-1)/(2*r)+A*A*(eps*N*K*K*r/4+K*V-3*V*V/(2*N*r))
        +mu*A*A*N*r*(N**(-2)-1)**2/8)
    F=s.factor(s.cancel(u/r+r*FN-h))
    Fcompact=((T-N)**2/(2*N)+A*A*(eps*N*K*K*r*r/4+K*V*r
              -3*V*V/(2*N))+mu*A*A*N*r*r*(N**(-2)-1)**2/8)
    assert s.cancel(F-Fcompact)==0
    G=s.factor(s.cancel(T*S+mu*u))
    J=s.factor(s.cancel(T*T*V*(N*N-1)/N**7))
    sub={r:1/t,u:c*c*t**3*U,h:c*c*t**3*H,V:c*t*t*P,K:c**3*t**5*Z/eps}
    x=c*c*t**4*U; nn=1+x;tt=1+c*c*t**3*H;aa=tt/nn
    fh=c*c*t*t*(H-t*U)**2/(2*nn)+c**4*t**4*aa*aa*nn*Z*Z/(4*eps)+c*c*t*t*aa*aa*P*Z/eps-s.Rational(3,2)*aa*aa*P*P/nn+mu*c*c*t*t*aa*aa*U*U*(2+x)**2/(8*nn**3)
    gh=mu*c*c*t*t*U*(t*U*(2*sum(nn**j for j in range(6))-1)-H*(2+x)*(tt*tt+tt+1))/(2*nn**6)
    jh=P*U*tt*tt*(2+x)/nn**7
    assert s.factor(s.cancel(F.subs(sub)/(c*c*t**4)-fh))==0
    assert s.factor(s.cancel(G.subs(sub)/(c*c*t**4)-gh))==0
    assert s.factor(s.cancel(J.subs(sub)/(c**3*t**6)-jh))==0
    print('PASS independently derived exact nonlinear normalized Green sources')
    C=s.symbols('C');n=s.Function('n')(r);a=s.Function('a')(r)
    z={u:C*C*r*n,h:C*C*(a+n),V:C/r**2,K:0}
    fl=s.simplify(s.diff(F.subs(z),C,2).subs(C,0)/2)
    gl=s.simplify(s.diff(G.subs(z),C,2).subs(C,0)/2)
    assert s.simplify(fl+3/(2*r**4))==0
    assert s.simplify(gl)==0
    equation=(s.diff(r*n,r,2)+mu*r*n-6/r**5)/r
    assert s.simplify(equation-(s.diff(n,r,2)+2*s.diff(n,r)/r+mu*n-6/r**6))==0
    for j in range(1,20):
        a0=6*(-1)**(j-1)*s.rf(5,2*j-2)/mu**j
        a1=6*(-1)**j*s.rf(5,2*j)/mu**(j+1)
        assert s.simplify(mu*a1+(2*j+4)*(2*j+3)*a0)==0
    print('PASS C² radial Helmholtz equation and factorial divergent formal tail')
    print('SCOPE: no claim of convergent full nonlinear 1/r series or horizon matching')

if __name__=='__main__':main()
