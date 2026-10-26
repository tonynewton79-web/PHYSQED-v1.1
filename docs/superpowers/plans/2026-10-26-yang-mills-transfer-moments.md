# Yang--Mills transfer moment obstruction implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce exact, fail-closed evidence showing that nearly identical decaying positive-transfer moments do not force uniform spectral gaps.

**Architecture:** A bounded pure rational module generates and replays moments, Hankel minors and a finite-period transfer fixture. The existing evidence bridge separately verifies and source-hashes the mathematical receipt; documentation maintains the physical/abstract boundary.

**Tech Stack:** Python standard library `Fraction`, `json`, `hashlib`, `unittest`.

**Spec:** `docs/superpowers/specs/2026-10-26-yang-mills-transfer-moments-design.md`

## Global constraints

- All generated certificate arithmetic is rational and exactly replayed; no float approximations.
- Parameter limits: `3<=n<=4096`, `0<=horizon<=32`; reject bool-as-int and false physical claims.
- Exact finite fixture is period four with transfer eigenvalues `1,1/2`.
- General finite-period fixture inputs have period `2..32`, `0<q<1`, and at most 128 bits in either rational component.
- No evidence kind claims Yang--Mills mass gap, continuum existence, Lean formalization, or actual external-solver execution.

## Review focus

- `n=True` or `horizon=False`: reject as invalid inputs.
- Very large or negative indices: reject before exponentiation.
- Forged moment, Hankel minor or physical status: fail closed on replay.
- A wrong determinant exponent (`t+1` instead of `t`): caught by nonzero-`t` hand-derived fixture.
- Mislabeling abstract proof as SU(2) physics: bridge must preserve abstract scope and false physical flags.
- Duplicate raw JSON proof-status keys: reject before the parser can silently overwrite an earlier contradictory value.

---

### Task 1: Exact transfer moments and independent fixture

**Files:** Create `research/yang_mills_su2/transfer_moment_obstructions.py`; test `research/yang_mills_su2/tests/test_transfer_moment_obstructions.py`.

**Interfaces:** `two_mode_moment(n: int, t: int) -> Fraction`; `two_mode_hankel_minor(n: int, t: int) -> Fraction`; `finite_period_two_state_correlator(period: int, q: Fraction) -> tuple[Fraction,...]`; `transfer_moment_receipt(n: int, horizon: int) -> dict`; `replay_transfer_moment_receipt(receipt: object) -> bool`.

- [ ] Write isolated exact tests with literal `n=10` `m(1)=27/50`, `minor(0)=9/625`, `minor(1)=81/12500`, the 4-step finite fixture `(1,10/17,8/17,10/17)`, and strict input/tamper rejection.
- [ ] Run isolated tests and see them fail from missing module or implementation.
- [ ] Implement bounded rational moments and minors, finite-period trace, canonical receipt, and strict replay.
- [ ] Rerun isolated tests until all pass, then run the full Yang--Mills suite.
- [ ] Commit test+module+spec+plan when green.

### Task 2: PHYSQED evidence-bridge integration and scope note

**Files:** Modify `research/yang_mills_su2/evidence_bridge.py`; modify `research/yang_mills_su2/tests/test_evidence_bridge.py`; create `research/yang_mills_su2/TRANSFER_MOMENT_SCOPE.md` and `research/yang_mills_su2/artifacts/abstract_transfer_moments_n10.json`.

**Interfaces:** New evidence kind `EXACT_TRANSFER_MOMENT_OBSTRUCTION` replays a source JSON receipt, hashes the source and exact implementation, and preserves all false physical flags.

- [ ] Write failing evidence-ledger tests for legitimate receipt and source tampering/reclassification.
- [ ] Test contradictory abstract metadata and duplicate raw JSON keys as negative ingress cases.
- [ ] Verify red, then add minimal evidence-bridge branch, scope label and independent hashing.
- [ ] Regenerate exact n=10 receipt as reproducible JSON fixture and replay it; prove the finite and limit statements in the scope note.
- [ ] Run all Yang--Mills and repository PHYSQED tests, verify clean output, inspect diff and commit.
