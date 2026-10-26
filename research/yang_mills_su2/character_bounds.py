"""Exact rational enclosures for selected SU(2) finite character diagnostics.

Bounds concern modified Bessel functions and do NOT establish the physical
spectrum, a continuum limit, or a four-dimensional Yang–Mills mass gap.
"""

from __future__ import annotations

from fractions import Fraction
from math import factorial


def bessel_i_bounds(order: int, beta: Fraction, terms: int) -> tuple[Fraction, Fraction]:
    """Bound I_order(beta) using positive series and a geometric tail."""
    if (type(order) is not int or order < 0 or type(terms) is not int or
        not 1 <= terms <= 10000 or not isinstance(beta, Fraction) or beta <= 0):
        raise ValueError("positive rational beta, nonnegative order and term count required")
    half = beta / 2
    half_sq = half * half
    term = half**order / factorial(order)
    partial = Fraction(0)
    for k in range(terms):
        partial += term
        term *= half_sq / ((k + 1) * (k + order + 1))
    next_ratio = half_sq / ((terms + 1) * (terms + order + 1))
    if next_ratio >= 1:
        raise ValueError("insufficient terms to certify a decreasing geometric tail")
    return partial, partial + term / (1 - next_ratio)


def character_ratio_bounds(beta: Fraction, terms: int) -> tuple[Fraction, Fraction]:
    """Enclose finite SU(2) character diagnostic I_2(beta)/I_1(beta)."""
    i1_lo, i1_hi = bessel_i_bounds(1, beta, terms)
    i2_lo, i2_hi = bessel_i_bounds(2, beta, terms)
    ratio_lo, ratio_hi = i2_lo / i1_hi, i2_hi / i1_lo
    if not 0 < ratio_lo <= ratio_hi < 1:
        raise ValueError("series enclosure does not certify 0 < I2/I1 < 1")
    return ratio_lo, ratio_hi


def negative_log_bounds(q: Fraction, terms: int) -> tuple[Fraction, Fraction]:
    """Enclose -log(q) for rational 0<q<=1 with positive atanh terms."""
    if (not isinstance(q, Fraction) or not 0 < q <= 1 or
        type(terms) is not int or not 1 <= terms <= 10000):
        raise ValueError("rational q in (0,1] and positive term count required")
    z = (1 - q) / (1 + q)
    z2 = z*z
    term = z
    partial = Fraction(0)
    for k in range(terms):
        partial += 2*term / (2*k + 1)
        term *= z2
    remainder = 2*term / ((2*terms + 1) * (1 - z2))
    return partial, partial + remainder


def character_gap_bounds(beta: Fraction, bessel_terms: int, log_terms: int) -> tuple[Fraction, Fraction]:
    """Pointwise exact bounds on -log(I_2(beta)/I_1(beta))."""
    ratio_lo, ratio_hi = character_ratio_bounds(beta, bessel_terms)
    lower = negative_log_bounds(ratio_hi, log_terms)[0]
    upper = negative_log_bounds(ratio_lo, log_terms)[1]
    return lower, upper
