# Chordal mixing and the strong-coupling SU(2) Wilson transfer spectrum

## 1. Significance and precise claim

The previously established estimate on four-dimensional SU(2) Wilson
lattices uses total-variation influence and gives a Dobrushin row sum
`18 beta`; its spectral consequence applies when `beta<1/18`.
Viewing SU(2) as the unit quaternion sphere `S³` exposes a stronger
comparison in the **chordal** metric. A concentration-uniform spherical
Poincare inequality yields row sum `6 beta`, making the same transfer
argument valid in the strictly larger window `0<beta<1/6`.

This is a reconstruction and independently checked specialization of
existing small-coupling tools. A recent public preprint [3] states a
sharper result reaching `beta<2/9`; that separate sharp-quarter theorem
uses a lengthy argument not certified in the present work. Nothing here
constructs a four-dimensional continuum Yang--Mills field theory.

**Theorem (finite-volume Wilson SU(2), chordal bound).** Let the three
periodic spatial extents each be at least two. For the actual positive,
gauge-projected Wilson transfer operator `T_beta` of
`WILSON_TRANSFER_SCOPE.md`, with spatial plaquette weight
`exp(beta Re Tr(U_p)/2)` and `0<beta<1/6`, write its eigenvalues in
descending order as `lambda_0>lambda_1>=...>=0`. Then

\[
 0\le \lambda_n/\lambda_0\le6\beta<1\quad(n\ge1),
 \qquad \Delta_{\rm lattice}\ge-\log(6\beta)>0.
\]

The bounds hold uniformly in spatial volume **in lattice units**.

## 2. A concentration-uniform Poincare inequality on S³

Each SU(2) link is a unit quaternion `x in S³ subset R⁴`. Given all
other link variables, the conditional Wilson density is
`dnu_b(x) = exp(b dot x) dσ(x) / Z(b)`, with `b` the vector sum of
six weighted unit-quaternion staples. Rotate so that `b=kappa e1`,
`kappa>=0`, and take the polar angle `theta in (0,pi)` from `e1`.
The reversible unit-sphere diffusion generator separates into degree
`l` spherical harmonics on the remaining `S²`:

\[
 L_l=\frac1w\partial_\theta(w\partial_\theta)
       -\frac{l(l+1)}{\sin^2\theta},\qquad
 w=\sin^2\theta\,e^{\kappa\cos\theta}.
\]

The angular drift is `b_theta=2cot(theta)-kappa sin(theta)`.
The eigenvalue zero corresponds to constant functions at degree zero.
We now verify a lower bound of `3` on all other eigenvalues.

For any strictly positive trial function `psi`, integration by parts
with `f=psi h` gives Barta's ground-state representation

\[
 \int (|f'|^2+q_l|f|^2)w
 =\int\psi^2|h'|^2w+
   \int(-L_l\psi)\psi|h|^2w,
 \quad q_l=l(l+1)\csc^2\theta.
\]

For `l>=1`, it suffices to take `l=1` because the added potential
increases with `l`. A regular degree-`l` mode is `O(theta^l)` at the
north pole (and likewise at the south pole). Its ground-state boundary
term `w(psi'/psi)f²` is `O(theta^(2l+1))` and hence vanishes; this also
justifies passing from the compactly supported form computation to
regular eigenfunctions. With `psi=sin(theta) exp(a kappa cos(theta))`,
direct differentiation gives

\[
 -L_1\psi/\psi
 =3+(5a+1)\kappa\cos\theta
    -a(a+1)\kappa^2\sin^2\theta.
\]

Choose `a=-1/5`; the linear term cancels and the remainder is
`3+(4/25)kappa² sin²(theta)>=3`. The singular positive potential
at both endpoints makes compactly supported functions a quadratic-form
core, so the conclusion extends from test functions to the `l>=1`
spectrum.

For the nonconstant degree-zero eigenfunctions `g`, differentiate
`L_0 g=-lambda g` and put `h=g'`. Regularity at the poles gives
`h=O(theta)` at the north pole and the corresponding order at the
south pole, so the ground-state boundary term vanishes as `O(theta³)`.
The derivative obeys `M h=-lambda h`, where
`M=(1/w)∂theta(w∂theta)+b_theta'` and
`-b_theta'=2csc²(theta)+kappa cos(theta)`.
For the same trial form,

\[
 -M\psi/\psi
 =3+(5a+2)\kappa\cos\theta
    -a(a+1)\kappa^2\sin^2\theta.
\]

At `a=-2/5`, the lower bound becomes
`3+(6/25)kappa² sin²(theta)>=3`. Therefore **every** concentration
`kappa` has nonconstant spherical spectral gap at least `3`, giving

\[
 \operatorname{Var}_{\nu_b}(f)
 \le \tfrac13\int_{S^3}|\nabla_{S^3} f|^2\,d\nu_b.
 \tag{1}
\]

The exact Python receipt checks the rational quadratic coefficients
`4/25` and `6/25`; it does not kernel-formalize Barta's theorem.

## 3. Chordal Wasserstein coupling

Let `f:S³->R` be 1-Lipschitz for the **chordal distance**
`rho(x,y)=|x-y|` in R⁴. Then its intrinsic gradient has norm at most
one almost everywhere. The same is true of `h dot x` for any unit
`h in R⁴`. Applying (1) twice and Cauchy--Schwarz yields

\[
 |\operatorname{Cov}_{\nu_b}(f,h\cdot x)|\le1/3.
\]

Differentiate `E_{nu_{b+s(b'-b)}} f` with respect to `s`:
its derivative is `Cov(f,(b'-b) dot x)`. Integrating along the
parameter segment and using Kantorovich duality gives

\[
 W_{1,\rm chordal}(\nu_b,\nu_{b'})
 \le \tfrac13|b-b'|.\tag{2}
\]

This is a safe, **not sharp**, coefficient. The claimed `1/4`
coefficient in [3] is not an input to our theorem. Chordal distance
must not silently be replaced by geodesic distance; its coupling
properties differ.

## 4. From local Wilson influences to transfer eigenvalues

Every Wilson link belongs to six plaquettes. Each plaquette contains
three other positive-link variables, giving exactly `18` neighbor
incidences with multiplicity, including extent-two periodic tori.
If a neighboring link `f` changes by chordal distance `rho`, the
conditional parameter at link `e` changes by at most
`beta m(e,f)rho`, since staple multiplication and inversion are
orthogonal maps of quaternion coordinates. Thus (2) bounds the
coordinate Wasserstein influence by

\[
 c_{ef}\le\frac\beta3 m(e,f),\qquad
 \sum_f c_{ef}\le\frac{18\beta}3=6\beta=:q.
\]

For clarity, the metric Dobrushin covariance comparison can be obtained
from Corollary 2.6 of [2] by tilting one Gibbs measure by `exp(s G)`.
Since each chordal single-link space has diameter two, the local
comparison perturbation is bounded by `|s| delta_j G`, where
`delta_j G` is the coordinate chordal Lipschitz seminorm. Dividing
the comparison by `|s|` and taking `s->0` gives

\[
 |\operatorname{Cov}(F,G)|
 \le \sum_{i,j}\delta_iF\,[(I-C)^{-1}]_{ij}\,\delta_jG,
 \qquad C=(c_{ij}).
\]

In `q<1`, the row sum of the resolvent's paths that cross at least `r`
link-neighbor steps is at most `q^r/(1-q)`. This bounds
covariances of Lipschitz spatial-slice observables `F` at temporal
separation `r=min(t,T-t)` by
`|Cov(F_0,F_t)| <= A_F(V) q^r`, where the finite positive prefactor
depends on the observable and spatial volume but **not** on the
temporal period or separation. The dependency graph takes at least
`r` shared-plaquette steps to travel `r` periodic time slices.
We need only the rate `q`, not an optimized prefactor.

The genuine gauge-invariant finite-volume Wilson transfer is obtained
by gauge projection of a smooth, strictly positive integral kernel
on the compact spatial configuration **manifold**. Gauge-invariant
eigenfunctions descend to the orbit space, which may have singular
strata; smoothness is asserted on the original manifold, not on a
putative smooth quotient. Its simple Perron eigenfunction `phi_0`
is smooth and bounded away from zero; every nonzero excited
eigenfunction `phi_n` is smooth. Hence the ratio
`F_n=phi_n/phi_0` is a bounded gauge-invariant **Lipschitz**
spatial observable. At infinite Euclidean time the transfer
spectral representation gives the exact covariance
`Cov(F_n(0),F_n(t))=(lambda_n/lambda_0)^t`.
The metric comparison therefore forces

\[
 (\lambda_n/\lambda_0)^t\le A_{F_n}(V)q^t.
\]

Take the `t`th root and let `t->infinity`; the prefactor disappears.
This proves the claimed `lambda_n/lambda_0<=6beta` for all excited
gauge-invariant transfer modes, uniformly in spatial volume.

## 5. Exact arithmetic, novelty and continuum limits

For rational `beta=1/10`, outside the old `beta<1/18` interval, the
new ratio ceiling is exactly `3/5`. Its logarithmic gap is at least
`-log(3/5)=0.5108256...` lattice time units. With
`y=(1-6beta)/(1+6beta)`, the exact positive sum

\[
 2\sum_{j=0}^{K-1}\frac{y^{2j+1}}{2j+1}< -\log(6\beta)
\]

provides a rational lower certificate. The PHYSQED receipt replays
only these exact algebraic consequences and source provenance; it
does not machine-prove the analytic diffusion, Wasserstein comparison
or the reconstructed transfer operator.

The threshold `1/6` is a classical-method small-coupling threshold
stated in [3]; it is not asserted as new to mathematics. This argument
does not approach the four-dimensional continuum scaling regime,
where `beta=4/g²` grows as the lattice spacing shrinks. The continuum
existence problem and physical mass gap remain open.

## References

1. K. Osterwalder and E. Seiler, *Gauge Field Theories on a Lattice*,
   Annals of Physics **110** (1978), 440--471.
2. P. Rebeschini and R. van Handel, *Comparison Theorems for Gibbs
   Measures*, Journal of Statistical Physics **157** (2014), 234--281,
   https://arxiv.org/abs/1308.4117.
3. D. Bhattacharjee and U. Bhattacharya, *Sharp Curvature and Finite-Box
   Criteria for Lattice Yang--Mills Theory*, source
   `strong-coupling/paper/main.tex` at tag v3.3.1, 2026,
   https://github.com/creelie/4Y-M/tree/v3.3.1.
   An accompanying longer Dobrushin-ceiling paper claims the sharper
   chordal constant `1/4`; that claim is not independently proved here.
