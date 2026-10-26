"""Gauge-invariant finite heatbath timeslices, not a physical mass gap.

The periodic cosh formula is an exploratory fit diagnostic. Neither the
short chains nor positive fitted values certify equilibrium, reflection
positivity of an estimated covariance, or a lower transfer-matrix bound.
"""

from __future__ import annotations

import math
import random
import statistics

from .beta_zero_correlators import (
    beta_zero_corrected_correlator, beta_zero_correlator_receipt,
)
from .heatbath import heatbath_sweep
from .lattice import Lattice4D
from .simulation import connected_timeslice, haar_su2, timeslice_plaquette


def cosh_effective_mass(correlator: tuple[float, ...], time: int) -> float | None:
    """Return finite-period cosh mass only if three positive samples permit it.

    For a single cosh C(t)=A*cosh(m*(T/2-t)), the ratio
    (C(t-1)+C(t+1))/(2*C(t)) equals cosh(m).  Sampling noise and
    excited-state admixtures invalidate a lower-bound interpretation.
    """
    if (not isinstance(correlator, (tuple, list))
            or len(correlator) < 4
            or type(time) is not int
            or not 1 <= time < len(correlator)//2):
        raise ValueError("interior time and temporal extent >= 4 required")
    local = correlator[time-1:time+2]
    if any(type(x) not in (int, float) or
           not math.isfinite(x) or x <= 0 for x in local):
        return None
    ratio = (local[0]+local[2])/(2*local[1])
    if not math.isfinite(ratio) or ratio < 1:
        return None
    return math.acosh(ratio)


def _validate(
    extents: tuple[int,int,int,int], beta: float, seeds: tuple[int,...],
    warmup: int, sweeps: int, thin: int,
) -> None:
    if (type(extents) is not tuple or len(extents) != 4
            or any(type(x) is not int for x in extents)
            or not 4 <= extents[0] <= 6
            or any(not 2 <= x <= 3 for x in extents[1:])
            or math.prod(extents) > 128
            or type(beta) not in (int, float) or not math.isfinite(beta)
            or not 0 <= beta <= 8
            or type(seeds) is not tuple or not 2 <= len(seeds) <= 4
            or any(type(x) is not int or abs(x)>2**32 for x in seeds)
            or len({abs(x) for x in seeds}) != len(seeds)
            or any(type(x) is not int for x in (warmup, sweeps, thin))
            or not 0 <= warmup <= 512 or not 2 <= sweeps <= 512
            or not 1 <= thin <= 16 or sweeps//thin < 2
            or math.prod(extents)*4*(warmup+sweeps)*len(seeds)*2 > 80000):
        raise ValueError("bounded finite heatbath time-series parameters required")


def run_heatbath_timeslices(
    extents: tuple[int,int,int,int], beta: float, seeds: tuple[int,...],
    warmup: int, sweeps: int, thin: int,
) -> dict:
    """Retain gauge-invariant plaquette timeslices from cold/Haar Gibbs chains."""
    _validate(extents, beta, seeds, warmup, sweeps, thin)
    groups = {}
    time_extent = extents[0]
    for initialization in ("cold", "haar"):
        chains = []
        for seed in seeds:
            rng = random.Random(seed)
            lat = Lattice4D(extents)
            if initialization == "haar":
                for site in lat.sites:
                    for mu in range(4):
                        lat.set_link(site, mu, haar_su2(rng))
            for _ in range(warmup):
                heatbath_sweep(lat, beta, rng)
            measured: list[tuple[float,...]] = []
            trace = []
            for sweep in range(1, sweeps + 1):
                heatbath_sweep(lat, beta, rng)
                if sweep % thin == 0:
                    points = timeslice_plaquette(lat)
                    measured.append(points)
                    trace.append({"sweep": sweep, "timeslice": list(points)})
            connected = connected_timeslice(measured)
            chain = {
                "seed": seed, "trace": trace,
                "connected_correlator": list(connected),
                "mean_spatial_plaquette": statistics.fmean(
                    x for point in measured for x in point),
            }
            if beta == 0:
                chain["beta_zero_bias_corrected_correlator"] = list(
                    beta_zero_corrected_correlator(measured, extents))
            chains.append(chain)
        raw_connected = tuple(statistics.fmean(
            chain["connected_correlator"][time] for chain in chains)
            for time in range(time_extent))
        folded = tuple(
            raw_connected[0] if time == 0 else
            (raw_connected[time] + raw_connected[-time])/2
            for time in range(time_extent))
        masses = [{
            "time": time,
            "cosh_effective_mass": cosh_effective_mass(folded, time),
        } for time in range(1, time_extent//2)]
        group = {
            "chains": chains,
            "connected_correlator": list(raw_connected),
            "folded_connected_correlator": list(folded),
            "cosh_diagnostics": masses,
        }
        if beta == 0:
            group["beta_zero_exact_receipt"] = beta_zero_correlator_receipt(
                extents, sweeps // thin)
            group["beta_zero_bias_corrected_correlator"] = [
                statistics.fmean(chain["beta_zero_bias_corrected_correlator"][time]
                                 for chain in chains)
                for time in range(time_extent)
            ]
        groups[initialization] = group

    return {
        "schema_version": "ym-su2-heatbath-timeslices-0.1",
        "status": "FINITE_HEATBATH_TIMESLICE_DIAGNOSTIC",
        "parameters": {
            "extents": list(extents), "beta": float(beta), "seeds": list(seeds),
            "warmup": warmup, "sweeps": sweeps, "thin": thin,
            "action": "SU2 Wilson, beta sum_p (1-ReTr(U_p)/2)",
            "boundary_conditions": "periodic",
            "update": "single-link SU2 Wilson conditional heatbath",
        },
        "groups": groups,
        "equilibrium_claim": False,
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
        "limitations": [
            "finite 4D Euclidean lattice and seeded pseudo-random finite chains",
            "no mixing-time or integrated autocorrelation upper bound at positive beta",
            "finite centered covariance is not a rigorous transfer-matrix spectrum",
            "cosh diagnostics can be biased by excited states and finite-time wrapping",
            "no physical scale, continuum construction or positive spectral lower bound",
        ],
    }
