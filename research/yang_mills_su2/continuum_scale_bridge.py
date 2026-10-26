"""Exact *conditional* transfer-scale arithmetic and abstract countermodels.

No function here bounds the real four-dimensional Wilson transfer operator.
The spectral hypotheses must be established independently before applying
the conditional inequality to a physical theory.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json


_MAX_BITS = 384


def _bounded_fraction(value: Fraction, *, strictly_positive: bool = True) -> None:
    if (type(value) is not Fraction or value.denominator.bit_length() > _MAX_BITS
            or abs(value.numerator).bit_length() > _MAX_BITS
            or (strictly_positive and value <= 0)):
        raise ValueError("positive bounded exact rational required")


def _log_bounds(x: Fraction, terms: int) -> tuple[Fraction, Fraction]:
    """Rational enclosure for -log(x), with x strictly between zero and one."""
    if not 0 < x < 1:
        raise ValueError("log argument must be strictly between zero and one")
    y = (1-x)/(1+x)
    partial = Fraction(0)
    power = y
    for j in range(terms):
        partial += 2*power/(2*j+1)
        power *= y*y
    # All remaining denominators are at least 2*terms+1.
    tail = 2*power/((2*terms+1)*(1-y*y))
    return partial, partial+tail


def physical_block_window(
    spacing: Fraction, steps: int, upper_block: Fraction,
    correlator_lower: Fraction, variance_upper: Fraction, terms: int,
) -> dict[str, Fraction]:
    """Consequences of TWO UNVERIFIED transfer hypotheses, using rationals.

    If S=T/lambda_0 is positive self-adjoint with simple vacuum, Q=S-P0,
    then ||Q**steps|| <= upper_block and a centered vacuum correlator
    C(steps) >= correlator_lower with norm squared <= variance_upper imply
    correlator_lower/variance_upper <= ||Q||**steps <= upper_block.
    The function *does not* verify these physical spectral premises.
    """
    for value in (spacing, upper_block, correlator_lower, variance_upper):
        _bounded_fraction(value)
    if type(steps) is not int or not 1 <= steps <= 4096:
        raise ValueError("bounded positive integer block steps required")
    if type(terms) is not int or not 1 <= terms <= 32:
        raise ValueError("bounded positive integer logarithm terms required")
    lower_block = correlator_lower/variance_upper
    if not lower_block <= upper_block < 1:
        raise ValueError("inconsistent two-sided excited-sector block window")
    physical_scale = spacing*steps
    mass_lower, _ = _log_bounds(upper_block, terms)
    _, mass_upper = _log_bounds(lower_block, terms)
    return {
        "physical_scale": physical_scale,
        "block_lower": lower_block,
        "block_upper": upper_block,
        "mass_lower": mass_lower/physical_scale,
        "mass_upper": mass_upper/physical_scale,
    }


def residual_stable_block_upper(
    approximate_block_upper: Fraction, one_step_error: Fraction, steps: int,
) -> Fraction:
    """Telescope two *aligned*, norm-at-most-one excited-sector operators.

    Given an independently justified ||Q-Q_D|| <= one_step_error and
    ||Q_D**steps|| <= approximate_block_upper, the power telescope gives
    ||Q**steps|| <= approximate_block_upper + steps*one_step_error.
    Neither spectral-projection alignment nor these norm inputs is checked
    from Wilson data; the function is exact conditional arithmetic only.
    """
    _bounded_fraction(approximate_block_upper, strictly_positive=False)
    _bounded_fraction(one_step_error, strictly_positive=False)
    if (not 0 <= approximate_block_upper < 1 or one_step_error < 0
            or type(steps) is not int or not 1 <= steps <= 4096):
        raise ValueError("bounded contracting approximation and error required")
    upper = approximate_block_upper + steps*one_step_error
    if upper >= 1:
        raise ValueError("residual budget cannot certify a strict block contraction")
    return upper


def diagonal_transfer_family(family: str, n: int, terms: int) -> dict:
    """Exact diagonal T_n=diag(1,r_n); this is NOT a Wilson SU(2) model."""
    if (type(family) is not str or family not in
            ("finite_mass", "gap_collapse", "ultralocal")):
        raise ValueError("unknown abstract diagonal transfer family")
    if type(n) is not int or not 2 <= n <= 256:
        raise ValueError("abstract family index must be in [2,256]")
    if type(terms) is not int or not 1 <= terms <= 32:
        raise ValueError("bounded log certificate terms required")
    if family == "finite_mass":
        ratio = Fraction(n-1, n)
    elif family == "gap_collapse":
        ratio = Fraction(n*n-1, n*n)
    else:
        ratio = Fraction(1, 2)
    block = ratio**n
    window = physical_block_window(
        Fraction(1, n), n, block, block, Fraction(1), terms)
    return {
        "family": family,
        "index": n,
        "spacing": Fraction(1, n),
        "steps": n,
        "single_step_ratio": ratio,
        "block_ratio": block,
        "window": window,
    }


def _fraction_json(value: Fraction) -> dict[str, str]:
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def _canonical(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def scale_bridge_receipt(family: str, n: int, terms: int) -> dict:
    """A source-replayable *abstract* certificate, not an analytic YM proof."""
    sample = diagonal_transfer_family(family, n, terms)
    window = sample["window"]
    receipt = {
        "schema_version": "ym-abstract-scale-bridge-0.1",
        "status": "EXACT_ABSTRACT_DIAGONAL_TRANSFER_ARITHMETIC",
        "scope": "DIAGONAL_POSITIVE_TWO_MODE_TRANSFER_ONLY",
        "input": {"family": family, "n": n, "atanh_terms": terms},
        "single_step_ratio": _fraction_json(sample["single_step_ratio"]),
        "block_ratio": _fraction_json(sample["block_ratio"]),
        "derived": {
            "physical_scale": _fraction_json(window["physical_scale"]),
            "block_lower": _fraction_json(window["block_lower"]),
            "block_upper": _fraction_json(window["block_upper"]),
            "physical_gap_lower": _fraction_json(window["mass_lower"]),
            "physical_gap_upper": _fraction_json(window["mass_upper"]),
        },
        "analytic_premises": [
            "normalized transfer is exactly diag(1,r_n), not an interacting Wilson operator",
            "centered diagonal toy observable has unit excitation norm and block correlation r_n**n",
            "Wilson weak-coupling crossing, continuum QFT and physical scale setting are not provided",
        ],
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
        "analytic_theorem_kernel_verified": False,
    }
    receipt["fingerprint"] = hashlib.sha256(_canonical(receipt)).hexdigest()
    return receipt


def _strict_equal(a: object, b: object) -> bool:
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(_strict_equal(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(_strict_equal(x, y) for x, y in zip(a, b))
    return a == b


def replay_scale_bridge_receipt(obj: object) -> bool:
    if type(obj) is not dict or type(obj.get("input")) is not dict:
        return False
    inp = obj["input"]
    if set(inp) != {"family", "n", "atanh_terms"}:
        return False
    try:
        expected = scale_bridge_receipt(inp["family"], inp["n"],
                                        inp["atanh_terms"])
        return _strict_equal(obj, expected)
    except (ValueError, TypeError, KeyError, OverflowError, RecursionError):
        return False
