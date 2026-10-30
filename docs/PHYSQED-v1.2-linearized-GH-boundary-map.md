# Linearized Generalized-Harmonic Einstein Boundary-to-Constraint Map

## Objective and claim boundaries

This note implements the next verification gate beyond the Maxwell
positive control and the elementary harmonic Dirichlet obstruction.
It treats a **specific** vacuum, trace-reversed, linearized harmonic
Einstein system on the Minkowski half-space \(x\ge0\), with a planar
boundary at \(x=0\). This is the zero-source, flat-background special
case of the generalized-harmonic gauge framework, not an arbitrary
nonlinear gauge source or an Einstein–Maxwell IBVP.

PHYSQED computes a **differential constraint intertwiner**, a
ten-by-ten Laplace–Fourier boundary matrix and determinant,
and explicit initial/corner compatibility tests. The relevant
generalized-harmonic boundary ideas are established prior art.

A successful algebraic result does **not** establish a uniform
Kreiss–Lopatinski boundary estimate at glancing frequencies, all
higher-order compatibility, nonhomogeneous boundary-data solvability,
curved variable-coefficient energy estimates or nonlinear Einstein
initial-boundary well-posedness.

## Field equations and differential constraint propagation

Use \(\eta=\mathrm{diag}(-1,1,1,1)\). Let
\(\bar h_{\mu\nu}=\bar h_{\nu\mu}\) be the trace-reversed
metric perturbation and define the harmonic constraints

\[
C_\nu=\partial^\mu\bar h_{\mu\nu}.
\]

The **reduced** vacuum linearized equations are

\[
\Box\bar h_{\mu\nu}=0,\qquad
\Box=-\partial_t^2+\partial_x^2+\partial_y^2+\partial_z^2 .
\]

Commutativity of flat partial derivatives gives the full,
off-shell differential intertwiner

\[
\boxed{\Box C_\nu
=\partial^\mu(\Box\bar h_{\mu\nu}).}
\]

For the linearized Einstein tensor,

\[
\boxed{
\delta G_{\mu\nu}
=\tfrac12[-\Box\bar h_{\mu\nu}
+\partial_\mu C_\nu+\partial_\nu C_\mu
-\eta_{\mu\nu}\partial^\alpha C_\alpha].
}
\]

Thus a reduced wave solution is a full vacuum linearized Einstein
solution if it also has \(C_\nu=0\). PHYSQED checks these as
**separate** components, never conflating the reduced wave
equations with full Einstein dynamics.

## A specific set of ten boundary operators

Write \(a,b\in\{t,y,z\}\) for indices tangent to the boundary.
For the six independent components \(\bar h_{ab}\), impose

\[
D_-\bar h_{ab}|_{x=0}=0,\quad
D_-=\partial_t-\partial_x.
\]

For the four remaining boundary rows, impose the actual
harmonic constraint conditions

\[
\boxed{C_\nu|_{x=0}
=\left[-\partial_t\bar h_{t\nu}
+\partial_x\bar h_{x\nu}
+\partial_y\bar h_{y\nu}
+\partial_z\bar h_{z\nu}\right]_{x=0}=0.}
\]

This is a **triangular** coupling of the metric normal
derivatives to the tangential derivatives of metric components.
Unlike prescribing ten unrelated metric Sommerfeld conditions,
it explicitly controls the four gauge constraints at the
boundary. A constant-gauge source has been set to zero in this
linear benchmark.

## Laplace–Fourier normal-mode test

Consider a homogeneous decaying normal mode

\[
\bar h_{\mu\nu}
 = H_{\mu\nu} e^{st+i\eta y+i\zeta z-\kappa x},\qquad
 \kappa^2=s^2+\eta^2+\zeta^2,\quad\Re\kappa>0,\quad\Re s>0,
\]

where \(\eta,\zeta\) are real transverse frequencies.
Order the ten fields by six tangent-tangent variables, followed
by \((tx,xy,xz,xx)\). The six Sommerfeld boundary rows have
diagonal factor \(s+\kappa\). On the remaining four fields,
the constraint rows have a triangular normal block
with diagonal \(-\kappa\). Exact symbolic elimination gives

\[
\boxed{\det B(s,\kappa,\eta,\zeta)
=\kappa^4(s+\kappa)^6.}
\]

For \(\Re s>0\) with the decaying branch, neither
\(\kappa=0\) nor \(s+\kappa=0\) is possible: if
\(\kappa=0\), then \(s^2=-\eta^2-\zeta^2\), contradicting
\(\Re s>0\); and \(s+\kappa=0\) contradicts the positive
real parts. Therefore the homogeneous boundary symbol has
no nonzero decaying solution for the strictly right-half-plane
normal-mode problem.

**Do not promote this to a uniform boundary stability theorem.**
The determinant has vanishing factors at the glancing
\(\kappa=0\) limit. A complete Kreiss–Lopatinski bound
requires quantitative normalized resolvent estimates, and
is not obtained merely by exhibiting a nonzero determinant
when \(\Re s>0\).

## Constraint energy uniqueness: explicit assumptions

The four constraints solve \(\Box C_\nu=0\).
If a sufficiently regular finite-energy reduced-system
solution satisfies the four homogeneous \(C_\nu=0\) boundary
conditions and its initial Cauchy constraints satisfy

\[
C_\nu(0,x,y,z)=0,\qquad
\partial_tC_\nu(0,x,y,z)=0,
\]

the standard scalar wave energy identity on the half-space
(with controlled decay or transverse periodicity) has no
boundary flux, because \(\partial_t C_\nu=0\) on the boundary.
Hence constraint energy remains zero, so \(C_\nu=0\)
throughout the period for which the smooth solution exists.
The full linearized Einstein equations then follow from the
displayed expression for \(\delta G\).

This is a **conditional constraint-preservation/uniqueness
argument**, not proof that arbitrary initial/boundary data
admit a smooth reduced Einstein solution.

## Initial and first temporal corner compatibility

Given initial metric data
\(f_{\mu\nu}=\bar h_{\mu\nu}|_{t=0}\) and velocities
\(g_{\mu\nu}=\partial_t\bar h_{\mu\nu}|_{t=0}\),
both symmetric, compute from their spatial derivatives

\[
\begin{aligned}
C_\nu|_0
&=-g_{t\nu}+\partial_i f_{i\nu},\\
\partial_t C_\nu|_0
&=-\Delta f_{t\nu}+\partial_i g_{i\nu}.
\end{aligned}
\]

(The second identity uses the **reduced wave equation** to
replace \(\partial_t^2\bar h\).)
PHYSQED tests both expressions **on the full initial slice**.
Their restrictions to \(x=0\) provide the first two
harmonic-boundary corner conditions.

For each of the six tangential metric components, it additionally
tests at the corner

\[
g_{ab}-\partial_x f_{ab}=0,\qquad
\Delta f_{ab}-\partial_x g_{ab}=0
\quad\text{at }x=0.
\]

These are the temporal boundary compatibility conditions of
orders zero and one. Higher orders may be necessary for higher
regularity, and are not certified by this first-stage gate.

## Positive reference family and two negative controls

For the nontrivial trace-reversed plane wave

\[
\boxed{\bar h_{yz}=F(t+x),\qquad
\bar h_{\mu\nu}=0\text{ otherwise},}
\]

all ten reduced wave equations, harmonic constraints,
tangential Sommerfeld conditions and initial/corner identities
vanish exactly for any sufficiently differentiable \(F\).
If \(F\in C_c^\infty((0,\infty))\) and the transverse directions
are periodic on \(\mathbb T^2\), the corresponding initial
wave data have finite energy. The symbolic certificate
tests the differential expressions, **not** the external
compact-support claim.

The earlier obstruction
\(\bar h_{xx}=tx\), all others zero, solves the reduced wave
equation but has \(C_x=t\). Although \(C_x|_{t=0}=0\),
it has \(\partial_tC_x|_{t=0}=1\), and is rightly rejected.

Another independent case \(\bar h_{yz}=t\) has
\(C_\nu=0\) but violates the outgoing metric Sommerfeld condition
at the corner. Thus checking the harmonic constraints alone
is insufficient for the full ten-row boundary contract.

A sharper negative control refutes the shortcut
"apply Sommerfeld independently to all ten metric components":

\[
\bar h_{xx}=y^2+t^2+2tx.
\]

Here all reduced wave equations and all ten componentwise
Sommerfeld conditions at \(x=0\) hold, but

\[
C_x|_{x=0}=2t,\qquad
(D_-C_x)|_{x=0}=2
 =(\partial_y^2+\partial_z^2)\bar h_{xx}|_{x=0}.
\]

This exhibits the **tangential derivative obstruction** to
an uncoupled metric-to-constraint boundary inference.

## Implementation and replay

The source module
\`projects/physqed/v12/gh_boundary_map.py\` provides:

- \`general_differential_intertwiner\`: exact identity on ten
  independent formal fields;
- \`normal_mode_symbol\`: 10×10 symbolic operator matrix and factorization;
- \`linearized_einstein\` and \`harmonic_constraint\`;
- \`first_corner_gate\`: initial and first two temporal corner levels;
- \`certify_explicit_linearized_metric\`: checks a supplied exact
  mathematical metric perturbation and hashes the receipt;
- \`naive_sommerfeld_counterexample\`: adversarial boundary inference;
- \`certify_symbol_and_controls\`: scoped cumulative gate.

The CLI only accepts pre-defined benchmark cases, not free-form
Python or SymPy text:

\`\`\`bash
PYTHONPATH=projects/physqed python -m v12.gh_boundary_cli \
  --case all --output gh_boundary_receipt.json

python -m unittest discover -s projects/physqed/tests \
  -p 'test_physics_v12_gh_boundary_map.py' -v
\`\`\`

The local independent prototype passed **18/18 exact regression
tests under Python 3.13.5 / SymPy 1.14.0**. The actual
GitHub implementation is subject to native Python 3.15.2 CI
and inherited regression tests before release.

## Prior art and next mathematical gate

These findings fit established harmonic-gravity IBVP theory.
Relevant references include:

- Szilágyi, Schmidt and Winicour, *Boundary conditions in
  linearized harmonic gravity*, Phys. Rev. D 65, 064015 (2002),
  https://doi.org/10.1103/PhysRevD.65.064015.
- Kreiss and Winicour, *Problems which are well posed in a
  generalized sense with applications to the Einstein equations*,
  Class. Quantum Grav. 23, S405 (2006),
  https://doi.org/10.1088/0264-9381/23/16/S07.
- Babiuc, Kreiss and Winicour, *Constraint-preserving Sommerfeld
  conditions for the harmonic Einstein equations*, Phys. Rev. D 75,
  044002 (2007), https://doi.org/10.1103/PhysRevD.75.044002.
- Kreiss, Reula, Sarbach and Winicour, *Boundary Conditions for
  Coupled Quasilinear Wave Equations with Application to Isolated
  Systems*, Commun. Math. Phys. 289, 1099–1129 (2009),
  https://doi.org/10.1007/s00220-009-0788-2.

**Next gate:** prove a quantitative **uniform normalized boundary
resolvent/Kreiss estimate** through the glancing sector, analyze
higher-order corner compatibility and choose a concrete curved
linearized generalized-harmonic source model before attempting
any variable-coefficient or nonlinear theorem. In particular,
a successful right-half-plane determinant test by itself is not
the needed proof.
