# Yang-Mills Beta-Zero Correlator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add exact, replayable beta-zero SU(2) time-correlator and centring-bias controls to the finite physical simulator.

**Architecture:** Use independent Haar-link spatial-plaquette orthogonality to calculate exact rational targets. Keep the historical numerical estimator unchanged and report a separately named corrected diagnostic only for beta zero.

**Tech Stack:** Python 3.12 standard library, `fractions.Fraction`, `unittest`, existing lattice and heatbath modules.

**Spec:** `docs/superpowers/specs/2026-10-26-yang-mills-beta0-correlator-design.md`

## Global Constraints

- Every existing raw numerical measurement and historical artifact must retain its existing meaning.
- Only exact `beta == 0` may enable the known-null-model correction.
- Validate bounded extents and sample sizes before expensive work or receipt serialization.
- Exact rational receipts are proof-scope limited to ideal independent Haar links and the stated elementary SU(2) moments.
- Preserve false values of all equilibrium, continuum mass-gap, physical-law, and Lean-kernel proof flags.

## Review Focus

1. A spatial side length two must not cause two listed plaquette loops to be counted as the same.
2. The estimated mean has `M*T` samples, not `M` samples; wrong denominators must fail fixture tests.
3. The correction must apply at time zero as well as nonzero lags, and must not claim every realised corrected lag is positive.
4. Bool-as-int, malformed extents, oversized samples, altered receipts and extra fields must be rejected.
5. Positive-beta diagnostic paths must remain untouched by beta-zero null-model fields.

---

### Task 1: Exact covariance and centring receipt

**Files:** Create `research/yang_mills_su2/beta_zero_correlators.py`; create `research/yang_mills_su2/tests/test_beta_zero_correlators.py`.

**Interfaces:** `exact_beta_zero_covariance(extents: tuple[int,int,int,int]) -> tuple[Fraction,...]`; `expected_centered_covariance(extents, measurements: int) -> tuple[Fraction,...]`; `beta_zero_correlator_receipt(extents, measurements) -> dict`; `replay_beta_zero_correlator_receipt(receipt: object) -> bool`.

- [ ] Write literal exact tests for `(4,2,2,2), M=2`: theoretical `(1/96,0,0,0)`; centring correction `1/768`; raw expectation `(7/768,-1/768,-1/768,-1/768)`; corrected expectation `(1/96,0,0,0)`; replay/tampering/refusal cases.
- [ ] Run `PYTHONPATH=../../../ym_deps python -m unittest research.yang_mills_su2.tests.test_beta_zero_correlators -v` from the worktree and confirm a missing-interface failure.
- [ ] Implement minimal bounded exact arithmetic and canonical JSON receipt, including analytical premises and all false proof flags.
- [ ] Rerun focused tests and check green; commit with message `feat: certify exact beta-zero time-correlator null model`.

### Task 2: Controlled estimator and runner integration

**Files:** Modify `research/yang_mills_su2/beta_zero_correlators.py`; modify `research/yang_mills_su2/transfer_diagnostics.py`; modify `research/yang_mills_su2/tests/test_beta_zero_correlators.py`; modify `research/yang_mills_su2/tests/test_transfer_diagnostics.py`.

**Interfaces:** `beta_zero_corrected_correlator(samples: list[tuple[float,...]], extents: tuple[int,int,int,int]) -> tuple[float,...]`; conditional numerical fields `beta_zero_corrected_connected_correlator` and `beta_zero_expected_finite_sample` in exact-beta-zero group data only.

- [ ] Write failing tests for the additive known correction at all lags, beta-zero cold/Haar runner fields and exactly unchanged positive-beta fields; independently enumerate all 256 synthetic eight-bit independent Rademacher samples and test ensemble correction as a separate mathematical fixture.
- [ ] Run focused tests to verify the absent estimator/integration fails for the intended reason.
- [ ] Add minimal estimator and beta-zero-only runner fields; retain original raw and folded connected arrays, all proof-scope flags and limits.
- [ ] Rerun focused suites green and commit `feat: label finite-sample beta-zero correlator correction`.

### Task 3: Proof explanation and complete regression

**Files:** Create `research/yang_mills_su2/BETA_ZERO_CORRELATOR_SCOPE.md`; modify `research/yang_mills_su2/evidence_bridge.py` and its tests; review `docs/superpowers/specs/2026-10-26-yang-mills-beta0-correlator-design.md`.

**Interfaces:** source-indexed mathematical proof of SU(2) Haar normalized trace second moment, distinct-loop orthogonality, exact centring expectation and absence of physical spectral conclusion.

- [ ] Write complete elementary proof and restrictions without decorative figures or unearned novelty claims.
- [ ] Watch a new ledger-integration test reject the previously unknown exact-Haar-correlator kind; register only that scoped evidence kind and independently replay source and implementation hashes.
- [ ] Run all `research/yang_mills_su2/tests`, all `projects/physqed/tests`, and independent historical receipt verifiers with the pinned SymPy dependency; verify the clean worktree after committing.
- [ ] Commit `docs: prove and scope beta-zero time-correlator benchmark`.
