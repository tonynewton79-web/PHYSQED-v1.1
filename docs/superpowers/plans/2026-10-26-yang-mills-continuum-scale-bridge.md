# Yang--Mills Continuum-Scale Bridge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add exact, fail-closed arithmetic checks for a conditional two-sided physical-scale transfer window and mathematically informative countermodels.

**Architecture:** A standard-library rational module handles a conditional block-transfer theorem, safe logarithmic enclosures, and three diagonal-transfer families. Focused unittest checks cover exactness and falsification; a distinct PHYSQED evidence-bridge category identifies the finite *arithmetic* scope. A research note supplies mathematical proofs and continuum limitations.

**Tech Stack:** Python 3, `fractions.Fraction`, unittest, JSON, SHA-256, Git.

**Spec:** `docs/superpowers/specs/2026-10-26-yang-mills-continuum-scale-bridge-design.md`

## Global Constraints

- No four-dimensional continuum existence or physical mass-gap claim.
- No Newton Solver or EINSTEIN-X Omega execution claim without source.
- Never accept supplied `verified=True` or other physical promotion flags.
- Assume only a finite positive self-adjoint normalized transfer and explicit block hypotheses.
- Existing Python and PHYSQED tests must remain compatible.

## Review Focus

1. A forged positive correlator cannot certify a Wilson transfer spectrum.
2. False, float, bool, or oversized rational inputs must reject fail-closed.
3. The physical upper *mass* bound must use a correlator *lower* witness, not a reversed inequality.
4. A fixed lattice ratio below one drives physical mass to infinity as `a -> 0`.
5. Evidence replay must reject altered proof-status flags and receipt content.

---

### Task 1: Conditional exact scale window and abstract model

**Files:** Create `research/yang_mills_su2/continuum_scale_bridge.py`, `research/yang_mills_su2/tests/test_continuum_scale_bridge.py`.

**Interfaces:**
- `physical_block_window(spacing: Fraction, steps: int, upper_block: Fraction, correlator_lower: Fraction, variance_upper: Fraction, terms: int) -> dict`
- `diagonal_transfer_family(family: str, n: int, terms: int) -> dict`
- `scale_bridge_receipt(family: str, n: int, terms: int) -> dict`
- `replay_scale_bridge_receipt(obj: object) -> bool`

- [ ] Write tests for the exact two-sided bounds, three spectral families, endpoint rejection and tamper rejection.
- [ ] Run tests and confirm missing-module failure.
- [ ] Implement bounded fraction arithmetic and atanh log lower/upper intervals.
- [ ] Run focused tests to pass, and rerun them after any refactor.
- [ ] Commit the tested mathematical module and tests.

### Task 2: PHYSQED evidence firewall

**Files:** Modify `research/yang_mills_su2/evidence_bridge.py`, `research/yang_mills_su2/tests/test_evidence_bridge.py`.

**Interfaces:** Add `EXACT_ABSTRACT_PHYSICAL_SCALE_BRIDGE` for the generated abstract diagonal-transfer receipt only; it always denies continuum and physical-law claims.

- [ ] Add a failing integration and forged-metadata regression test.
- [ ] Implement the allowlisted evidence kind, exact replay, and implementation-source hash.
- [ ] Run bridge and integration tests; verify altered evidence is rejected.
- [ ] Commit the integration.

### Task 3: Proof note and final verification

**Files:** Create `research/yang_mills_su2/CONTINUUM_SCALE_BRIDGE.md`, an exact example under `artifacts/`; update research README.

**Interfaces:** Full elementary proof, exact reproduction commands and explicit open weak-coupling/continuum obligations.

- [ ] Write proof and case classification; distinguish spectral necessity from field-theory sufficiency.
- [ ] Generate a sample receipt using the committed module, replay it and trace to the evidence ledger.
- [ ] Run full Yang--Mills and PHYSQED test suites and `git diff --check`.
- [ ] Check isolated branch status, commit, then prepare a stacked PR without merging.
