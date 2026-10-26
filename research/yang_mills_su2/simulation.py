"""Seeded finite-cutoff SU(2) Wilson-lattice Monte Carlo diagnostics.

This intentionally small pilot uses complete-action Metropolis differences.
It cannot establish a continuum field theory or a mass gap.
"""

from __future__ import annotations

import math
import random
import statistics

from .lattice import Lattice4D
from .su2 import axis_angle, mul


def haar_su2(rng: random.Random) -> tuple[float, float, float, float]:
    """Haar-distributed SU(2) link via normalized independent Gaussians on S3."""
    while True:
        values = tuple(rng.gauss(0.0, 1.0) for _ in range(4))
        length_sq = sum(x*x for x in values)
        if length_sq > 0 and math.isfinite(length_sq):
            return tuple(x / math.sqrt(length_sq) for x in values)


def _controls(beta: float, epsilon: float) -> None:
    if not isinstance(beta, (int, float)) or not math.isfinite(beta) or beta < 0:
        raise ValueError("finite nonnegative beta required")
    if not isinstance(epsilon, (int, float)) or not math.isfinite(epsilon) or not 0 < epsilon <= math.pi:
        raise ValueError("finite proposal angle within (0, pi] required")


def metropolis_sweep(
    lattice: Lattice4D,
    beta: float,
    epsilon: float,
    rng: random.Random,
) -> tuple[int, int]:
    """One deterministic-order sweep of symmetric unit-quaternion proposals."""
    _controls(beta, epsilon)
    accepted = 0
    attempted = 0
    action = lattice.wilson_action(beta)
    for site in lattice.sites:
        for mu in range(4):
            old_link = lattice.link(site, mu)
            axis = tuple(rng.gauss(0.0, 1.0) for _ in range(3))
            theta = rng.uniform(-epsilon, epsilon)
            proposal = mul(axis_angle(axis, theta), old_link)
            lattice.set_link(site, mu, proposal)
            proposed_action = lattice.wilson_action(beta)
            difference = proposed_action - action
            attempted += 1
            if difference <= 0 or rng.random() < math.exp(-difference):
                accepted += 1
                action = proposed_action
            else:
                lattice.set_link(site, mu, old_link)
    return accepted, attempted


def timeslice_plaquette(lattice: Lattice4D) -> tuple[float, ...]:
    """Mean spatial ReTr(U_p)/2 by Euclidean-time slice."""
    slices = [[] for _ in range(lattice.extents[0])]
    for site in lattice.sites:
        for mu in (1, 2, 3):
            for nu in range(mu + 1, 4):
                slices[site[0]].append(lattice.plaquette(site, mu, nu)[0])
    return tuple(statistics.fmean(values) for values in slices)


def connected_timeslice(samples: list[tuple[float, ...]]) -> tuple[float, ...]:
    """Translation-averaged sample connected covariance, not a spectral bound."""
    if len(samples) < 2:
        raise ValueError("at least two samples required for covariance")
    times = len(samples[0])
    if times < 2 or any(len(s) != times for s in samples):
        raise ValueError("inconsistent or too-short timeslices")
    average = statistics.fmean(v for sample in samples for v in sample)
    return tuple(
        statistics.fmean(
            (sample[t] - average) * (sample[(t + shift) % times] - average)
            for sample in samples for t in range(times)
        )
        for shift in range(times)
    )


def run_chains(
    extents: tuple[int, int, int, int],
    beta: float,
    seeds: tuple[int, ...],
    warmup: int,
    sweeps: int,
    thin: int,
    epsilon: float,
    initialization: str = "cold",
) -> dict:
    _controls(beta, epsilon)
    if initialization not in ("cold", "haar"):
        raise ValueError("initialization must be cold or haar")
    if type(warmup) is not int or warmup < 0:
        raise ValueError("warmup must be a nonnegative integer")
    if type(sweeps) is not int or sweeps < 2:
        raise ValueError("at least two sampling sweeps required")
    if type(thin) is not int or thin < 1:
        raise ValueError("thin must be a positive integer")
    if (len(seeds) < 2 or len({abs(seed) for seed in seeds}) != len(seeds) or
        any(type(seed) is not int for seed in seeds)):
        raise ValueError("at least two distinct integer chain seeds required")
    if sweeps // thin < 2:
        raise ValueError("at least two samples per chain required")

    per_chain = []
    total_accepted = total_attempted = 0
    for seed in seeds:
        rng = random.Random(seed)
        lattice = Lattice4D(extents)
        if initialization == "haar":
            for site in lattice.sites:
                for mu in range(4):
                    lattice.set_link(site, mu, haar_su2(rng))
        samples = []
        measurements = []
        chain_accepted = chain_attempted = 0
        for _ in range(warmup):
            a, b = metropolis_sweep(lattice, beta, epsilon, rng)
            chain_accepted += a
            chain_attempted += b
        for i in range(1, sweeps + 1):
            a, b = metropolis_sweep(lattice, beta, epsilon, rng)
            chain_accepted += a
            chain_attempted += b
            if i % thin == 0:
                measurement = timeslice_plaquette(lattice)
                samples.append(measurement)
                measurements.append({"sweep": i, "timeslice": list(measurement)})
        chain_mean = statistics.fmean(v for s in samples for v in s)
        per_chain.append({
            "seed": seed,
            "samples": len(samples),
            "measurements": measurements,
            "mean_spatial_plaquette": chain_mean,
            "connected_correlator": list(connected_timeslice(samples)),
            "acceptance_rate": chain_accepted / chain_attempted,
        })
        total_accepted += chain_accepted
        total_attempted += chain_attempted

    def mean_error(values: list[float]) -> dict:
        return {
            "mean": statistics.fmean(values),
            "independent_chain_standard_error": statistics.stdev(values) / math.sqrt(len(values)),
        }

    covariance = [mean_error([chain["connected_correlator"][t] for chain in per_chain])
                  for t in range(extents[0])]
    return {
        "schema_version": "ym-su2-finite-pilot-0.1",
        "status": "FINITE_LATTICE_NUMERICAL",
        "continuum_mass_gap_proven": False,
        "physical_law_proven": False,
        "equilibrium_claim": False,
        "thermalization_status": ("UNTHERMALIZED_COLD_START_TRANSIENT" if initialization == "cold"
                                  else "UNTHERMALIZED_HAAR_START_TRANSIENT"),
        "parameters": {
            "extents": list(extents), "beta": float(beta), "seeds": list(seeds),
            "warmup": warmup, "sweeps": sweeps, "thin": thin,
            "epsilon": float(epsilon), "initialization": initialization,
            "boundary_conditions": "periodic",
            "action": "SU2 Wilson, beta sum_p (1-ReTr(U_p)/2)",
        },
        "acceptance_rate": total_accepted / total_attempted,
        "spatial_plaquette": mean_error([c["mean_spatial_plaquette"] for c in per_chain]),
        "connected_correlator": covariance,
        "per_chain": per_chain,
        "limitations": [
            "finite lattice and finite sampling only",
            "the thermalization and autocorrelation times are unmeasured",
            "cold initialization makes short low-angle runs strong transient diagnostics, not equilibrium estimates",
            "no autocorrelation-time or continuum-limit certification",
            "a single spatial-plaquette channel is not the entire physical spectrum",
            "independent-chain standard errors are exploratory, not full systematic errors",
        ],
    }
