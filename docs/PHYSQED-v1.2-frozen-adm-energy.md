# PHYSQED — Frozen-coefficient ADM constraint-energy theorem and audit

## Statement and scope

Consider the **homogeneous** ADM constraint propagation system on the
spatial three-torus \(\mathbb T^3\), with a **constant**
positive-definite \(3\times3\) spatial metric \(h_{ij}\), constant
lapse \(N>0\) and constant contravariant shift \(\beta^i\). These are
the frozen-coefficient equations extracted from the trace-reversed
spatial Einstein evolution and matter-conservation assumptions:

\[
(\partial_t-\beta^j\partial_j)H=2N h^{ij}\partial_i M_j,
\qquad
(\partial_t-\beta^j\partial_j)M_i=\frac N2\partial_i H.
\]

This is an independently solvable constant-coefficient linear
periodic model. It does **not** claim that arbitrary curved Einstein
initial data produce global smooth solutions, and it does not cover
nonperiodic boundary conditions or variable \(h,N,\beta\).

### Exact energy theorem

Define the pointwise nonnegative density and periodic energy

\[
e=\frac12H^2+2h^{ij}M_iM_j,\qquad
\mathcal E(t)=\int_{\mathbb T^3}e(t,x)\,d^3x .
\]

Because \(h,N,\beta\) are spatially and temporally constant, multiply
the scalar equation by \(H\) and the \(i\)-th momentum equation by
\(4h^{ij}M_j\). Adding and applying the product rule yields the
**pointwise conservation law**

\[
\boxed{\partial_t e-\beta^i\partial_i e
 -2N\partial_i(Hh^{ij}M_j)=0.}
\]

For a smooth periodic solution, integrate over \(\mathbb T^3\).
Periodic fluxes cancel, giving
\(\mathcal E(t)=\mathcal E(0)\). Since \(h^{ij}\) is positive
definite, \(\mathcal E(0)=0\) implies \(H=M_i=0\)
at every time where the smooth solution exists.

This proves **conditional preservation of zero constraints for this
particular frozen, periodic, smooth model** by elementary energy
conservation. It neither proves global existence of that solution nor
establishes global propagation in general relativity.

### Symmetric-hyperbolic principal part

With \(U=(H,M_1,M_2,M_3)^T\), the principal part is
\[
\partial_t U+A^i\partial_i U=0,\quad
A^i=
\begin{pmatrix}
-\beta^i&-2Nh^{ij}\\
-\frac N2\delta_k{}^i&-\beta^i I_3
\end{pmatrix},
\]
where the top-right block is a row indexed by \(j\) and the
lower-left block a column indexed by \(k\).

Set
\[
S=\operatorname{diag}(1,4h^{ij}) .
\]
Its positive definiteness follows from \(h_{ij}>0\).
One checks \(SA^i=(SA^i)^T\) for every spatial direction.
For a nonzero covector \(\xi_i\), let
\(b=\beta^i\xi_i\) and \(q=N^2h^{ij}\xi_i\xi_j>0\).
The characteristic polynomial is exactly
\[
\boxed{\det(\lambda I-A(\xi))
=(\lambda+b)^2\big((\lambda+b)^2-q\big).}
\]
Therefore the speeds along \(\xi\) are
\(-b\pm\sqrt q\) and \(-b\) (twice).
These real characteristic speeds and the positive symmetrizer
give the standard symmetric-hyperbolic algebraic structure.

## Independent exact arithmetic verifier

The module \`v12/frozen_energy.py\` uses **only the standard-library
Fraction class**, separate from SymPy and PHYSQED geometry.

It implements direct rational elimination to verify positive
definiteness and invert \(h\), constructs the three \(A^i\)
matrices and the symmetrizer, verifies matrix symmetry, computes
characteristic polynomials by exact Faddeev–LeVerrier recurrences,
and evaluates the pointwise flux law on multiple exact rational
coefficient/derivative datasets.

The file emits a deterministic JSON receipt. The output is
**finite exact arithmetic evidence** for the mathematical derivation;
the source code and a receipt hash do not constitute a kernel-checked
formal proof of the continuous PDE theorem. The proof of the
periodic conservation law is the explicit multiplication,
product-rule and integration argument above.

### Positive and refusal controls

Nine separate native unit tests cover flat identity metric, a
non-diagonal positive-definite rational spatial metric with nonzero
shift and lapse, an extra oblique characteristic covector, invalid
signature, nonsymmetric metric, nonpositive lapse, floating-point
inputs, zero wave covector, and the incorrect flux-sign alternative.

\`\`\`bash
PYTHONPATH=projects/physqed python -m unittest discover \
  -s projects/physqed/tests \
  -p 'test_physics_v12_frozen_energy.py' -v
\`\`\`

## Relationship to the general shifted Einstein verifier

\`v12/adm_shift.py\` derives \(H,M_i\) and the off-shell
propagation equations from an arbitrary **supplied**
four-dimensional chart with shift. If trace-reversed spatial
evolution and stress conservation hold, its symbolic identities
produce a variable-coefficient homogeneous constraint system.

\`v12/frozen_energy.py\` is an **independent constant-coefficient
positive control** of that principal part, its wave speeds and exact
periodic flux cancellation. It does not independently certify all
nonconstant lower-order terms, boundary regularity, or a global
Einstein Cauchy evolution.

A future variable-coefficient result needs a quantified interval
for the lapse and spatial metric, bounds on first derivatives and
their time dependence, a specified spatial domain, complete
boundary-flux conditions, and a justified integration/energy
estimate. No extrapolation from this frozen test is allowed.
