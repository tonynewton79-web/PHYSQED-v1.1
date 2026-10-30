# A Regular-Source Inhomogeneous Resolvent for the Adapted Linearized Harmonic Einstein Half-Space

## Result and precise status

This note advances the previously certified **homogeneous stable-mode trace inequality** to an **inhomogeneous Laplace–Fourier source-to-solution estimate** for the same *flat, zero-shift, constant-coefficient, ten-field, trace-reversed linearized harmonic* system on \(x\ge0\). Sources may enter all five first-order equations per metric component; their auxiliary first-order reduction defects are retained explicitly.

The theorem is valid for a specified **regular source class**, including enough normal derivatives for its effective second-order forcing to lie in \(L^2(0,\infty)\). It allows **nonzero data in all ten adapted boundary rows**. It is uniform across glancing in the sense that its constants are independent of normalized frequency and depend only on the standard \(\gamma^{-1}\), \(\gamma^{-1/2}\) Laplace weights, where \(\gamma=\Re s>0\).

It is **not yet** a derivative-loss-free resolvent estimate relative to completely arbitrary \(L^2\) sources in all 50 first-order evolution equations. It does not by itself establish time-domain strong well-posedness, all-orders corner compatibility, curved coefficients, Einstein–Maxwell matter coupling, or nonlinear Einstein IBVP existence. These limitations remain explicit machine-readable claim flags.

The relevant general harmonic Einstein boundary well-posedness theory is established prior art; see Kreiss–Reula–Sarbach–Winicour (2007, 2009) and Rinne (2006).

## 1. The forced first-order system

For each symmetric metric component \(\psi=\bar h_{\mu\nu}\), use
\[
\Pi=-\partial_t\psi,\qquad \Phi_i=\partial_i\psi
\]
as the homogeneous geometric reduction and consider independent volume-source terms:
\[
\begin{aligned}
\partial_t\psi+\Pi&=F_0,\\
\partial_t\Pi+\partial_i\Phi_i&=F_\Pi,\\
\partial_t\Phi_i+\partial_i\Pi&=F_i.
\end{aligned}
\]

Laplace-transform time (\(\Re s=\gamma>0\)), Fourier-transform tangential \((y,z)\) with real frequencies \((\eta,\zeta)\), and retain normal coordinate \(x\ge0\). The exact source-driven **reduction defects** are
\[
\begin{split}
D_x&=\Phi_x-\partial_x\psi=(F_x-\partial_xF_0)/s,\\
D_y&=\Phi_y-i\eta\psi=(F_y-i\eta F_0)/s,\\
D_z&=\Phi_z-i\zeta\psi=(F_z-i\zeta F_0)/s.
\end{split}
\]

These equations result by subtracting spatial derivatives of the first evolution equation from the auxiliary evolution equations. In particular, \(D_i=0\) only for *compatible* sources \(F_i=\partial_i F_0\); arbitrary first-order volume forcing does **not** preserve vanishing auxiliary constraints automatically.

Substitution into the momentum equation gives exactly
\[
\boxed{
\left(\partial_x^2-\kappa^2\right)\psi=f_{\rm eff},
\qquad
\kappa^2=s^2+\eta^2+\zeta^2,
}
\]
where
\[
\boxed{
f_{\rm eff}=F_\Pi-sF_0-
\left(\partial_xD_x+i\eta D_y+i\zeta D_z\right).
}
\]

The original state is reconstructed by
\[
\Pi=F_0-s\psi,\quad
\Phi_x=\partial_x\psi+D_x,\quad
\Phi_y=i\eta\psi+D_y,\quad
\Phi_z=i\zeta\psi+D_z.
\]

PHYSQED symbolically verifies **every one** of the five forced equations from this reconstruction; the momentum row reduces identically to the displayed scalar forced wave equation.

### Regular-source hypotheses

For the resolvent statement, fix \(s\ne0\) with \(\gamma>0\) and take \(F_0\in H^2(0,\infty)\), \(F_x\in H^1(0,\infty)\), and \(F_\Pi,F_y,F_z\in L^2(0,\infty)\), with these conditions applied componentwise to all ten fields and sufficient decay/integrability for the Green construction. They imply \(D\in L^2\) and \(f_{\rm eff}\in L^2\).

To implement the metric derivative conditions **as boundary traces of the first-order variables** one must also control the traces of the needed \(F_i\) and \(D_i\), for example by taking all \(F_i\in H^1\) near \(x=0\). The estimate below treats boundary data as derivatives of reconstructed \(\psi\); the source corrections in this translation cannot be omitted.

## 2. The ten nonhomogeneous adapted boundary conditions

Let \(P\) be the exact 6×10 map selecting the adapted null-metric combinations from the previous stage:
\[
\psi_{tt}-2\psi_{tx}+\psi_{xx},\quad
\psi_{ty}-\psi_{xy},\quad
\psi_{tz}-\psi_{xz},\quad
\psi_{yy},\quad\psi_{yz},\quad\psi_{zz}.
\]

Let \(N\) select the four \(x\nu\) components in the same ten-vector basis. For a transformed metric \(\psi\), prescribe
\[
P(s-\partial_x)\psi(0)=g_P,\qquad
\big(-s\psi_{t\nu}+\partial_x\psi_{x\nu}
+i\eta\psi_{y\nu}+i\zeta\psi_{z\nu}\big)_{x=0}=g_{C,\nu}.
\]

These form ten **metric-derivative** boundary conditions, written \(g=(g_P,g_C)\), and reduce on a homogeneous normal mode to the previously verified null-adapted matrix \(B(s,\kappa,\eta,\zeta)a\). For geometric constraint preservation one requires \(g_C=0\), whereas the six incoming free data \(g_P\) may be nonzero if compatible with initial data and evolution.

Expressed through the first-order state, the six Sommerfeld conditions contain **source trace corrections** \(F_0+D_x\); the harmonic constraint conditions contain \(F_0\) and the \(D_i\). A forced first-order implementation must account for these, rather than imposing the homogeneous field formulas unchanged.

## 3. Dirichlet Green function and boundary forcing correction

Set \(\omega^2=\eta^2+\zeta^2\),
\[
\Lambda^2=|s|^2+\omega^2,\qquad \gamma=\Re s>0.
\]
Use the decaying branch \(\Re\kappa>0\). One has the exact inequality
\[
\Re\kappa\ge\gamma.
\]
Indeed, if \(\kappa=a+ib\), \(s=\gamma+i\tau\), then \(ab=\gamma\tau\) and
\[
(a^2-\gamma^2)(a^2+\tau^2)=a^2\omega^2\ge0,
\]
so \(a\ge\gamma>0\).

The inhomogeneous wave is decomposed as
\[
\psi(x)=u_D(x)+e^{-\kappa x}a_0,
\]
where \(u_D\) has **zero boundary value** and solves the forced wave equation. Its exact Dirichlet Green kernel is
\[
u_D(x)=-\frac1{2\kappa}\int_0^\infty
\left(e^{-\kappa|x-y|}-e^{-\kappa(x+y)}\right)
f_{\rm eff}(y)\,dy.
\]
Consequently,
\[
u_D(0)=0,\quad
u_D'(0)=-J,\quad
J=\int_0^\infty e^{-\kappa y}f_{\rm eff}(y)\,dy.
\]

For this particular solution, the six adapted Sommerfeld boundary rows equal \(PJ\), while its four harmonic constraint rows equal \(-NJ\). With
\[
T=\begin{pmatrix}P\\-N\end{pmatrix},
\]
the corrected boundary equation is exactly
\[
\boxed{B a_0=g-TJ.}
\]

The matrix \(P P^\mathsf T=\operatorname{diag}(6,2,2,1,1,1)\) and \(NN^\mathsf T=I_4\) are checked **exactly**. Thus \(\|T\|^2\le\|P\|^2+\|N\|^2=7\), while Cauchy–Schwarz gives
\[
\|J\|\le\frac{\|f_{\rm eff}\|}{\sqrt{2\Re\kappa}}
\le\frac{\|f_{\rm eff}\|}{\sqrt{2\gamma}}.
\]

## 4. Complete estimate for regular sources

For any \(\psi\), define the second-order wave norm
\[
W(\psi)^2=\Lambda^2\|\psi\|_{L^2_x}^2+
\|\partial_x\psi\|_{L^2_x}^2.
\]

For the Dirichlet particular solution, multiply the forced Helmholtz equation by \(\bar s\,\bar u_D\), integrate by parts and take real parts. The zero boundary value makes the boundary term vanish, yielding
\[
\gamma W(u_D)^2\le \|f_{\rm eff}\|\,W(u_D),
\qquad
\boxed{W(u_D)\le\frac{\|f_{\rm eff}\|}{\gamma}.}
\]

For the decaying homogeneous correction the previously independently proved adapted boundary inverse gives
\[
\Lambda\|a_0\|\le30\,\|B a_0\|.
\]
Also, \(|\kappa|\le\Lambda\), \(\Re\kappa\ge\gamma\), and therefore
\[
W(a_0e^{-\kappa x})
\le\frac{\Lambda\|a_0\|}{\sqrt\gamma}
\le \frac{30}{\sqrt\gamma}
\left(\|g\|+\sqrt7\|J\|\right).
\]
Since \(\sqrt{7/2}<2\), this gives
\[
\boxed{
W(\psi)\le \frac{61}{\gamma}\|f_{\rm eff}\|+
\frac{30}{\sqrt\gamma}\|g\|.
}
\]

Use the first-order **frequency-weighted** norm
\[
\|U\|_{\rm w}^2=
\Lambda^2\|\psi\|^2+\|\Pi\|^2+
\|\Phi_x\|^2+\|\Phi_y\|^2+\|\Phi_z\|^2.
\]
From \(\Pi=F_0-s\psi\) and \(\Phi=\nabla\psi+D\) and the triangle inequality,
\[
\|U\|_{\rm w}\le\sqrt2\,W(\psi)+\|F_0\|+\|D\|.
\]

The explicitly checked inequalities \(61\sqrt2<90\) and \(30\sqrt2<45\) prove the uniform bound
\[
\boxed{
\|U\|_{\rm w}
\le \frac{90}{\gamma}\|f_{\rm eff}\|
+\frac{45}{\sqrt\gamma}\|g\|
+\|F_0\|+\|D\|.
}
\]

**The constants 90 and 45 are conservative, independent of normalized frequency and remain valid in the glancing regime.** The estimate is complete for the stated regular-source resolvent class, with no concealed assumption \(D=0\).

It is **not** the usual strong first-order Kreiss resolvent estimate expressed solely through the \(L^2\) norms of arbitrary \((F_0,F_\Pi,F_i)\). The effective forcing contains derivatives of the arbitrary first-order sources; this is precisely the derivative-loss/uncontrolled-source issue that remains to be addressed before a full \(L^2\)-strong-well-posedness assertion.

## 5. Nonzero initial data and sourced corner compatibility

For Cauchy data \(f=\psi(0,\cdot)\), \(g_0=\partial_t\psi(0,\cdot)\), the time Laplace transform of the first-order system can absorb the data into source terms:
\[
F_0\mapsto F_0+f,\quad
F_\Pi\mapsto F_\Pi-g_0,\quad
F_i\mapsto F_i+\partial_i f,
\]
provided the initial first-order reduction variables satisfy \(\Phi_i(0)=\partial_i f\), \(\Pi(0)=-g_0\). For initial reduction defects, the corresponding source/constraint corrections must also be retained.

These substitutions are **algebraic Laplace-transform identities**; compatible initial traces and time-domain solution existence are not inferred from them.

For the sourced second-order wave equation
\[
-\partial_t^2\psi+\Delta\psi=F_\Pi,
\]
the initial time jets are computed exactly by
\[
J_0=f,\quad J_1=g_0,\quad
J_{m+2}=\Delta J_m-\partial_t^mF_\Pi(0,\cdot).
\]

At each temporal order \(m\), the checker tests six nonhomogeneous Sommerfeld corner equations
\[
P\left(J_{m+1}-\partial_xJ_m\right)|_{x=0}
=\partial_t^m g_P|_{t=0}
\]
and four harmonic corner equations
\[
\left[-J_{m+1,t\nu}+
\sum_{i=x,y,z}\partial_iJ_{m,i\nu}\right]_{x=0}
=\partial_t^m g_{C,\nu}|_{t=0}.
\]
It checks a requested finite hierarchy through order \(m\le6\), **not all orders**.

For constraint-preserving Einstein forcing, it separately tests
\[
\partial^\mu F_{\Pi,\mu\nu}=0.
\]
Indeed \(\Box C_\nu=-\partial^\mu F_{\Pi,\mu\nu}\), so homogeneous constraint evolution is available only under this conservation condition. To obtain \(C_\nu=0\) for an existing smooth solution one also needs \(g_C=0\) and initial \(C_\nu=\partial_tC_\nu=0\).

### Exact sourced positive and negative controls

Set
\[
\bar h_{yz}(t,x)=t^2e^{-x},\qquad
\bar h_{\mu\nu}=0\text{ otherwise},\quad y,z\text{ periodic}.
\]
This is a **nonvacuum forced** wave, with
\[
F_{\Pi,yz}=(t^2-2)e^{-x}.
\]
The source has zero covariant divergence in this flat model; the harmonic constraints vanish identically, and zero initial metric and velocity data hold. The nonhomogeneous adapted boundary datum is
\[
g_{P,yz}(t)=(2t+t^2),\qquad g_C=0.
\]
All sourced boundary compatibility conditions through temporal order four pass exactly.

If the boundary datum is modified to \(g_{P,yz}=2t\), orders zero and one still pass, but **order two fails by 2**. A separate source with nonzero divergence is refused as a constraint-preserving Einstein source.

A second independent forced control sets, at \(s=1\), \(F_0=e^{-x}\), \(F_\Pi=F_i=0\), with \(\psi=0\), \(\Pi=\Phi_x=e^{-x}\). It satisfies every first-order forced equation and has a **nonzero reduction defect** \(D_x=e^{-x}\), but effective wave forcing zero. This proves that a \(\|D\|\) term cannot simply be discarded.

## 6. Reproducibility and release boundaries

The new GitHub modules are:
- \`projects/physqed/v12/gh_forced_resolvent.py\`
- \`projects/physqed/v12/gh_forced_corners.py\`
- \`projects/physqed/tests/test_physics_v12_gh_forced_resolvent.py\`

A separate independent local reference prototype passed **24/24 exact tests under Python 3.13.5 / SymPy 1.14.0**, before adding the explicit reduction-defect demonstration. The GitHub source is a refactored implementation; **native GitHub Python 3.15.2 CI must pass before those results are attributed to the exact committed code**.

The mathematical content relies on exact scalar wave Green functions, energy integrations and the previous adapted-symbol bound. It is an independent verification of standard mathematical physics techniques, not a claim to have originated harmonic Einstein boundary well-posedness theory.

Relevant prior art:
- Kreiss, Reula, Sarbach and Winicour, *Well-posed initial-boundary value problem for the harmonic Einstein equations using energy estimates*, Class. Quantum Grav. 24 (2007) 5973–5984, DOI 10.1088/0264-9381/24/23/017.
- Kreiss, Reula, Sarbach and Winicour, *Boundary Conditions for Coupled Quasilinear Wave Equations with Application to Isolated Systems*, Commun. Math. Phys. 289 (2009) 1099–1129.
- Rinne, *Stable radiation-controlling boundary conditions for the generalized harmonic Einstein equations*, Class. Quantum Grav. 23 (2006) 6275–6300.

## 7. Remaining decisive proof gate

The next necessary theorem is a **no-derivative-loss \(L^2\) estimate for all 50 independent first-order sources**, including their constraint subsystem and boundary traces, with a suitable full symmetrizer or frequency-dependent Kreiss multiplier. The finite sourced-corner hierarchy must be converted into the all-orders/Sobolev regularity compatibility required by the actual time-domain theorem.

Nonzero shift and variable/curved coefficients then require new frozen boundary symbols, domain-uniform positivity, face geometry, evolution-to-constraint boundary coupling and full-energy estimates. No part of the present certificate proves nonlinear Einstein or Einstein–Maxwell initial-boundary well-posedness.
