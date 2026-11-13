"""Attack 010: radial forced Helmholtz exterior and divergent amplitude tail.

Exact Fraction recurrence; independent mpmath integral checks are diagnostic.
The analytic remainder estimate follows from repeated integration by parts.
"""
from fractions import Fraction as Q
from math import factorial
import mpmath as mp

def coefficient(j,mu=Q(1)):
    return Q(6)*(-1)**j*Q(factorial(4+2*j),factorial(4))/mu**(j+1)

def exact_replay():
    for j in range(1,50):
        assert coefficient(j)+(2*j+4)*(2*j+3)*coefficient(j-1)==0
    for j in range(20):
        assert abs(coefficient(j+1)/coefficient(j))==(5+2*j)*(6+2*j)
    print('PASS factorial recurrence; C² inverse-radius power series has zero radius')

def n2_integral(r,mu=1):
    k=mp.sqrt(mu)
    J=mp.im(mp.exp(-1j*k*r)*k**4*mp.gammainc(-4,-1j*k*r,mp.inf))
    return 6*J/(k*r)

def numerical_replay():
    mp.mp.dps=65;r=mp.mpf(12)
    exact=n2_integral(r)
    quad=6/r*mp.quad(lambda s:mp.sin(s-r)/s**5,
                      [r,20,30,50,80,120,200,400,800,1600,5000])
    assert abs(exact-quad)<mp.mpf('1e-11')
    for m in range(1,9):
        partial=mp.fsum(mp.mpf(coefficient(j).numerator)/
               coefficient(j).denominator/r**(6+2*j) for j in range(m))
        remainder=mp.mpf(12*factorial(4+2*m)//factorial(4))/r**(6+2*m)
        assert abs(exact-partial)<remainder
    print('PASS two independent high-precision integral computations')
    print('PASS analytic integration-by-parts bound at m=1,...,8')
    print('n2(12)=',mp.nstr(exact,30))
    print('NOT CLAIMED: fixed-C nonlinear inverse-radius series divergent or no exterior')

if __name__=='__main__':
    exact_replay();numerical_replay()
