# Wilson Strong-Coupling Lattice Spectral Gap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Derive, document and exactly replay a spatial-volume-uniform normalized Wilson SU(2) transfer spectral bound for `0 < beta < 1/18`.

**Architecture:** A mathematical theorem note connects the current arbitrary-observable Dobrushin covariance comparison to the genuine positive transfer operator. A narrow standard-library rational module and PHYSQED bridge certify only the exact arithmetic consequences.

**Tech Stack:** Python 3 standard library `fractions.Fraction`, `unittest`, Markdown, existing PHYSQED provenance machinery.

**Spec:** `docs/superpowers/specs/2026-10-26-wilson-lattice-spectral-gap-design.md`

## Global Constraints

- Positive rational `beta` strictly below `1/18`; never report a continuum mass gap.
- No numerical simulation or third-party eigensolver required.
- Never present arithmetic replay as a formalized proof of the analytic hypotheses.

## Review Focus

1. `beta=0` or `beta=1/18`: rejected rather than silently dividing by zero.
2. Boolean integers masquerading as denominators or term counts: rejected.
3. Rational logarithm lower enclosure: must not exceed the true logarithm.
4. Tampered ratio, gap, or continuum flags: replay fails closed.
5. New evidence kind with misleading physical/Lean metadata: rejected.

---

### Task 1: Spectral ratio arithmetic and theorem note

**Files:**
- Create: `research/yang_mills_su2/wilson_spectral_gap.py`
- Create: `research/yang_mills_su2/tests/test_wilson_spectral_gap.py`
- Create: `research/yang_mills_su2/WILSON_LATTICE_SPECTRAL_GAP.md`
- Modify: `research/yang_mills_su2/STRONG_COUPLING_SCOPE.md`

**Interfaces:**
- Produces: `lattice_spectral_gap_receipt(beta_num: int, beta_den: int, log_terms: int) -> dict`.
- Produces: `replay_lattice_spectral_gap_receipt(obj: object) -> bool`.

- [ ] Write failing regression tests for the exact bound `q=9/50` at `beta=1/100`, a finite atanh lower sum, strict type/coupling rejection, and tamper rejection.
- [ ] Execute `python -m unittest research.yang_mills_su2.tests.test_wilson_spectral_gap -v`, see the intended missing-interface failure.
- [ ] Implement the minimal rational arithmetic/replay interface with a strict fixed schema and bounded input sizes.
- [ ] Run that test again to see all green.
- [ ] Write the full derivation, including the Perron eigenfunction ratio argument and explicit non-continuum scope; link from strong-coupling note.
- [ ] Commit the task's tests, module, and mathematical note.

### Task 2: PHYSQED evidence bridge

**Files:**
- Modify: `research/yang_mills_su2/evidence_bridge.py`
- Modify: `research/yang_mills_su2/tests/test_evidence_bridge.py`
- Create: `research/yang_mills_su2/artifacts/wilson_lattice_spectral_gap_beta1_over_100.json`

**Interfaces:**
- Consumes: the task-1 `lattice_spectral_gap_receipt` and replay interface.
- Produces: strict evidence type `EXACT_WILSON_LATTICE_SPECTRAL_RATIO`, with source hashing and denied continuum/Lean claims.

- [ ] Write failing evidence tests for an accepted exact receipt, source change detection, forged physical metadata rejection, and committed-artifact replay.
- [ ] Run `python -m unittest research.yang_mills_su2.tests.test_evidence_bridge -v`, observe the expected missing-kind failure.
- [ ] Extend known kinds, metadata allowlist, receipt dispatch, and implementation hashes; write the exact artifact.
- [ ] Run evidence tests and both complete Yang--Mills/PHYSQED test suites.
- [ ] Commit only the task-2 changes.

### Completion

- [ ] Verify a clean diff against the strong-coupling parent and run both suites freshly.
- [ ] Independently inspect the proof; mark published strong-coupling prior art.
- [ ] Keep local branch isolated pending publication decision.
