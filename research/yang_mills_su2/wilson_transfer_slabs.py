"""Exact structural Wilson action decomposition, numerically on SU(2) links.

The equality is algebraic for group elements; its quaternion implementation
uses floating point and is checked within rounding. No equilibrium or
spectral-mass conclusion follows from an individual finite configuration.
"""

from __future__ import annotations

import math

from .lattice import Lattice4D
from .su2 import dagger, mul


def wilson_temporal_kernel_log(lattice: Lattice4D, beta: float, time: int) -> float:
    """Timelike Wilson slab via U_e h_y V_e^-1 h_x^-1, before gauge averaging.

    U is the spatial field at time `time`, V at the next time, and h_x
    are the *actual* temporal links. The kernel is the gauge-integrated
    product of these positive link factors in the transfer construction.
    """
    if (type(lattice) is not Lattice4D or len(lattice.sites) > 256 or
            type(beta) not in (int,float) or not 0 <= beta <= 8 or
            not math.isfinite(beta) or type(time) is not int or
            not 0 <= time < lattice.extents[0]):
        raise ValueError("finite Wilson slab, nonnegative beta and valid time required")
    contributions = []
    for site in lattice.sites:
        if site[0] != time:
            continue
        next_time = lattice.shifted(site, 0)
        h_x = lattice.link(site, 0)
        for direction in (1,2,3):
            endpoint = lattice.shifted(site, direction)
            u = lattice.link(site, direction)
            h_y = lattice.link(endpoint, 0)
            v = lattice.link(next_time, direction)
            product = mul(mul(mul(u, h_y), dagger(v)), dagger(h_x))
            contributions.append(product[0])
    return float(beta)*math.fsum(contributions)


def wilson_slab_log_weights(lattice: Lattice4D, beta: float) -> tuple[float, ...]:
    """Return beta*(temporal faces + half of each adjacent spatial cap).

    For periodic Euclidean time every spatial plaquette belongs to two
    neighboring half-caps. Thus sum_t slab_t=beta*sum_all ReTr(U_p)/2,
    which is the Wilson Gibbs log density up to its constant normalization.
    """
    if (type(lattice) is not Lattice4D or len(lattice.sites) > 256 or
            type(beta) not in (int, float) or not 0 <= beta <= 8 or
            not math.isfinite(beta)):
        raise ValueError("bounded Wilson SU2 lattice and nonnegative finite beta required")
    periods = lattice.extents[0]
    spatial = [0.0]*periods
    temporal = [0.0]*periods
    for t in range(periods):
        sites = (site for site in lattice.sites if site[0] == t)
        s_values, t_values = [], []
        for site in sites:
            for mu in range(1, 4):
                for nu in range(mu+1, 4):
                    s_values.append(lattice.plaquette(site, mu, nu)[0])
                t_values.append(lattice.plaquette(site, 0, mu)[0])
        spatial[t] = math.fsum(s_values)
        temporal[t] = math.fsum(t_values)
    return tuple(float(beta)*(temporal[t] +
                              (spatial[t]+spatial[(t+1)%periods])/2)
                 for t in range(periods))
