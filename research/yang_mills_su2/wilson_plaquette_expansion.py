"""Finite Wilson plaquette subset and character-product truncation bounds.

These are global finite-product errors. The subset expansion is not a
connected-polymer convergence proof and neither estimate is volume uniform.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb, prod

from .wilson_transfer_characters import _exp_positive_upper, character_tail_upper


def _request(extents: tuple[int, int, int, int], beta: Fraction,
             terms: int, positive: bool) -> int:
    if (type(extents) is not tuple or len(extents) != 4 or
            any(type(x) is not int or not 2 <= x <= 64 for x in extents) or
            prod(extents) > 32 or
            type(beta) is not Fraction or
            not (0 < beta < Fraction(1, 18) if positive else
                 0 <= beta < Fraction(1, 18)) or
            beta.numerator.bit_length() > 12 or beta.denominator.bit_length() > 12 or
            type(terms) is not int or not 1 <= terms <= 16):
        raise ValueError("bounded rational strong-coupling plaquette request required")
    return 6 * prod(extents)


def _limited(value: Fraction) -> Fraction:
    if (value.numerator.bit_length() > 100_000 or
            value.denominator.bit_length() > 100_000):
        raise ValueError("global rational truncation exceeds resource budget")
    return value


def wilson_subset_tail(extents: tuple[int, int, int, int], beta: Fraction,
                       max_order: int, exp_terms: int) -> Fraction:
    """Bound all terms with more than K activated plaquettes in exp(beta H).

    The exact formal expansion is prod_p(1+v_p), v_p=exp(beta W_p)-1.
    Since |v_p|<=exp(beta)-1, a *finite global* triangle bound follows.
    """
    plaquettes = _request(extents, beta, exp_terms, positive=False)
    if type(max_order) is not int or not 0 <= max_order <= plaquettes:
        raise ValueError("retained subset order must lie between 0 and P")
    if max_order == plaquettes or beta == 0:
        return Fraction(0)
    activity = _exp_positive_upper(beta, exp_terms) - 1
    tail = sum((comb(plaquettes, k)*activity**k
                for k in range(max_order+1, plaquettes+1)), Fraction(0))
    return _limited(tail)


def wilson_plaquette_character_product_tail(
    extents: tuple[int, int, int, int], beta: Fraction, D: int,
    exp_terms: int,
) -> Fraction:
    """Bound prod_p exp(beta W_p) minus its product of D-character cuts.

    Telescoping P factors, each true factor has size <=e^beta and each
    truncated character factor has size <=e^beta+R_D. This is *not*
    a numerical interacting-transfer eigenvalue approximation.
    """
    plaquettes = _request(extents, beta, exp_terms, positive=True)
    if type(D) is not int or not 2 <= D <= 16:
        raise ValueError("bounded SU(2) character dimension required")
    single_tail = character_tail_upper(beta, D, exp_terms)
    upper_factor = _exp_positive_upper(beta, exp_terms) + single_tail
    return _limited(plaquettes * single_tail * upper_factor**(plaquettes-1))
