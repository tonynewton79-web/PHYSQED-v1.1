# Yang–Mills Three-Track Programme — Design Proposal

**Date:** 25 October 2026  
**Owner:** Tony Newton / Newton Astro Labs  
**Status:** PROPOSED — awaiting approval; not an implementation plan or a claim of a solution  
**Proposed home:** a research branch of PHYSQED-v1.1, with isolated experimental modules and no changes to its established certification semantics.

## 1. Purpose

Investigate the four-dimensional pure Yang–Mills existence and mass-gap problem using three coordinated but epistemically separate tracks:

1. a physically interpretable four-dimensional lattice gauge model and reproducible computational measurements;
2. Newton Solver and EINSTEIN-X Ω to search for exact estimates, counterexamples, and a rigorous continuum argument;
3. PHYSQED to check every claim within its supported formal domain, to register unresolved mathematical/physical assumptions, and to require independent replay.

Success in the first milestone means a reproducible **finite-model baseline and proof-obligation ledger**, not a solution to the Clay problem. The ultimate target is a nontrivial quantum Yang–Mills theory on four-dimensional spacetime with a positive physical spectral gap, initially for SU(2), ultimately for any compact simple gauge group.

## 2. Approaches and selected integration

- **Simulation alone** supplies spectra, scaling evidence, and physical intuition comparatively quickly but cannot prove the existence of a continuum quantum field theory.
- **Abstract theorem search alone** may isolate a decisive uniform inequality but lacks numerical falsification and reliable normalization diagnostics.
- **An integrated three-track programme (selected by Tony)** tests physically motivated conjectures and certifies precisely scoped mathematical consequences, with simulation and independent adversarial review. This has the strongest audit trail, at the cost of more engineering and explicit open proof obligations.

The tracks are coordinated sequentially: a finite exact benchmark calibrates the model, numerical experiments guide conjectures, and the mathematical programme attempts estimates uniform in the relevant limits. Formal gates never inherit a stronger status from numerical agreement.

## 3. Mathematical and physical model

Start with pure SU(2) lattice gauge theory on a finite four-dimensional Euclidean hypercubic lattice of spacing a and spatial/temporal extents N_s, N_t. Each oriented link e carries U_e in SU(2). For an oriented plaquette p, U_p is the ordered link product; a consistent convention for reversed links uses U_{e^{-1}}=U_e^\dagger. Adopt the Wilson action

S_beta(U) = beta * sum_p [1 - (1/2) Re Tr(U_p)],

and finite normalized expectations under product Haar measure with density proportional to exp(-S_beta). Record beta, boundary conditions, gauge group, lattice spacing convention, and all normalization choices in each result.

Physical observables must be gauge invariant. Use connected correlators of a documented basis of plaquette/loop operators and, when suitable, a variational correlation matrix for several quantum-number channels. A single scalar-glueball channel cannot establish a gap for the entire physical Hilbert space.

As a finite diagnostic, independently rederive and numerically replay the known SU(2) character ratio c(beta)=I_2(beta)/I_1(beta), its positive logarithmic gap g(beta)=-log c(beta), and beta*g(beta)->3/2. Treat this as a character-model check, **not** an automatic statement about the complete 4D transfer-matrix spectrum.

For a reflection-positive lattice transfer matrix T_{a,L} acting on the relevant physical gauge-invariant space, define the dimensionless gap delta_{a,L}=-log(lambda_1/lambda_0), where lambda_0 and lambda_1 are the vacuum and next physical eigenvalues when well defined. The proposed noncollapse proof target is a positive lower bound for delta_{a,L}/a along an explicitly fixed infinite-volume/continuum limiting procedure. Establishing such a bound without the other axiomatic properties remains insufficient for Clay's full problem.

## 4. Three workstreams

### A. Physical simulation

- Implement a reproducible, versioned four-dimensional SU(2) Wilson-lattice baseline once design approval is received.
- Verify group closure/unitarity, Haar/update invariance, local gauge invariance, plaquette orientation, and finite-volume normalization using independent deterministic tests.
- Introduce a documented Monte Carlo update, thermalization/autocorrelation controls, independent seeds, and resampling uncertainty; cross-check against trusted lattice literature where feasible.
- Measure Wilson loops and gauge-invariant connected correlators. Keep raw measurements, random seeds, uncertainties, operator definitions, and scaling assumptions.
- Distinguish lattice units from physical units; never infer a continuum gap from a finite fitted mass or plateau.

### B. Mathematical discovery and proof search

- Use Newton Solver to discover identities, character expansions, interval bounds, transfer-matrix inequalities, and candidate decay estimates.
- Use EINSTEIN-X Ω as an independent physics/symmetry reviewer and counterexample search engine; verify gauge covariance/invariance, reflection positivity assumptions, limits, and spectral interpretations.
- Seek cutoff- and volume-uniform controls on *the appropriate family* of renormalized gauge-invariant Schwinger functions, together with reflection positivity, continuum limits, clustering, uniqueness of vacuum, nontriviality, and the correct short-distance behavior.
- Maintain a dependency graph stating which result is finite, conditional, numerical, exact, analytic, or formally kernel-checked. Classify false conjectures explicitly.
- After an SU(2) result, investigate extension to all compact simple G; do not assume that replacing Casimir constants automatically establishes this step.

### C. PHYSQED certification

- Preserve the v1.1 engine's exact algebraic domain and refusal semantics. Its existing multi-premise rational-polynomial checker is not a proof of gauge-theory existence.
- Issue versioned claim contracts tying each local identity/inequality to exact definitions, units, hypotheses, data sources, proof artifacts, and independently reproducible verification.
- Extend verification only through separately tested modules: exact character/representation algebra first, then certified numerical enclosures and carefully scoped operator inequalities. Any Lean status requires actual pinned toolchain compilation and an exact theorem/claim alignment.
- Independent oracles must check material identities without simply calling the same code path. Simulations, formal theorems, and physical predictions receive distinct evidence labels.
- No certificate may claim a Yang–Mills mass-gap solution until all global analytic and axiomatic obligations are discharged and externally scrutinized.

## 5. Deliverables and first milestone

1. **Model contract:** action, gauge group, lattice geometry, boundary conditions, observable family, dimensions, transfer-matrix conventions.
2. **Exact calibration:** independent Bessel-character asymptotics/positivity checks and a counterexample showing finite positive gaps need not survive limits.
3. **Reproducible pilot:** small-volume SU(2) 4D Wilson data with uncertainty and gauge-invariance/algorithm checks; no fitted quantity promoted into a theorem.
4. **Research ledger:** explicitly indexed global proof obligations, candidate inequalities, counterexamples, dependency statuses, provenance, and a novelty comparison.
5. **PHYSQED extension proposal and tests:** narrow claim contracts and replay receipts before any new verifier semantics are activated.
6. **Cumulative scholarly report:** only defensible mathematical contributions and physics results; theorem statements early, notation defined, proofs complete, limitations stated without internal research-diary language.

Acceptance for milestone 1: independent algebra checks agree; gauge-invariance and normalization tests pass; simulation is repeatable with disclosed seeds/uncertainty; the missing continuum proof obligations are stated; PHYSQED makes no unsupported proof claim.

## 6. Boundaries, dependencies, and release gates

The first milestone is a testable research instrument, not an announced Clay solution, an empirical discovery of glueballs, or a coupling of Yang–Mills to dynamical Einstein gravity. Adding gravity or quarks would change the target theory and requires a separately identified model.

The current public PHYSQED-v1.1 repository is accessible. Historical descriptions identify Newton Solver and EINSTEIN-X Ω v2.5 integrated archives, but their complete executable sources have not been located in the current workspace or this public repository. Before claiming those engines were actually run, obtain their exact source archives/commits and verify independent baseline tests; otherwise mark the corresponding adapter/review steps **not executed**.

Protect PHYSQED main with a separate feature branch and targeted tests/CI. Publication requires (i) independently audited novelty and priority, (ii) complete and independently checked proofs for each claimed theorem, (iii) readable manuscript and layout review. Reserve the phrase “solution of the Yang–Mills existence and mass-gap problem” for a complete proof of the stated continuum/axiomatic problem with external assessment.

**Approval requested:** proceed to an executable work plan and implementation of the first calibrated, 4D SU(2) integrated pilot, retaining the full theorem programme as an explicit longer-term track.
