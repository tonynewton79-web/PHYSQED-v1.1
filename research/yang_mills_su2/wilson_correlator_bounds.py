"""Coarse exact finite-beta continuity bound for genuine Wilson correlations.

Unlike seeded Monte Carlo output, this is a deterministic bound on the
finite-volume Gibbs expectation. Its factor of total plaquette count means
it cannot yield a uniform infinite-volume or continuum mass-gap estimate.
"""

from __future__ import annotations

from fractions import Fraction
from math import prod


def finite_beta_spatial_correlator_bound(
    extents: tuple[int, int, int, int], beta: Fraction, time_lag: int,
) -> Fraction:
    """Bound |Cov_beta(X_0,X_t)| by min(1,M*beta+(M*beta)^2), t>0.

    X_t is the normalized spatial-plaquette timeslice average in [-1,1]
    for Wilson SU(2). M=6*number_of_4D_sites bounds |sum_p W_p|.

    For any |F|<=1, the Gibbs derivative is Cov_beta(F,H) with |H|<=M,
    hence |d E_beta[F]/d beta|<=M by Cauchy/variance-range bounds. At
    beta=0, E[X_t]=0 and E[X_0 X_t]=0 for distinct time slices. Integrate
    the bound for F=X_t, X_0 and X_t X_0 and subtract the product of
    means. The independent variance estimate gives |Cov|<=1.
    """
    if (type(extents) is not tuple or len(extents) != 4 or
            any(type(v) is not int or not 2 <= v <= 64 for v in extents) or
            prod(extents) > 512 or
            type(time_lag) is not int or not 1 <= time_lag < extents[0] or
            type(beta) is not Fraction or not 0 <= beta <= 4 or
            beta.numerator.bit_length() > 16 or beta.denominator.bit_length() > 16):
        raise ValueError("bounded positive-beta Wilson geometry and nonzero time lag required")
    plaquettes = 6 * prod(extents)
    mbeta = plaquettes * beta
    return min(Fraction(1), mbeta + mbeta*mbeta)
