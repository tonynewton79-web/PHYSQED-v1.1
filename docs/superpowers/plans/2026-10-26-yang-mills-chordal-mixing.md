# Wilson SU(2) Chordal Strong-Coupling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Certify an explicit stronger lattice-unit transfer ratio `lambda_n/lambda_0 <= 6 beta` at `0<beta<1/6`.

**Architecture:** Preserve all previous certificates; use a new rational module for the exact implications of the spherical Poincare/Wasserstein comparison. Extend the fail-closed PHYSQED evidence bridge, and document the complete finite-volume transfer argument and prior art.

**Tech Stack:** Python `fractions.Fraction`, `unittest`, mathematical Markdown, existing PHYSQED ledger.

**Spec:** `docs/superpowers/specs/2026-10-26-yang-mills-chordal-mixing-design.md`

## Global Constraints

- Strict rational `0<beta<1/6`; the sharp unreviewed `1/4` estimate is NOT a premise.
- Only gauge-invariant finite-volume Wilson transfer ratios in lattice units.
- Python replays exact rational algebra but not the analytic Poincare and coupling theorems.

## Review Focus

1. Source normalization: Wilson `beta` multiplying `Re Tr(U_p)/2` versus any author's alternative convention.
2. Geodesic versus **chordal** Wasserstein metric; do not interchange them.
3. Lipschitz observable needed for the metric covariance theorem; verify smooth eigenfunction ratios.
4. Strict beta=1/6 endpoint and adversarial integer/bool input rejection.
5. Fail-closed receipt and source metadata; false continuum/Lean assertions must never replay.

---

### Task 1: Exact chordal transfer ratio and analytical proof

**Files:**
- Create: `research/yang_mills_su2/wilson_chordal_mixing.py`
- Create: `research/yang_mills_su2/tests/test_wilson_chordal_mixing.py`
- Create: `research/yang_mills_su2/WILSON_CHORDAL_MIXING.md`
- Modify: `research/yang_mills_su2/WILSON_LATTICE_SPECTRAL_GAP.md`

**Interfaces:**
- Produces: `chordal_spectral_ratio_upper(beta: Fraction)->Fraction`.
- Produces: `chordal_gap_log_lower(beta: Fraction, terms: int)->Fraction`.
- Produces: `chordal_mixing_receipt(beta_num: int,beta_den: int,terms: int)->dict` and strict `replay_chordal_mixing_receipt(receipt: object)->bool`.

- [ ] Write the failing test for `beta=1/10` giving ratio `3/5`, Barta `4/25`, `6/25`, increasing rational log-lower partial sums, and strict beta/forged fields rejection.
- [ ] Run focused test and see missing-module failure.
- [ ] Implement minimal bounded rational module; watch focused test pass.
- [ ] Write and verify full Poincare/Barta/Wasserstein/Gibbs/transfer proof, with prior-art limitations.
- [ ] Commit task-1 proof/module/tests/docs.

### Task 2: Separate PHYSQED evidence and artifact

**Files:**
- Modify: `research/yang_mills_su2/evidence_bridge.py`
- Modify: `research/yang_mills_su2/tests/test_evidence_bridge.py`
- Create: `research/yang_mills_su2/artifacts/wilson_chordal_beta1_over_10.json`

**Interfaces:**
- Consumes: task-1 strict replay.
- Produces: evidence kind `EXACT_WILSON_CHORDAL_LATTICE_RATIO` with bounded scope and source hash.

- [ ] Write failing evidence test for valid record/ledger, source tamper, forged flags and committed artifact.
- [ ] Run and observe failure on absent kind.
- [ ] Implement minimal evidence-kind dispatch and exact committed artifact.
- [ ] Run focus and full Yang--Mills/PHYSQED regression tests.
- [ ] Commit task-2 changes.

### Final gate

- [ ] Independently review the analytic argument, excluding any unexamined sharp-quarter claim.
- [ ] Freshly run all tests on final committed tree and preserve clean isolated worktree.
- [ ] Present a stacked-PR option against the prior lattice-spectral-gap branch.
