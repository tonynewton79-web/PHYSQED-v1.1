"""Exact arithmetic for the SU(2) *chordal* strong-coupling lattice bound.

Analytic premises include the concentration-uniform Poincare inequality
on S^3 and metric Dobrushin comparison; neither is formally verified here.
No theorem about beta approaching infinity or a continuum mass is claimed.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction


def _check_beta(beta: Fraction) -> None:
    if (type(beta) is not Fraction or not 0 < beta < Fraction(1, 6)
            or beta.numerator.bit_length() > 16
            or beta.denominator.bit_length() > 16):
        raise ValueError("rational SU2 Wilson beta in (0,1/6) required")


def _check_terms(terms: int) -> None:
    if type(terms) is not int or not 1 <= terms <= 32:
        raise ValueError("bounded positive atanh term count required")


def barta_quadratic_coefficients() -> tuple[Fraction, Fraction]:
    """Check the angular supersolutions' algebraic coefficients exactly.

    For degree-one harmonics the trial exponential exponent is a=-1/5,
    with -L_1 psi/psi = 3+(5a+1)k cos(theta)-a(a+1)k²sin²(theta).
    For differentiated zonal eigenfunctions, a=-2/5 and (5a+2).
    The derivation of these operator identities is an *analytic premise*;
    this function verifies the rational cancellations they require.
    """
    a1, a0 = Fraction(-1, 5), Fraction(-2, 5)
    if 5*a1+1 != 0 or 5*a0+2 != 0:
        raise ArithmeticError("Barta linear terms do not cancel")
    return -a1*(a1+1), -a0*(a0+1)


def chordal_spectral_ratio_upper(beta: Fraction) -> Fraction:
    """Restricted gauge-invariant Wilson transfer eigenvalue ratio ceiling.

    The input theorem gives W1(nu_b,nu_b') <= |b-b'|/3. Six plaquettes
    times three other link incidences gives the row coefficient 18/3=6.
    """
    _check_beta(beta)
    return 6*beta


def chordal_gap_log_lower(beta: Fraction, terms: int) -> Fraction:
    """Finite positive rational lower bound on -log(6*beta)."""
    q = chordal_spectral_ratio_upper(beta)
    _check_terms(terms)
    y = (1-q)/(1+q)
    power = y
    result = Fraction(0)
    for j in range(terms):
        result += 2*power/(2*j+1)
        power *= y*y
    return result


def _ratio(x: Fraction) -> dict[str, str]:
    return {"numerator": str(x.numerator), "denominator": str(x.denominator)}


def _canonical(x: object) -> bytes:
    return json.dumps(x, sort_keys=True, separators=(",", ":"),
                      allow_nan=False, ensure_ascii=True).encode("ascii")


def chordal_mixing_receipt(beta_num: int, beta_den: int, terms: int) -> dict:
    """Replayable exact consequences, not a Poincare/continuum proof token."""
    if (type(beta_num) is not int or type(beta_den) is not int
            or not 0 < beta_num < 2**16 or not 0 < beta_den < 2**16):
        raise ValueError("bounded positive rational beta integers required")
    _check_terms(terms)
    beta = Fraction(beta_num, beta_den)
    q = chordal_spectral_ratio_upper(beta)
    a1, a0 = barta_quadratic_coefficients()
    result = {
        "schema_version": "ym-wilson-chordal-mixing-0.1",
        "status": "FINITE_SU2_CHORDAL_MIXING_RATIO_ARITHMETIC",
        "scope": "GAUGE_INVARIANT_FINITE_LATTICE_BETA_LT_1_OVER_6_ONLY",
        "input": {"beta": _ratio(beta), "atanh_terms": terms},
        "barta_degree_one_quadratic": _ratio(a1),
        "barta_zonal_derivative_quadratic": _ratio(a0),
        "chordal_wasserstein_parameter_upper": _ratio(Fraction(1, 3)),
        "link_neighbor_plaquette_incidences": 18,
        "dobrushin_row_sum_upper": _ratio(q),
        "spectral_ratio_upper": _ratio(q),
        "lattice_gap_lower": _ratio(chordal_gap_log_lower(beta, terms)),
        "analytic_premises": [
            "unit S3 von Mises-Fisher spectral gap >=3 for every concentration",
            "chordal (not geodesic) W1 sensitivity <=parameter distance/3",
            "standard Wasserstein-Dobrushin covariance comparison for smooth slice functions",
            "strictly positive smooth gauge-invariant Wilson transfer and Perron ratio test",
        ],
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
        "analytic_theorem_kernel_verified": False,
        "sharp_quarter_wasserstein_bound_verified": False,
    }
    result["fingerprint"] = hashlib.sha256(_canonical(result)).hexdigest()
    return result


def _strict_equal(a: object, b: object) -> bool:
    if type(a) is not type(b):
        return False
    if type(b) is dict:
        return a.keys() == b.keys() and all(_strict_equal(a[k],v) for k,v in b.items())
    if type(b) is list:
        return len(a) == len(b) and all(_strict_equal(x,y) for x,y in zip(a,b))
    return a == b


def replay_chordal_mixing_receipt(obj: object) -> bool:
    if type(obj) is not dict or type(obj.get("input")) is not dict:
        return False
    inp = obj["input"]
    if set(inp) != {"beta", "atanh_terms"} or type(inp["beta"]) is not dict:
        return False
    if set(inp["beta"]) != {"numerator", "denominator"}:
        return False
    values = (inp["beta"]["numerator"], inp["beta"]["denominator"])
    if any(type(s) is not str or not 1 <= len(s) <= 5 or not s.isascii()
           or not s.isdecimal() or str(int(s)) != s for s in values):
        return False
    try:
        expected = chordal_mixing_receipt(int(values[0]), int(values[1]),
                                          inp["atanh_terms"])
        return _strict_equal(obj, expected)
    except (TypeError, ValueError, OverflowError, KeyError, RecursionError):
        return False
