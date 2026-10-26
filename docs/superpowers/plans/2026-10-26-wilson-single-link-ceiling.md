# Wilson Single-Link Ceiling and Updated Paper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove and test an explicit 18-neighbor obstruction to a global single-link Dobrushin contraction, and integrate it alongside the physical-block bridge into the cumulative Wilson SU(2) paper.

**Architecture:** An exact four-dimensional incidence builder identifies a sign-staple environment; independent quaternion perturbation tests check that all 18 neighbors give unit parameter response. A bounded exact rational receipt enters a distinct PHYSQED evidence category. A compact mathematical section is inserted into the existing TeX source and rebuilt PDF.

**Tech Stack:** Python 3 standard library, unittest, existing SU2 lattice module, LaTeX/AMS, pdfLaTeX, Poppler, Git.

**Spec:** `docs/superpowers/specs/2026-10-26-wilson-single-link-ceiling-design.md`

## Global Constraints

- The `2/9` value is a **method ceiling**, not a physical mass-gap claim.
- Prove only for dimension-four periodic lattices with extents >=3 in this construction.
- No unverified sharp `1/4` *global upper* Wasserstein assertion.
- Cite earlier unrefereed work for ceiling priority and avoid a novelty claim.
- Preserve the previous 8-section manuscript source and produce a nine-section cumulative revision.

## Review Focus

1. Opposite-sign staple choices must be geometrically independent.
2. Every 4D link must have exactly 18 *distinct* neighboring links at extents >=3.
3. A `1/4` necessary local slope does not prove a global `1/4` upper bound.
4. Side-length-two aliasing must be excluded, not silently accepted.
5. Tampered geometry and physical-proof metadata must be rejected by replay.

---

### Task 1: Exact Wilson local ceiling witness

**Files:** `research/yang_mills_su2/wilson_dobrushin_ceiling.py`, `research/yang_mills_su2/tests/test_wilson_dobrushin_ceiling.py`.

**Interfaces:** `local_ceiling_witness(extents: tuple[int,int,int,int]) -> dict`, `ceiling_row_lower(beta: Fraction) -> Fraction`, `ceiling_receipt(beta_num:int,beta_den:int)->dict`, `replay_ceiling_receipt(obj)->bool`.

- [ ] Test geometry, six signed staples, all 18 independent neighbor responses, exact coefficient and strict rejection.
- [ ] Run test and see missing function/module error.
- [ ] Implement minimal source with bounded deterministic receipt, exact rational arithmetic and no physical promotion.
- [ ] Run focused suite, code review, commit.

### Task 2: Evidence integration

**Files:** `research/yang_mills_su2/evidence_bridge.py`, `research/yang_mills_su2/tests/test_evidence_bridge.py`, artifact JSON.

- [ ] Write failing test for allowlisted new kind and tamper rejection.
- [ ] Implement source-hash-bound exact replay with noncontinuum scope.
- [ ] Run focused evidence tests; commit.

### Task 3: Revised cumulative paper

**Files:** `research/yang_mills_su2/paper/Yang_Mills_Proof_Carrying_Wilson_SU2.tex` and `.pdf`; scope note/README.

- [ ] Prove local ceiling, distinguish necessary slope vs unverified global sharp upper, and integrate the two-sided physical-block criterion.
- [ ] Rebuild PDF twice, check logs, render and visually review each page.
- [ ] Run full YM/PHYSQED regression suites and `git diff --check`.
- [ ] Commit, verify remote tree identity, create stacked draft PR without merge.
