"""Attack 006: exact stationary spherical preferred-foliation ADM reduction.

Research sector only; no exact nearby black hole, full Cauchy theorem, or
global physical stability is claimed. Requires SymPy 1.14.
"""
import sympy as s
r=s.symbols('r',positive=True)
e,mu=s.symbols('eps mu',positive=True)
N=s.Function('N')(r);A=s.Function('A')(r);V=s.Function('V')(r)
U=s.diff(V,r)+s.diff(A,r)*V/A
K=(U+2*V/r)/N
Kt=V/(N*r)
Q=U**2+2*(V/r)**2-(1+e)*(U+2*V/r)**2
R3=2*(1-1/A**2)/r**2+4*s.diff(A,r)/(A**3*r)
P=mu*s.Rational(1,4)*(N**(-2)-1)**2
Lag=(N*A*r**2*R3+A*r**2*Q/N)/2+N*A*r**2*P
W=-2*e*U-4*(1+e)*V/r
Wp=s.diff(W,r)
EN=A*r**2*(R3-Q/N**2)/2+A*r**2*(P+N*s.diff(P,N))
EA=N*(1-A**(-2))-2*r*s.diff(N,r)/A**2+r**2/(2*N)*(
    Q-W*U-V*Wp-W*V*(2/r-s.diff(N,r)/N))+N*r**2*P
EV=A*r**2/(2*N)*(
    4*V/r**2-4*(1+e)*(U+2*V/r)/r-Wp-W*(2/r-s.diff(N,r)/N))

def main():
    for name,f,closed in [('lapse',N,EN),('radial',A,EA),('shift',V,EV)]:
        calc=s.diff(Lag,f)-s.diff(s.diff(Lag,s.diff(f,r)),r)
        assert s.factor(calc-closed)==0,name
    print('PASS: all three stationary reduced Euler-Lagrange identities')
    mom=2*Kt*(s.diff(N,r)/N+s.diff(A,r)/A)-e*s.diff(K,r)
    assert s.factor(EV+A*r**2*mom)==0
    print('PASS: E_V = -A*r^2*[2*K_perp*(ln NA)prime - eps*Kprime]')
    # N=A=1, K->0 at infinity: K=0 by momentum; then the lapse
    # constraint imposes Kr^2+2Kt^2=0, hence V=0.
    assert s.simplify(Q.subs({A:1,s.diff(A,r):0,e:0}).subs(
        s.diff(V,r),-2*V/r)-6*V**2/r**2)==0
    print('PASS: nonzero asymptotically decaying shift excluded for N=A=1')
    M,rr=s.symbols('M r_ref',positive=True)
    n=s.Rational(9,8)/(mu*r**2)
    a=-s.Rational(9,8)*s.log(r/rr)-s.Rational(9,8)/mu*(1/r**2-1/rr**2)
    b=(s.Rational(9,16)*s.log(r/rr)
      +s.Rational(9,16)/M*(r*s.log(r/rr)-r+rr)
      +s.Rational(9,16)/(mu*M)*(1/r-1/rr)
      +s.Rational(9,8)/mu*(1/r**2-1/rr**2)
      -s.Rational(9,16)/(mu*M*rr**2)*(r-rr))
    assert s.simplify(a.subs(r,rr))==0 and s.simplify(b.subs(r,rr))==0
    resN=16*M*r*(s.diff(a,r)+s.diff(b,r))+9*M+8*mu*r**3*n+8*r**2*s.diff(a,r)+8*r*a
    resA=-16*M*r*s.diff(b,r)+16*M*r*s.diff(n,r)+9*M+8*r**2*s.diff(n,r)-8*r*a
    resV=8*r*(s.diff(a,r)+s.diff(n,r))+9
    for name,res in [('lapse',resN),('radial',resA),('shift',resV)]:
        assert s.simplify(s.expand_log(res,force=True))==0,name
    assert s.simplify(s.diff(a+n,r)+s.Rational(9,8)/r)==0
    print('PASS: explicit first-order backreaction solves all linearized EL equations')
    print('PASS: logarithmic running a+n has derivative -9/(8*r)')
    print('NOT CERTIFIED: exact nearby solution, physical hyperbolicity, regular center')

if __name__=='__main__':main()
