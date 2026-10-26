# From single-link spherical geometry to stronger Wilson lattice mixing

## Research goal

Replace the old total-variation Dobrushin factor `18 beta` by a sharper
Wasserstein coupling estimate that uses the exact SU(2) conditional law on
the quaternion three-sphere. Establish an explicit, spatial-volume-uniform
gauge-invariant Wilson transfer ratio in a strictly larger beta interval,
without claiming any four-dimensional continuum construction.

## Approaches and decision

1. **Old TV comparison:** valid for `beta<1/18` but ignores the geometry of
   the single-link distribution.
2. **Uniform spherical Poincare gap (selected):** use the documented and
   independently checked elementary Barta supersolutions to bound the
   concentration-uniform von Mises--Fisher gap below by `3` on unit `S^3`.
   Cauchy--Schwarz then gives a globally uniform chordal Wasserstein
   sensitivity `1/3`, yielding Wilson Dobrushin row sum `6 beta` and the
   lattice spectral gap for `beta<1/6`.
3. **Sharp chordal `1/4` sensitivity:** a recent long unrefereed proof
   claims `beta<2/9`, but its global Bessel/entire-function positivity
   argument is beyond this separately verified step. It must not be
   certified here without complete independent review.

## Mathematical requirements

For every parameter vector `b` in `R^4`, the conditional SU(2) law is
`dnu_b(x) = Z(b)^-1 exp(b dot x) dσ(x)` on unit `S^3`. Its reversible
generator decomposes in polar angle `theta` into spherical `S²` harmonics:

`L_l = w^-1 ∂theta(w ∂theta) - l(l+1)/sin(theta)^2`,
`w=sin(theta)^2 exp(kappa cos(theta))`.

For `l>=1`, the positive trial function
`psi=sin(theta) exp(-kappa cos(theta)/5)` gives
`-L_1 psi/psi = 3 + (4/25) kappa^2 sin(theta)^2`.
For zonal `l=0` nonconstant modes, differentiate the eigenvalue
equation; its derivative has Dirichlet endpoints and auxiliary operator
`M=w^-1∂(w∂)+b'(theta)`. The positive trial function
`psi=sin(theta) exp(-2 kappa cos(theta)/5)` gives
`-M psi/psi = 3 + (6/25) kappa^2 sin(theta)^2`.
Barta's ground-state representation then gives spherical Poincare gap
at least `3` at every concentration, including the endpoint limits.

For any chordally 1-Lipschitz `f`, intrinsic `|grad f|<=1` a.e.; for
`h` a unit vector, the same holds for `h dot x`. Poincare and covariance
Cauchy--Schwarz yield `|Cov_nu_b(f,h dot x)| <= 1/3`. Differentiate along
the segment between any two parameters and use Kantorovich duality:
`W1_chordal(nu_b,nu_b') <= |b-b'|/3`.

Each Wilson spatial/temporal link shares six plaquettes, each with three
other link incidences. Altering a neighboring link by chordal distance
`rho` changes the quaternion staple parameter by at most
`beta*m(e,f)*rho`. Therefore Wasserstein Dobrushin row sum is at most
`(18/3)beta = 6beta`. With `6beta<1`, standard metric Dobrushin
comparison gives exponential temporal clustering for finite-volume
**Lipschitz** spatial observables. The strictly positive smooth Wilson
transfer eigenfunctions divided by the Perron eigenfunction are Lipschitz
on the compact spatial configuration manifold. The eigenfunction-ratio
test from `WILSON_LATTICE_SPECTRAL_GAP.md` therefore yields
`lambda_n/lambda_0 <= 6 beta` and `Delta_lattice >= -log(6 beta)`.

The source of the uniform Poincare Barta technique is the recent
Bhattacharjee--Bhattacharya public source (v3.3.1, `strong-coupling/paper/main.tex`).
Its stronger quarter constant is not imported or proven by this project.
The classical geometric and comparison methods must be credited; the
contribution here is an independently worked, strictly scoped numerical
certificate and link to the existing PHYSQED transfer machinery.

## Implementation and safety

Add a new rational module, tests and scholarly Markdown proof. The exact
receipt must replay `6beta`, both Barta quadratic rational coefficients,
and a positive finite atanh lower bound for `-log(6beta)`. Add a separate
PHYSQED kind with strict source-hash, implementation-hash and replay;
never repurpose previous evidence types. Reject `beta>=1/6`, beta zero,
non-rational/boolean values, excessive term counts, and false continuum or
Lean claims. Do not claim that the Python kernel proves Sturm--Liouville,
metric Dobrushin comparison, or the continuum existence-and-mass-gap goal.

## Success/failure gate

Success means reproducing a nontrivial exact interval at `beta=1/10`,
which the previous `beta<1/18` theorem did not reach, with full prior
Yang--Mills and PHYSQED regression tests green and independent mathematical
review. Failure of any analytic step means recording the claim as
conditional rather than promoting it to a lattice spectral theorem.
