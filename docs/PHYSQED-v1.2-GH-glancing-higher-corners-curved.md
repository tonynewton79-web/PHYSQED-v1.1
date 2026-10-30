# PHYSQED v1.2 — Glancing Counterexample, Higher Harmonic Corners and Curved pp-Wave Control

## Executive mathematical status

This update attacks the three release-critical gaps left by the
linearized harmonic Einstein half-space benchmark:

1. **Uniform boundary stability near glancing:** establishes a
   counterexample to a proposed *unweighted metric-amplitude inverse*
   estimate for the existing 10×10 boundary symbol. It does **not**
   disprove any well-posed first-order generalized-harmonic
   formulation or an appropriately weighted Kreiss estimate.
2. **Higher temporal corner compatibility:** implements an exact
   recursive hierarchy of the four harmonic constraint and six
   tangential Sommerfeld compatibility conditions through
   user-specified finite order (maximum 8). It detects a concrete
   failure at order 2 that is invisible to the previous order-1 gate.
3. **Genuinely curved spacetime:** on an explicit Ricci-flat
   Brinkmann gravitational pp-wave with nonzero Riemann curvature,
   verifies covariantly the linearized Einstein Bianchi identity
   and the reduced generalized-harmonic constraint wave operator
   for a nontrivial polynomial metric perturbation.

These are scoped established geometric/mathematical facts and new
verification engineering, not novel global Einstein well-posedness
or an independent proof of historical harmonic IBVP theorems.

## 1. Quantitative unweighted glancing obstruction

The existing Minkowski half-space is x≥0, with ten reduced
trace-reversed wave equations and the 10-row boundary operator

\[
D_-\bar h_{ab}|_{x=0}=0,\qquad
C_\nu=\partial^\mu\bar h_{\mu\nu}|_{x=0}=0,
\]

where \(D_-=\partial_t-\partial_x\),
\(a,b\in\{t,y,z\}\), and \(C_\nu\) has four components.

For a Laplace–Fourier normal mode
\[
\bar h_{\mu\nu}
 =a_{\mu\nu}\exp(st+i\eta y+i\zeta z-\kappa x),
\qquad \kappa^2=s^2+\eta^2+\zeta^2,
\quad\Re\kappa>0,\ \Re s>0,
\]
the boundary matrix has determinant
\[
\det B=\kappa^4(s+\kappa)^6.
\]

The determinant is nonzero in the open right-half-plane, but
it is **not a uniform inverse estimate** in the ordinary
metric-amplitude norm. Choose the unit metric amplitude with
\(\bar h_{xx}=1\) and all other amplitudes zero. Its six
Sommerfeld rows vanish, as do three constraint rows; the
fourth (x) constraint row is exactly \(-\kappa\). Hence
\[
\|Ba\|=|\kappa|,\qquad \|a\|=1.
\]

Now choose the explicit sequence, for integers n≥2,
\[
s_n=i+n^{-2},\qquad \eta=1,\quad\zeta=0,\qquad
\kappa_n^2=n^{-4}+2in^{-2}.
\]
The decaying branch has \(\Re\kappa_n>0\), and
\[
|\kappa_n|^2
=n^{-2}\sqrt{4+n^{-4}}
<\frac{3}{n^2}.
\]

Any standard tangential frequency normalization \(\Lambda_n\)
which stays bounded below by a positive constant on this
sequence yields
\[
\frac{\|B_na\|}{\Lambda_n\|a\|}
\le \frac{\sqrt3}{n\Lambda_n}\longrightarrow0 .
\]

Therefore there is **no frequency-independent** c>0 for the
unweighted ten-component metric-amplitude estimate
\(\|Ba\|\ge c\Lambda\|a\|\) over the decaying
right-half-plane normal modes.

This is an exact counterexample to **that particular proposed
estimate**. A valid Kreiss estimate may use pseudodifferential
weights, characteristic first-order variables, a frequency-
dependent stable-subspace norm, or a different boundary
operator. The current code does **not** rule out those options.
In particular, established harmonic Einstein boundary
well-posedness results are not contradicted.

## 2. Finite higher-order metric and constraint corners

Let \(f_{\mu\nu}=\bar h_{\mu\nu}(0,\cdot)\) and
\(g_{\mu\nu}=\partial_t\bar h_{\mu\nu}(0,\cdot)\).
For \(\Box\bar h=0\), define the formal time jets

\[
J_0=f,\quad J_1=g,\quad
J_{j+2}=\Delta J_j,\qquad j\ge0.
\]

At boundary x=0, the six Sommerfeld temporal derivatives
at each order j are the exact expressions

\[
D_-^{(j)}\bar h_{ab}|_{t=0,x=0}
=J_{j+1,ab}-\partial_xJ_{j,ab}.
\]

The four harmonic-constraint temporal derivatives are

\[
\partial_t^j C_\nu|_{t=0}
=-J_{j+1,t\nu}
+\sum_{i=x,y,z}\partial_iJ_{j,i\nu}.
\]

The program checks **initial C and initial ∂t C on the
whole initial slice**, plus both boundary families at every
requested temporal order from 0 through a finite max_order
(0..8). It refuses input that depends on initial time,
unsupported source types and excessive orders. Higher-than-
requested compatibility is always marked unproved.

An exact positive control is an outgoing polynomial wave
\(\bar h_{yz}=F(t+x)\) with
\(F(\xi)=\xi^3+3\xi^2+6\xi+6\).
All 6 metric and 4 constraint boundary jets vanish through
order 6, and both initial constraints vanish identically.

The decisive negative control is

\[
f_{yz}=x^3,\qquad g_{yz}=0,
\quad\text{other initial components zero}.
\]

Its harmonic constraints vanish, and the Sommerfeld
compatibility conditions at orders 0 and 1 are satisfied.
But at order 2,

\[
\Delta g_{yz}-\partial_x\Delta f_{yz}
=0-\partial_x(6x)=-6\ne0
\quad (x=0).
\]

This explicitly disproves the inference that passing the
old first-order corner gate guarantees sufficient
higher-regularity compatibility.

## 3. A genuinely curved Ricci-flat generalized-harmonic benchmark

Choose the exact Brinkmann pp-wave metric

\[
\boxed{
ds^2=-2\,du\,dv+dx^2+dy^2+(x^2-y^2)\,du^2.
}
\]

Direct independent coordinate computation gives
\[
R_{\mu\nu}=0,\qquad
R^x{}_{uxu}=-1,\quad R^y{}_{uyu}=1,\qquad
g^{\mu\nu}\Gamma^\alpha_{\mu\nu}=0.
\]

Thus the background is genuinely curved and vacuum
Ricci-flat, in harmonic Brinkmann coordinates.

For an explicit trace-reversed perturbation, set
\[
\bar h_{vv}=ux,\quad
\bar h_{ux}=\bar h_{xu}=vy,\quad
\bar h_{xy}=\bar h_{yx}=xy,
\]
with other entries zero. Define
\(C_\nu=\nabla^\mu\bar h_{\mu\nu}\), and

\[
Q_{\mu\nu}[C]=\nabla_\mu C_\nu+\nabla_\nu C_\mu
-g_{\mu\nu}\nabla^\alpha C_\alpha .
\]

The code computes the **linearized Einstein tensor independently**
by differentiating the Levi-Civita connection:

\[
\delta\Gamma^\alpha{}_{\mu\nu}
=\frac12g^{\alpha\beta}\big(
\nabla_\mu h_{\beta\nu}+\nabla_\nu h_{\beta\mu}
-\nabla_\beta h_{\mu\nu}\big),
\]

where \(h_{\mu\nu}=\bar h_{\mu\nu}
-\frac12g_{\mu\nu}g^{\alpha\beta}\bar h_{\alpha\beta}\).
It then forms
\(\delta R_{\mu\nu}=
\nabla_\alpha\delta\Gamma^\alpha{}_{\mu\nu}
-\nabla_\nu\delta\Gamma^\alpha{}_{\mu\alpha}\) and
\(\delta G_{\mu\nu}\).

The exact checks give

\[
\nabla^\mu\delta G_{\mu\nu}=0,\qquad
\nabla^\mu Q_{\mu\nu}[C]=
\Box_g C_\nu+R_\nu{}^\alpha C_\alpha.
\]

Ricci is zero for this background, so the latter equals
\(\Box_g C_\nu\). If the reduced operator is
\(E^{red}_{\mu\nu}=\delta G_{\mu\nu}
-\frac12Q_{\mu\nu}[C]\), the checked relationship is
\[
\nabla^\mu E^{red}_{\mu\nu}
=-\frac12\Box_g C_\nu.
\]

The explicit source has a nonzero linearized Einstein
residual, which is intentional: this is an **off-shell
differential-intertwining test**, not a claimed radiating
solution of the full linearized equation.

It does **not** implement a curved spacetime boundary normal
symbol, trace operator, uniformly timelike boundary,
corner hierarchy on this background, global hyperbolicity or
a curved-background energy estimate. Those remain separate
mandatory proof gates.

## 4. Reproducible implementation

Source and tests:

- \`projects/physqed/v12/gh_glancing_corners.py\`
- \`projects/physqed/v12/gh_curved_ppwave.py\`
- \`projects/physqed/tests/test_physics_v12_gh_glancing_curved.py\`

The independent local prototype of these controls passed
**14/14 tests** on SymPy 1.14.0, including replay/tamper
refusal. The actual committed GitHub version still requires
native Python 3.15.2 and legacy CI success before release.

\`\`\`bash
python -m unittest discover -s projects/physqed/tests \
  -p test_physics_v12_gh_glancing_curved.py -v
\`\`\`

This module's normal-mode counterexample is an **analytic
obstruction**, not a numerical failure inferred from a
finite scan. The finite exact frequency sequence only
replays the displayed inequality.

## 5. Prior art and precise next goal

- Szilágyi, Schmidt and Winicour, *Boundary conditions in
  linearized harmonic gravity*, Phys. Rev. D 65, 064015 (2002).
- Kreiss and Winicour, *Problems which are well posed in a
  generalized sense with applications to the Einstein
  equations*, Class. Quantum Grav. 23, S405 (2006).
- Babiuc, Kreiss and Winicour, *Constraint-preserving
  Sommerfeld conditions for the harmonic Einstein equations*,
  Phys. Rev. D 75, 044002 (2007).
- Kreiss, Reula, Sarbach and Winicour, *Boundary Conditions
  for Coupled Quasilinear Wave Equations with Application to
  Isolated Systems*, Commun. Math. Phys. 289, 1099–1129 (2009).
- Rinne, *Stable radiation-controlling boundary conditions for
  the generalized harmonic Einstein equations*,
  Class. Quantum Grav. 23 (2006).

These prior results already establish important harmonic
Einstein boundary stability formulations, including formulations
with nonzero shift and curved backgrounds. This PHYSQED
work is therefore framed as a reproducible independent
verification system and counterexample-first audit, not
a novel general well-posedness theorem.

The **next decisive target** is to replace the failing
unweighted second-order boundary norm with the actual
frequency-weighted *first-order generalized-harmonic
incoming-characteristic* system of a specified formulation.
One must derive its stable subspace/characteristic boundary
operator and prove a **uniform normalized** resolvent
estimate at every normalized frequency, including the
glancing sector, plus full corner/trace and background
regularity assumptions. The pp-wave bulk identity is a
valuable positive curvature test, not a substitute for
that boundary analysis.
