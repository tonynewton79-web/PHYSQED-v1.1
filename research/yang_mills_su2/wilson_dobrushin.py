"""Exact strong-coupling Wilson SU(2) spatial-plaquette correlation envelope.

Uses classical Dobrushin--Föllmer covariance theory, not an independent
constructive continuum result. Valid only for beta < 1/18 on finite tori.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from math import prod


def _geometry(extents: tuple[int, int, int, int]) -> None:
    if (type(extents) is not tuple or len(extents) != 4 or
            any(type(x) is not int or not 2 <= x <= 64 for x in extents) or
            prod(extents) > 512):
        raise ValueError("bounded periodic four-dimensional lattice required")


def _shift(site: tuple[int, ...], direction: int,
           extents: tuple[int, int, int, int]) -> tuple[int, ...]:
    result = list(site)
    result[direction] = (result[direction] + 1) % extents[direction]
    return tuple(result)


def max_wilson_link_incidences(extents: tuple[int, int, int, int]) -> int:
    """Enumerate adjacent plaquette-other-link incidences (with multiplicity)."""
    _geometry(extents)
    sites = list(itertools.product(*(range(x) for x in extents)))
    counts = {(site, mu): 0 for site in sites for mu in range(4)}
    for site in sites:
        for mu in range(4):
            for nu in range(mu + 1, 4):
                # A positively oriented plaquette contains these four
                # *variables*, regardless of the signs in its holonomy.
                edges = ((site, mu), (_shift(site, mu, extents), nu),
                         (_shift(site, nu, extents), mu), (site, nu))
                if len(set(edges)) != 4:
                    raise ValueError("plaquette reuses a link variable")
                for edge in edges:
                    counts[edge] += 3
    return max(counts.values())


def _coupling(beta: Fraction) -> None:
    if (type(beta) is not Fraction or not 0 <= beta < Fraction(1, 18) or
            beta.numerator.bit_length() > 16 or
            beta.denominator.bit_length() > 16):
        raise ValueError("exact rational beta strictly below 1/18 required")


def strong_coupling_timeslice_bound(
    extents: tuple[int, int, int, int], beta: Fraction, lag: int,
) -> Fraction:
    """Uniform-in-volume |Cov(X_0,X_lag)| upper bound via link influences.

    The Wilson link conditional influence row sum is bounded by 18*beta.
    Each spatial timeslice average has total coordinate oscillation <=8;
    the Dobrushin--Föllmer 1/4 bound and graph-distance estimate give
    16*q**distance/(1-q). This says nothing about the full continuum gap.
    """
    _geometry(extents)
    _coupling(beta)
    if type(lag) is not int or not 1 <= lag < extents[0]:
        raise ValueError("nonzero temporal separation inside period required")
    q = 18 * beta
    distance = min(lag, extents[0] - lag)
    return min(Fraction(1), 16 * q**distance / (1 - q))


def _ratio_json(value: Fraction) -> dict[str, str]:
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def _canonical(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      allow_nan=False, ensure_ascii=True).encode("ascii")


def strong_coupling_receipt(extents: tuple[int, int, int, int],
                            beta_num: int, beta_den: int, lag: int) -> dict:
    """Replayable rational finite Wilson covariance bound, not a proof token."""
    if (type(beta_num) is not int or type(beta_den) is not int or
            beta_num < 0 or beta_den <= 0 or
            beta_num.bit_length() > 16 or beta_den.bit_length() > 16):
        raise ValueError("bounded positive rational denominator required")
    beta = Fraction(beta_num, beta_den)
    result = strong_coupling_timeslice_bound(extents, beta, lag)
    record = {
        "schema_version": "ym-wilson-dobrushin-0.1",
        "status": "FINITE_STRONG_COUPLING_COVARIANCE_BOUND",
        "extents": list(extents),
        "beta": _ratio_json(beta),
        "time_lag": lag,
        "temporal_distance": min(lag, extents[0] - lag),
        "max_link_plaquette_neighbor_incidences": max_wilson_link_incidences(extents),
        "dobrushin_row_sum_upper": _ratio_json(18 * beta),
        "covariance_upper": _ratio_json(result),
        "continuum_mass_gap_proven": False,
        "physical_law_proven": False,
        "full_spectrum_gap_proven": False,
        "lean_kernel_verified": False,
    }
    record["fingerprint"] = hashlib.sha256(_canonical(record)).hexdigest()
    return record


def replay_strong_coupling_receipt(obj: object) -> bool:
    """Strict recomputation with bounded untrusted receipt parsing."""
    if type(obj) is not dict or len(obj) != 14:
        return False
    try:
        extents = obj["extents"]
        beta = obj["beta"]
        if (type(extents) is not list or len(extents) != 4 or
                type(beta) is not dict or set(beta) != {"numerator", "denominator"}):
            return False
        parts = (beta["numerator"], beta["denominator"])
        if any(type(x) is not str or not 1 <= len(x) <= 6 or
               not x.isascii() or not x.isdecimal() or
               str(int(x)) != x for x in parts):
            return False
        expected = strong_coupling_receipt(tuple(extents), int(parts[0]),
                                           int(parts[1]), obj["time_lag"])
        return obj == expected and _canonical(obj) == _canonical(expected)
    except (KeyError, ValueError, TypeError, OverflowError, RecursionError):
        return False
