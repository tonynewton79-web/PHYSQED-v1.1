# Finite Wilson SU(2): volume-uniform strong-coupling and spectral cutoff design

## Intent and scope

Advance all three user-approved routes from the finite Wilson transfer paper:
(1) a gauge-invariant spatial-plaquette covariance estimate independent of spatial volume;
(2) controlled finite Wilson plaquette/character expansion truncation;
(3) a controlled finite-rank approximation to the *interacting gauge-projected* transfer operator.
Keep the continuum Yang--Mills construction, the full excitation gap, and the weak-coupling scaling limit explicitly open.

## Approaches and decisions

The requested order is Dobrushin link influences, character/plaquette subset expansion,
then projected-transfer spectral approximation. The Dobrushin approach gives a restricted
uniform estimate; connected polymer expansions might improve its coupling interval but
require a separate genuine convergence proof. A truncated character product is a finite
subset expansion, **not** a connected-polymer convergence theorem. Spectral Fourier
truncation bounds eigenvalue errors but does not compute eigenvalues for a physical 3D slice.

## Mathematical contract

On a periodic 4D torus with every extent at least two, links are independent normalized SU(2)
Haar variables before weighting by `exp(beta sum_p W(U_p))`, `W=ReTr/2`. Each link belongs to six
plaquettes, and each of those has three other link incidences. Altering one other link in
`m` shared plaquettes changes the conditional log-density *oscillation* by at most `4m beta`.
The total variation influence is consequently at most `tanh(m beta)<=m beta`, so the Dobrushin
matrix has maximum row sum `q<=18 beta`. The Föllmer covariance inequality bounds
`|Cov(F,G)| <= (1/4) sum_ij osc_i(F) [(I-C)^-1]_ij osc_j(G)` when `q<1`.

The normalized spatial plaquette average `X_t` depends on `3V` links in slice `t`, has
`osc_i(X_t)<=8/(3V)`, and total oscillation at most `8`. Link-dependency paths move in
Euclidean time by at most one per edge, so if `r=min(t,T-t)`,

`|Cov_beta(X_0,X_t)| <= min(1, 16 (18beta)^r/(1-18beta))`, for `0<=beta<1/18`.

The lower zero endpoint follows from existing Wilson transfer positivity. The new upper
estimate is a consequence of classical Dobrushin--Föllmer machinery; we do not claim its
general method as original. In particular, the beta window does not reach continuum scaling.

For a finite set of `P=6 TL1L2L3` plaquettes, set `v_p=e^(beta W_p)-1` and `u=e^beta-1`.
The subset sum of activated plaquettes with cardinality at most `K` differs uniformly from
the full Wilson weight by at most `sum_(k>K) binomial(P,k) u^k`; all exp enclosures must be
outward rational. Separately, if the character cutoff has per-plaquette uniform error `R_D`,
the full product error is at most `P R_D (e^beta+R_D)^(P-1)`. Neither is volume-uniform.

For `m=3V` spatial links, normalize the one-link temporal convolution to its trivial
eigenvalue `2I_1(beta)/beta`. Its Peter--Weyl eigenvalues are `r_d=I_d/I_1`, in `[0,1]`.
Let `Q_D` retain spatial-link representations of dimension at most `D`; its tensor cutoff
to the normalized product convolution has operator-norm error `<=epsilon_D`, where
`epsilon_D` is a positive rational bound for `sup_(d>D) I_d/I_1`. The interacting projected
operator `M P C P M` and its finite-rank truncation then differ in norm by at most
`e^(3 beta V) epsilon_D`. Min-max gives the same absolute eigenvalue error, but this
volume-dependent bound cannot certify a continuum gap. No Ritz eigenvalues are claimed.

## Components

- `wilson_dobrushin.py`: link incidence counts, exact strong-coupling covariance envelopes,
  bounded request and strict rational receipt replay.
- `wilson_plaquette_expansion.py`: two separate exact global truncation bounds with rational
  exponential enclosures; names clearly distinguish subset order and character dimension.
- `wilson_projected_cutoff.py`: exact per-link normalized Fourier and interacting projected
  operator-norm bound, with no claim of having diagonalized the projected matrix.
- Tests for literal rational examples, extent-2 periodic incidences, beta threshold, impossible
  limits, monotonicity of error bounds, tampering, and refusal of continuum claim flags.
- A cumulative scope note and the existing fail-closed PHYSQED evidence ledger updated only
  for exact statements that genuinely replay.

## Acceptance boundaries

All three components use bounded standard-library rational computation, except the existing
verified Bessel interval routines. Run both full Yang--Mills and PHYSQED suites. Distinguish
an exact checked rational receipt from a formal proof in Lean; keep the full Wilson interacting
spectrum, physical units and continuum axioms explicitly open.

## Primary literature

- K. Osterwalder and E. Seiler, *Gauge Field Theories on a Lattice*, Ann. Phys. 110 (1978).
- H. Föllmer, *A Covariance Estimate for Gibbs Measures*, J. Funct. Anal. 46 (1982).
- P. Rebeschini and R. van Handel, *Comparison Theorems for Gibbs Measures* (2014).
