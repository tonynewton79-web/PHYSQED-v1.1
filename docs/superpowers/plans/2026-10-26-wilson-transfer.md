# Wilson SU(2) finite-coupling transfer implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Certify the finite-beta Wilson temporal-link character kernel and independently validate the genuine 4D Wilson transfer-slab action decomposition.

**Architecture:** One bounded pure-rational character module with replayable receipt, one physical float-quaternion slab module based on existing Lattice4D, and one separate abstract-versus-physical classification in the PHYSQED evidence bridge.

**Tech Stack:** Python 3 standard library; SymPy used only by independent tests; existing Wilson simulator/PHYSQED evidence bridge.

**Spec:** `docs/superpowers/specs/2026-10-26-wilson-transfer-design.md`

## Global constraints

- Positive rational beta at most 4, with numerator/denominator at most 16 bits; D in [2,16], Bessel and exponential series terms in [1,32]; fail before expensive computations.
- All kernel certificates and replay calculations use `fractions.Fraction`, not float approximations.
- Wilson slab checks use existing 4D float quaternions, explicitly approximate, and never claim equilibrated finite-beta expectations.
- No continuum, uniform physical mass-gap, or Lean-kernel claim. External Newton/EINSTEIN-X code remains unexecuted.

## Review focus

- A missing dimension factor `d` in character coefficients or convolution eigenvalues: independent SU2 Fourier tests.
- Wrong tail-ratio index or missing character amplitude `d`: independent exponential inclusion check at trace -1,0,1.
- A reversed/omitted temporal plaquette or doubled spatial cap: periodic Wilson-action equality and gauge-transformed repeat.
- An accidental equal-time use of the beta-zero cross-slice independence premise: reject time lag zero in the rational correlator bound.
- Bad integer/bool/rational inputs and resource bombs: fail-closed tests.
- Forged exact intervals, ambiguous JSON and physically misleading ledger metadata: source replay and ledger tests.
- Legacy PHYSQED-polynomial/character evidence with free-form `"mass gap proven"` metadata: reject, while preserving supported beta-zero negative-control provenance.

---

### Task 1: Exact rational character expansion bounds

**Files:** Create `research/yang_mills_su2/wilson_transfer_characters.py` and `research/yang_mills_su2/tests/test_wilson_transfer_characters.py`.

**Interfaces:** `character_tail_upper(beta: Fraction, D: int, exp_terms: int) -> Fraction`; `wilson_character_kernel_interval(beta: Fraction, D: int, bessel_terms: int, exp_terms: int, x: Fraction) -> tuple[Fraction,Fraction]`; `wilson_transfer_receipt(beta_num: int, beta_den: int, D: int, bessel_terms: int, exp_terms: int) -> dict`; `replay_wilson_transfer_receipt(receipt: object) -> bool`.

- [ ] Test exact coefficient and tail identities with hand-derived rational values; compare kernel enclosure against independent SymPy `exp(beta*x)` at x=-1,0,1/2,1.
- [ ] Confirm focused tests fail because the new feature is absent.
- [ ] Implement bounded rational character series, Taylor tail bound, kernel enclosure, strict receipt replay.
- [ ] Run focused and full Yang-Mills tests; commit.

### Task 2: Four-dimensional Wilson transfer-slab consistency

**Files:** Create `research/yang_mills_su2/wilson_transfer_slabs.py` and `research/yang_mills_su2/tests/test_wilson_transfer_slabs.py`.

**Interfaces:** `wilson_slab_log_weights(lattice: Lattice4D, beta: float) -> tuple[float,...]`; `wilson_temporal_kernel_log(lattice: Lattice4D, beta: float, time: int) -> float`.

- [ ] Write tests for all-identity links, seeded Haar links, exact action balance and per-slab gauge invariance under random local transformations.
- [ ] Compare the explicit `U_e h_y V_e^-1 h_x^-1` kernel sum with the separate temporal Wilson plaquette implementation at each time and after gauge transforms.
- [ ] Verify red, implement using existing plaquette routines and time decomposition, then verify green.
- [ ] Document why positive-beta sampled correlators are not certified transfer expectations; commit.

### Task 3: PHYSQED evidence and scientific scope

**Files:** Modify `research/yang_mills_su2/evidence_bridge.py` and its tests; create `research/yang_mills_su2/WILSON_TRANSFER_SCOPE.md` and `artifacts/wilson_transfer_beta2_exact.json`.

**Interfaces:** New evidence kind `EXACT_WILSON_TRANSFER_CHARACTER` strictly replays exact receipt and preserves false continuum flags. No claim that the PHYSQED polynomial engine verifies the operator-theoretic construction.

- [ ] Write failing tamper/metadata classification tests, including the committed source.
- [ ] Add exact ledger replay, bounded source/implementation hashing, and fixture.
- [ ] Add operator derivation, tail proof and explicit volume-dependence obstruction in scientific note.
- [ ] Run 4D/PHYSQED suites, inspect diff, request independent review, commit.

### Task 4: Unconditional finite-volume correlation continuity

**Files:** Create `research/yang_mills_su2/wilson_correlator_bounds.py` and `research/yang_mills_su2/tests/test_wilson_correlator_bounds.py`.

**Interface:** `finite_beta_spatial_correlator_bound(extents: tuple[int,int,int,int], beta: Fraction, time_lag: int) -> Fraction`.

- [ ] Test the hand-derived `(4,2,2,2)`, `beta=1/1000` bound `3576/15625`, volume deterioration, and invalid zero-lag inputs.
- [ ] Verify red, then implement finite Wilson Gibbs derivative/variance bound and verify green.
- [ ] Integrate the precise proof, scope and limitations into `WILSON_TRANSFER_SCOPE.md`; include in complete regression/review.
