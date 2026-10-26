# Yang--Mills continuum-scale bridge: design

## Intent

Identify and mechanize a genuinely physical-scale proof obligation beyond the
finite-spacing `lambda_n/lambda_0 <= 6 beta`, `beta < 1/6` theorem. The
research instrument is for the Wilson SU(2)/PHYSQED programme, not an
assertion that four-dimensional continuum Yang--Mills has been constructed.

## Mathematical target

For a finite-volume nonnegative self-adjoint transfer `T`, with normalized
vacuum eigenvalue one, put `Q=T-P_0` and `r=||Q||<1`. At lattice spacing
`a>0` and time block length `k`, the following are separate *hypotheses*:

1. a certified **full excited-sector** block contraction `||Q^k|| <= U < 1`;
2. a centered gauge-invariant observable `F` with positive block correlator
   `C_F(k) >= c > 0` and vacuum excitation norm squared `||F Omega||^2 <= A`.

For nonnegative transfer spectrum, `c/A <= r^k <= U`. The resulting
physical-scale spectral window is

`-log(U)/(ak) <= -log(r)/a <= -log(c/A)/(ak)`.

Uniform `c/A > 0` and `U < 1`, at a fixed physical block scale `ak -> R > 0`,
would prevent both gap collapse and the entire excited spectrum running to
infinite physical energy. It **does not**, by itself, prove existence of a
nontrivial continuum field theory, operator convergence, continuum overlap,
or the Clay problem. At finite spacing each use needs justified hypotheses,
not user-chosen numbers.

## Approaches

1. Sharpen chordal Dobrushin from `1/3` to `1/4`: a finite-lattice
   improvement, but still bounded coupling far from `beta -> infinity`.
2. **Chosen:** rigorous two-sided physical-block criterion, exact rational
   log enclosures, adversarial replay and three toy transfer families. This
   gives a precise target for future renormalization calculations.
3. Direct continuum proof from the existing finite-lattice tests: excluded
   because the assumptions needed to pass to the limit are absent.

## Boundaries and deliverables

- Create a focused independent module in `research/yang_mills_su2/` using
  Python standard-library `Fraction`; reject floats, bools, extreme inputs,
  invalid spectral intervals and forged claims.
- Expose a *conditional* exact arithmetic receipt and a distinct *abstract
  diagonal-transfer toy* generator. Integrate only its deliberately limited
  evidence kind into the PHYSQED source-hashed ledger.
- Give complete elementary proofs, precise necessary-versus-sufficient
  distinctions, the ultralocal and vanishing-gap obstructions, and what
  actual weak-coupling Wilson data would be needed.
- Keep Newton Solver and EINSTEIN-X Omega at
  `SOURCE_UNAVAILABLE_NOT_EXECUTED` until versioned executable sources and
  independently testable claims become available.
- Preserve existing paper, branch and evidence history. Work on a separate
  branch and do not merge earlier stacked PRs.

## Explicit non-goals

No speculative numerical RG trajectory, invented physical-scale data,
formal Lean proof, novelty claim for elementary spectral inequalities,
nontrivial continuum construction, or assertion of a Yang--Mills mass gap.
