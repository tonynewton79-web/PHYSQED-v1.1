"""Independent arithmetic reference oracle (stdlib only; no SymPy).

These are selected standard textbook results, not general tensor or QFT
solvers. Use the oracle alongside, never as a substitute for, the main
symbolic backend. Exact Fractions avoid floating tolerance mistakes.
"""
from __future__ import annotations
from fractions import Fraction


def _r(x):
    if isinstance(x,bool) or not isinstance(x,(int,str,Fraction)):
        raise ValueError("exact integer, string or Fraction required; floats refused")
    return Fraction(x)


def warped_surface_scalar(f, second_derivative):
    """Scalar curvature for ds^2 = dx^2 + f(x)^2 dy^2 at a point."""
    f,d2=_r(f),_r(second_derivative)
    if not f:
        raise ValueError("degenerate warped metric")
    return -2*d2/f


def cross3(a,b):
    """Exact structure-constant bracket for oriented so(3) basis."""
    if len(a)!=3 or len(b)!=3:
        raise ValueError("cross product requires three components")
    x,y=[tuple(map(_r,v)) for v in (a,b)]
    return (x[1]*y[2]-x[2]*y[1],
            x[2]*y[0]-x[0]*y[2],
            x[0]*y[1]-x[1]*y[0])


def normal_even_moment(variance, order):
    """Zero-mean one-dimensional Gaussian: E[X^(2k)] = (2k-1)!! v^k."""
    v=_r(variance)
    if not isinstance(order,int) or order<0 or order>20 or order%2:
        raise ValueError("only even bounded Gaussian moment orders")
    out=Fraction(1)
    for j in range(1,order,2):
        out*=j
    return out*v**(order//2)


def phi4_two_point_first_order(variance,coupling=1):
    """Coefficient -lambda/24*(E[X^6]-E[X^2]E[X^4])."""
    v,lam=_r(variance),_r(coupling)
    return -lam*(normal_even_moment(v,6)-
                 normal_even_moment(v,2)*normal_even_moment(v,4))/24


def polynomial_poisson_reference(q,p):
    """At q,p, bracket {q^2 p, q p^2} = 3 q^2 p^2."""
    q,p=_r(q),_r(p)
    return 3*q*q*p*p
