# 4D SU(2) Wilson Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Build a reproducible small-volume, four-dimensional SU(2) Wilson-lattice simulation with gauge-invariant measurements and no unsupported physical mass-gap claims.

**Architecture:** Use pure-Python SU(2) unit-quaternion operations, periodic 4D lattice geometry, and a symmetric local Metropolis proposal. Independent seeded chains provide plaquette and time-slice connected-correlation diagnostics; no inference beyond finite samples is made.

**Tech Stack:** Python 3.11+, standard library, unittest. No new runtime dependency in the pilot.

**Spec:** docs/superpowers/specs/2026-10-25-yang-mills-three-track-design.md

## Global Constraints

- Work on an isolated branch derived from the approved design branch, not main.
- Pure SU(2) Wilson theory on a finite 4D periodic lattice; no quarks or gravity coupling.
- Record beta, extents, seeds, proposal scale, warmup, sample spacing and chain count.
- Mark all outputs FINITE_LATTICE_NUMERICAL; never mark them continuum/Lean/Clay verified.
- Preserve all pre-existing PHYSQED modules and tests.

## Review Focus

1. Zero-norm or non-unit quaternion input must be rejected by validation tests in Task 1.
2. Periodic wraparound and inverted link orientation must be tested in Task 2.
3. Nonconstant site-wise gauge transforms must leave Wilson action unchanged in Task 2.
4. Re-running a fixed seed must yield byte-identical JSON samples in Task 3.
5. Very short time extent, invalid beta/epsilon and insufficient chains must receive explicit errors in Task 3.

---

## Files and interfaces

- Create research/yang_mills_su2/__init__.py: research package.
- Create research/yang_mills_su2/su2.py: SU(2) quaternion algebra and validation.
- Create research/yang_mills_su2/lattice.py: finite periodic 4D geometry, plaquettes, action and gauge transformation.
- Create research/yang_mills_su2/simulation.py: Metropolis and measurements.
- Create research/yang_mills_su2/run_pilot.py: deterministic CLI and JSON evidence.
- Create research/yang_mills_su2/tests/test_su2.py, test_lattice.py, test_simulation.py.
- Create research/yang_mills_su2/README.md with scope, fixed run command and interpretation limits.

### Task 1: Quaternion SU(2) algebra

**Files:** su2.py, __init__.py, tests/test_su2.py.

**Interfaces:** Define Quaternion as a tuple[float,float,float,float]. Provide mul(q,p)->Quaternion; dagger(q)->Quaternion; norm2(q)->float; normalized(q)->Quaternion (reject zero/nonfinite); scalar_trace(q)->float returning 2*q[0]; axis_angle(axis,theta)->Quaternion (normalize nonzero 3-axis).

- [ ] Step 1: Write unittest cases for mul(identity,q)=q, mul(q,dagger(q))=(norm2(q),0,0,0) within 1e-12, axis_angle unit norm, invalid zero/nonfinite input rejection.
- [ ] Step 2: Run python -m unittest research.yang_mills_su2.tests.test_su2 -v; expect import/test failure.
- [ ] Step 3: Implement Hamilton quaternion multiplication and functions above; reject nonfinite values and invalid shapes.
- [ ] Step 4: Run the focused test; expect all PASS.
- [ ] Step 5: Commit su2.py and its tests.

### Task 2: Periodic 4D Wilson action

**Files:** lattice.py and tests/test_lattice.py.

**Interfaces:** class Lattice4D(extents: tuple[int,int,int,int], links: dict[tuple[tuple[int,int,int,int],int],Quaternion]|None=None); methods shifted(x,mu,step=1), link(x,mu), plaquette(x,mu,nu), wilson_action(beta:float)->float, gauge_transformed(site_gauge:dict[site,Quaternion])->Lattice4D. All unit links initially identity. Include a no-mutation set_link(...)->None for Metropolis.

- [ ] Step 1: Test identity lattice action=0, 6 plaquettes per lattice site, wraparound shift, reversed orientation via dagger, and action invariance under nonconstant deterministic gauge rotations.
- [ ] Step 2: Run test_lattice; expect failures before implementation.
- [ ] Step 3: Implement the ordered product U(x,mu) U(x+mu,nu) U(x+nu,mu)^dagger U(x,nu)^dagger and action beta*sum_p(1-ReTr(U_p)/2), with one count per unordered mu<nu pair.
- [ ] Step 4: Run test_lattice and test_su2; expect PASS.
- [ ] Step 5: Commit lattice.py and tests.

### Task 3: Reproducible finite simulation and connected diagnostics

**Files:** simulation.py, run_pilot.py, README.md, tests/test_simulation.py.

**Interfaces:** metropolis_sweep(lattice:Lattice4D,beta:float,epsilon:float,rng:random.Random)->tuple[int,int]; timeslice_plaquette(lattice)->tuple[float,...]; connected_timeslice(samples:list[tuple[float,...]])->tuple[float,...]; run_chains(extents,beta,seeds,warmup,sweeps,thin,epsilon)->dict; cli main(argv:list[str]|None=None)->int.

- [ ] Step 1: Test beta=0 accepts every well-formed proposal; fixed seed repeat produces identical result; outputs label numerical finite only; a nontrivial time slice and correlation have expected dimension N_t; reject beta<0, epsilon<=0 or >pi, extents<2, empty/duplicate seeds, sweeps<=0, thin<=0 and fewer than two independent chains for uncertainty.
- [ ] Step 2: Run test_simulation; expect missing implementation failure.
- [ ] Step 3: Implement a symmetric random-axis, uniform signed-angle proposal multiplied onto each link; accept using min(1,exp(-DeltaS)). Use the full action for pilot ΔS to favor simple independent correctness; sample after warmup/thinning. Use spatial plaquettes averaged per time slice for a gauge-invariant diagnostic.
- [ ] Step 4: Aggregate independent chain sample means and standard error; write canonical deterministic sorted-key JSON with declared parameters, convergence caveat, and numerical evidence status; never derive a physical continuum gap from the correlator.
- [ ] Step 5: Run all three pilot test files and two CLI calls with identical args; assert byte-identical result; inspect beta=0 and a small positive-beta case.
- [ ] Step 6: Commit simulator, CLI, README and tests.

## Completion gate

- [ ] All focused unittest suites pass and one fixed-seed CLI record is reproducible.
- [ ] Gauge invariance is tested with nonconstant site transformations.
- [ ] Any Monte Carlo estimates are explicitly finite-cutoff diagnostics with independent chain uncertainty, not continuum physics certificates.
