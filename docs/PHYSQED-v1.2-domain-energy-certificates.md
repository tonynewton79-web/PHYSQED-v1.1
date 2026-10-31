# PHYSQED — Exact rational-polynomial domain energy certificates

## Research objective and release claim

The next mathematical gate after symbolic energy-balance identities is
to establish **uniform inequalities on an entire declared spacetime
domain**, not at a finite set of sample points. This verifier supplies
a conservative sufficient certificate for such inequalities when all
matrix coefficients are **exact rational polynomials**, and the domain
is a closed box with rational endpoints.

It does **not** certify the full global Einstein Cauchy problem,
arbitrary rational functions, unbounded domains or nonpolynomial
curved-spacetime coefficient fields. In particular, the inverse
spatial metric in the general ADM symmetrizer is typically rational
rather than polynomial; that extension requires a separate
denominator-sign and interval proof.

## Mathematical theorem — Bernstein and Gershgorin bounds

Let \(U\in\mathbb R^n\), \(1\le n\le6\), solve a homogeneous
first-order system on \(D=[t_0,t_1]\times\Omega\):

\[
 \partial_t U + A^j(t,x)\partial_j U+B(t,x)U=0 .
\]

Assume all entries of \(S,A^j,B\) are rational polynomials in the
declared coordinates and \(S=S^\top\),
\(SA^j=(SA^j)^\top\) hold as exact symbolic identities. Define

\[
 R=S_t+\sum_j\partial_j(SA^j)-SB-B^\top S.
\]

For declared exact rational \(s_*>0\) and \(C\ge0\), the engine
constructs two symmetric polynomial matrices

\[
P=S-s_*I,\qquad Q=CS-R .
\]

For each entry \(p_{ij}\) of either matrix, affine-transform the
box \(D\) to \([0,1]^d\) and convert the resulting polynomial
\(\sum_i c_i t^i\) into multivariate Bernstein form. The exact
coefficients are

\[
 b_k=\sum_{i\le k}
 c_i\prod_{j=1}^d
 \frac{\binom{k_j}{i_j}}{\binom{n_j}{i_j}} .
\]

Because Bernstein basis polynomials are nonnegative and sum to one,

\[
 \min_k b_k\le p_{ij}(t,x)\le\max_k b_k
\]

holds **everywhere** in the box. The calculator uses exact
\`fractions.Fraction\` arithmetic for these coefficients.

For a symmetric matrix \(P\), let \(L_{ii}\) denote a certified
lower bound for diagonal entry \(P_{ii}\), and
\(U_{ij}\) a certified upper bound for \(|P_{ij}|\).
If for each row

\[
 L_{ii}\ge \sum_{j\ne i}U_{ij},
\]

Gershgorin's theorem implies \(P(t,x)\succeq0\) on the entire
box. Apply the same test to \(Q\). When both pass, the program has
certified

\[
 \boxed{S\succeq s_*I,\qquad R\preceq CS\quad\text{on }D.}
\]

A failed Gershgorin/Bernstein inequality returns **INCONCLUSIVE**:
these bounds are sufficient, not necessary, and an inconclusive
certificate does not imply the target matrix inequality is false.

## The conditional PDE consequence

Define \(e=\tfrac12 U^\top S U\) and
\(F^j=\tfrac12 U^\top SA^jU\). For an existing sufficiently
regular homogeneous solution, the previously implemented local
energy-balance identity gives

\[
 \partial_t e+\partial_jF^j=\tfrac12 U^\top R U
 \le C e.
\]

If the total outward boundary flux is nonnegative, including a
smooth periodic solution with correctly identified opposing faces,
then \(\mathcal E'(t)\le C\mathcal E(t)\), hence

\[
 \boxed{\mathcal E(t)\le
 e^{C(t-t_0)}\mathcal E(t_0).}
\]

The engine **checks the interior polynomial bounds**. It does
not verify that a smooth solution exists, that the field is
periodic or boundary flux is nonnegative, or that a supplied
Einstein–matter evolution satisfies the source-free constraint
propagation equations. Those appear as separate assumption/status
fields in its receipt.

The \`periodic_solution_assumed\` mode reports whether the
polynomial coefficients are spatially independent (a sufficient
periodic-coefficient check), but the periodicity of the actual
solution and boundary cancellation remain assumptions, not outputs.

## Current public API and a reproducible example

\`\`\`python
import sympy as sp
from v12.domain_energy import certify_domain_energy

t,x = sp.symbols("t x")
S = sp.diag(1+t, 2+t)
A = [sp.diag(1,2)]
B = sp.zeros(2)

receipt = certify_domain_energy(
    (t,x),
    {t:(0,1), x:(0,1)},
    S,A,B,
    coercivity=1,
    growth=2,
    boundary="periodic_solution_assumed"
)
assert receipt["coercivity_bound_proved"]
assert receipt["growth_bound_proved"]
assert not receipt["underlying_smooth_solution_existence_proven"]
\`\`\`

For this example, the exact inequalities hold throughout
\(D=[0,1]\times[0,1]\). It has positive S, constant symmetric
principal matrices, \(R=S_t=I\), and can use
\(s_*=1\), \(C=2\).

## Adversarial checks and limits

The 12-test suite in
\`test_physics_v12_domain_energy.py\` covers:
multivariate Bernstein inclusion on a sampling grid as a sanity
check, an identically zero polynomial, spatially variable S,
time-varying periodic-coefficient example, offdiagonal S,
insufficient coercivity or growth bounds (INCONCLUSIVE),
nonsymmetrizable principal matrices, nonpolynomial input, floats,
invalid domains and altered-receipt replay.

Exact arithmetic tests are an *implementation check* of the
coefficient formula; the mathematics of the enclosure follows
from the explicit Bernstein representation and the Gershgorin
inequality, not from sampling.

This API accepts **programmatically constructed, trusted SymPy
expressions**, not arbitrary user-entered Python or free-form
\`sympify\` strings. The separate typed JSON system must be used
when accepting externally supplied models.

The algorithm deliberately limits polynomial degree and matrix
dimensions to avoid unsafe unbounded symbolic expansion.
It does not perform adaptive subdivision. Stronger matrices may
be positive but fail this conservative certificate.

## Further verification targets

1. Rational-function extension with denominator-sign certificates
   for the ADM inverse metric and lapse, rather than silently
   rationalizing them.
2. Exact finite-box inequality enclosures with adaptive subdivision,
   Bernstein degree elevation or interval LDL to reduce Gershgorin
   conservatism.
3. Typed JSON domain declarations with explicit coordinate units,
   boundaries and coefficient-generation provenance.
4. A separate boundary integration and trace theorem certificate
   for periodic, maximally dissipative or other admissible PDE
   boundaries.
5. Formalize the bounded-domain energy implication and its analytic
   premises inside a suitable proof assistant.

Native Python **3.15.2** CI and inherited regression checks remain
release gates. The feature branch must not be described as a stable
formal proof kernel before those succeed.
