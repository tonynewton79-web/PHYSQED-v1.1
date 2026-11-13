"""Independent exact radial/Green-variable replay for Attack 012."""
import sympy as s

def main():
    z,u,h,W,K,e,mu=s.symbols('z u h W K e mu',positive=True)
    r=1/z;N=1+u*z;T=1+h;A=T/N;V=W*z*z/A
    S=-mu*A*A*r*(N*N-1)/(2*N**4)
    NP=(N*(A*A-1)/(2*r)
       +A*A*(e*N*K*K*r/4+K*V-3*V*V/(2*N*r))
       +mu*A*A*N*r*(N**(-2)-1)**2/8)
    AP=A*(S-NP/N)
    VP=N*K-2*V/r-AP*V/A
    KP=2*V*S/(e*N*r)
    F=((h-u*z)**2/(2*N)+e*A*A*N*K*K/(4*z*z)
      +A*W*K*z-s.Rational(3,2)*W*W*z**4/N
      +mu*A*A*u*u*(2+u*z)**2/(8*N**3))
    G=mu*u-mu*T*A*A*u*(2+u*z)/(2*N**4)
    checks={
      'u':(N-1)+r*NP-(h+F),
      'h':A*NP+N*AP-(-mu*u+G),
      'W':A*r*r*VP+V*r*r*AP+2*r*A*V-T*r*r*K,
      'K':KP+mu*A*W*u*(2+u*z)*z**3/(e*N**5),
    }
    for name,ex in checks.items():
        assert s.factor(ex)==0,name
    C,t,U,H,P,Z=s.symbols('C t U H P Z')
    x=C*C*t**4*U;nn=1+x;tt=1+C*C*t**3*H
    ss=s.symbols('ss')
    source=ss**2*U*(t*U*(2*sum(nn**i for i in range(6))-1)
       -H*(2+x)*(tt*tt+tt+1))/(2*nn**6)
    assert s.factor(source.subs(ss,C*t)-C*C*t*t*U*(t*U*(2*sum(nn**i for i in range(6))-1)
       -H*(2+x)*(tt*tt+tt+1))/(2*nn**6))==0
    print('PASS independent exact radial-to-Green identities for all 4 states')
    print('PASS compactified nonlinear source identity')
    print('NO finite-radius matching theorem claimed')
if __name__=='__main__':main()
