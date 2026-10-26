# Explicit strong-coupling bounds for the finite Wilson SU(2) measure

## 1. The problem and contribution

For the periodic four-dimensional SU(2) Wilson model, the previous bound for a
connected temporal spatial-plaquette correlator grew with the total number
of plaquettes. A local Gibbs influence argument removes that volume factor
when the bare Wilson coupling is sufficiently small. We give an explicit
specialization of the classical Dobrushin--Föllmer estimate to this model,
then quantify two finite expansion errors and the finite-rank Fourier error
of the *interacting gauge-projected* transfer operator. The method and the
existence of a lattice strong-coupling regime are established ideas [1--4];
no new continuum Yang--Mills existence or mass-gap theorem is claimed.

Let the torus have extents `(T,L1,L2,L3)`, each at least two, and set
`V=L1 L2 L3`, `N=TV`. One oriented link variable in each positive coordinate
direction is distributed with normalized SU(2) Haar measure before the
Wilson density `exp(beta sum_p W(U_p))` is applied. Write
`W(g)=Re Tr(g)/2`, so `|W|<=1`. The average `X_t` of the `3V` spatial
plaquettes on time slice `t` is gauge invariant and satisfies `|X_t|<=1`.

## 2. Uniform strong-coupling temporal correlations

**Theorem (explicit local-influence specialization).** If
`0<=beta<1/18`, then for every such torus and `1<=t<T`, with
`r=min(t,T-t)` and `q=18beta`, the *exact interacting Wilson Gibbs
expectation* obeys

\[
  0\leq \operatorname{Cov}_\beta(X_0,X_t)
    \leq \min\left\{1,\frac{16q^r}{1-q}\right\}.
\]

The spatial size is absent from this estimate. Positivity of the covariance
uses the finite Wilson transfer construction in `WILSON_TRANSFER_SCOPE.md`.

**Proof of the upper bound.** Fix one positive-link variable `e` and all
others. Its conditional log-density is a sum of precisely six Wilson
plaquettes involving `e`. If another link `f` is changed, and the pair
shares `m(e,f)` plaquette incidences, the resulting difference between the
two conditional log-densities, considered as a function of `U_e`, has
oscillation at most `4 beta m(e,f)`: each plaquette trace lies in `[-1,1]`,
so two changes and one oscillation can each contribute a factor two.
The standard bounded-density comparison therefore yields a total variation
influence

\[
 c_{ef}\leq \tanh(\beta m(e,f))\leq\beta m(e,f).
\]

Each of the six plaquettes has three further positive-link variables, and
therefore `sum_f m(e,f)=18`, counted *with multiplicity*. The incidence
enumerator in `wilson_dobrushin.py` verifies this even on extent-two tori.
Thus the Dobrushin influence matrix `C=(c_ef)` has row sum at most `q=18beta`.
If `q<1`, the resolvent `D=(I-C)^(-1)=sum_(n>=0) C^n` exists. Entries of
`C^n` vanish unless a path of `n` shared-plaquette link interactions joins
their indices, and each row sum of `C^n` is at most `q^n`. Consequently,

\[
 D_{ef}\leq\frac{q^{d(e,f)}}{1-q},
\]

where `d(e,f)` is the link-interaction graph distance. Changing one spatial
link changes at most four spatial plaquette traces in its time slice, so
its coordinate oscillation in `X_t` is at most `8/(3V)`. Summing over the
`3V` spatial links in that slice gives `sum_e osc_e(X_t)<=8`. A single
shared-plaquette interaction can shift a link's time coordinate by at most
one, hence the interaction-graph distance between the supports of `X_0`
and `X_t` is at least `r`. Föllmer's covariance estimate [2] now gives

\[
 |\operatorname{Cov}(X_0,X_t)|
 \leq \frac14\sum_{e,f}\operatorname{osc}_e(X_0)
 D_{ef}\operatorname{osc}_f(X_t)
 \leq\frac{16q^r}{1-q}.
\]

Finally `|Cov(X_0,X_t)|<=1` by Cauchy--Schwarz and `|X_t|<=1`. This
completes the calculation. The exact rational receipt replays the link
incidence count, coupling window, time distance and stated upper bound.
The general covariance theorem itself is cited, not kernel-formalized in Lean.

The conclusion is a fixed-lattice-spacing, high-temperature estimate.
Four-dimensional asymptotic-freedom scaling moves the Wilson coupling
towards large beta rather than this narrow interval; no positive bound in
physical units survives from this theorem without substantially new input.

## 3. Two different finite expansion errors

There are `P=6N` plaquettes. Put `v_p=e^(beta W_p)-1` and
`u=e^beta-1`. For any `K` between 0 and `P`, expand the Wilson weight as
`prod_p(1+v_p)` and keep subsets of size at most `K`. Since
`|v_p|<=u`, the uniform remainder is at most

\[
 E_{\mathrm{subset}}(K)\leq
 \sum_{k=K+1}^{P}\binom Pk u^k.
\]

Separately, let `S_D(g)` be the exact SU(2) character expansion of
`e^(beta W(g))` restricted to representation dimensions `d<=D`, and
let `R_D(beta)` be the previously certified pointwise uniform tail.
The telescoping identity for products gives

\[
 \left|\prod_p e^{\beta W_p}-\prod_p S_D(U_p)\right|
 \leq P R_D(\beta)\bigl(e^\beta+R_D(\beta)\bigr)^{P-1}.
\]

`wilson_plaquette_expansion.py` evaluates outward rational upper bounds
for both expressions. The first is a *finite subset expansion*, not a
convergent connected-polymer cluster expansion. Both global errors can
become uninformative as `P` grows and cannot be substituted for the
volume-uniform correlation bound above.

## 4. Controlled cutoff of the interacting projected transfer

For a spatial slice with `m=3V` links, let `C_beta` denote the normalized
product temporal-link convolution, obtained by dividing each link kernel
by its constant-sector eigenvalue `2I_1(beta)/beta`. On representation
dimension `d` the normalized one-link eigenvalue is
`r_d=I_d(beta)/I_1(beta)`. These eigenvalues are positive and at most one:
the normalized kernel is a self-adjoint Markov contraction.

Let `Q_D` be the finite-rank Peter--Weyl projector retaining dimensions
`d<=D` on every spatial link. Left and right regular gauge transformations
preserve representation dimensions, so `Q_D` commutes with the gauge
projection `P_G`. It also commutes with `C_beta`. With `h=beta/2` and a
certified positive lower bound `L_1<=I_1(beta)`, the positive Bessel series
gives the all-sector bound

\[
 \epsilon_D=\min\left\{1,
 \frac{e^{h^2}h^{D+1}}{(D+1)!L_1}\right\},
 \qquad \|C_\beta-Q_D C_\beta Q_D\|\leq\epsilon_D.
\]

There is **no factor `m`** in this normalized-convolution error: in the
simultaneous Peter--Weyl eigenbasis, every excluded tensor product has at
least one small eigenvalue and all remaining factors have modulus <=1.

Define `B(U)` as the sum of spatial Wilson plaquette traces,
`M_beta=e^(beta B/2)`, and

\[
 T_\beta=M_\beta P_G C_\beta P_G M_\beta,
 \qquad T_{\beta,D}=M_\beta P_G Q_D C_\beta Q_D P_G M_\beta.
\]

Both are positive and `T_(beta,D)` is finite rank. Since
`|B(U)|<=3V`, operator norm submultiplicativity yields

\[
 \|T_\beta-T_{\beta,D}\|
 \leq e^{3\beta V}\epsilon_D.
\]

The ordered eigenvalues of these compact positive operators differ by
no more than this absolute error. The exact Python module
`wilson_projected_cutoff.py` certifies a rational upper bound, including
a rational upper enclosure for the exponential prefactor. It does
**not** assemble or diagonalize the enormous finite-rank matrix, and
the factor `e^(3beta V)` prevents a uniform interacting spectral-gap
conclusion from this comparison alone.

## 5. What remains

The main mathematical obstacle is now sharply identified: controlling
the spatial Wilson multiplier and gauge-projected sector *without* a
volume-growing norm estimate, then extending estimates beyond the
strong-coupling window to the continuum scaling regime. PHYSQED can
replay exact inequalities and source provenance; this does not formally
certify the underlying infinite-dimensional analytic propositions or
establish a physical mass gap.

## References

1. K. Osterwalder and E. Seiler, *Gauge Field Theories on a Lattice*, Annals of Physics **110** (1978), 440--471, https://doi.org/10.1016/0003-4916(78)90039-8.
2. H. Föllmer, *A Covariance Estimate for Gibbs Measures*, Journal of Functional Analysis **46** (1982), 387--395.
3. H. Künsch, *Decay of Correlations under Dobrushin's Uniqueness Condition and Its Applications*, Communications in Mathematical Physics **84** (1982), 207--222.
4. P. Rebeschini and R. van Handel, *Comparison Theorems for Gibbs Measures*, Journal of Statistical Physics **157** (2014), 234--281, https://arxiv.org/abs/1308.4117.
