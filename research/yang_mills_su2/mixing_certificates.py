"""Exact rational certificates for the beta=0 axis-angle SU(2) Markov kernel.

The Peter--Weyl character decomposition is the analytical premise; the
finite bounds below are recomputed with Fractions and are not a Lean proof
of representation theory, nor the Yang--Mills transfer-matrix mass gap.
"""

from __future__ import annotations

from fractions import Fraction


# A conservative ceiling under Python's default 4300 decimal digit guard.
# Bit counts are checked before converting an exact integer to JSON text.
_MAX_RECEIPT_INTEGER_BITS = 12000


def beta_zero_rep_eigenvalue(spin_twice: int) -> Fraction:
    """Central beta=0, epsilon=pi proposal eigenvalue in spin j=spin_twice/2."""
    if type(spin_twice) is not int or spin_twice < 0:
        raise ValueError("spin_twice must be a nonnegative integer")
    if spin_twice % 2:
        return Fraction(0)
    return Fraction(1, spin_twice + 1)


def _validate(sweeps: int, links: int, terms: int) -> None:
    if (any(type(v) is not int for v in (sweeps, links, terms))
            or not 2 <= sweeps <= 12
            or not 1 <= links <= 512
            or not 1 <= terms <= 32
            or sweeps * links * terms > 4000):
        raise ValueError("bounded sweeps, link count and rational tail terms required")


def cold_l2_squared_bounds(
    sweeps: int, links: int, terms: int,
) -> tuple[Fraction, Fraction]:
    """Enclose ||p_n-1||_2^2 on SU(2)^links from cold start, n>=2.

    For p=2n-2, S= sum_(j>=1) (2j+1)^(-p).  The uncomputed
    tail after j=J is bounded by the integral from J to infinity.
    Product-link independence gives ||p_n-1||_2^2 = (1+S)^links-1.
    """
    _validate(sweeps, links, terms)
    power = 2 * sweeps - 2
    partial = sum((Fraction(1, (2 * j + 1) ** power)
                   for j in range(1, terms + 1)), Fraction(0))
    tail = Fraction(1, 2 * (power - 1) * (2 * terms + 1) ** (power - 1))
    return ((1 + partial) ** links - 1,
            (1 + partial + tail) ** links - 1)


def _rational_json(q: Fraction) -> dict[str, str]:
    return {"numerator": str(q.numerator), "denominator": str(q.denominator)}


def mixing_receipt(sweeps: int, links: int, terms: int) -> dict:
    """Human- and machine-readable exact finite Markov-model scope receipt."""
    low, high = cold_l2_squared_bounds(sweeps, links, terms)
    if any(max(q.numerator.bit_length(), q.denominator.bit_length())
           > _MAX_RECEIPT_INTEGER_BITS for q in (low, high)):
        raise ValueError("exact rational receipt exceeds serialization budget")
    return {
        "schema_version": "ym-su2-beta-zero-mixing-0.1",
        "certificate_scope": "EXACT_FINITE_BETA_ZERO_PROPOSAL",
        "parameters": {"sweeps": sweeps, "links": links, "terms": terms,
                       "coupling_beta": 0, "proposal_angle": "pi"},
        "l2_distance_squared_interval": {
            "lower": _rational_json(low), "upper": _rational_json(high)},
        "mean_zero_markov_operator_norm": _rational_json(Fraction(1, 3)),
        "cold_fundamental_plaquette_at_first_sweep": _rational_json(Fraction(0)),
        "cold_adjoint_plaquette_at_first_sweep": _rational_json(Fraction(1, 81)),
        "analytical_premises": [
            "Peter-Weyl SU2 character decomposition, not Lean formalized",
            "independent link updates at beta=0 from cold initialization",
            "exact central proposal: axis uniform on S2, angle uniform [-pi,pi]",
        ],
        "equilibrium_claim": False,
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
    }


def replay_mixing_receipt(receipt: object) -> bool:
    """Reject any altered exact interval, claim, field or bounded input.

    A receipt is self-describing and has a canonical finite schema.  The
    verifier independently recomputes all rational outputs from the three
    integer inputs rather than accepting a stored fingerprint or claimed
    'verified' flag. It assumes the stated representation-theoretic lemma.
    """
    if type(receipt) is not dict:
        return False
    parameters = receipt.get("parameters")
    if type(parameters) is not dict:
        return False
    try:
        expected = mixing_receipt(
            parameters["sweeps"], parameters["links"], parameters["terms"])
    except (KeyError, TypeError, ValueError):
        return False
    return receipt == expected
