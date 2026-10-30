# PHYSQED v1.2 — Nonzero ADM Shift and Constraint Propagation

## Objective

Extend the typed Einstein–Maxwell verifier from zero ADM shift to
a full local \(3+1\) decomposition with lapse \(N\), spatial metric
\(h_{ij}\) and contravariant shift \(\beta^i\). Derive the Einstein
Hamiltonian/momentum constraints from the same spacetime metric and
matter, and independently verify the **off-shell contracted-Bianchi
constraint propagation identities**. Identify the trace-reversed
spatial evolution equations that produce a symmetric-hyperbolic
constraint subsystem.

The implementation checks mathematical identities under explicit
regularity and domain assumptions. It is not a proof of global Einstein
evolution, nonlinear existence or long-time PDE regularity.

## Conventions and exact geometric decomposition

Work in signature \((-+++)\), spacetime coordinates \((t,x^i)\),
positive lapse and positive-definite \(h_{ij}\). Set

\[
g_{00}=-N^2+h_{ij}\beta^i\beta^j,\quad
g_{0i}=h_{ij}\beta^j,\quad g_{ij}=h_{ij},
\qquad
n^\mu=N^{-1}(1,-\beta^i).
\]

The *positive* extrinsic-curvature convention carried over from
the previous PHYSQED zero-shift contract is

\[
K_{ij}=\frac{1}{2N}
   \bigl(\partial_t h_{ij}-{\cal L}_\beta h_{ij}\bigr),\qquad
({\cal L}_\beta h)_{ij}
=\beta^k\partial_kh_{ij}
+h_{ik}\partial_j\beta^k+h_{kj}\partial_i\beta^k.
\]

This \(K\) is the opposite sign of the most common ADM convention.
All Codazzi/momentum signs below follow the *positive* convention.

For electromagnetic curvature \(F=dA\), Maxwell stress tensor
\(T_{\mu\nu}=F_{\mu\alpha}F_\nu{}^\alpha
-\frac14g_{\mu\nu}F_{\alpha\beta}F^{\alpha\beta}\),
and Einstein residual
\(E_{\mu\nu}=G_{\mu\nu}+\Lambda g_{\mu\nu}-\kappa T_{\mu\nu}\), define

\[
\rho=T_{\mu\nu}n^\mu n^\nu,\qquad
j_i=T_{\mu i}n^\mu,\qquad
H={}^3R+K^2-K_{ij}K^{ij}-2\Lambda-2\kappa\rho,
\]
\[
M_i=D_jK^j{}_i-D_iK-\kappa j_i .
\]

The **off-shell projection identities** are

\[
\boxed{H=2E_{\mu\nu}n^\mu n^\nu,\qquad
M_i=E_{\mu i}n^\mu.}
\]

They must hold whether or not Einstein's equations are satisfied.
Passing these bridge identities alone never establishes a solution.

## Exact Bianchi propagation

Let \(C_{ij}=E_{ij}\) denote the spatial Einstein residual, and
\(a_i=D_i\ln N\) denote normal acceleration. Write
\[
J_n=n^\nu\nabla^\mu E_{\mu\nu},
\qquad J_i=\nabla^\mu E_{\mu i}.
\]
The contracted Bianchi identity with constant \(\Lambda,\kappa\)
gives
\[
J_\nu=-\kappa\nabla^\mu T_{\mu\nu}.
\]
For the scalar constraint \(H\), spatial covector constraint \(M_i\),
and \(K=h^{ij}K_{ij}\), the off-shell identities are
\[
(\partial_t-{\cal L}_\beta)H =
2N\!\left(D_iM^i+2a_iM^i-\frac K2 H
-K^{ij}C_{ij}-J_n\right),
\]
\[
(\partial_t-{\cal L}_\beta)M_i =
N\!\left(-KM_i+\frac H2a_i+D^jC_{ji}
+a^jC_{ji}-J_i\right).
\]

The lapse acceleration and Lie-derivative terms are essential.
Simply writing \(\partial_t h_{ij}/(2N)\) for \(K_{ij}\) when
\(\beta^i\ne0\) is incorrect.

If **full spatial Einstein** \(C=0\) and matter conservation
\(J=0\) hold, these equations are homogeneous in \(H\) and \(M\).
The stronger formulation for a symmetric-hyperbolic propagation
system uses trace-reversed spatial evolution:

\[
Q_{ij}=C_{ij}-\frac H2 h_{ij}=0.
\]

For four-dimensional Einstein residuals, \(Q=0\) is equivalent
to the spatial trace-reversed Ricci-form field equations, but
it does **not** by itself imply the full Einstein equations.

With general \(Q\), the exact off-shell equations become
\[
(\partial_t-{\cal L}_\beta)H =
2N\!\left(D_iM^i+2a_iM^i-KH
-K^{ij}Q_{ij}-J_n\right),
\]
\[
(\partial_t-{\cal L}_\beta)M_i =
N\!\left(-KM_i+Ha_i+\tfrac12D_iH
+D^jQ_{ji}+a^jQ_{ji}-J_i\right).
\]
Each equality is checked as an exact component residual.

When \(Q=0\), \(\nabla^\mu T_{\mu\nu}=0\) and the coupling and
cosmological constant are spacetime constants, the system closes:

\[
\boxed{
\begin{aligned}
(\partial_t-{\cal L}_\beta)H
 &=2N D_iM^i+4N a_iM^i-2NKH,\\
(\partial_t-{\cal L}_\beta)M_i
 &=\frac N2 D_iH +NH a_i-NK M_i .
\end{aligned}}
\]

## Symmetric-hyperbolic energy gate

For \(U=(H,M_1,M_2,M_3)\), the principal matrices \(A^i\)
of the closed system (written as
\(\partial_t U + A^i \partial_i U =\text{lower order}\))
admit the pointwise positive symmetrizer

\[
\boxed{\mathcal S=\mathrm{diag}(1,4h^{ij}).}
\]

Here the \((H,M)\) off-diagonal blocks of \(A^i\) are
\(-2Nh^{ij}\) and \(-\frac N2\delta_i^j\), while the shift
contributes \(-\beta^iI\). The source checks
\(\mathcal S A^i=(\mathcal S A^i)^T\) symbolically in all
three spatial directions. Positive definiteness follows
from positive-definite \(h\), **provided it holds throughout
the intended domain**, not only at the test witnesses.

A standard conditional energy argument takes
\[
e=\frac12H^2+2h^{ij}M_iM_j .
\]
For smooth bounded coefficients on compact spatial slices
without boundary, or with boundary conditions controlling the
energy flux, integration by parts and Gronwall's inequality
give \(E(t)\le E(0)e^{Ct}\) for an appropriate finite
coefficient bound \(C\). Thus **zero initial constraints
remain zero as long as the stated trace-reversed evolution,
conservation and regularity hypotheses hold**. This is a
conditional PDE uniqueness consequence of the verified
principal-part structure and standard energy method—not
a computer-certified global spacetime solution.

## What PHYSQED actually checks

The shifted backend currently emits **18 component gates**:

- Unit normal and orthogonality to the slice
- Maxwell Bianchi, source-free Maxwell dynamics, stress conservation
- Full Einstein dynamics
- Spatial Einstein and trace-reversed spatial evolution residuals
- Hamiltonian and momentum constraints
- Gauss and Codazzi off-shell projection bridges
- Einstein–stress Bianchi consistency
- Two projected off-shell Bianchi propagation bridges
- Two trace-reversed symmetric-hyperbolic propagation bridges
- Principal-symbol symmetrizer identity

Independent exact rational metric 2-jet curvature is also compared
in four and three dimensions at declared regular witnesses.
The "symmetric hyperbolic" gate proves a finite symbolic matrix
identity; it cannot by itself certify all conditions needed by
the infinite-dimensional PDE energy theorem.

The structured input kind is
\`einstein_maxwell_shift\` and the supported claim is
\`linked_shifted_adm_propagation\`. Input declarations must
include a 3×3 spatial metric, a positive lapse, a rank-1 upper-index
spatial shift, Maxwell one-form, geometrized-length coordinate and
parameter dimensions, valid witness values, source and assumptions.

The shift dimensions are \([\beta^i]=L^{d_i-d_0}\) when the
coordinate dimensions are \([x^a]=L^{d_a}\).
The physical-type checker enforces this **before** evaluating
the field equations. The unit type system is *geometrized
length*, not unrestricted SI dimensions.

## Reproducible examples

- \`einstein_maxwell_shifted_flat.json\`:
  Minkowski spacetime in a time-dependent nonzero-shift chart
  with \(\beta^x=t/\tau\). Exact metric curvature, all 18
  nodes and conditional closure are expected to pass.
- \`einstein_maxwell_shifted_offshell.json\`:
  a varying spatial metric and nonzero shift; Gauss/Codazzi
  and Bianchi propagation bridge identities should pass,
  while Einstein equations fail.
- \`einstein_maxwell_shifted_invalid_dimension.json\`:
  same flat spacetime, but a shift component with the wrong
  physical dimension. It must be **refused before physics**.

\`\`\`bash
PYTHONPATH=projects/physqed python -m v12.typed_cli \
  --input projects/physqed/examples/typed/einstein_maxwell_shifted_flat.json \
  --plan

PYTHONPATH=projects/physqed python -m v12.typed_cli \
  --input projects/physqed/examples/typed/einstein_maxwell_shifted_flat.json \
  --output shifted_adm_receipt.json
\`\`\`

Native test suites:
\`test_physics_v12_adm_shift.py\` and
\`test_physics_v12_typed_shift.py\`.

## Release and claim boundary

These source changes are a research-grade *candidate verification
implementation*. The GitHub-hosted Python 3.15.2 workflows are the
release gate. Do not assert that CI passed until an actual successful
run is observed, and do not merge the branch into main prematurely.

Not implemented: unrestricted spacetime foliation topology, complete
physical SI units, tensor-index inference for arbitrary expressions,
non-Abelian stress coupling, full theorem-prover-kernel certification,
boundary regularity proof or global-in-time existence of Einstein
solutions. Geometric positivity at a finite set of witnesses does not
prove positivity everywhere in the domain.
