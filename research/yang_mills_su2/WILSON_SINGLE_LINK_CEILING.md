# An explicit single-link Dobrushin ceiling in four-dimensional Wilson SU(2)

Tony Newton — 26 October 2026

## Principal result and significance

Consider the four-dimensional pure SU(2) Wilson Gibbs weight
`exp(beta sum_p W(U_p))`, `W(g)=Re Tr(g)/2`, on a periodic lattice whose
four periods are at least three. Identify SU(2) with the unit quaternions
`S^3` and use chordal distance `rho(x,y)=|x-y|`.

For positive links `e != f`, define the optimal single-link conditional
Wasserstein influence

    c_ef = sup{ W1_rho(mu_e(.|u),mu_e(.|u')) / rho(u_f,u'_f) },

where the supremum is over backgrounds differing only at link `f`,
and `mu_e` is the Wilson conditional distribution of `U_e`. This is a
*global* worst-case coefficient; backgrounds may be chosen separately
for different `f`.

**Proposition.** For every positive link `e` there are 18 distinct
neighboring positive links `f` for which `c_ef >= beta/4`. Consequently

    sum_{f != e} c_ef >= (9/2) beta.

The ordinary unweighted single-link Dobrushin row-sum criterion
`sup_e sum_f c_ef < 1` therefore cannot hold when `beta >= 2/9`.
This is a ceiling for **that proof method**, not a claim that a physical
Yang--Mills mass gap vanishes, that a gauge-fixed or block-based method
fails, or that the global sensitivity *upper* bound is exactly `1/4`.

## Proof by a central-sign Wilson background

By translation and axis permutation, put `e=(x,mu)` with `x=0` and `mu=0`.
For each transverse direction `nu=1,2,3`, the six plaquettes containing
`e` are rooted at `x` and `x-e_nu` in the `(0,nu)` plane. Each contains
three other positive links. Their 18 neighbors are pairwise distinct when
the periods are at least three.

Set all surrounding positive links to the identity except the three
parallel links at `(x-e_nu,0)`, which are set to `-I`. The three parallel
links at `(x+e_nu,0)` remain `+I`. Every side link is `+I`.
Then, for any value `q` of `U_e`, the six Wilson plaquette contributions
are exactly three copies of `W(q)` and three copies of `W(-q)`. They cancel
identically; the conditional distribution of `q` is normalized Haar.

Fix any one of the 18 neighboring links `f`, with unperturbed value
`sigma I` for `sigma=+1` or `-1`, and change it to
`sigma exp(t X)` for a unit imaginary quaternion `X` and small real `t`.
It appears in exactly one incident plaquette. All other factors in that
plaquette are central signs, so the one-link conditional parameter
`b_e(t) in R^4`, defined by density proportional to `exp(b_e(t).q)`, obeys

    b_e(0)=0,       |b'_e(0)|=beta.

Let `h=b'_e(0)/beta` be a unit vector and take the coordinate observable
`F(q)=h.q`. It is one-Lipschitz for chordal distance. At the Haar point,
rotational symmetry gives `Var(F)=1/4`. Differentiating its conditional
mean along `b_e(t)` yields

    d/dt E_{b_e(t)} F |_{t=0} = beta/4.

Since `rho(sigma I,sigma exp(tX))/|t| -> 1`, Kantorovich duality implies
`c_ef >= beta/4`. Sum over the 18 distinct neighbors. QED.

The distinction between necessary and sufficient estimates is essential:
our existing proof gives the **upper** influence estimate `c_ef <=
beta m(e,f)/3`, hence row sum `<=6 beta`; the new lower construction
gives row sum `>= (9/2) beta`. It does *not* establish equality or the
unrefereed sharp global coefficient `1/4` claimed in related work.

## Reproducibility and prior art

`wilson_dobrushin_ceiling.py` constructs the exact six-plaquette link
incidence and central-sign background at side lengths 3--8, counts
the 18 distinct neighbors, evaluates the rational lower coefficient,
and generates tamper-checked receipts. A separate test uses the actual
`Lattice4D.plaquette` implementation to recover the four conditional
field coordinates from quaternion-basis evaluations. It perturbs all
18 neighbors independently and checks their unit first-order response;
this numeric regression supports but does not substitute for the proof.

The committed `artifacts/wilson_single_link_ceiling_beta2_over_9.json`
has exact row lower bound one at `beta=2/9`. The source-hashed PHYSQED
ledger category `EXACT_WILSON_SINGLE_LINK_METHOD_CEILING` only certifies
the finite incidence and rational-arithmetic consequences. It carries
explicit false physical-law, global-sharp-upper, continuum-gap, and
Lean-kernel proof flags.

The `2/9` single-link Dobrushin ceiling and the proposed sharp quarter
Wasserstein upper bound have previously been discussed in unrefereed
Bhattacharjee--Bhattacharya v3.3.1 material. The proposition here is an
independent explicit Wilson-star derivation, not a novelty/priority claim.

## What this rules out and what it leaves open

No improvement of the *same global single-link row-sum comparison* can
reach the weak-coupling trajectory `beta(a)->infinity`. This does not
rule out block couplings, restricted gauges, renormalized transfer
operators, cancellation-based analysis, or an eventual continuum theory.
The companion `CONTINUUM_SCALE_BRIDGE.md` specifies the required
fixed-physical-block full-spectrum contraction and nonvanishing
correlator witness. Neither hypothesis has been established for the
weak-coupling interacting Wilson transfer.

References:

- D. Bhattacharjee and U. Bhattacharya, *Mass Gap of Lattice Yang--Mills
  Theory up to the Dobrushin Ceiling*, unrefereed v3.3.1 source,
  https://github.com/creelie/4Y-M/tree/v3.3.1/strong-coupling/prd .
- H. Föllmer, *A covariance estimate for Gibbs measures*, J. Funct.
  Anal. **46** (1982), 387--395.
- P. Rebeschini and R. van Handel, *Comparison theorems for Gibbs
  measures*, J. Stat. Phys. **157** (2014), 234--281.
