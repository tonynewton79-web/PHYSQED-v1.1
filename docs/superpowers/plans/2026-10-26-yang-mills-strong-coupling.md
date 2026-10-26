# Finite Wilson Strong-Coupling Certificates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement three rigorously delimited finite Wilson SU(2) estimates and expose exact replay in PHYSQED.

**Architecture:** Small modules distinguish high-temperature covariance, finite product expansions,
and finite-rank transfer spectral cutoff. Each performs exact rational arithmetic with bounded inputs;
the ledger verifies scope and source provenance independently.

**Tech Stack:** Python 3 standard library, existing SymPy-assisted Bessel interval routine, unittest.

**Spec:** `docs/superpowers/specs/2026-10-26-yang-mills-strong-coupling-design.md`

## Global Constraints

- Require all four periodic extents >=2 and impose exact finite request budgets.
- Do not infer a global mass gap, continuum limit or a Lean proof from these checks.
- Every new algorithm must first fail a real test; independently hand-derive fixture values.
- Preserve existing PHYSQED evidence categories and metadata allowlist.

## Review Focus

1. At spatial length 2, shared plaquette incidence multiplicity remains 18, not a distinct-neighbor count.
2. Reject beta exactly `1/18`, negative beta, floats, booleans, oversized numerator/denominator, and oversized lattice.
3. A covariance estimate must remain independent of spatial volume when time separation is fixed.
4. Character/subset bounds must enclose both negative plaquette trace and the product's worst sign.
5. The projected cutoff must use the *normalized* trivial eigenvalue and retain its volume-dependent spatial multiplier.

---

### Task 1: Dobrushin link-influence and temporal covariance

**Files:** Create `research/yang_mills_su2/wilson_dobrushin.py`; test in
`research/yang_mills_su2/tests/test_wilson_dobrushin.py`.

**Interfaces:** `max_wilson_link_incidences(extents)->int`,
`strong_coupling_timeslice_bound(extents,beta: Fraction,lag:int)->Fraction`,
`strong_coupling_receipt(extents,beta_num,beta_den,lag)->dict`,
`replay_strong_coupling_receipt(obj)->bool`.

- [ ] Write tests: 18 incidences on `2^4` and `4x2^3`; beta `1/100`, lag 4 in `8x2^3` gives `13122/640625`; change spatial volume without changing answer; reject `1/18`, types and tampered receipt.
- [ ] Run test module and confirm it fails because these public functions are missing.
- [ ] Implement minimal exact incidence enumeration, rational bound, schema/fingerprint receipt and recomputation on replay.
- [ ] Run the module tests, then full research and PHYSQED suites; commit `feat: certify strong-coupling Wilson temporal decay`.

### Task 2: Character and plaquette subset truncation

**Files:** Create `research/yang_mills_su2/wilson_plaquette_expansion.py`; test in
`research/yang_mills_su2/tests/test_wilson_plaquette_expansion.py`.

**Interfaces:** `wilson_subset_tail(extents,beta:Fraction,max_order:int,exp_terms:int)->Fraction`,
`wilson_plaquette_character_product_tail(extents,beta:Fraction,D:int,exp_terms:int)->Fraction`.

- [ ] Tests: hand-derived single omitted-order value for 96 plaquettes and rational upper exp enclosure, order P gives zero, product bound decreases with higher D, reject unsupported request size.
- [ ] Run RED tests for missing functions.
- [ ] Implement positive rational `exp` bound using existing code or a safe small helper, finite binomial tail, product telescoping bound from `character_tail_upper`.
- [ ] Run GREEN tests, both full suites, commit `feat: bound finite Wilson plaquette expansions`.

### Task 3: Genuine projected-transfer finite-rank spectral error

**Files:** Create `research/yang_mills_su2/wilson_projected_cutoff.py`; test in
`research/yang_mills_su2/tests/test_wilson_projected_cutoff.py`.

**Interfaces:** `normalized_link_spectral_tail(beta:Fraction,D:int,bessel_terms:int,exp_terms:int)->Fraction`,
`projected_transfer_operator_error(spatial_extents:tuple[int,int,int],beta:Fraction,D:int,bessel_terms:int,exp_terms:int)->Fraction`.

- [ ] Tests: finite exact β and D cases, bound <=1 where appropriate, D improvement, dependence on `V` only through explicit spatial multiplication, zero/invalid beta and guard errors.
- [ ] Verify RED before implementation.
- [ ] Implement exact Bessel lower and exponential/factorial upper; normalize by I1, show Markov `r_d<=1` and tensor-product cutoff `||C-C_D||<=eps`; multiply with outward `exp(3beta V)`.
- [ ] Verify GREEN, full suites, commit `feat: bound gauge-projected Wilson spectral cutoff`.

### Task 4: Reproducible PHYSQED integration and reader-facing theorem

**Files:** Modify `research/yang_mills_su2/evidence_bridge.py`, tests,
`research/yang_mills_su2/README.md`; create `research/yang_mills_su2/STRONG_COUPLING_SCOPE.md`
and a small committed receipt under `artifacts/`.

- [ ] Write failing bridge tests accepting one exact strong-coupling receipt and rejecting forged continuum claims, wrong scope, tampering and ambiguous metadata.
- [ ] Verify RED; add one precise evidence class and source-bound implementation hashes; replay without trusting reported numbers.
- [ ] Complete mathematical proof note and explicit comparison with prior strong-coupling theorems; no claim of novelty for classical method.
- [ ] Run both full suites and `git diff --check`; commit `feat: integrate scoped strong-coupling evidence in PHYSQED`.

### Finish

- [ ] Independently review mathematical constants and branch diff; address important findings test-first.
- [ ] Preserve branch/worktree and report next scaling obstruction. Any remote push or PR is a separate integration decision.
