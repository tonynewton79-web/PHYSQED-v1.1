# Exact positive-transfer moment obstruction

## Purpose and scope

The SU(2) Wilson pilot and exact beta-zero control produce finite mathematical and numerical quantities, not a mass-gap theorem. This extension supplies an exact, independently replayable obstruction to inferring a uniform physical gap solely from apparently exponential, positive, finite transfer-correlator measurements. It is an **abstract transfer model** and makes no assertion that its operators are Yang--Mills transfer operators.

## Mathematical target

For integers `n >= 3`, set `a=1/2`, `b=1-1/n`, and `w=1/n`, and let

`m_n(t)=(1-w)*a**t+w*b**t`, `t=0,1,...`.

These moments are realized by the positive self-adjoint three-state transfer matrix `diag(1,a,b)` in its vacuum, using a self-adjoint observable that connects the vacuum to the two excitations with amplitudes `sqrt(1-w)` and `sqrt(w)`. Verify exactly:

1. `m_n(0)=1`, `0<=m_n(t)-(1/2)**t<=1/n` for all integer `t>=0`.
2. `m_n(t)*m_n(t+2)-m_n(t+1)**2 = w*(1-w)*(a*b)**t*(b-a)**2 >= 0`.
3. The lowest observable-coupled energy `-log(b)` tends to zero with `n`, even though all correlators are uniformly within `1/n` of the reference `2**(-t)`.

An independent positive finite-period fixture with `T=diag(1,1/2)` and `A` swapping the two states, period `N=4`, has `C_N=(1,10/17,8/17,10/17)`. Its center mass-ratio diagnostic is `5/4`. This tests the finite-period trace formula and reflection-symmetric log-convexity without making any gauge-theory claim.

## Implementation and assurance

- Use only bounded integer parameters and `fractions.Fraction`, with a bit-length cap on general finite-period rational input and no floating arithmetic in certificate production.
- Write a small standalone moment module with exact finite-period fixture and canonical JSON receipt; strict schema-replay rejects edits, booleans in integer fields, out-of-bounds inputs and false physical claims.
- Register a separate abstract-obstruction kind in the existing source-hashed PHYSQED Yang--Mills evidence bridge. Allow only empty provenance metadata or the precise `positive-transfer-abstract` model label, and reject ambiguous duplicate JSON object keys. Do not reclassify it as physical, numerical, formal Lean or Wilson evidence.
- Test hand-derived moments, minors, inequality margins, finite-period trace, malformed receipts and full evidence-ledger replay. Retain the existing test suite.
- Document precisely that positive transfer operators alone do not give uniform spectral lower bounds; this result does not establish the converse, or the existence of continuum Yang--Mills theory.

## Approaches and choice

- **Selected:** an exact bounded constructive counterexample and one trace-formula fixture; this settles a logical obstruction without relying on unverified spectral numerics.
- Simulation-only finite-beta fits cannot exclude weakly coupled low-energy modes.
- A putative finite-beta Wilson transfer gap estimate is the longer mathematical objective; it requires genuinely model-specific inequalities and remains outside this phase.
