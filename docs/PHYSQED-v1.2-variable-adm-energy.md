# PHYSQED — Variable-Coefficient ADM Constraint-Energy Obligations

## Purpose

This note distinguishes a **symbolically verified local energy-balance
identity** from a **conditional PDE uniqueness theorem**, and from the
unresolved problem of rigorously certifying a specific global
Einstein–matter Cauchy development.

The implementation \`v12/variable_energy.py\` works directly with
a first-order linear symmetric-hyperbolic system

\[
\partial_t U+A^j(t,x)\partial_jU+B(t,x)U=f(t,x)
\]

for at most six fields in 1–3 spatial dimensions. A symmetric matrix
\(S(t,x)\) is supplied, with \(SA^j=(SA^j)^\top\).
The verifier *does not* silently infer that \(S>0\) everywhere.

## Exact product-rule identity

Define

\[
e=\tfrac12U^\top S U,\qquad
F^j=\tfrac12U^\top S A^j U,
\]
\[
R=\partial_t S+\sum_j\partial_j(SA^j)-SB-B^\top S.
\]

For any sufficiently differentiable solution of the system, exact
matrix differentiation yields

\[
\boxed{\partial_t e+\sum_j\partial_jF^j
 =\tfrac12U^\top R U+U^\top S f.}
\]

The code constructs this expression with symbolic component fields
and substitutes **only** the displayed first-order system for their
time derivatives. It then verifies the component identity.
It refuses nonsymmetric \(S\), mismatched matrix shapes and
violations of \(SA^j=(SA^j)^\top\).

A passing identity is not evidence that \(f=0\), that the data
satisfy the Einstein constraints, or that the coefficients meet
the hypotheses for any global energy estimate.

## Conditional quantitative energy estimate

Let the spatial domain \(\Omega\) be periodic, or a smooth bounded
domain with flux boundary conditions. Suppose on \([0,T]\times\Omega\):

1. The coefficients \(S,A^j,B\) and the relevant first derivatives
   are regular and bounded, and \(\Omega\) is compatible with the
   integrations by parts used below.
2. There exist constants \(0<s_* \le s^*<\infty\) with
   \(s_*I\preceq S(t,x)\preceq s^*I\) everywhere.
3. There exists a finite explicit or otherwise independently justified
   \(C\) such that \(R(t,x)\preceq C S(t,x)\) everywhere.
4. The total outward flux is nonnegative:
   \(\int_{\partial\Omega} F^j\nu_j\,dA\ge0\), including the
   periodic case where it vanishes.
5. The source is zero, \(f=0\), or an independently bounded source
   term is incorporated into the inequality.

For the homogeneous system \(f=0\), integration of the local balance
identity then gives

\[
\frac{d}{dt}\mathcal E(t)\le C\mathcal E(t),
\quad \mathcal E(t)=\int_\Omega e(t,x)\,d^3x,
\]

hence

\[
\boxed{\mathcal E(t)\le e^{Ct}\mathcal E(0).}
\]

In particular, an existing smooth solution with zero initial
constraint energy has vanishing constraints throughout the domain
where those hypotheses hold. The existence of a finite \(C\)
can be justified, for example, by a uniform bound on the maximum
eigenvalue of \(S^{-1/2}RS^{-1/2}\).

**PHYSQED does not currently certify the global constant \(C\),
uniform positivity on the full domain, boundary conditions, or
existence of the corresponding nonlinear Einstein solution.**
Those are required input/proof obligations, not implicit consequences
of finitely many symbolic checks or rational witness points.

## Actual shifted-ADM coefficients

For the previously implemented positive extrinsic curvature
\(K_{ij}=(\partial_t h_{ij}-\mathcal L_\beta h_{ij})/(2N)\),
write \(U=(H,M_i)\) for the Hamiltonian and covector momentum
constraints. Assume trace-reversed spatial Einstein evolution and
matter conservation so that the homogeneous constraints obey

\[
\begin{split}
(\partial_t-\mathcal L_\beta)H
 &=2ND_iM^i+4N a_iM^i-2NKH,\\
(\partial_t-\mathcal L_\beta)M_i
 &=\tfrac N2D_iH+NH a_i-NKM_i .
\end{split}
\]

Here \(a_i=D_i\log N\). Expanding the connections and covector Lie
derivative into coordinate partial derivatives gives the matrices
used by \`adm_constraint_matrices\`. In block notation:

\[
S=\mathrm{diag}(1,4h^{ij}),\qquad
A^j=\begin{pmatrix}
-\beta^j&-2Nh^{jk}\\
-\tfrac N2\delta_i^j&-\beta^jI_3
\end{pmatrix}.
\]

The lower-order matrix \(B\) is explicitly

\[
B_{00}=2NK,\quad
B_{0k}=2Nh^{ij}\Gamma^k{}_{ij}-4Na^k,\quad
B_{i0}=-Na_i,\quad
B_{ik}=NK\delta_i^k-\partial_i\beta^k.
\]

These terms include the full lapse acceleration, spatial Christoffel
contraction, trace of the extrinsic curvature and the spatial
gradient of the shift. A missing shift-gradient term can give a
false propagation certificate even if the frozen principal symbol
is correct.

## Two complementary checks

**Independent exact-rational frozen test:** The separate
\`frozen_energy.py\` uses standard-library \`Fraction\` arithmetic
for constant \(S,A^j,B=0\), verifies exact characteristic
polynomials and pointwise flux cancellation. Together with the
explicit periodic integration argument, this establishes a
well-scoped constant-coefficient conditional zero-constraint
propagation result.

**Symbolic variable-coefficient test:** \`variable_energy.py\`
constructs \(S,A^j,B,R\), verifies \(SA^j\) symmetric and the
universal differentiated balance identity. Tests include scalar
transport, a coupled wave system, a failed symmetrizer, flat ADM
and a shifted metric with nonconstant spatial geometry.

These are mathematical verification checks, not proof-assistant
kernel validations. Neither test family substitutes for verifying
the domain hypotheses of a concrete nonlinear Einstein evolution.

## Reproducibility

\`\`\`bash
python -m unittest discover -s projects/physqed/tests \
  -p 'test_physics_v12_frozen_energy.py' -v

python -m unittest discover -s projects/physqed/tests \
  -p 'test_physics_v12_variable_energy.py' -v
\`\`\`

The corresponding Python 3.15.2 GitHub workflow runs both suites
before the slower curved-spacetime symbolic checks.
The release remains a draft until all native tests and inherited
regressions pass.
