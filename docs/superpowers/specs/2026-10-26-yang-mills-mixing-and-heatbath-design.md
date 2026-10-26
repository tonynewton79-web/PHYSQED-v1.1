# Exact β=0 Mixing and Positive-Coupling SU(2) Heatbath: Design

## Purpose

Extend the independently checked 4D SU(2) Wilson finite-lattice pilot in two connected but logically distinct ways. The first is an exact, replayable β=0 Markov-chain certificate that explains the observed cold-start bias. The second replaces slow local-angle Metropolis trials with a genuine one-link Gibbs/heatbath draw and records gauge-invariant time-separated plaquette diagnostics. The numerical and mathematical claims remain finite-cutoff only.

## Approach and decisions

1. **Exact representation calculation** is preferred over fitting mixing rates from two seeds. At ε=π the axis-angle proposal law is central; its SU(2) character eigenvalues are zero on half-integer spins and 1/(2j+1) on integer spins. The Markov operator has an exact one-sweep mean-zero L² norm 1/3. A cold delta distribution becomes L² after two sweeps. Rational truncation-plus-integral bounds certify the full finite product-volume L² norm at every integer sweep n≥2.
2. **One-link exact conditional heatbath** is preferred over further ad hoc Metropolis tuning. Determine the four-dimensional linear coefficient h of the six affected plaquette traces by evaluating the same local action with four quaternion basis links, restoring the original link in a finally block. The conditional law is proportional to exp(β h·q) on SU(2)≈S³. Sample it with a truncated-exponential scalar proposal, a sqrt(1−t²) rejection step, a uniform two-sphere direction, and a quaternion rotation. At β=0 use an independent Haar draw. Keep the full-action Metropolis evaluator and the original receipts unchanged.
3. **Gauge-invariant time-correlator diagnostics** will use timeslice spatial plaquettes on a temporal extent of at least four, finite connected covariance, and a cosh effective-mass *diagnostic* only when its arccosh argument is admissible. No estimate will be called a spectral lower bound or a proof of equilibrium.

## Mathematical invariants

- With n complete β=0 sweeps from cold identity links and update angle ε, the expectation of an elementary fundamental plaquette is [sin(ε)/ε]^(4n). It equals zero for ε=π and n≥1. The Haar-start expectation is zero.
- At β=0, ε=π, write d=2j+1. For integer j≥1 the transition eigenvalue is 1/d; for half-integer j it is zero. For N independently updated links and n≥2, the cold-start density satisfies
  ||p_n−1||²_L²(Haar^N) = (1+S_n)^N−1, S_n=Σ_(j≥1) (2j+1)^(2−2n).
- Rational tail estimate for p=2n−2≥2 after J terms is 0 < tail ≤ (2J+1)^(1−p)/(2(p−1)).
- For local coefficient h with κ=β|h|>0, mean link alignment satisfies E[(h/|h|)·q]=I₂(κ)/I₁(κ). Existing rational Bessel bounds certify this **conditional heatbath mean**, not a lattice transfer-matrix spectral mass. Tests compare actual heatbath samples independently to that bound.
- Wilson plaquette local action and orientation conventions are taken from `lattice.py`; one-link conditional scalar f(q) must equal h·q for all unit q, including directions with μ=3.

## Files and interfaces

- `research/yang_mills_su2/mixing_certificates.py`: exact rational `beta_zero_rep_eigenvalue(spin_twice)`, `cold_l2_squared_bounds(sweeps, links, terms)`, and `mixing_receipt(...)`; no numerical spectrum claim.
- `research/yang_mills_su2/heatbath.py`: `staple_linear_coefficients`, `sample_heatbath_link`, and `heatbath_sweep`; depends on existing quaternion and lattice code, not on PHYSQED proof declarations.
- `research/yang_mills_su2/transfer_diagnostics.py`: `cosh_effective_mass`, `run_heatbath_timeslices`; finite raw traces, deterministic seeds, acceptance-independent heatbath, explicit uncertainty limitations and false proof flags.
- Targeted `tests/test_mixing_certificates.py`, `test_heatbath.py`, `test_transfer_diagnostics.py`, and an explanatory `MIXING_HEATBATH_SCOPE.md`.

## Non-goals

No continuum limit, scaling law, infinite volume, analytically proved positive-coupling gap, full transfer-matrix construction, Osterwalder–Schrader reconstruction, or physical mass-gap claim. No inference of actual implementation of Newton Solver or EINSTEIN-X Ω without versioned executable sources. The PHYSQED algebraic proof engine is not changed; the new certificate is explicit rational finite-model arithmetic with a documented Peter–Weyl theorem dependency, not a Lean proof of that theorem.

## Acceptance gates

1. Rational representation constants and L² bounds agree with hand-derived values; invalid/over-budget inputs rejected and physical flags remain false.
2. Six-plaquette h·q matches independently evaluated plaquettes and complete Wilson-action differences on nontrivial 2⁴ and anisotropic temporal lattices; rollback on evaluation failure.
3. Heatbath β=0 yields seeded Haar-distributed links and cold/Haar first-moment diagnostics; at κ=2 the finite-sample mean is compatible with the independently bounded I₂(2)/I₁(2).
4. Synthetic periodic cosh data recover the planted finite effective mass, while negative/noisy samples refuse unjustified mass extraction.
5. Previous SU(2) and PHYSQED tests, original JSON receipts, and existing source-control branch remain intact; new work is isolated and unmerged.
