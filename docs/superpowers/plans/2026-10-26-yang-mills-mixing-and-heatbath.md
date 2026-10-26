# Yang–Mills Exact Mixing and Heatbath Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Certify the finite β=0 SU(2) Markov kernel exactly and add an independently tested finite Wilson heatbath plus honest time-correlator diagnostics.

**Architecture:** The β=0 certificate depends only on exact SU(2) representation coefficients and rational tail bounds. Heatbath sampling uses the existing full-action and six-plaquette oracles; finite correlators are an independent consumer. Each component has separate false physical-proof flags and tests.

**Tech Stack:** Python 3.12 standard library, Fraction, unittest, existing SU(2) quaternion/lattice modules and exact character-ratio bounds.

**Spec:** `docs/superpowers/specs/2026-10-26-yang-mills-mixing-and-heatbath-design.md`

## Global Constraints

- Existing historical artifacts, PHYSQED v1.1 source, and Wilson-action baseline remain unchanged.
- Never claim equilibrium from short Markov chains, or a physical continuum mass gap from a finite link-update spectrum.
- No external mathematical packages in production modules; independent SymPy testing remains optional.
- Work only on `feat/yang-mills-mixing-heatbath-20261026`; no merge or push without a separate decision.

## Review Focus

1. A link in backward-oriented plaquettes must have the correct sign in h·q: include a random nontrivial μ=3 regression.
2. Temporary basis substitution must restore the original link even if plaquette evaluation raises: use a monkeypatched exception test.
3. κ≈0 and κ≫1 sampler acceptance must be finite and legitimate: test β=0, small β, and κ≈48 separately.
4. Extreme terms/volumes in rational products must reject before huge integer construction: test invalid bounds.
5. A time-correlator fit with C(t)≤0 or arccosh argument<1 must refuse an effective mass, not return an apparently physical number.

---

### Task 1: Rational SU(2) β=0 mixing certificate

**Files:** Create `research/yang_mills_su2/mixing_certificates.py`, `research/yang_mills_su2/tests/test_mixing_certificates.py`.

**Interfaces:** `beta_zero_rep_eigenvalue(spin_twice:int)->Fraction`; `cold_l2_squared_bounds(sweeps:int, links:int, terms:int)->tuple[Fraction,Fraction]`; `mixing_receipt(sweeps:int,links:int,terms:int)->dict`.

- [ ] Write failing tests that spin_twice=(0,1,2,3,4) gives (1,0,1/3,0,1/5), and at n=2/one link the lower bound is positive and the upper bound finite. Test monotonic interval contraction, invalid n=1, overlarge resource inputs, false physical flags, and exact adjoint plaquette 1/81 after one cold β=0, ε=π sweep.
- [ ] Run `python -m unittest research.yang_mills_su2.tests.test_mixing_certificates -v`; confirm failures are missing module/function.
- [ ] Implement exact Fraction eigenvalues and first J terms of Σ odd d^-p plus integral tail; raise integer-power bounds to links and serialize bounded rational certificates. Explain the external Peter–Weyl identity.
- [ ] Re-run targeted tests; run the existing SU(2) unit suite.
- [ ] Commit task with message `feat: certify exact beta-zero SU2 proposal mixing`.

### Task 2: Independently audited one-link SU(2) heatbath

**Files:** Create `research/yang_mills_su2/heatbath.py`, `research/yang_mills_su2/tests/test_heatbath.py`.

**Interfaces:** `staple_linear_coefficients(lat,site,mu)->Quaternion`; `sample_heatbath_link(coeff:Quaternion,beta:float,rng:Random)->Quaternion`; `heatbath_sweep(lat,beta:float,rng:Random)->int`.

- [ ] Write failing tests for h·q matching independently summed six plaquette traces and whole-action ΔS for μ=0..3 on nontrivial 2⁴ and (4,2,2,2) configurations. Assert original link restored after normal/exceptional evaluations. Add deterministic-seed β=0 Haar, κ=2 sample alignment against external character-ratio interval, high concentration finite unit norm and invalid input checks.
- [ ] Run `python -m unittest research.yang_mills_su2.tests.test_heatbath -v`; confirm missing implementation.
- [ ] Implement four basis substitutions, stable inverse-CDF truncated exponential with sqrt(1−t²) rejection, uniform axis, quaternion orientation and deterministic site/link sweep; maintain original Metropolis kernel untouched.
- [ ] Re-run targeted tests, targeted prior local-action tests, and the entire SU(2) suite.
- [ ] Commit task with message `feat: add independently checked Wilson SU2 heatbath`.

### Task 3: Gauge-invariant finite time-correlator diagnostics

**Files:** Create `research/yang_mills_su2/transfer_diagnostics.py`, `research/yang_mills_su2/tests/test_transfer_diagnostics.py`; create `research/yang_mills_su2/MIXING_HEATBATH_SCOPE.md`.

**Interfaces:** `cosh_effective_mass(correlator:tuple[float,...],time:int)->float|None`; `run_heatbath_timeslices(extents:tuple[int,int,int,int],beta:float,seeds:tuple[int,...],warmup:int,sweeps:int,thin:int)->dict`.

- [ ] Write failing tests for cosh periodic synthetic data with mass log 2, refusal of negative/noisy invalid correlators, minimum temporal extent 4 and resource limits, determinism, raw gauge-invariant timeslices, false equilibrium/physical/Lean flags, and no mass value when conditions fail.
- [ ] Run `python -m unittest research.yang_mills_su2.tests.test_transfer_diagnostics -v`; confirm missing implementation.
- [ ] Implement seeded cold/Haar chains with heatbath sweeps, per-time plaquette samples, connected finite correlator and folded values, cautious cosh diagnostic and explicit limitations; write scope note with mixing and Bessel-mean proofs.
- [ ] Re-run targeted and full Yang–Mills + PHYSQED unit suites and old exact receipt replay.
- [ ] Commit task with message `feat: report gauge-invariant heatbath time correlators`.

### Task 4: Whole-branch verification and evidence handoff

**Files:** No historical files overwritten.

- [ ] Run all 3 focused test modules, full 4D SU(2) tests, 237 baseline PHYSQED tests, and old deterministic receipt validators.
- [ ] Generate one ephemeral finite diagnostic on (4,2,2,2), β=1/2 with seeded warmup/sweeps, review actual correlator and false status fields. Do not select a positive effective mass from noisy results post hoc.
- [ ] Verify branch diff excludes H8/Navier–Stokes and excludes altered original evidence receipts. Check source hashes if recording new reports.
- [ ] Request independent branch review, fix material issues with a failing regression test first; present source changes and scientific limitations.
