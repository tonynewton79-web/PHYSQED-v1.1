# A two-sided physical-scale criterion for positive lattice transfer operators

**Tony Newton — 26 October 2026**

## 1. Motivation and principal statement

The finite-spacing Wilson SU(2) estimate obtained in the accompanying
manuscript is a bound on transfer eigenvalue ratios in *lattice* time units.
Asymptotically free four-dimensional Yang--Mills requires a bare-coupling
trajectory that moves beyond the strong-coupling range. Furthermore, a
uniform spectral bound much smaller than one at *every lattice step* would
drive the corresponding physical excitation energies to infinity as the
lattice spacing shrinks. That is not evidence for a finite-mass interacting
continuum theory.

The appropriate next target is a spectral contraction measured over a
*fixed physical separation*, accompanied by a nonvanishing spectral witness.
The following elementary criterion makes the two requirements exact.

**Proposition 1 (two-sided block spectral window).** Let `T` be a compact,
nonnegative, self-adjoint finite-volume transfer operator with simple
largest eigenvalue `lambda_0 > 0` and normalized vacuum `Omega`. Put

    S = T/lambda_0,  P = |Omega><Omega|,  Q = S-P,
    r = ||Q|| < 1.

Let `a>0` be the physical lattice spacing in temporal units and `k>=1`
an integer. Suppose that the full excited-sector bound

    ||Q^k|| <= U < 1                                            (H1)

has been proved and that a centered self-adjoint observable `F` satisfies

    <Omega,F Omega> = 0,
    <F Omega,S^k F Omega> >= c > 0,
    ||F Omega||^2 <= A.                                       (H2)

Then necessarily `0 < c/A <= U < 1`, and the physical finite-volume gap
`m_a = -log(r)/a` obeys

    -log(U)/(ak) <= m_a <= -log(c/A)/(ak).                     (1)

**Proof.** Since `F Omega` is orthogonal to `Omega`, its block correlator
equals `<F Omega,Q^k F Omega>`. The nonnegative self-adjoint spectrum
implies `||Q^k||=r^k`, while Cauchy--Schwarz gives

    0 < c <= <F Omega,Q^k F Omega> <= A r^k <= A U.

Hence `c/A <= r^k <= U`. Applying the decreasing function `-log` and
dividing by the positive `ak` proves (1). The strict upper bound on the
physical *mass* is not produced by contraction alone: it uses the
separate **lower** correlator witness. QED.

If along a sequence `a -> 0`, `k(a)a -> R` with `0<R<infinity`, the same
constants `U<1` and `c/A>0` are justified independently of lattice
spacing and volume, (1) gives a two-sided bounded finite-volume physical
excitation threshold. It does **not** prove convergence of the transfer
operators, persistence of the witness as a local continuum field, a
non-Gaussian continuum measure, the Osterwalder--Schrader axioms, or a
Yang--Mills mass gap. These are additional independent obligations.

## 2. Rational certificates without an unevaluated logarithm

For rational `0<x<1` let `y=(1-x)/(1+x)` and

    L_N(x) = 2 sum_{j=0}^{N-1} y^(2j+1)/(2j+1).

The exact positive series for `-log(x)` gives

    L_N(x) <= -log(x)
             <= L_N(x) + 2 y^(2N+1)/((2N+1)(1-y^2)).          (2)

The tail inequality follows by replacing all remaining odd denominators
by `2N+1` and summing the geometric series. Consequently, inserting
`L_N(U)` in the left side of (1), and the right side of (2) at `c/A`
on the right of (1), produces a wholly rational certified *conditional*
interval. The Python module `continuum_scale_bridge.py` implements this
bound with strict input limits and no floating-point arithmetic.

The numerical premises `U,c,A` must not be inferred from a user-supplied
receipt. Exact replay verifies the implication and its arithmetic, **not**
whether the Wilson transfer operator satisfies (H1)--(H2).

## 3. Stability under a blocked approximation

**Proposition 2 (power-telescope stability).** Let `Q` and `Q_D` be
operators on the same Hilbert space with norms at most one and suppose
`||Q-Q_D|| <= delta`. Then

    ||Q^k|| <= ||Q_D^k|| + k delta.                              (3)

**Proof.** Apply the algebraic telescoping identity

    Q^k - Q_D^k = sum_{j=0}^{k-1} Q^(k-1-j)(Q-Q_D)Q_D^j

and the triangle inequality. Each term has norm at most `delta`. QED.

For a fixed physical block `ak -> R`, transferring a strict approximate
contraction by this elementary argument needs a **normalized, aligned
excited-sector** one-step residual controlled on the `O(a)` scale or
better, with room below one in the block bound. The current Wilson
finite-rank cutoff only bounds an *unnormalized* transfer error with a
factor `exp(3 beta V)`; this does not furnish the needed `delta`, nor
does it control vacuum-projector alignment. `residual_stable_block_upper`
checks only the rational conclusion of (3), failing when the proposed
residual budget reaches one.

## 4. Why the existing strong-coupling bound cannot finish the argument

Suppose a sequence with spacing `a_n=1/n` had a fixed single-step excited
ratio `r_n <= q < 1`, and a normalized family of observables with
`||F_n Omega_n||^2 <= A`, independent of `n`. At unit physical time
(`k_n=n`) the connected correlator satisfies

    0 <= C_n(n) <= A q^n -> 0,

while its finite-volume physical gap is

    m_n = -n log(r_n) >= n[-log(q)] -> infinity.

Thus a fixed `q<1` single-step contraction cannot coexist with a
nonvanishing uniformly normalized correlator at a fixed positive physical
separation. The proven Wilson estimate `r<=6 beta<1` occupies a coupling
regime that does not approach the required asymptotically free trajectory
`beta(a)->infinity`; extrapolating it would miss this distinction.

## 5. Three exactly soluble control families

Take `T_n=diag(1,r_n)`, `a_n=1/n`, `k_n=n`, and the elementary centered
observable swapping the vacuum and excited basis vectors. It has excitation
norm one and block correlation `C_n(n)=r_n^n`.

| Abstract family | `r_n` | `r_n^n` as `n->infinity` | `-n log(r_n)` |
| --- | --- | --- | --- |
| Finite physical mass | `1-1/n` | `e^-1` | `1` |
| Collapsing physical gap | `1-1/n^2` | `1` | `0` |
| Ultralocal/infinite energy | `1/2` | `0` | `+infinity` |

The first family has `1/4 <= (1-1/n)^n < e^-1 < 1/2` for every `n>=2`.
Indeed the continuous function `x log(1-1/x)` has positive derivative
`u-log(1+u)>0`, `u=1/(x-1)`, and begins at `log(1/4)` for `x=2`.
It therefore supplies simultaneous, scale-independent block witnesses.
The second cannot have a uniform `U<1`; the third cannot have a uniform
positive `c/A` at fixed physical separation. All families are
**abstract two-mode matrices, not SU(2) Wilson examples**.

## 6. The Wilson renormalization-scale programme

A candidate input to the conditional bridge must provide each of the
following with independent provenance, at a sequence of weak-coupling
parameters and increasing physical volumes:

1. The actual gauge-invariant Wilson transfer normalization and vacuum
   projector, with self-adjoint positivity and a controlled volume limit.
2. A bound on the *entire excited sector* after `k(a) ~ R/a` time steps,
   from a rigorously controlled block/renormalization calculation.
3. A bounded-norm gauge-invariant local correlator with a positive lower
   witness at the same physical separation, consistent under scaling.
4. A normalized projector-aligned residual estimate that makes (3) useful;
   its error must be controlled independently of volume and cutoff.
5. Existence, locality, reflection positivity, nontriviality and the
   appropriate continuum field-theory reconstruction. The precise Clay
   formulation concerns any compact simple gauge group, not just SU(2).

Newton Solver and EINSTEIN-X Omega may eventually supply independent
multiscale candidates, but no versioned executable source for either is
available in this repository. Their present status remains
`SOURCE_UNAVAILABLE_NOT_EXECUTED`; no integration or calculation is claimed.

## 7. Reproduction and significance

From repository root:

    python -m unittest research.yang_mills_su2.tests.test_continuum_scale_bridge -v
    python -m unittest research.yang_mills_su2.tests.test_evidence_bridge -v

`artifacts/abstract_physical_scale_bridge_n2.json` is a small exact
receipt for the first abstract family; its fingerprint, all rational
fields and negative physical-proof flags are regenerated during replay.
It enters the source-hashed PHYSQED evidence ledger under
`EXACT_ABSTRACT_PHYSICAL_SCALE_BRIDGE`, deliberately **not** as a Wilson
spectral-gap certificate.

The contribution here is an explicit, reproducible division between
one-sided contraction, nonvanishing spectral weight, stability of block
approximations and the far deeper continuum construction. The spectral
inequalities themselves are elementary functional analysis; no novelty
or Millennium Prize resolution is claimed for them.

References for the physical problem and lattice transfer context:

- A. Jaffe and E. Witten, *Quantum Yang--Mills Theory*, official Clay
  Mathematics Institute problem description.
- K. Osterwalder and E. Seiler, *Gauge field theories on a lattice*,
  Annals of Physics **110** (1978), 440--471.
- T. Newton, *Proof-Carrying Diagnostics and Spectral Bounds for
  Four-Dimensional Wilson SU(2)*, cumulative working manuscript in
  `paper/` of this repository (26 October 2026).
