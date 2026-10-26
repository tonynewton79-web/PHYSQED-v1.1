"""Exact arithmetic consequence of a *restricted* Wilson lattice spectral gap.

The analytical route is Dobrushin--Föllmer temporal mixing plus the strictly
positive finite-volume Wilson transfer kernel (see WILSON_LATTICE_SPECTRAL_GAP.md).
This module replays rational arithmetic; it does not prove those analytic
theorems in a proof assistant and does not control the continuum limit.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction


def _check_beta(beta: Fraction) -> None:
    if (type(beta) is not Fraction or not 0 < beta < Fraction(1, 18)
            or beta.numerator.bit_length() > 16
            or beta.denominator.bit_length() > 16):
        raise ValueError("rational positive Wilson strong coupling beta < 1/18 required")


def _check_terms(log_terms: int) -> None:
    if type(log_terms) is not int or not 1 <= log_terms <= 32:
        raise ValueError("bounded positive rational logarithm series term count required")


def lattice_spectral_ratio_upper(beta: Fraction) -> Fraction:
    """Upper bound for every excited/ground Wilson transfer eigenvalue ratio.

    Analytic premises: strict Perron ground state and finite-dimensional-slice
    extension of the link Dobrushin covariance estimate. No eigenvalue is
    diagonalized here.
    """
    _check_beta(beta)
    return 18 * beta


def lattice_gap_log_lower(beta: Fraction, log_terms: int) -> Fraction:
    """Exact rational lower bound to -log(18*beta) in lattice time units.

    If q=18 beta and y=(1-q)/(1+q) in (0,1), then
      -log(q) = 2 sum_(j>=0) y^(2j+1)/(2j+1).
    A finite positive partial sum is a *strict lower* bound.
    """
    q = lattice_spectral_ratio_upper(beta)
    _check_terms(log_terms)
    y = (1 - q) / (1 + q)
    term = y
    result = Fraction(0)
    for j in range(log_terms):
        result += 2 * term / (2*j + 1)
        term *= y*y
    return result


def _rational(value: Fraction) -> dict[str, str]:
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      allow_nan=False, ensure_ascii=True).encode("ascii")


def lattice_spectral_gap_receipt(
    beta_num: int, beta_den: int, log_terms: int,
) -> dict:
    """Strict exact numerical consequence, NOT an analytic proof token."""
    if (type(beta_num) is not int or type(beta_den) is not int
            or not 0 < beta_num < 2**16 or not 0 < beta_den < 2**16):
        raise ValueError("bounded positive integer rational inputs required")
    _check_terms(log_terms)
    beta = Fraction(beta_num, beta_den)
    q = lattice_spectral_ratio_upper(beta)
    result = {
        "schema_version": "ym-wilson-lattice-spectral-ratio-0.1",
        "status": "FINITE_WILSON_LATTICE_SPECTRAL_RATIO_ARITHMETIC",
        "scope": "FINITE_SPATIAL_VOLUME_GAUGE_INVARIANT_STRONG_COUPLING_ONLY",
        "input": {"beta": _rational(beta), "log_terms": log_terms},
        "spectral_ratio_upper": _rational(q),
        "lattice_gap_lower": _rational(lattice_gap_log_lower(beta, log_terms)),
        "analytic_premises": [
            "four-dimensional periodic SU2 Wilson links with beta < 1/18",
            "classical Dobrushin-Follmer all-bounded-slice covariance estimate",
            "strictly positive trace-class gauge-projected Wilson transfer",
            "Perron ground state, time-period limit and excited-state test observable",
        ],
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
        "analytic_theorem_kernel_verified": False,
    }
    result["fingerprint"] = hashlib.sha256(_canonical(result)).hexdigest()
    return result


def _strict_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(right) is dict:
        return (left.keys() == right.keys()
                and all(_strict_equal(left[key], value)
                        for key, value in right.items()))
    if type(right) is list:
        return (len(left) == len(right)
                and all(_strict_equal(a, b) for a, b in zip(left, right)))
    return left == right


def replay_lattice_spectral_gap_receipt(receipt: object) -> bool:
    """Fail closed on incorrect fractions, forged flags, or altered premises."""
    if (type(receipt) is not dict or type(receipt.get("input")) is not dict
            or set(receipt["input"]) != {"beta", "log_terms"}):
        return False
    req = receipt["input"]
    beta = req["beta"]
    if type(beta) is not dict or set(beta) != {"numerator", "denominator"}:
        return False
    values = (beta["numerator"], beta["denominator"])
    if any(type(x) is not str or not 1 <= len(x) <= 5 or not x.isascii()
           or not x.isdecimal() or str(int(x)) != x for x in values):
        return False
    try:
        expected = lattice_spectral_gap_receipt(
            int(values[0]), int(values[1]), req["log_terms"])
        return _strict_equal(receipt, expected)
    except (ValueError, TypeError, OverflowError, KeyError, RecursionError):
        return False
