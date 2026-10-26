"""Certified finite-rank Fourier error for the *interacting* Wilson transfer.

No projected Galerkin matrix or eigenvalue is numerically diagonalized here.
The bound concerns approximation of the full positive operator in norm;
its multiplier grows exponentially with the spatial volume.
"""

from __future__ import annotations

from fractions import Fraction
from math import factorial, prod

from .character_bounds import bessel_i_bounds
from .wilson_transfer_characters import _exp_positive_upper


def _link_request(beta: Fraction, D: int, bessel_terms: int,
                  exp_terms: int) -> None:
    if (type(beta) is not Fraction or not 0 < beta <= 4 or
            beta.numerator.bit_length() > 12 or beta.denominator.bit_length() > 12 or
            type(D) is not int or not 2 <= D <= 16 or
            type(bessel_terms) is not int or not 1 <= bessel_terms <= 32 or
            type(exp_terms) is not int or not 1 <= exp_terms <= 32):
        raise ValueError("finite rational Wilson character cutoff required")


def _spatial_request(spatial_extents: tuple[int, int, int], D: int) -> int:
    if (type(spatial_extents) is not tuple or len(spatial_extents) != 3 or
            any(type(x) is not int or not 2 <= x <= 64 for x in spatial_extents)
            or prod(spatial_extents) > 64 or
            type(D) is not int or not 2 <= D <= 16):
        raise ValueError("bounded three-dimensional periodic spatial slice required")
    return prod(spatial_extents)


def _limit(value: Fraction) -> Fraction:
    if (value.numerator.bit_length() > 100_000 or
            value.denominator.bit_length() > 100_000):
        raise ValueError("finite projected spectral rational budget exceeded")
    return value


def _exp_upper_scaled(x: Fraction, terms: int) -> Fraction:
    """Rational exp upper via Taylor + repeated exact squaring."""
    if x > 64:
        raise ValueError("spatial multiplier exceeds certified exponential budget")
    scale = 1
    while x > Fraction(1, 2):
        x /= 2
        scale *= 2
    return _limit(_exp_positive_upper(x, terms)**scale)


def normalized_link_spectral_tail(
    beta: Fraction, D: int, bessel_terms: int, exp_terms: int,
) -> Fraction:
    """Enclose sup_(d>D) I_d(beta)/I_1(beta) for Wilson convolution.

    Normalizing the positive one-link convolution by its trivial eigenvalue
    makes it a self-adjoint Markov contraction, hence every ratio <=1.
    The factorial Bessel upper sequence decreases for d>D>=2, beta<=4.
    """
    _link_request(beta, D, bessel_terms, exp_terms)
    lower_i1, _ = bessel_i_bounds(1, beta, bessel_terms)
    if lower_i1 <= 0:
        raise ValueError("nonpositive certified Bessel denominator")
    h = beta / 2
    d = D + 1
    upper_i = h**d * _exp_positive_upper(h*h, exp_terms) / factorial(d)
    return _limit(min(Fraction(1), upper_i / lower_i1))


def projected_transfer_operator_error(
    spatial_extents: tuple[int, int, int], beta: Fraction,
    D: int, bessel_terms: int, exp_terms: int,
) -> Fraction:
    """Operator-norm / ordered eigenvalue absolute error for projected T_D.

    C is the normalized temporal convolution, P the site-gauge projector,
    Q_D the finite product Peter--Weyl cutoff, and M=e^(beta B/2).
    T=MPCPM; T_D=MPQ_D C Q_D PM, finite-rank and positive. Since Q_D
    commutes with C and P and the one-link C is Markov, the tensor-product
    operator error is <=epsilon_D, with NO factor for the number of links.
    Congruence by M costs ||M||^2<=exp(3 beta V).
    """
    volume = _spatial_request(spatial_extents, D)
    epsilon = normalized_link_spectral_tail(beta, D, bessel_terms, exp_terms)
    return _limit(epsilon * _exp_upper_scaled(3 * beta * volume, exp_terms))


def uncoupled_fourier_cutoff_dimension(
    spatial_extents: tuple[int, int, int], D: int,
) -> int:
    """Before gauge projection, rank upper bound (sum_(d<=D)d^2)^(3V)."""
    volume = _spatial_request(spatial_extents, D)
    return (sum(d*d for d in range(1, D+1)))**(3*volume)
