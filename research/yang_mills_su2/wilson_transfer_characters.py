"""Rational character tail bounds for the *actual* SU(2) Wilson time-link kernel.

On the full gauge-invariant spatial Hilbert space the interacting transfer
operator also contains a spatial Wilson potential and gauge projection.
Its spectrum is NOT computed by the single-link character eigenvalues.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from math import factorial

from .character_bounds import bessel_i_bounds, character_ratio_bounds

MAX_INTEGER_BITS = 16000


def _check_beta(beta: Fraction) -> None:
    if (type(beta) is not Fraction or not 0 < beta <= 4 or
            beta.numerator.bit_length() > 16 or
            beta.denominator.bit_length() > 16):
        raise ValueError("positive bounded rational Wilson coupling required")


def _check_parameters(beta: Fraction, D: int, exp_terms: int) -> None:
    _check_beta(beta)
    if (type(D) is not int or not 2 <= D <= 16 or
            type(exp_terms) is not int or not 1 <= exp_terms <= 32):
        raise ValueError("bounded character cutoff and exponential term count required")


def _bounded(value: Fraction) -> Fraction:
    if (value.numerator.bit_length() > MAX_INTEGER_BITS or
            value.denominator.bit_length() > MAX_INTEGER_BITS):
        raise ValueError("exact certificate exceeds rational byte budget")
    return value


def _exp_positive_upper(x: Fraction, terms: int) -> Fraction:
    """Positive Taylor-series enclosure for e^x using a geometric tail."""
    if (type(x) is not Fraction or x < 0 or
            type(terms) is not int or not 1 <= terms <= 32):
        raise ValueError("nonnegative rational x and bounded terms required")
    partial, term = Fraction(0), Fraction(1)
    for k in range(terms):
        partial += term
        term *= x / (k + 1)
    next_ratio = x / (terms + 1)
    if next_ratio >= 1:
        raise ValueError("insufficient exponential Taylor terms to enclose tail")
    return _bounded(partial + term / (1 - next_ratio))


def character_tail_upper(beta: Fraction, D: int, exp_terms: int) -> Fraction:
    """Uniform SU(2) character tail for d>D, including |chi_d|<=d."""
    _check_parameters(beta, D, exp_terms)
    h = beta / 2
    d0 = D + 1
    ratio = h * (d0 + 1) / d0**2
    if ratio >= 1:
        raise ValueError("character cutoff too small for certified geometric tail")
    leading = Fraction(d0**2, factorial(d0)) * h**d0
    return _bounded(Fraction(2, 1) / beta *
                    _exp_positive_upper(h*h, exp_terms) * leading / (1 - ratio))


def wilson_character_kernel_interval(
    beta: Fraction, D: int, bessel_terms: int, exp_terms: int, x: Fraction,
) -> tuple[Fraction, Fraction]:
    """Enclose exp(beta*x), x=ReTr(g)/2, using positive Wilson characters."""
    _check_parameters(beta, D, exp_terms)
    if (type(x) is not Fraction or not -1 <= x <= 1 or
            x.numerator.bit_length() > 16 or x.denominator.bit_length() > 16 or
            type(bessel_terms) is not int or not 1 <= bessel_terms <= 32):
        raise ValueError("bounded SU2 trace and Bessel term count required")
    lower = upper = Fraction(0)
    prev, current = Fraction(0), Fraction(1)  # U_{-1}, U_0 Chebyshev values
    for d in range(1, D + 1):
        i_lo, i_hi = bessel_i_bounds(d, beta, bessel_terms)
        coefficient = Fraction(2*d, 1) / beta
        if current >= 0:
            lower += coefficient * i_lo * current
            upper += coefficient * i_hi * current
        else:
            lower += coefficient * i_hi * current
            upper += coefficient * i_lo * current
        prev, current = current, 2*x*current - prev
    tail = character_tail_upper(beta, D, exp_terms)
    return _bounded(lower-tail), _bounded(upper+tail)


def _rational_json(value: Fraction) -> dict[str, str]:
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")


def _check_receipt_request(
    beta_num: int, beta_den: int, D: int, bessel_terms: int, exp_terms: int,
) -> Fraction:
    if (type(beta_num) is not int or type(beta_den) is not int or
            beta_num <= 0 or beta_den <= 0 or
            beta_num.bit_length() > 16 or beta_den.bit_length() > 16 or
            type(bessel_terms) is not int or not 1 <= bessel_terms <= 32):
        raise ValueError("positive bounded rational coupling and series terms required")
    beta = Fraction(beta_num, beta_den)
    _check_parameters(beta, D, exp_terms)
    return beta


def wilson_transfer_receipt(
    beta_num: int, beta_den: int, D: int, bessel_terms: int, exp_terms: int,
) -> dict:
    """Exact finite Wilson *time-link* certificate, never a 4D mass-gap claim."""
    beta = _check_receipt_request(beta_num, beta_den, D, bessel_terms, exp_terms)
    ratio_low, ratio_high = character_ratio_bounds(beta, bessel_terms)
    _bounded(ratio_low)
    _bounded(ratio_high)
    trace_samples = (Fraction(-1), Fraction(0), Fraction(1,2), Fraction(1))
    receipt = {
        "schema_version": "ym-wilson-temporal-character-0.1",
        "status": "FINITE_WILSON_TRANSFER_CHARACTER_EXACT",
        "scope": "ACTUAL_WILSON_TEMPORAL_LINK_KERNEL_NOT_FULL_TRANSFER_SPECTRUM",
        "input": {
            "beta": _rational_json(beta), "D": D,
            "bessel_terms": bessel_terms, "exp_terms": exp_terms,
        },
        "uniform_character_tail_upper": _rational_json(
            character_tail_upper(beta, D, exp_terms)),
        "fundamental_to_trivial_ratio": {
            "lower": _rational_json(ratio_low),
            "upper": _rational_json(ratio_high),
        },
        "kernel_samples": [
            {
                "trace_half": _rational_json(x),
                "lower": _rational_json(
                    wilson_character_kernel_interval(beta,D,bessel_terms,exp_terms,x)[0]),
                "upper": _rational_json(
                    wilson_character_kernel_interval(beta,D,bessel_terms,exp_terms,x)[1]),
            } for x in trace_samples
        ],
        "analytic_premises": [
            "SU2 Peter-Weyl characters chi_(d-1)=U_(d-1)(ReTr(g)/2)",
            "exp(beta ReTr(g)/2)=sum_(d>=1) (2d/beta) I_d(beta) chi_(d-1)(g)",
            "I_d(beta)>0 for beta>0 and every integer d>=1",
            "full Wilson transfer requires spatial potential and site gauge projection",
        ],
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
    }
    receipt["fingerprint"] = hashlib.sha256(_canonical(receipt)).hexdigest()
    return receipt


def _strict_equal(received: object, expected: object) -> bool:
    if type(received) is not type(expected):
        return False
    if type(expected) is dict:
        return len(received) == len(expected) and all(
            key in received and _strict_equal(received[key], v) for key, v in expected.items())
    if type(expected) is list:
        return len(received) == len(expected) and all(
            _strict_equal(a,b) for a,b in zip(received,expected))
    return received == expected


def replay_wilson_transfer_receipt(receipt: object) -> bool:
    if type(receipt) is not dict or type(receipt.get("input")) is not dict:
        return False
    data = receipt["input"]
    if type(data.get("beta")) is not dict:
        return False
    try:
        expected = wilson_transfer_receipt(
            int(data["beta"]["numerator"]), int(data["beta"]["denominator"]),
            data["D"], data["bessel_terms"], data["exp_terms"])
    except (KeyError, ValueError, TypeError, OverflowError):
        return False
    return _strict_equal(receipt, expected)
