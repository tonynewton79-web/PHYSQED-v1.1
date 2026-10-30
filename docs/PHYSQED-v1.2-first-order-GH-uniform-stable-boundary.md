# First-Order Linearized Generalized-Harmonic Boundary Stability: An Exact Flat-Background Benchmark

## Result and sharp claim boundary

This note gives a fully specified, **zero-shift, flat-background,
undamped linearized generalized-harmonic first-order principal
reduction** of the ten trace-reversed metric wave equations. It
replaces the previous glancing-degenerate six-tangential-metric
Sommerfeld boundary hierarchy by six **null-adapted** metric
Sommerfeld combinations, retaining four explicit harmonic
constraint boundary equations.

For this *new* boundary operator, an exact algebraic decomposition
proves a **frequency-uniform homogeneous stable-mode trace
inequality**, including all right-half-plane frequencies approaching
glancing. Its conservative explicit constant is \(1/60\).

This is **not** a complete first-order forced resolvent estimate,
a result for nonzero shift, a global energy estimate, a variable-
coefficient/general-background theorem, or an Einstein initial-
boundary-value existence or well-posedness theorem. It is a
specified reproducible positive control. There is extensive
existing research establishing appropriate well-posed
constraint-preserving generalized-harmonic boundary formulations;
the inequality here is presented as a computationally checkable
benchmark, **not** a priority or novelty claim.

## 1. First-order reduction and incoming characteristics

For each of the ten symmetric trace-reversed metric components
\(\psi_A=\bar h_{\mu\nu}\), write

\[
\Pi_A=-\partial_t\psi_A,\qquad
\Phi_{iA}=\partial_i\psi_A,\quad i=x,y,z.
\]

The frozen flat first-order reduction reads

\[
\begin{split}
\partial_t\psi_A&=-\Pi_A,\\
\partial_t\Pi_A+\partial_i\Phi_{iA}&=0,\\
\partial_t\Phi_{iA}+\partial_i\Pi_A&=0.
\end{split}
\]

For each metric component, the \(x\)-normal principal matrix
in \((\psi,\Pi,\Phi_x,\Phi_y,\Phi_z)\) has
\(A^x_{\Pi,\Phi_x}=A^x_{\Phi_x,\Pi}=1\), with other entries zero.
Its eigenvalues are

\[
-1,\ 0,\ 0,\ 0,\ +1.
\]

For the half-space \(x\ge0\), the speed-\(+1\) field
\(w_{\rm in}=\Pi+\Phi_x\) enters from \(x=0\);
the speed-\(-1\) field \(w_{\rm out}=\Pi-\Phi_x\) leaves.
Thus the ten-component system has ten incoming wave fields,
ten outgoing wave fields, and thirty zero-speed variables.

The auxiliary reduction constraints
\(D_i=\partial_i\psi-\Phi_i\) and
\(D_{ij}=\partial_i\Phi_j-\partial_j\Phi_i\)
satisfy \(\partial_t D_i=\partial_t D_{ij}=0\) for this
source-free constant-coefficient system. Their vanishing is
a separate initial-data obligation.

## 2. Stable subspace in Laplace–Fourier space

Let \(s\in\mathbb C\), \(\Re s>0\); take real
transverse frequencies \(\eta,\zeta\), and define the decaying
normal exponent \(\kappa\) by

\[
\kappa^2=s^2+\eta^2+\zeta^2,\qquad
\Re\kappa>0.
\]

For each independent symmetric metric amplitude \(a_A\),
a stable solution of the first-order reduced equations has

\[
(\psi,\Pi,\Phi_x,\Phi_y,\Phi_z)
=(1,-s,-\kappa,i\eta,i\zeta)a_A
\,e^{st+i\eta y+i\zeta z-\kappa x}.
\]

All five reduced equations and all spatial reduction constraints
are verified exactly using the dispersion polynomial
\(\kappa^2-s^2-\eta^2-\zeta^2=0\). The physical, reduction-
constraint-compatible decaying stable subspace is ten-dimensional
inside the fifty-dimensional first-order state space.

Set
\[
\Lambda^2=|s|^2+\eta^2+\zeta^2.
\]

The norm used in the theorem is the **frequency-weighted
first-order stable-state norm**

\[
\|U_{\mathrm{st}}\|^2=
\|\Lambda\psi\|^2+\|\Pi\|^2+
\|\Phi_x\|^2+\|\Phi_y\|^2+\|\Phi_z\|^2.
\]

Here Euclidean norms run over the *ten independent symmetric
metric components*, not a Lorentzian tensor norm. Because
\(|\kappa|^2=|s^2+\eta^2+\zeta^2|
\le\Lambda^2\), the stable norm is bounded by
\(\|U_{\mathrm{st}}\|\le\sqrt3\,\Lambda\|a\|\).
This weighting is essential to the comparison.

## 3. A new null-adapted boundary hierarchy

Index the symmetric amplitudes in the order

\[
(tt,ty,tz,yy,yz,zz,tx,xy,xz,xx).
\]

The **six free metric combinations** are

\[
\begin{aligned}
p_1 &= \psi_{tt}-2\psi_{tx}+\psi_{xx},\\
p_2 &= \psi_{ty}-\psi_{xy},\\
p_3 &= \psi_{tz}-\psi_{xz},\\
p_4 &= \psi_{yy},\quad p_5=\psi_{yz},\quad p_6=\psi_{zz}.
\end{aligned}
\]

Impose six outgoing Sommerfeld conditions
\((\partial_t-\partial_x)p_j=0\) at \(x=0\).
As the remaining four boundary equations, impose the actual
linearized harmonic constraints

\[
C_\nu=-\partial_t\psi_{t\nu}
+\partial_x\psi_{x\nu}
+\partial_y\psi_{y\nu}+\partial_z\psi_{z\nu}=0,
\quad \nu=t,x,y,z.
\]

The six free boundary rows act on the incoming combinations
of the first-order characteristic fields
\(w_{\rm in,A}=\Pi_A+\Phi_{xA}\).
The four constraint rows involve the remaining incoming
components as well as outgoing/tangential fields; their
right-hand side is **not** assumed to be arbitrary independent
boundary data if constraint preservation is required.

The resulting normal-mode boundary matrix is

\[
B_{\rm adapted}(s,\kappa,\eta,\zeta)
=\begin{pmatrix}(s+\kappa)P\\Q\end{pmatrix},
\qquad (Qa)_\nu
=q^\mu a_{\mu\nu},\quad
q=(-s,-\kappa,i\eta,i\zeta).
\]

Exact determinant extraction gives

\[
\boxed{\det B_{\rm adapted}=(s+\kappa)^{10}.}
\]

This is different from the **previous** six
tangential-tensor Sommerfeld plus four constraints operator,
whose determinant is \(\kappa^4(s+\kappa)^6\).
A determinant alone is not a uniform estimate; the next
algebraic step is required.

## 4. Exact analytic uniform stable-mode trace estimate

Let \(\ell=(1,1,0,0)^T\), a constant boundary null direction
in Minkowski coordinates. Embed a four-vector \(v\) into a
symmetric metric amplitude by

\[
(Fv)_{\mu\nu}=\ell_\mu v_\nu+\ell_\nu v_\mu.
\]

Define the six-dimensional complementary injection \(E\) by
assigning independent nonzero components
\((xx,xy,xz,yy,yz,zz)=(p_1,-p_2,-p_3,p_4,p_5,p_6)\).
Direct exact matrix algebra gives

\[
PF=0,\qquad PE=I_6,\qquad
a=Fv+Ep.
\]

Moreover,

\[
QF=d I_4+\ell q^T,\qquad
d=q^T\ell=-(s+\kappa).
\]

Since \(q^T\ell=d\), the **exact inverse** is

\[
\boxed{(QF)^{-1}
=d^{-1}I_4-\frac{\ell q^T}{2d^2}.}
\]

PHYSQED verifies both products symbolically.
The scalar outgoing Sommerfeld estimate, proved in the
previous benchmark, is

\[
|s+\kappa|^2\ge\frac12\Lambda^2.
\]

The remaining exact norm bounds are

\[
|\kappa|\le\Lambda,\quad
\|q\|\le\sqrt2\,\Lambda,\quad
\|F\|=\sqrt6,\quad
\|E\|=1,\quad
\|QE\|\le2\Lambda.
\]

The operator norms of \(F\) and \(E\) follow from the
exact Gram matrices: the eigenvalues of \(F^TF\) are
\(6,4,2,2\) and \(E^TE=I\). The \(QE\) inequality
uses the Frobenius matrix bound for symmetric components.

Consequently

\[
\|(QF)^{-1}\|\le\frac{2+\sqrt2}{\Lambda}.
\]

Write \(b_P=(s+\kappa)p\) for the six Sommerfeld
boundary residuals and \(b_C=Qa\) for the four
constraint residuals. From

\[
p=\frac{b_P}{s+\kappa},\qquad
v=(QF)^{-1}(b_C-QEp)
\]

and the preceding bounds,

\[
\|a\|\le\frac{
\sqrt6(2+\sqrt2)\|b_C\|
+\sqrt2[\,2\sqrt6(2+\sqrt2)+1\,]\|b_P\|}
{\Lambda}.
\]

The coefficients are strictly less than \(9\) and \(28\),
respectively. Therefore

\[
\|a\|<
\frac{9\|b_C\|+28\|b_P\|}{\Lambda}
\le\frac{\sqrt{9^2+28^2}}{\Lambda}\|Ba\|
<\frac{30}{\Lambda}\|Ba\|.
\]

Combining with the first-order state bound gives

\[
\boxed{
\|B_{\rm adapted}a\|
\ge\frac1{60}\|U_{\rm st}\|
\qquad (\Re s>0,\;\eta,\zeta\in\mathbb R).
}
\]

This is a **frequency-independent bound on the decaying
homogeneous stable subspace** in a clearly specified
first-order norm. The proof remains valid as frequencies
approach glancing and uses no frequency sampling.

It is not a full inhomogeneous Laplace–Fourier resolvent
estimate. Source forcing, reduction constraints for general
nonhomogeneous data, boundary trace regularity, energy
spaces, corner compatibility and higher-order/variable
coefficients must still be handled before claiming strong
well-posedness.

## 5. Independent glancing diagnostic and prior negative result

At the glancing sequence
\(s_n=i+n^{-2},\eta=1,\zeta=0\), the previous
normal-mode matrix has vanishing smallest singular value
in the normalized metric-amplitude norm. The null-adapted
boundary matrix instead remains bounded below.
A secondary high-precision SVD diagnostic on this sequence
provides a check **separate from** the analytic proof.
It uses mpmath, installed with SymPy; no NumPy dependency is
added to the GitHub regression runner.

The original \(\kappa^4\) boundary symbol remains a
**negative reference case**, not retrospectively overwritten.

## 6. Connection to the Einstein constraints and curved benchmark

The harmonic constraints \(C_\nu=0\) remain four of the
boundary operators. Given an **existing sufficiently smooth**
reduced-wave solution with homogeneous boundary constraints,
zero initial \(C\) and zero initial \(\partial_t C\), the
standard homogeneous wave energy argument preserves \(C=0\),
so the reduced solution is a full linearized Einstein
solution throughout its lifespan.

The separately verified curved Brinkmann plane wave
\(ds^2=-2du\,dv+dx^2+dy^2+(x^2-y^2)du^2\)
remains a **genuinely nonflat Ricci-flat bulk positive
control only**. The present uniform boundary inequality
was proved exclusively for the flat zero-shift
constant-coefficient reduction and is **not transferred**
to the curved pp-wave, even locally, without freezing the
curved principal symbol and proving corresponding
characteristic/boundary and regularity conditions.

The full generalized-harmonic evolution system normally
includes nonzero lapse/shift, damping parameters,
gauge source terms and lower-order geometric couplings.
Those features are not covered by this positive control.

## 7. Reproduction and release gate

\`\`\`bash
python -m unittest discover \
  -s projects/physqed/tests \
  -p test_physics_v12_gh_first_order_uniform.py -v
\`\`\`

The standalone independent flat benchmark and exact matrix
derivation were validated locally, including exact determinant
and first-order dispersion checks. The current GitHub feature
branch runs **18 new first-order regression tests** and two
high-precision glancing SVD checks in Python 3.15.2 CI.
The branch is not ready for release until native and
inherited regressions are green.

**Prior-art boundaries:** Lindblom–Scheel–Kidder–Owen–Rinne,
*A new generalized harmonic evolution system* (2006);
Rinne, *Stable radiation-controlling boundary conditions
for the generalized harmonic Einstein equations* (2006);
Kreiss–Winicour (2006); Kreiss–Reula–Sarbach–Winicour
(2009). The present statement is a narrowly scoped
independent benchmark, not a claim to have originated the
first-order generalized-harmonic well-posedness theory.

**Next theoretical target:** prove the corresponding
**inhomogeneous source-to-solution resolvent** estimate for
the specified adapted boundary hierarchy, including the
zero-speed reduction constraints, nonzero boundary data,
trace regularity and all corner orders. Then extend the
coefficient/symmetrizer analysis to a specified curved
spacetime with a uniformly timelike boundary. Nothing
here proves general nonlinear Einstein–Maxwell initial-
boundary well-posedness.
