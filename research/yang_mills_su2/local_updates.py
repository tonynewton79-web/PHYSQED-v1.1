"""Local six-plaquette Wilson-action updates, checked against the full action.

These are finite-lattice numerical algorithms, not a thermalization proof,
continuum construction or certified physical mass-gap computation.
"""

from __future__ import annotations

import math
import random

from .lattice import Lattice4D, Site
from .su2 import Quaternion, axis_angle, mul


def affected_plaquettes(
    lattice: Lattice4D, site: Site, direction: int,
) -> tuple[tuple[Site, int, int], ...]:
    """Return the six positively oriented plaquettes touching one 4D link."""
    lattice.link(site, direction)  # Validate the canonical link and site.
    affected = []
    for other in range(4):
        if other == direction:
            continue
        lo, hi = sorted((direction, other))
        affected.append((site, lo, hi))
        affected.append((lattice.shifted(site, other, -1), lo, hi))
    return tuple(affected)


def link_delta_action(
    lattice: Lattice4D, site: Site, direction: int,
    proposal: Quaternion, beta: float,
) -> float:
    """Compute S(proposed)-S(original), restoring the original link always."""
    if type(beta) not in (float, int) or not math.isfinite(beta) or beta < 0:
        raise ValueError("finite nonnegative Wilson coupling required")
    old = lattice.link(site, direction)
    keys = affected_plaquettes(lattice, site, direction)
    old_sum = math.fsum(lattice.plaquette(root, lo, hi)[0] for root, lo, hi in keys)
    try:
        lattice.set_link(site, direction, proposal)
        new_sum = math.fsum(lattice.plaquette(root, lo, hi)[0]
                            for root, lo, hi in keys)
    finally:
        lattice.set_link(site, direction, old)
    return float(beta) * (old_sum - new_sum)


def metropolis_sweep_local(
    lattice: Lattice4D, beta: float, epsilon: float, rng: random.Random,
) -> tuple[int, int]:
    """One deterministic-order Metropolis sweep with local action differences."""
    if (type(beta) not in (float, int) or not math.isfinite(beta) or beta < 0 or
        type(epsilon) not in (float, int) or not math.isfinite(epsilon) or
        not 0 < epsilon <= math.pi):
        raise ValueError("invalid finite coupling or proposal angle")
    accepted = 0
    attempted = 0
    for site in lattice.sites:
        for mu in range(4):
            axis = tuple(rng.gauss(0.0, 1.0) for _ in range(3))
            theta = rng.uniform(-epsilon, epsilon)
            proposal = mul(axis_angle(axis, theta), lattice.link(site, mu))
            delta = link_delta_action(lattice, site, mu, proposal, beta)
            attempted += 1
            if delta <= 0 or rng.random() < math.exp(-delta):
                lattice.set_link(site, mu, proposal)
                accepted += 1
    return accepted, attempted
