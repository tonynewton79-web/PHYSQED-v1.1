# PHYSQED v1.2 — Exact Rational-Function Domain Certification for ADM Energy Bounds

## Objective and precise scope

This extension advances PHYSQED's domain energy system from exact rational **polynomial** coefficient matrices to exact **rational-function** coefficient matrices. That is needed for the spatial inverse metric, lapse-dependent terms, connection coefficients and the lower-order matrices in a general 3+1 Einstein constraint propagation system.

Given an explicitly declared *compact rational coordinate box* \(D\), a first-order linear homogeneous system

\[
\partial_t U+A^j(t,x)\partial_j U+B(t,x)U=0
\]

and a symmetric symmetrizer \(S(t,x)\), the tool checks

\[
S A^j=(SA^j)^\top,\qquad
S(t,x)\succeq s_*I,\qquad R(t,x)\preceq C S(t,x)
\quad\text{for all }(t,x)\in D,
\]

where

\[
R=S_t+\sum_j\partial_j(SA^j)-SB-B^\top S .
\]

A **PASS** certifies these *interior inequalities for the explicitly supplied rational mathematical functions*, subject to correct identification of their original source-domain restrictions. It does not prove full Einstein field equations, nonlinear Cauchy evolution, a global geometric chart, boundary conditions or PDE well-posedness.

## Why denominator signs are essential

For a rational entry \(f=p/q\), both \(p\) and \(q\) must be exact rational-coefficient polynomials in declared coordinate variables. We first calculate rigorous multivariate Bernstein enclosures

\[
p(D)\subseteq[p_-,p_+],\qquad q(D)\subseteq[q_-,q_+].
\]

If \(q_->0\) or \(q_+<0\), then \(q\) has **one strict sign** throughout the entire closed box and cannot vanish. In that case,

\[
f(D)\subseteq
\left[
\min_{\substack{a\in\{p_-,p_+\}\\b\in\{q_-,q_+\}}}\frac ab,\quad
\max_{\substack{a\in\{p_-,p_+\}\\b\in\{q_-,q_+\}}}\frac ab
\right].
\]

Every bound and division is evaluated with exact \`fractions.Fraction\` arithmetic. If the denominator interval intersects zero, the result is **INCONCLUSIVE**; the program never divides by an uncertified denominator.

The same procedure is applied to **every received coefficient entry** of \(S\), \(A^j\) and \(B\) before inspecting derived matrices. This prevents a pole from being hidden by a cancellation when constructing \(SA^j\), taking spatial derivatives, or forming \(R\).

### Original expression-domain caveat

A symbolic language may erase a singularity **before** the compiler receives an expression, e.g. by turning \((t-\frac12)/(t-\frac12)\) into 1. No mathematical check of the final object alone can recover the lost source-domain restriction. The API therefore accepts optional \`denominator_guards\`, which must each have a separately certified strict nonzero sign, and a caller declaration \`original_expression_denominators_complete\`. The latter is recorded as a **caller assertion**, never an independently proven fact.

For publication-level input, retain the original expression tree and list every denominator whose nonvanishing is required, including factors that might simplify away. Future secure typed ingestion should extract these guards *before simplification* automatically.

## Matrix positivity with exact interval enclosures

Define

\[
P=S-s_* I,\qquad Q=C S-R .
\]

Both are symmetric rational matrices under the supplied principal-symbol assumptions. On each box, the checker bounds every diagonal component of \(P,Q\) below and the absolute value of each off-diagonal component above. It uses the sufficient row conditions

\[
\underline{P}_{ii}\ge
\sum_{j\ne i}\overline{|P_{ij}|},
\qquad
\underline{Q}_{ii}\ge
\sum_{j\ne i}\overline{|Q_{ij}|}.
\]

Gershgorin's theorem gives \(P,Q\succeq0\) **everywhere on the certified box**, hence the desired global-in-box matrix inequalities. Because Gershgorin bounds are sufficient rather than necessary, a failed row test is *inconclusive*, not a counterexample.

## Exact adaptive dyadic subdivision

A polynomial can be strictly positive even when its global Bernstein coefficients include negatives. The verifier optionally bisects a failing box along a declared coordinate, recursively to a bounded depth. Child boxes cover their parent exactly, and the parent is certified **only when every leaf is certified**.

For example,

\[
q(t)=t^2-t+\frac{3}{10}
\]

is positive throughout \([0,1]\) but its degree-2 Bernstein coefficients on the whole interval are \((3/10,-1/5,3/10)\), yielding an inconclusive global sign test. On \([0,\frac12]\) and \([\frac12,1]\), all Bernstein coefficients are positive; one exact bisection establishes the strict sign.

Cells, source denominator checks, guard signs, matrix bounds, rational row margins and every leaf status are retained in the deterministic receipt. There is a finite degree, matrix rank, AST and subdivision budget.

## Actual shifted-ADM example

Define, in coordinates \((t,x,y,z)\),

\[
h_{ij}=\mathrm{diag}(1+t,1,1),\qquad
N=1+t,\qquad
\beta^i=(1/5,0,0),\qquad 0\le t,x,y,z\le1 .
\]

PHYSQED's \`adm_constraint_matrices\` derives the full principal and lower-order matrices from this supplied \(h,N,\beta\). Its symmetrizer contains \(4/(1+t)\), and lapse and extrinsic-curvature factors introduce further rational denominators.

For this **specified coefficient system**, exact Bernstein/Gershgorin calculations certify

\[
\boxed{S\succeq I,\qquad R\preceq 12S}
\]

on the entire four-dimensional box, with the source denominator \(1+t\) strictly positive. The certificate also verifies the received coefficient denominators and the principal symmetrizer identities.

This is a nontrivial rational-ADM **constraint-propagation coefficient bound**. It does **not** mean that the chosen \(h,N,\beta\) satisfy Einstein equations or that the constraint PDE has a smooth solution with arbitrary data. The spatial periodicity or boundary flux of actual solutions remains separately assumed.

## Proof consequence and remaining hypotheses

For a sufficiently smooth *existing* solution with homogeneous constraint source \(f=0\), the independently checked local energy identity reads

\[
\partial_t e+\partial_jF^j=\tfrac12 U^\top R U,\qquad
e=\tfrac12U^\top S U,\quad F^j=\tfrac12U^\top SA^jU .
\]

Under \(R\preceq C S\), the right side is bounded above by \(Ce\). If boundary contributions have nonnegative total outward flux (or periodic cancellation), integration yields

\[
\mathcal E(t)\le \mathcal E(t_0)\,e^{C(t-t_0)} .
\]

Thus zero initial constraints remain zero **conditional on** the smooth solution and the declared boundary, evolution and source hypotheses. Those hypotheses are **not** inferred from a source-free algebraic matrix check.

The present verifier only supports rational functions in up to four declared coordinates, a compact rational rectangular domain, up to six state components, bounded total degree, a small exact dyadic refinement depth, and trusted programmatic SymPy input. It is not an arbitrary-coordinate or full SI dimensional-analysis engine.

## Executable commands

\`\`\`bash
python -m unittest discover -s projects/physqed/tests \
  -p 'test_physics_v12_rational_energy.py' -v
\`\`\`

Programmatic example:

\`\`\`python
import sympy as sp
from v12.variable_energy import adm_constraint_matrices
from v12.rational_energy import certify_rational_domain_energy

t,x,y,z=sp.symbols("t x y z")
S,A,B=adm_constraint_matrices(
    (t,x,y,z), sp.diag(1+t,1,1), 1+t,
    [sp.Rational(1,5),0,0])

receipt=certify_rational_domain_energy(
    (t,x,y,z),
    {t:(0,1),x:(0,1),y:(0,1),z:(0,1)},
    S,A,B,coercivity=1,growth=12,
    denominator_guards=[1+t],
    original_expression_denominators_complete=True,
    boundary="periodic_solution_assumed")
\`\`\`

The 14-test regression set includes this exact ADM example, a genuine pole, a pole obscured by a derived-matrix cancellation, a strict negative denominator, source-guard checks, a positive but Bernstein-inconclusive denominator rescued by bisection, floating/nonrational failures, principal symmetry, insufficient growth, undeclared parameters and tampered-receipt replay.

## Next frontier

The most valuable advancement is to construct a **typed rational expression AST that retains original denominator factors before SymPy simplification**, then incorporate exact box-wise positivity of the ADM lapse, eigenvalue bounds for the entire spatial metric, and domain boundary/flux certificates. This would allow stronger integrated conditions for a user-supplied curved-spacetime model.

Native Python 3.15.2 GitHub CI and inherited regression checks remain necessary before promoting the feature branch as a stable release.
