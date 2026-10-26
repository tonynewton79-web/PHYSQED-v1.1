"""Exact local incidence witness for a *method* ceiling in Wilson SU(2).

The 9*beta/2 lower row sum is for the unfixed-gauge, globally optimized,
single-link chordal Wasserstein Dobrushin matrix. It says nothing about
the existence of a positive continuum Yang--Mills mass gap.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json

Site = tuple[int, int, int, int]
Link = tuple[Site, int]


def _shift(site: Site, direction: int, step: int,
           extents: tuple[int, int, int, int]) -> Site:
    result = list(site)
    result[direction] = (result[direction] + step) % extents[direction]
    return tuple(result)  # type: ignore[return-value]


def local_ceiling_witness(extents: tuple[int, int, int, int]) -> dict:
    """Six incident plaquettes and 18 independent neighboring positive links.

    The three opposite 0-links behind the chosen center are assigned -I;
    the three opposite 0-links ahead are +I. All transverse links are +I.
    The six staple contributions are then +I,+I,+I,-I,-I,-I.
    """
    if (type(extents) is not tuple or len(extents) != 4
            or any(type(n) is not int or not 3 <= n <= 8 for n in extents)):
        raise ValueError("bounded four-torus with every period at least three required")
    center: Site = (0, 0, 0, 0)
    edge = (center, 0)
    plaquettes: list[tuple[Site, int]] = []
    opposite_negative: list[Link] = []
    other_links: list[Link] = []
    for nu in (1, 2, 3):
        behind = _shift(center, nu, -1, extents)
        ahead = _shift(center, nu, 1, extents)
        plaquettes.extend(((center, nu), (behind, nu)))
        opposite_negative.append((behind, 0))
        # Positive-link support of the two (0,nu) plaquettes.
        other_links.extend(((center, nu), (_shift(center, 0, 1, extents), nu),
                            (ahead, 0), (behind, 0), (behind, nu),
                            (_shift(behind, 0, 1, extents), nu)))
    if len(set(other_links)) != 18 or edge in other_links:
        raise ArithmeticError("neighbor aliases violate incidence construction")
    return {
        "extents": extents,
        "center_link": edge,
        "incident_plaquettes": tuple(plaquettes),
        "neighbor_links": tuple(sorted(other_links)),
        "negative_opposite_links": tuple(sorted(opposite_negative)),
        "signed_staple_sum": 0,
        "neighbor_count": 18,
    }


def ceiling_row_lower(beta: Fraction) -> Fraction:
    """Necessary global single-link Dobrushin row sum; not an upper bound."""
    if (type(beta) is not Fraction or beta <= 0
            or beta.numerator.bit_length() > 16
            or beta.denominator.bit_length() > 16):
        raise ValueError("bounded positive exact Wilson coupling required")
    return Fraction(9, 2) * beta


def _ratio(value: Fraction) -> dict[str, str]:
    return {"numerator": str(value.numerator),
            "denominator": str(value.denominator)}


def _canonical(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      allow_nan=False, ensure_ascii=True).encode("ascii")


def ceiling_receipt(beta_num: int, beta_den: int) -> dict:
    if (type(beta_num) is not int or type(beta_den) is not int
            or not 0 < beta_num < 2**16 or not 0 < beta_den < 2**16):
        raise ValueError("bounded exact positive Wilson coupling integers required")
    beta = Fraction(beta_num, beta_den)
    witness = local_ceiling_witness((3, 3, 3, 3))
    record = {
        "schema_version": "ym-single-link-dobrushin-ceiling-0.1",
        "status": "FINITE_WILSON_SINGLE_LINK_METHOD_CEILING_ARITHMETIC",
        "scope": "UNFIXED_GAUGE_SU2_SINGLE_LINK_DOBRUSHIN_ONLY",
        "input": {"beta": _ratio(beta), "torus_extents": [3, 3, 3, 3]},
        "incident_plaquettes": len(witness["incident_plaquettes"]),
        "distinct_neighbor_links": witness["neighbor_count"],
        "negative_opposite_links": [
            {"site": list(site), "direction": direction}
            for site, direction in witness["negative_opposite_links"]],
        "signed_staple_sum": witness["signed_staple_sum"],
        "local_wasserstein_slope_lower": _ratio(beta/4),
        "row_lower": _ratio(ceiling_row_lower(beta)),
        "necessary_dobrushin_ceiling": _ratio(Fraction(2, 9)),
        "analytic_premises": [
            "six independent central-sign staples on four-tori with transverse period at least three",
            "each neighboring link changes one staple at chordal unit speed",
            "a normalized Haar S3 coordinate has variance one quarter",
            "optimal global Dobrushin coefficient takes a supremum separately for each neighbor",
        ],
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
        "analytic_theorem_kernel_verified": False,
        "global_sharp_wasserstein_upper_proven": False,
    }
    record["fingerprint"] = hashlib.sha256(_canonical(record)).hexdigest()
    return record


def _strict_equal(a: object, b: object) -> bool:
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(_strict_equal(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(_strict_equal(x, y) for x, y in zip(a, b))
    return a == b


def replay_ceiling_receipt(obj: object) -> bool:
    if type(obj) is not dict or type(obj.get("input")) is not dict:
        return False
    inp = obj["input"]
    if (set(inp) != {"beta", "torus_extents"} or
        inp["torus_extents"] != [3, 3, 3, 3] or
        type(inp["beta"]) is not dict or
        set(inp["beta"]) != {"numerator", "denominator"}):
        return False
    strings = (inp["beta"]["numerator"], inp["beta"]["denominator"])
    if any(type(s) is not str or not 1 <= len(s) <= 5 or not s.isascii()
           or not s.isdecimal() or str(int(s)) != s for s in strings):
        return False
    try:
        expected = ceiling_receipt(int(strings[0]), int(strings[1]))
        return _strict_equal(obj, expected)
    except (KeyError, TypeError, ValueError, OverflowError, RecursionError):
        return False
