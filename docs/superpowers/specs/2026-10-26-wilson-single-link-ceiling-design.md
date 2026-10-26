# Wilson single-link coupling ceiling and cumulative paper design

## Intent

Advance the current Wilson SU(2) argument by asking why a single-link
Dobrushin proof cannot run into weak coupling. Give an explicit finite
four-dimensional Wilson link environment realizing the local Haar-point
sensitivity on every one of 18 neighbors; distinguish a *method ceiling*
from failure of the physical mass gap. Incorporate the previous two-sided
physical-block criterion into the same cumulative paper, with TeX/PDF.

## Mathematical target

On periodic four-dimensional hypercubic tori with every extent at least
three, exhibit for a fixed positive link `e` a central-sign configuration
of its neighboring links in which the six staples sum to zero. For each of
the 18 distinct neighboring links `f`, independently perturb `f` along a
unit quaternion tangent. The single-link conditional field changes with
chordal speed `beta`. The Haar covariance of a unit coordinate is `1/4`;
hence each *optimal* Wasserstein influence coefficient satisfies
`c[e,f] >= beta/4`. Thus the optimal unfixed-gauge single-link Dobrushin
row sum is at least `(9/2)*beta`. Its strict row-contraction criterion is
impossible for `beta >= 2/9`.

This is a geometric obstruction to a particular proof method, not a
statement about the transfer gap. The `2/9` ceiling has already been
discussed in unrefereed Bhattacharjee--Bhattacharya work and is not a
priority claim.

## Approach

- Selected: independent local Wilson sign-background construction,
  unit-quaternion finite-perturbation regression, exact incidence/rational
  arithmetic receipt, and a short analytic proof.
- Rejected: treating the previously published `1/6` sufficient estimate
  as near-continuum evidence; it is only strong coupling.
- Deferred: certified block/renormalization crossing along `beta->infinity`;
  the proof inputs are still unavailable, so no invented scale data.

## Updated cumulative manuscript

Preserve the original eight-page paper and all sections; insert one ninth
section giving the method-ceiling proposition and physical-block criterion.
Update abstract, conclusion and citations; keep at most nine main sections,
short definitions, complete elementary proofs, modest graphics and no
decorative plots. Compile the TeX twice, render every PDF page and inspect
clipping/overlaps. Preserve original source and PDF in the prior PR branch.

## Deliverables and exclusions

- New source/test under `research/yang_mills_su2/`, source-hashed PHYSQED
  evidence kind with explicit noncontinuum flags and adversarial checks.
- Focused exact proof note and updated cumulative `.tex` and `.pdf`.
- Fresh full Yang--Mills and PHYSQED suites; isolated stacked draft PR.
- No claim of proving a new foundational theorem, a continuum field theory,
  Lean kernel formalization, or operating Newton Solver/EINSTEIN-X Omega.
