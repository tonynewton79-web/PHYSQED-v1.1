"""Directly rederive and differentiate full reduced EL equations at eps=0.

This independently checks the Taylor-zero assumptions needed in the strict
rational interval residual certificate. SymPy 1.14. No global theorem.
"""
import sympy as s
r=s.symbols('r',positive=True);ep,mu=s.symbols('ep mu',positive=True)
N=s.Function('N')(r);A=s.Function('A')(r);V=s.Function('V')(r)
U=s.diff(V,r)+s.diff(A,r)*V/A
Q=U**2+2*(V/r)**2-(1+ep)*(U+2*V/r)**2
R3=2*(1-A**-2)/r**2+4*s.diff(A,r)/(A**3*r)
P=mu*(N**-2-1)**2/4
L=N*A*r**2*R3/2+A*r**2*Q/(2*N)+N*A*r**2*P
n=s.Rational(9,8)/r**2
z=s.log(r/4)
a=-s.Rational(9,8)*z-s.Rational(9,8)*(r**-2-s.Rational(1,16))
b=s.Rational(9,16)*z+s.Rational(9,16)*(r*z-r+4)+s.Rational(9,16)*(r**-1-s.Rational(1,4))+s.Rational(9,8)*(r**-2-s.Rational(1,16))-s.Rational(9,256)*(r-4)
d=s.symbols('d');v0=s.sqrt(2/r)
sub={ep:d,mu:1,N:1+d*n,A:1+d*a,V:v0*(1+d*b)}
for field,ans in [(N,1+d*n),(A,1+d*a),(V,v0*(1+d*b))]:
    for order in (1,2):sub[s.diff(field,r,order)]=s.diff(ans,r,order)
for name,field in [('lapse',N),('radial',A),('shift',V)]:
    EL=s.diff(L,field)-s.diff(s.diff(L,s.diff(field,r)),r)
    expr=EL.subs(sub)
    assert s.simplify(expr.subs(d,0))==0,name+' background'
    derivative=s.factor(s.diff(expr,d).subs(d,0))
    assert s.simplify(s.expand_log(derivative,force=True))==0,(name,derivative)
    print('PASS full nonlinear action E(0)=Eprime(0)=0:',name)
print('Verifies Taylor-zero premises independently of closed linear equations')
