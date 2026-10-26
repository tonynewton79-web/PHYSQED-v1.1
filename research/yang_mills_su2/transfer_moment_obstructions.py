"""Exact abstract positive-transfer moments; NOT a Yang--Mills mass gap.

A three-state positive self-adjoint transfer operator with vacuum energy
zero realizes these rational moments. The operator family does not arise
from, or claim to approximate, a Wilson SU(2) gauge transfer operator.
"""

from __future__ import annotations

from fractions import Fraction


def _validate_index(n: int, t: int) -> None:
    if (type(n) is not int or not 3 <= n <= 4096 or
            type(t) is not int or not 0 <= t <= 64):
        raise ValueError("bounded integer n in [3,4096] and t in [0,64] required")


def two_mode_moment(n: int, t: int) -> Fraction:
    """<0|A T^t A|0> for spectrum {1, 1/2, 1-1/n}."""
    _validate_index(n, t)
    weight = Fraction(1, n)
    a = Fraction(1, 2)
    b = Fraction(n - 1, n)
    return (1 - weight) * a**t + weight * b**t


def two_mode_hankel_minor(n: int, t: int) -> Fraction:
    """Closed-form log-convex minor, nonnegative for every allowed n,t."""
    _validate_index(n, t)
    weight = Fraction(1, n)
    a = Fraction(1, 2)
    b = Fraction(n - 1, n)
    return weight * (1 - weight) * (a*b)**t * (b - a)**2


def finite_period_two_state_correlator(
    period: int, q: Fraction,
) -> tuple[Fraction, ...]:
    """Tr[T^(N-t) A T^t A]/Tr[T^N], T=diag(1,q), A=swap."""
    if (type(period) is not int or not 2 <= period <= 32 or
            type(q) is not Fraction or not 0 < q < 1 or
            q.numerator.bit_length() > 128 or q.denominator.bit_length() > 128):
        raise ValueError("finite period [2,32] and rational q in (0,1) required")
    denominator = 1 + q**period
    return tuple((q**t + q**(period-t))/denominator for t in range(period))


def _rational_json(value: Fraction) -> dict[str, str]:
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def transfer_moment_receipt(n: int, horizon: int) -> dict:
    """Recomputable exact finite sample of a uniform-in-time obstruction."""
    if (type(horizon) is not int or not 0 <= horizon <= 32):
        raise ValueError("bounded integer horizon in [0,32] required")
    _validate_index(n, horizon + 2)
    a, b, weight = Fraction(1, 2), Fraction(n - 1, n), Fraction(1, n)
    return {
        "schema_version": "ym-abstract-transfer-moments-0.1",
        "certificate_scope": "ABSTRACT_POSITIVE_TRANSFER_OPERATOR_ONLY",
        "parameters": {"n": n, "horizon": horizon},
        "reference_eigenvalue": _rational_json(a),
        "slow_eigenvalue": _rational_json(b),
        "slow_spectral_weight": _rational_json(weight),
        "moments": [_rational_json(two_mode_moment(n, t))
                    for t in range(horizon + 3)],
        "reference_moments": [_rational_json(a**t)
                              for t in range(horizon + 3)],
        "hankel_minors": [_rational_json(two_mode_hankel_minor(n, t))
                          for t in range(horizon + 1)],
        "uniform_absolute_error_bound": _rational_json(weight),
        "positive_period_four_fixture": [
            _rational_json(c) for c in finite_period_two_state_correlator(4, a)],
        "analytical_premises": [
            "T_n=diag(1,1/2,1-1/n) is a positive self-adjoint transfer matrix",
            "vacuum A couplings are sqrt(1-1/n) and sqrt(1/n)",
            "the lowest observable-coupled gap is -log(1-1/n) and tends to zero",
            "the uniform error bound follows from 0<=b^t-a^t<=1",
        ],
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
    }


def _strict_equal(received: object, expected: object) -> bool:
    """Fail closed, including Python's normally equal bool and int values."""
    if type(received) is not type(expected):
        return False
    if type(expected) is dict:
        return (len(received) == len(expected) and all(
            key in received and _strict_equal(received[key], value)
            for key, value in expected.items()))
    if type(expected) is list:
        return (len(received) == len(expected) and all(
            _strict_equal(left, right) for left, right in zip(received, expected)))
    return received == expected


def replay_transfer_moment_receipt(receipt: object) -> bool:
    """Exactly regenerate finite values from bounded, explicit parameters."""
    if type(receipt) is not dict or type(receipt.get("parameters")) is not dict:
        return False
    parameters = receipt["parameters"]
    try:
        expected = transfer_moment_receipt(parameters["n"], parameters["horizon"])
    except (KeyError, ValueError, TypeError):
        return False
    return _strict_equal(receipt, expected)
