# A volume-uniform strong-coupling lattice transfer gap

## Intent and limits

The existing four-dimensional periodic Wilson SU(2) calculation gives a
volume-independent Dobrushin--Föllmer bound on *one* temporal plaquette
correlator when `0 <= beta < 1/18`. The next mathematical question is whether
this mixing estimate controls the entire gauge-invariant finite-spatial-volume
transfer spectrum, avoiding the `exp(3 beta V)` cost of the separate Fourier
cutoff estimate. The result is limited to the strong-coupling lattice model;
it does not address the beta-to-infinity continuum trajectory.

## Approaches

1. **Global Fourier operator-norm approximation:** retained as a valuable
   finite-rank diagnostic, but its multiplicative Wilson potential has a
   volume-growing norm. Nothing presently justifies removing that factor.
2. **Temporal mixing to transfer eigenvalues (selected):** extend the same
   classical covariance bound from plaquette averages to arbitrary bounded
   gauge-invariant spatial-slice functions. Strict positivity and compactness
   of the finite-volume Wilson transfer then turn temporal mixing into a
   bound on every excited eigenvalue relative to the Perron eigenvalue.
   Unlike approach 1, this compares ratios rather than absolute errors.
3. **Cluster/polymer transfer estimates:** may extend the coupling domain,
   but requires substantial new estimates and is not this feature.

## Proposed theorem and proof obligations

Let `V=L1*L2*L3` with each spatial period at least two, `m=3V`, and let
`T_beta` be the genuine positive gauge-invariant Wilson transfer operator
defined in `WILSON_TRANSFER_SCOPE.md`. For `0 < beta < 1/18`, write
`q=18 beta`. For the ordered eigenvalues, prove

`0 <= lambda_n(T_beta)/lambda_0(T_beta) <= q` for every `n >= 1`.

The proof must independently justify all of the following:

- The gauge-projected transfer kernel is strictly positive, smooth, and
  trace class on the finite spatial gauge-invariant Hilbert space. Its Perron
  eigenvalue is simple and its positive ground-state eigenfunction is bounded
  away from zero on the compact configuration space.
- The Dobrushin--Föllmer estimate on a Euclidean periodic time torus bounds
  covariance of **any** two copies of bounded real gauge-invariant spatial
  functions `F`, separated by `r` time steps, by
  `m ||F||_infty^2 q^r/(1-q)`; no spatial-volume uniformity of the prefactor
  is required. The nearest-time-slice graph distance is at least `r`.
- At fixed spatial volume the time-period limit gives the transfer-vacuum
  spectral representation of this covariance, with nonnegative weights.
- For any normalized excited eigenfunction `phi_n`, the bounded spatial
  function `F=phi_n/phi_0` has centered vacuum mean zero and couples exactly
  to that eigenfunction. Taking arbitrarily large temporal separations
  forces `lambda_n/lambda_0 <= q`, independently of spatial volume.

No claim is made of a new strong-coupling mechanism: classic lattice
strong-coupling spectral gaps predate this project. Recent stronger claimed
thresholds in publicly available work require separate peer-level appraisal.

## Exact certificate and integration

Create a bounded rational certificate for the numerical consequence
`lambda_excited/lambda_ground <= 18 beta`, with a rational **lower** bound
for `-log(18 beta)` from a finite positive atanh series. Every source and
receipt must distinguish an analytically justified theorem statement from
Python's exact *arithmetic replay*; numerical replay does not prove the
functional-analytic input. Extend the PHYSQED evidence bridge with a separate
fail-closed category and tamper-replay test. Preserve all existing scientific
and continuum-problem disclaimers.

## Non-goals and failure boundaries

- No mass gap in physical units along `a -> 0, beta -> infinity`.
- No spectral diagonalization, no gauge fixing, no unproved cutoff removal.
- No assertion that generic unphysical or nongauge-invariant sectors are
  controlled by the physical transfer theorem.
- Do not confuse the arithmetic receipt with Lean or machine-certified
  Dobrushin--Föllmer / Perron--Frobenius functional analysis.
- Never silently accept `beta >= 1/18`, floating input, forged scope flags,
  oversized rationals, or altered source provenance.
