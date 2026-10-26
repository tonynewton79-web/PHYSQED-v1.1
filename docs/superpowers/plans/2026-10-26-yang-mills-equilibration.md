# SU(2) Equilibration and Local Wilson Updates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Provide a faster, checked finite-lattice SU(2) update and an explicitly noncertifying cold/Haar equilibration comparison.

**Architecture:** Keep the existing complete-action simulation and evidence report as stable independent references. Implement local action differences over exactly six plaquettes; build matched, seeded chain diagnostics on that verified kernel; add resource-limited deterministic replay.

**Tech Stack:** Python 3.12 standard library, unittest, existing SU(2) quaternion/lattice modules.

**Spec:** `docs/superpowers/specs/2026-10-26-yang-mills-equilibrium-extension-design.md`

## Global Constraints

- Existing historical artifacts and PHYSQED v1.1 source files remain unchanged.
- No thermalization, physical-law, continuum, or spectral-gap proof claim.
- Preserve transparent cold/Haar initialization, seeds, raw traces, and the full Wilson-action oracle.
- Changes live on a new isolated feature branch and draft PR; no merge.

## Review Focus

1. A changed link appearing in a backward-oriented plaquette must be counted exactly once.
2. The local delta routine must restore the original link even on an exception.
3. Random accept/reject trajectories must not change when a local update replaces a full-action difference, except for numerical tolerance-bound near-ties.
4. An apparent cold/hot agreement must never be promoted to an equilibrium or physical mass-gap certificate.
5. Oversized or malformed replay inputs must fail before expensive simulation.

---

### Task 1: Six-plaquette local action kernel

**Files:** Create `research/yang_mills_su2/local_updates.py`; create `research/yang_mills_su2/tests/test_local_updates.py`.

**Interfaces:** `affected_plaquettes(lat, site, mu) -> tuple[(site,mu,nu),...]`; `link_delta_action(lat,site,mu,proposed,beta)->float`; `metropolis_sweep_local(lat,beta,epsilon,rng)->tuple[int,int]`.

- [ ] Write tests for exactly six distinct oriented plaquettes per link on 2^4 and 3^4; check proposed-link action difference against `lat.wilson_action` with random nontrivial links.
- [ ] Run tests and observe missing implementation failure.
- [ ] Implement affected plaquette enumeration and temporary substitution with `try/finally` rollback.
- [ ] Implement local Metropolis sweep, preserving the original seeded proposal stream.
- [ ] Test accept/reject trajectory equality and all baseline physical tests. Commit.

### Task 2: Matched starting-state diagnostics

**Files:** Create `research/yang_mills_su2/equilibration.py`; create `research/yang_mills_su2/tests/test_equilibration.py`.

**Interfaces:** `run_equilibration(extents,beta,seeds,sweeps,epsilon)->dict` with both starting states, per-sweep spatial-plaquette traces, early/late drift, lag-one sample autocorrelation and explicit false certification flags.

- [ ] Write test for fixed seeds, matched protocol, bounded traces and beta-zero Haar control, with no equilibrium claim.
- [ ] Run test and confirm feature-missing failure.
- [ ] Implement reproducible paired runs with bounded lattice and sweep sizes.
- [ ] Document finite descriptive statistics and run tests. Commit.

### Task 3: Replay and research artifacts

**Files:** Create `research/yang_mills_su2/equilibration_cli.py`, add tests and `EQUILIBRATION_SCOPE.md`; create small independently replayable JSON report.

**Interfaces:** `certify_equilibration(...)->dict`, `replay_equilibration_receipt(receipt)->bool`, CLI `--verify`, with bounded raw values and canonical JSON hash.

- [ ] Write adversarial tests for altered observations, forged proof flags and unbounded requests; confirm failure.
- [ ] Implement deterministic re-execution and integrity/status checks.
- [ ] Generate 2^4 and 3^4 finite diagnostic examples, interpret as finite controls only.
- [ ] Run all SU(2), PHYSQED and report replay tests. Commit and prepare isolated GitHub draft PR (no merge).
