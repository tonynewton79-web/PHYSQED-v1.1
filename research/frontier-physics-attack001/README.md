# Frontier Physics Attack 001 — exact model-selection controls

Research-only addition to PHYSQED. This directory contains exact, **restricted** tests for candidate physics beyond general relativity and the Standard Model. It is not a new fundamental physical theory, experimental discovery, universal singularity theorem, or claim of novel mathematics.

## Executable checks

From the repository root with SymPy 1.14.0:

~~~bash
python research/frontier-physics-attack001/frontier_filters.py
python research/frontier-physics-attack001/full_tensor_check.py
python research/frontier-physics-attack001/koide_check.py
~~~

The three local Python checks passed on 12 November 2026 in the authoring environment. GitHub Actions and all inherited PHYSQED tests have **not** been run for this branch; the existing generalized-harmonic (GH) release hold remains in force.

### 1. Vacuum-energy screening obstruction for a restricted f(R) theory

In four spacetime dimensions, take the metric formalism action S = (1/2κ)∫√−g f(R) + S_m, with T_{μν}=−ρ_vac g_{μν} and a constant-curvature Einstein metric R_{μν}=(R/4)g_{μν}. Its trace equation is

    R f_R − 2f = −4κρ_vac.

For f(R)=R+αR²−2Λ_bare, the α term cancels exactly:

    4Λ_bare − R = −4κρ_vac,
    R = 4(Λ_bare+κρ_vac).

Thus **this restricted quadratic f(R) modification does not screen an arbitrary constant vacuum-energy shift on its constant-curvature branch**. This is established f(R) mathematics, not new physics. It says nothing universal about dynamic solutions, nonlocal theories, or vacuum-energy sequestering.

### 2. Retained singular Ricci-flat branch

For regular f(R) with f(0)=0, every Ricci-flat GR metric with R=0 also solves the zero-source metric f(R) equations, because f_R is constant on that metric. In particular Schwarzschild remains a branch, with

    K = R_{abcd} R^{abcd} = 48M²/r⁶     (G=c=1).

Hence adding αR² by itself cannot guarantee elimination of **all** black-hole singular solutions. The test does not claim singularity is mandatory for every solution of f(R).

### 3. Regular-center positive control, with energy-condition refusal

The known Hayward static model has

    ds² = −F dt² + F^(-1)dr² + r²dΩ²,
    F = 1 − 2Mr²/(r³+2Mℓ²),  M,ℓ>0.

Its center is de Sitter-like: R(0)=12/ℓ² and K(0)=24/ℓ⁴. Its effective GR source is

    ρ = 3M²ℓ²/[2π(r³+2Mℓ²)²],
    p_r = −ρ,
    p_t = 3M²ℓ²(r³−Mℓ²)/[π(r³+2Mℓ²)³].

The radial null energy inequality is saturated and the tangential null energy inequality is nonnegative. The strong energy condition fails for r³<Mℓ²; the tangential dominant energy condition fails for r³>4Mℓ². The model has degenerate-horizon threshold ℓ²=16M²/27. This is a **known effective geometry**, not a derivation of quantum gravity, geodesic completeness or an underlying matter action. The second script independently recomputes all four mixed Einstein-tensor components via Christoffel symbols; it still shares SymPy and is not an independent exact-arithmetic engine.

### 4. Koide mass-relation data control

For positive charged-lepton masses define

    Q = (m_e+m_mu+m_tau)/(sqrt(m_e)+sqrt(m_mu)+sqrt(m_tau))².

With m_e=0.51099895 MeV, m_mu=105.6583755 MeV, and PDG 2025-update m_tau=1776.93 ± 0.09 MeV, the input central values give

    Q = 0.666664463414500175...
    Q − 2/3 = −0.00000220325216649...

Imposing Q=2/3 algebraically and using the electron and muon mass inputs gives m_tau=1776.969027... MeV, 0.03903 MeV above the reported central value. This comparison is a **consistency check of an empirical relation, not a derivation of the mass hierarchy or a prediction independent of fitted masses**. A genuine flavor proposal must specify a radiatively consistent Lagrangian or symmetry, conventions for pole/running masses, and an additional independent observable.

## Next admissible physics candidate

A contender for the gravity track must specify a covariant action and admissible matter sector; recover GR and quantum field theory at low energies; pass propagator ghost and hyperbolicity tests; possess regular dynamical collapse (not just a regular static ansatz); control its entire horizon/causal structure and perturbation spectrum; and respond to radiative vacuum-energy shifts without hidden retuning. Cosmic acceleration must be fitted to the published data and likelihoods, not to a claimed consensus that evolving dark energy has already been established.

For the flavor track, a model must derive an invariant mass relation rather than encode its numeric value into adjustable parameters, and must provide an independent test after radiative corrections.

## Literature / priority controls

- S. Weinberg, *The cosmological constant problem*, Rev. Mod. Phys. 61 (1989): https://doi.org/10.1103/RevModPhys.61.1
- De Felice & Tsujikawa, *f(R) Theories*, Living Rev. Relativity (2010): https://link.springer.com/article/10.12942/lrr-2010-3
- S. A. Hayward, *Formation and Evaporation of Nonsingular Black Holes* (2006): https://doi.org/10.1103/PhysRevLett.96.031103
- H. Maeda, *Quest for realistic non-singular black-hole geometries: regular-center type* (2022): https://link.springer.com/article/10.1007/JHEP11%282022%29108
- Y. Koide, *Another formula for the charged lepton masses* (2018): https://www.sciencedirect.com/science/article/pii/S0370269317309814
- PDG tau mass listing (2025 update): https://pdglive.lbl.gov/DataBlock.action?node=S035M
- DESI DR2 publications and July 2026 update: https://data.desi.lbl.gov/doc/papers/dr2/ ; https://www.desi.lbl.gov/2026/07/30/new-desi-dr2-lyman-alpha-results-shed-light-on-dark-energy/

Do not reinterpret passed exact computations as physical verification, experimental confirmation, novelty, or clearance of existing PHYSQED release holds.
