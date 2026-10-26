# Exact SU(2) character diagnostics and the continuum obstruction

For positive rational β, the modified Bessel function of integer order
ν≥0 has the convergent positive series

\[
I_\nu(\beta)=\sum_{k=0}^\infty
\frac{(\beta/2)^{2k+\nu}}{k!(k+\nu)!}.
\]

Writing the k-th summand as t_k, the exact ratio

\[
\frac{t_{k+1}}{t_k}=\frac{(\beta/2)^2}{(k+1)(k+\nu+1)}
\]

decreases with k. After terms k=0,…,N−1, if
q_N=(β/2)²/((N+1)(N+ν+1))<1, the omitted tail is between 0 and
t_N/(1−q_N). Every quantity is a rational number, so these are exact
finite positive-series enclosures, not floating-point error estimates.
Propagating positive interval arithmetic gives bounds for
c(β)=I₂(β)/I₁(β). Only when these establish 0<c<1 do we enclose
g(β)=−log c(β).

For rational 0<q≤1, let z=(1−q)/(1+q). Then

\[
-\log q=2\sum_{k=0}^\infty\frac{z^{2k+1}}{2k+1}.
\]

After m terms, the omitted positive tail is at most
2z^(2m+1)/((2m+1)(1−z²)); monotonicity propagates rational bounds
through the character-ratio interval. A separate implementation based
on SymPy's besseli/log serves as a numerical cross-check in tests. The
receipt verifier **recomputes** exact Fraction bounds, never trusts the
input's reported verified field or SHA digest.

Example commands from the repository root:

    python -m research.yang_mills_su2.character_cli --beta-num 2 --beta-den 1 --bessel-terms 12 --log-terms 12 --output /tmp/ym-character-receipt.json
    python -m research.yang_mills_su2.character_cli --verify /tmp/ym-character-receipt.json

The finite SU(2) character-gap asymptotic βg(β)→3/2 is a known consequence
of the [NIST DLMF §10.40(i) expansion](https://dlmf.nist.gov/10.40.E1):
I_ν(β)=e^β/(2πβ)^(1/2)·[1−(4ν²−1)/(8β)+O(β^(−2))]. Thus
I₂/I₁=1−3/(2β)+O(β^(−2)) and −β log(I₂/I₁)→3/2.
**It is not proved by checking a
finite collection of rational β values**. The exact family
a_n=1/n, δ_n=1/n² has every finite gap δ_n>0 but δ_n/a_n=1/n→0.
It refutes the logical implication from pointwise finite positivity to
a uniform physical gap, without purporting to model the Yang–Mills spectrum.

None of these statements constructs the four-dimensional continuum
quantum theory, proves its full physical spectrum has a gap, or
discharges Osterwalder–Schrader axioms, nontriviality or all compact
simple gauge groups. Their appropriate role is a regression test and
certified local mathematical component in a larger research programme.

The v0.1 receipt schema deliberately limits β numerator/denominator to
24 bits, Bessel terms to 32, log terms to 24, and every serialized rational
numerator/denominator to 11,000 bits. Larger workloads fail explicitly
before generating an invalid JSON receipt; no process-global Python
integer-to-string safety limit is disabled. The exact mathematical
bound functions remain independently usable outside this receipt domain.
