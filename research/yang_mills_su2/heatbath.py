"""One-link SU(2) Wilson heatbath, with an independent six-plaquette oracle.

This is an exact finite-dimensional conditional distribution mathematically.
Its floating-point and pseudo-random implementation is a reproducible
simulation, not an exact sampler in machine arithmetic, proof of mixing,
physical spectral bound, or continuum Yang--Mills construction.
"""

from __future__ import annotations

import math
import random

from .lattice import Lattice4D, Site
from .local_updates import affected_plaquettes
from .simulation import haar_su2
from .su2 import Quaternion, mul


_QUATERNION_BASIS: tuple[Quaternion, ...] = (
    (1.0, 0.0, 0.0, 0.0),
    (0.0, 1.0, 0.0, 0.0),
    (0.0, 0.0, 1.0, 0.0),
    (0.0, 0.0, 0.0, 1.0),
)


def staple_linear_coefficients(
    lattice: Lattice4D, site: Site, direction: int,
) -> Quaternion:
    """Return h such that sum_(six plaquettes) ReTr(U_p(q))/2 = h·q.

    The six affected *positively oriented* plaquettes are independent of
    q, and each contains the proposed link precisely once. Therefore their
    scalar trace sum is a real-linear functional of its four coordinates.
    Four valid quaternion basis substitutions determine it exactly up to
    floating-point roundoff. Every mutation is restored, including failures.
    """
    old_link = lattice.link(site, direction)
    keys = affected_plaquettes(lattice, site, direction)
    coeffs: list[float] = []
    try:
        for basis in _QUATERNION_BASIS:
            lattice.set_link(site, direction, basis)
            coeffs.append(math.fsum(
                lattice.plaquette(root, mu, nu)[0] for root, mu, nu in keys))
    finally:
        lattice.set_link(site, direction, old_link)
    return (coeffs[0], coeffs[1], coeffs[2], coeffs[3])


def sample_heatbath_link(
    coeff: Quaternion, beta: float, rng: random.Random,
) -> Quaternion:
    """Sample dP(q) proportional to exp(beta*h·q) dHaar(q), q∈S³.

    With kappa=beta*|h| the projection t=(h/|h|)·q has density
    proportional to exp(kappa*t)*sqrt(1-t²) on [-1,1]. Draw t from
    the truncated exponential, reject with weight sqrt(1-t²), and draw
    the transverse axis uniformly on S². A unit-quaternion rotation
    maps the polar scalar axis to h/|h|.
    """
    if (type(beta) not in (int, float) or not math.isfinite(beta)
            or beta < 0 or len(coeff) != 4
            or any(type(x) not in (int, float) or not math.isfinite(x)
                   for x in coeff)):
        raise ValueError("finite nonnegative beta and finite four-vector required")
    if beta == 0:
        return haar_su2(rng)

    # Compute kappa and the unit staple direction without squaring
    # very small/large components or overflowing an intermediate norm.
    scale = max(abs(float(x)) for x in coeff)
    if scale == 0:
        return haar_su2(rng)
    unit_scaled = tuple(float(x) / scale for x in coeff)
    unit_length = math.hypot(*unit_scaled)
    kappa = (beta * scale) * unit_length
    if not math.isfinite(kappa) or kappa > 128:
        raise ValueError("bounded heatbath concentration required")
    direction = tuple(x / unit_length for x in unit_scaled)

    # The direct inverse CDF subtracts nearly equal floating values as
    # kappa -> 0; at subnormal kappa it collapses to the endpoints.
    # Haar rejection with bound exp(kappa) has no such subtraction, and
    # is an exact conditional-rejection construction in real arithmetic.
    if kappa < 1e-7:
        for _ in range(100000):
            candidate = haar_su2(rng)
            alignment = math.fsum(a*b for a, b in zip(direction, candidate))
            if rng.random() < math.exp(kappa * (alignment - 1.0)):
                return candidate
        raise RuntimeError("small-kappa heatbath rejection exceeded budget")

    # Inverse CDF of an exp(kappa*t) density on [-1,1].  log1p/expm1
    # stay well-conditioned when kappa approaches zero.
    exp_range = math.expm1(2 * kappa)
    for _ in range(100000):
        u = rng.random()
        t = -1.0 + math.log1p(u * exp_range) / kappa
        t = max(-1.0, min(1.0, t))
        transverse_sq = max(0.0, 1.0-t*t)
        if rng.random() < math.sqrt(transverse_sq):
            break
    else:
        raise RuntimeError("conditional rejection sampler exhausted its budget")

    while True:
        axis = (rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0),
                rng.gauss(0.0, 1.0))
        axis_length = math.hypot(*axis)
        if axis_length > 0 and math.isfinite(axis_length):
            break
    amplitude = math.sqrt(transverse_sq) / axis_length
    about_identity = (t, *(x * amplitude for x in axis))
    return mul(direction, about_identity)  # type: ignore[arg-type]


def heatbath_sweep(
    lattice: Lattice4D, beta: float, rng: random.Random,
) -> int:
    """One fixed-order SU(2) heatbath Gibbs sweep; return updated link count."""
    if type(beta) not in (int, float) or not math.isfinite(beta) or not 0 <= beta <= 8:
        raise ValueError("finite Wilson coupling in [0,8] required")
    updates = 0
    for site in lattice.sites:
        for direction in range(4):
            if beta == 0:
                q = haar_su2(rng)
            else:
                coeff = staple_linear_coefficients(lattice, site, direction)
                q = sample_heatbath_link(coeff, beta, rng)
            lattice.set_link(site, direction, q)
            updates += 1
    return updates
