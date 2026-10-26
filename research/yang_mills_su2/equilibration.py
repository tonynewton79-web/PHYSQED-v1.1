"""Matched finite cold/Haar-start trajectories; not equilibrium certification.

The output documents every sweep. Drift, lag-one correlation and cold/hot
differences are descriptive finite-sample diagnostics without confidence
bounds sufficient to establish thermalization or continuum mass gaps.
"""

from __future__ import annotations

import math
import random
import statistics

from .lattice import Lattice4D
from .local_updates import metropolis_sweep_local
from .simulation import haar_su2, timeslice_plaquette


def _lag_one_correlation(values: list[float]) -> float | None:
    if len(values) < 4:
        return None
    left, right = values[:-1], values[1:]
    left_mean, right_mean = statistics.fmean(left), statistics.fmean(right)
    x = [a-left_mean for a in left]
    y = [b-right_mean for b in right]
    denom = math.sqrt(math.fsum(v*v for v in x) * math.fsum(v*v for v in y))
    return math.fsum(a*b for a, b in zip(x, y)) / denom if denom > 0 else None


def run_equilibration(
    extents: tuple[int, int, int, int], beta: float,
    seeds: tuple[int, ...], sweeps: int, epsilon: float,
) -> dict:
    """Run paired short cold/Haar chains with exact reproducibility controls."""
    if (type(extents) is not tuple or len(extents) != 4 or
        any(type(s) is not int or not 2 <= s <= 3 for s in extents) or
        type(beta) not in (int, float) or not math.isfinite(beta) or
        not 0 <= beta <= 8 or
        type(seeds) is not tuple or not 2 <= len(seeds) <= 4 or
        any(type(s) is not int or abs(s) > 2**32 for s in seeds) or
        len({abs(s) for s in seeds}) != len(seeds) or
        type(sweeps) is not int or not 8 <= sweeps <= 64 or
        type(epsilon) not in (int, float) or not math.isfinite(epsilon) or
        not 0 < epsilon <= math.pi):
        raise ValueError("finite paired-trajectory budget and valid parameters required")

    groups: dict[str, dict] = {}
    half = sweeps // 2
    for initialization in ("cold", "haar"):
        chains = []
        for seed in seeds:
            rng = random.Random(seed)
            lat = Lattice4D(extents)
            if initialization == "haar":
                for site in lat.sites:
                    for mu in range(4):
                        lat.set_link(site, mu, haar_su2(rng))
            trace = []
            accepted = attempted = 0
            for sweep in range(1, sweeps + 1):
                a, b = metropolis_sweep_local(lat, beta, epsilon, rng)
                accepted += a
                attempted += b
                trace.append({"sweep": sweep,
                              "spatial_plaquette": statistics.fmean(timeslice_plaquette(lat))})
            values = [point["spatial_plaquette"] for point in trace]
            early = statistics.fmean(values[:half])
            late = statistics.fmean(values[-half:])
            chains.append({
                "seed": seed, "trace": trace,
                "early_mean": early, "late_mean": late,
                "late_minus_early": late-early,
                "lag_one_correlation": _lag_one_correlation(values),
                "acceptance_rate": accepted/attempted,
            })
        groups[initialization] = {
            "chains": chains,
            "early_mean": statistics.fmean(c["early_mean"] for c in chains),
            "late_mean": statistics.fmean(c["late_mean"] for c in chains),
        }
    return {
        "schema_version": "ym-su2-equilibration-0.1",
        "status": "FINITE_COLD_HAAR_TRAJECTORY_DIAGNOSTIC",
        "parameters": {"extents": list(extents), "beta": float(beta),
                       "seeds": list(seeds), "sweeps": sweeps,
                       "epsilon": float(epsilon), "boundary_conditions": "periodic",
                       "action": "SU2 Wilson, beta sum_p (1-ReTr(U_p)/2)"},
        "groups": groups,
        "cold_minus_haar_late_mean": (groups["cold"]["late_mean"] -
                                      groups["haar"]["late_mean"]),
        "equilibrium_claim": False,
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
        "limitations": [
            "finite Euclidean lattice and finite seeded sampling only",
            "no thermalization time, effective sample size or autocorrelation error certification",
            "early/late drift and cold/Haar agreement are descriptive, not proof of equilibrium",
            "spatial plaquette is not a full physical transfer-matrix spectral observable",
            "no continuum, infinite-volume, or physical mass-gap theorem",
        ],
    }
