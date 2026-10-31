# PHYSQED v1.2 — Boundary-to-Constraint Verification: Maxwell Positive Control and Harmonic Einstein Obstruction

## Objective

The preceding 18-node shifted Einstein–Maxwell contract checks exact
field equations, energy symmetrizers, uniform domain geometry and
maximal-nonnegative **constraint-system** boundary subspaces. It does
not prove that boundary conditions on the **physical evolution system**
induce the stated boundary restrictions on the constraints. This is
the missing boundary-to-constraint intertwining step.

The present increment supplies two controlled, independently
checkable models:

1. A **positive** six-face Maxwell evolution/constraint/energy
   calculation in shifted Minkowski coordinates with a moving
   physical boundary.
2. A **negative** linearized harmonic Einstein counterexample
   showing that homogeneous metric Dirichlet data for the reduced
   wave equations do **not** alone imply vanishing harmonic gauge
   constraints at the boundary.

These are standard mathematical physics facts recast as explicit
PHYSQED verification obligations; neither is a new general
Einstein–Maxwell IBVP theorem.

## A. Maxwell: exact positive constraint propagation

In inertial Cartesian coordinates \((t,X,Y,Z)\), source-free Maxwell
is

\[
\partial_tE=\nabla\times B,\qquad
\partial_tB=-\nabla\times E.
\]

Divergence of a curl is identically zero. Hence, for
\(C_E=\nabla\cdot E,\ C_B=\nabla\cdot B\),

\[
\partial_t C_E=\partial_t C_B=0.
\]

Therefore *if a smooth solution exists*, its zero Gauss constraints
propagate from zero initial values. This is an exact differential
intertwining identity, not a statement that boundary conditions
alone can repair nonzero initial constraints.

Take the same shifted Minkowski spacetime as the 18-node control,

\[
ds^2=-dt^2+(dx+v\,dt)^2+dy^2+dz^2,\qquad v=1/5,
\quad X=x+vt.
\]

The Maxwell equations in the shifted chart become

\[
(\partial_t-v\partial_x)E=\nabla\times B,\quad
(\partial_t-v\partial_x)B=-\nabla\times E,
\]

and their Gauss constraints satisfy the **advected** equations

\[
(\partial_t-v\partial_x)C_E
=(\partial_t-v\partial_x)C_B=0.
\]

This proves propagation along the flow of the shifted observer
for smooth fields satisfying the Maxwell equations.

## B. Exact moving-boundary flux and maximal nonnegative space

A physical rectangular box fixed in inertial \(X,Y,Z\) has walls
moving at coordinate velocity \(V^x=-v\) in the shifted chart.
For \(U=(E_x,E_y,E_z,B_x,B_y,B_z)\), the Maxwell principal
matrices \(A^j\) are symmetric. With the energy
\(e=\frac12(|E|^2+|B|^2)\), the shifted local law is

\[
\partial_t e-v\partial_xe+\nabla\cdot(E\times B)=0.
\]

For a moving wall with outward normal \(n\) and coordinate normal
velocity \(V_n\), the correct energy boundary quadratic form is
\[
\frac12 U^\top\big(A(n)-V_n I_6\big)U.
\]
Under \(V_n=-v n_x\), this equals \(n\cdot(E\times B)\).
The **moving-domain Reynolds transport term** is essential: using
the flux \(A(n)\) of a fixed shifted-coordinate boundary would
give a different sign on some faces.

For every spatial face, the relative boundary symbol has exact
characteristic polynomial

\[
\det(\lambda I_6-(A(n)-V_nI_6))
=\lambda^2(\lambda^2-1)^2.
\]

It has two positive, two negative and two zero characteristic
directions. A maximal nonnegative subspace is therefore four
dimensional.

For a perfect electric conductor, impose the homogeneous tangential
electric boundary condition \(n\times E=0\). The allowed trace
space has one electric normal component and three magnetic
components, dimension four. On this subspace,

\[
n\cdot(E\times B)=0.
\]

Thus its boundary quadratic form is exactly zero and the trace
space is maximal nonnegative. For any smooth solution in the
fixed inertial box satisfying these conditions and having
compatible initial data,

\[
\mathcal E(t)=\mathcal E(0).
\]

The independent exact verifier computes six 6×6 principal symbols,
the characteristic polynomials, frame ranks, restricted flux matrices
and the two divergence-of-curl identities. Recomputed receipts
refuse tampering. Negative controls include treating the moving
physical walls as stationary at constant shifted \(x\), an
undercomplete boundary frame, floating input and shifts outside
the deliberately scoped benchmark.

**Qualification:** In a full perfect-conductor Maxwell formulation
one may additionally require the normal magnetic constraint to
vanish on the boundary; its preservation is a compatibility result
linked to initial Gauss data and tangential electric data, not an
independent fifth incoming boundary condition imposed on the
symmetric-hyperbolic six-field system. The present engine does
not establish arbitrary-data Maxwell IBVP existence.

## C. The exact reduced-harmonic Einstein obstruction

In Minkowski coordinates with
\(\eta=\operatorname{diag}(-1,1,1,1)\),
let \(\bar h_{\mu\nu}\) be a trace-reversed linearized metric
perturbation. The harmonic constraint is

\[
C_\mu=\partial^\nu\bar h_{\mu\nu}.
\]

The reduced harmonic vacuum Einstein equation is
\(\square\bar h_{\mu\nu}=0\), but a *full* linearized
Einstein solution additionally requires \(C_\mu=0\).

Consider the explicit polynomial field

\[
\bar h_{xx}=t x,\qquad
\bar h_{\mu\nu}=0\quad\text{otherwise}.
\]

Since \(\partial_t^2(tx)=\partial_x^2(tx)=0\), it satisfies
the **complete reduced wave equation**
\(\square\bar h_{\mu\nu}=0\). At the planar boundary \(x=0\),
all metric perturbations obey homogeneous Dirichlet data.

Nevertheless

\[
\boxed{C_x=\partial_x(tx)=t,\qquad
C_x|_{x=0}=t\ne0\quad(t>0).}
\]

The other harmonic constraint components vanish, and
\(\square C_\mu=0\) as expected from differentiation of
the reduced equation. Thus:

\[
\boxed{\text{Reduced wave equations + metric Dirichlet data}
\not\implies \text{harmonic constraint boundary data}.}
\]

This counterexample does **not** have both zero initial
constraint and zero initial constraint time derivative:
\(C_x|_{t=0}=0\) but
\(\partial_tC_x|_{t=0}=1\). It therefore is not a
counterexample to a correctly constructed homogeneous
constraint evolution with fully compatible zero Cauchy data,
and it does not refute established constraint-preserving
Sommerfeld or maximally dissipative formulations.

The negative regression specifically prevents PHYSQED from
promoting a reduced-system boundary check to a full Einstein
constraint-preservation theorem without a verified
boundary-to-constraint differential map.

## D. Link to the existing 18-node PHYSQED reference

The tool
\`v12/linked_maxwell_ibvp.py\` takes the **same source**
\`einstein_maxwell_shift\` object as the existing 18-node
shifted Einstein–Maxwell contract, verifies its exact equations
and restricts to the explicit constant-shift flat vacuum
control. It then runs the shifted Maxwell moving-wall
boundary benchmark with the shift extracted from the model.

**Important geometry distinction:** the six Maxwell walls are
stationary in inertial \(X=x+vt\), and therefore move in shifted
\(x\). The earlier 18-node ADM boundary-energy example used
different **fixed shifted-coordinate** walls. The source
spacetime is the same but the domain/boundary conditions are
not interchangeable. The receipt explicitly records that the
gravitational boundary-to-constraint map is still unproved.

## E. Prior art and next proof gate

Established results include:

- Friedrich and Nagy (1999), *The Initial Boundary Value Problem for
  Einstein's Vacuum Field Equation*, Communications in Mathematical
  Physics 201, 619–655,
  https://users.math.msu.edu/users/gnagy/papers/hFgN99.pdf
- Kreiss and Winicour (2006), *Problems which are well posed in a
  generalized sense with applications to the Einstein equations*,
  Classical and Quantum Gravity 23, S405,
  https://doi.org/10.1088/0264-9381/23/16/S07
- Kreiss, Reula, Sarbach and Winicour (2009), *Boundary Conditions
  for Coupled Quasilinear Wave Equations with Application to Isolated
  Systems*, Communications in Mathematical Physics 289, 1099–1129,
  https://doi.org/10.1007/s00220-009-0788-2
- Babiuc, Kreiss and Winicour (2007), *Constraint-preserving
  Sommerfeld conditions for the harmonic Einstein equations*,
  Physical Review D 75, 044002,
  https://doi.org/10.1103/PhysRevD.75.044002

These references establish that general-relativistic boundary
formulations and harmonic constraint-preserving conditions are
prior art. The next PHYSQED engineering objective is to choose a
specific **linearized generalized-harmonic Einstein evolution**
formulation and implement the differential boundary intertwiner
that maps evolution boundary operators into homogeneous boundary
operators for \(C_\mu\). An exact symbol/normal-mode test should
precede claims about well-posedness or gravitational
constraint-preserving boundaries. A joint Maxwell–Einstein
nonlinear IBVP theorem remains well beyond this benchmark.

## Release status

A standalone local prototype of the Maxwell algebra passed 10/10
exact symbolic tests. The GitHub feature branch contains the
refactored Maxwell, source-link and harmonic obstruction modules,
plus native Python 3.15.2 workflow regression suites. The local
prototype result is **not** a verified successful run of the
native GitHub branch. No merge or stable release is authorized
without successful native and legacy CI.
