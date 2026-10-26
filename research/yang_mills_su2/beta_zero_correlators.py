"""Exact beta-zero Haar correlator expectations, not a Yang--Mills gap.

The identities assume ideal independent Haar links and distinct spatial
plaquette loops on a periodic lattice with spatial sides at least two.
They are exact identities about the finite Wilson model, not statements
about pseudorandom machine samples or continuum spectral positivity.
"""

from __future__ import annotations

from fractions import Fraction
import math

from .simulation import connected_timeslice


def _validate_extents(extents: tuple[int, int, int, int]) -> None:
    if (type(extents) is not tuple or len(extents) != 4
            or any(type(v) is not int for v in extents)
            or not 4 <= extents[0] <= 64
            or any(not 2 <= v <= 32 for v in extents[1:])
            or extents[0] * extents[1] * extents[2] * extents[3] > 32768):
        raise ValueError("bounded periodic four-dimensional extents required")


def _validate_measurements(extents: tuple[int, int, int, int], measurements: int) -> None:
    if (type(measurements) is not int or not 2 <= measurements <= 512
            or extents[0] * measurements > 4096):
        raise ValueError("bounded independent measurements required")


def exact_beta_zero_covariance(
    extents: tuple[int, int, int, int],
) -> tuple[Fraction, ...]:
    """Ideal beta-zero connected spatial-plaquette covariance by time lag.

    If V=L1*L2*L3, each of the 3V distinct plaquette traces has variance
    1/4 and pairwise different traces have covariance zero. Different time
    slices use disjoint links, hence C(0)=1/(12V), C(t)=0 for 1<=t<T.
    """
    _validate_extents(extents)
    volume = extents[1] * extents[2] * extents[3]
    return (Fraction(1, 12 * volume),) + (Fraction(0),) * (extents[0] - 1)


def expected_centered_covariance(
    extents: tuple[int, int, int, int], measurements: int,
) -> tuple[Fraction, ...]:
    """Expected old shared-mean estimator over independent beta-zero sweeps.

    With N=M*T independent time-slice observations, E[(X_i-Xbar)
    (X_j-Xbar)]=var*(delta_ij - 1/N). Averaging at each periodic lag
    leaves the same expectation, so every lag has negative bias -var/N.
    """
    _validate_extents(extents)
    _validate_measurements(extents, measurements)
    variance = exact_beta_zero_covariance(extents)[0]
    correction = variance / (measurements * extents[0])
    return (variance - correction,) + (-correction,) * (extents[0] - 1)


def beta_zero_corrected_correlator(
    samples: list[tuple[float, ...]], extents: tuple[int, int, int, int],
) -> tuple[float, ...]:
    """Debias the *expectation* of the empirical beta-zero connected trace.

    This function makes no pointwise positivity or mass-gap guarantee:
    finite realised samples can retain arbitrary statistical fluctuations.
    It is valid only for independent time slices across ideal beta-zero
    Haar-refresh configurations, not positive-beta Gibbs chains.
    """
    _validate_extents(extents)
    if type(samples) is not list:
        raise ValueError("measured time slices must be a list")
    _validate_measurements(extents, len(samples))
    if any(type(row) is not tuple or len(row) != extents[0] or
           any(type(value) not in (int, float) or
               not -1 <= value <= 1 or not math.isfinite(value)
               for value in row) for row in samples):
        raise ValueError("finite physical timeslices matching extents required")
    correction = float(exact_beta_zero_covariance(extents)[0] /
                       (len(samples) * extents[0]))
    return tuple(value + correction for value in connected_timeslice(samples))


def _rational_json(value: Fraction) -> dict[str, str]:
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def beta_zero_correlator_receipt(
    extents: tuple[int, int, int, int], measurements: int,
) -> dict:
    """Canonical exact expectation identity, recomputable from bounded input."""
    _validate_extents(extents)
    _validate_measurements(extents, measurements)
    exact = exact_beta_zero_covariance(extents)
    centered = expected_centered_covariance(extents, measurements)
    correction = exact[0] / (extents[0] * measurements)
    return {
        "schema_version": "ym-su2-beta-zero-correlator-0.1",
        "certificate_scope": "IDEAL_FINITE_BETA_ZERO_HAAR_EXPECTATIONS",
        "parameters": {
            "extents": list(extents), "measurements": measurements,
            "coupling_beta": 0,
        },
        "exact_covariance": [_rational_json(v) for v in exact],
        "expected_empirical_centered_covariance": [
            _rational_json(v) for v in centered],
        "centering_correction": _rational_json(correction),
        "expected_bias_corrected_covariance": [
            _rational_json(v) for v in exact],
        "analytical_premises": [
            "ideal independently refreshed Haar SU2 links at beta zero",
            "distinct spatial plaquette loops with spatial side lengths >=2",
            "Haar-normalized trace moment E[(ReTr U/2)^2]=1/4",
            "a common empirical mean of exactly M*T independent time-slice values",
        ],
        "equilibrium_claim": False,
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
    }


def _strict_equal(received: object, expected: object) -> bool:
    """Canonical schema equality without Python's bool/int numeric coercions."""
    if type(received) is not type(expected):
        return False
    if type(expected) is dict:
        return (len(received) == len(expected) and all(
            key in received and _strict_equal(received[key], value)
            for key, value in expected.items()))
    if type(expected) is list:
        return (len(received) == len(expected) and all(
            _strict_equal(a, b) for a, b in zip(received, expected)))
    return received == expected


def replay_beta_zero_correlator_receipt(receipt: object) -> bool:
    """Reject all noncanonical or forged claims by exact rational replay."""
    if type(receipt) is not dict:
        return False
    parameters = receipt.get("parameters")
    if type(parameters) is not dict:
        return False
    extents = parameters.get("extents")
    if type(extents) is not list or len(extents) != 4:
        return False
    try:
        expected = beta_zero_correlator_receipt(
            tuple(extents), parameters["measurements"])
    except (KeyError, TypeError, ValueError):
        return False
    return _strict_equal(receipt, expected)
