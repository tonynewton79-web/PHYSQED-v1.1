"""Exact reduced Euler-Lagrange derivation -> four-state radial normal form.

SymPy 1.14, no claim of global Cauchy theorem.
"""
import sympy as s
r=s.symbols('r',positive=True)
N,A,V,K,NP,AP,VP,KP,e,mu=s.symbols('N A V K NP AP VP KP e mu',real=True)
U=N*K-2*V/r
Q=s.expand(U**2+2*(V/r)**2-(1+e)*(N*K)**2)
R3=2*(1-A**-2)/r**2+4*AP/(A**3*r)
P=mu*s.Rational(1,4)*(N**-2-1)**2
W=-2*e*N*K-4*V/r
Wp=-2*e*(NP*K+N*KP)-4*(VP/r-V/r**2)
EN=A*r**2*(R3-Q/N**2)/2+A*r**2*(P+N*s.diff(P,N))
EA=N*(1-A**-2)-2*r*NP/A**2+r**2/(2*N)*(Q-W*U-V*Wp-W*V*(2/r-NP/N))+N*r**2*P
EV=A*r**2/(2*N)*(4*V/r**2-4*(1+e)*N*K/r-Wp-W*(2/r-NP/N))
C=s.factor(EA-V*EV/A)
S=-mu*A**2*r*(N**2-1)/(2*N**4)
FN=N*(A**2-1)/(2*r)+A**2*(e*N*K**2*r/4+K*V-3*V**2/(2*N*r))+mu*A**2*N*r*(N**-2-1)**2/8
FA=A*(S-FN/N)
FV=N*K-2*V/r-FA*V/A
FK=2*V*S/(e*N*r)

def main():
    det=s.Matrix([[s.diff(EN,z) for z in (NP,AP)],
                  [s.diff(C,z) for z in (NP,AP)]]).det()
    assert s.factor(det-4*r**2/A**4)==0
    moment=2*V/(N*r)*(NP/N+AP/A)-e*KP
    assert s.factor((EV+A*r**2*moment).subs(VP,N*K-2*V/r-AP*V/A))==0
    vals={NP:FN,AP:FA,VP:FV,KP:FK}
    for name,E in (('lapse',EN),('radial',EA),('shift',EV)):
        assert s.factor(E.subs(vals))==0,name
    assert s.factor(FN/N+FA/A-S)==0
    assert s.factor(FK+mu*A**2*V*(N**2-1)/(e*N**5))==0
    print('PASS exact 4-state first-order normal form of all three radial EL equations')
    print('PASS derivative determinant = 4*r^2/A^4 >0')
    print('PASS exact (ln NA) prime and K prime identities')
    print('NOT CLAIMED: global AF geometry, central regularity, physical kinetic stability')

if __name__=='__main__':main()
