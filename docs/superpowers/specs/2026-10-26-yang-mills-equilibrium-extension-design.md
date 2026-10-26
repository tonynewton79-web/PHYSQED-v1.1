# Finite SU(2) Equilibration Extension: Design

## Purpose

The first 4D Wilson SU(2) pilot records a reproducible short cold-start transient, not a thermalized expectation or physical spectral mass. Its beta-zero Haar control demonstrates the starting-state bias directly. The next step is a small, independently checked numerical instrument for investigating how cold- and Haar-start trajectories behave as sweep counts and finite volumes change.

## Design choices

1. **Full-action Metropolis for every link** is the trusted reference; its full-lattice action evaluation per proposal scales quadratically in site count and is too slow for comparisons beyond a tiny lattice.
2. **Six local plaquettes per proposed 4D link** supply the exact Wilson action difference and allow linear total work per sweep. This is the selected implementation. The old global evaluator remains the independent numerical oracle, and its results/receipts are left intact.
3. **SU(2) heatbath or overrelaxation** could improve mixing, but requires a separate transition-kernel audit and is outside this extension.

## Scope and interfaces

- New `research/yang_mills_su2/local_updates.py`: enumerate precisely six affected plaquettes, calculate a local link proposal's Wilson action difference without persistent mutation, and perform a seeded Metropolis sweep using that difference. Compare to full recomputation on nontrivial 2^4 and 3^4 configurations.
- New `research/yang_mills_su2/equilibration.py`: run matched cold/Haar chains, retain per-sweep spatial-plaquette traces, calculate explicitly described lag-one autocorrelation and early/late drift diagnostics, and serialize finite data with seeds, actions, and false physical/continuum/equilibrium-proof flags.
- New `research/yang_mills_su2/equilibration_cli.py`: regenerate and independently replay small, resource-bounded diagnostic receipts with exact input scope and integrity hashing.
- New tests verify six-plaquette geometry, change-of-action equality against the untouched Wilson action, rejection rollback, reproducibility, and honest lack-of-equilibrium claims. Use the beta-zero Haar expectation zero only as a statistical negative control, not an assertion that finite samples equal zero.

## Non-goals

No full four-dimensional transfer-matrix spectral gap, thermalization certificate, error-controlled continuum extrapolation, physical scale setting, or proof of the Yang–Mills millennium problem is asserted. Newton Solver and EINSTEIN-X Omega remain unexecuted without versioned executable sources. PHYSQED's existing polynomial engine is unchanged. Do not modify the five historical source-backed pilot artifacts or retroactively relabel their scope.

## Verification gates

1. Local action differences agree with full Wilson-action differences on each direction and randomly configured 2^4/3^4 lattices to a fixed floating-point tolerance; gauge-invariant reference diagnostics remain intact.
2. The optimized Markov kernel reproduces the original deterministic proposal/acceptance stream for a restricted seeded regression, with explicit acceptance/rejection rollback.
3. A beta-zero Haar control remains consistent with exact zero within declared sampling uncertainty; any cold/hot agreement at positive beta is only a convergence diagnostic.
4. Old Yang–Mills and PHYSQED tests still pass; old evidence report replay remains unchanged.
