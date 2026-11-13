# PHYSQED Frontier Physics — Attack 003

**Tony Newton, Newton Astro Labs (12 November 2026)**

## Research question and scope

Can a scalar \(\phi=qt+\psi(r)\) be smooth at the future event horizon, satisfy the off-diagonal Einstein equation, and solve *all* metric–scalar equations of the minimal shift-symmetric linear scalar–Gauss–Bonnet theory?

**Answer on the tested branch:** the scalar is smooth at the future horizon, and the off-diagonal equation passes, but the \(tt\) Einstein equation and asymptotic flatness fail for nonzero \(q\).

This is a **restricted analytic model-filter**, not an original physical theory, new general no-go theorem, full coupled gravitational solution, or kinetic-stability certification. The existing PHYSQED generalized-harmonic release hold is unchanged.

### Governing equations

Use signature \((-+++)\), conventional Riemann sign, and

\[
S=\int\sqrt{-g}\,\bigg[\frac{R}{2\kappa}-\frac12(\nabla\phi)^2+\eta\phi\mathcal G\bigg]d^4x.
\]

The equations are \(\Box\phi+\eta\mathcal G=0\) and

\[
G_{ab}/\kappa=T^{\rm can}_{ab}-8\eta P_{a\rho b\sigma}\nabla^\rho\nabla^\sigma\phi,
\]
where \(P\) is the double-dual Riemann tensor, equal to Riemann on Schwarzschild.

Take **fixed** Schwarzschild \(F=1-2M/r\) and \(\phi=qt+\psi(r)\). The scalar equation gives

\[
r^2F\psi'=C+16\eta M^2/r^3.
\]

With \(v=t+\int dr/F\) and \(\chi=\psi-qr_*\), regularity at the future horizon requires \(C+2\eta/M=4M^2q\). On \(C=0\),

\[
q_*=\eta/(2M^3),\quad
\chi'=-q_*\sum_{j=0}^4(2M/r)^j,\quad
\chi'(2M)=-5q_*,\quad
X_h=5q_*^2.
\]

The **off-diagonal** field equation on Schwarzschild is

\[
0=T^{\rm can}_{tr}-8\eta P_{t\rho r\sigma}\nabla^\rho\nabla^\sigma\phi
=qC/(r^2F).
\]

Thus it selects \(C=0\) for \(q\ne0\), consistent with the future-horizon condition.

However the **time-time** effective source on this branch is

\[
\mathcal E_{tt}
=\frac{q^2r^{10}+5888\eta^2M^4-3072\eta^2M^3r}{2r^{10}},
\]
so at \(r=4M\), \(q=q_*\),
\[
\mathcal E_{tt}=999\eta^2/(8192M^6)\ne0,
\]
whereas the fixed Schwarzschild Einstein tensor is zero. The model does **not** solve the coupled metric equation on Schwarzschild. Its asymptotic effective energy density is \(q^2/2\), incompatible with vacuum asymptotic flatness and a nondegenerate canonical scalar kinetic term. A bare cosmological constant alone cannot cancel simultaneously the homogeneous rolling scalar's temporal and spatial stress.

### Hayward two-horizon scalar-only control

For fixed Hayward \(F=1-2r^2/(r^3+1)\), the positive horizons are \(r_-=1\) and \(r_+=(1+\sqrt5)/2\). A smooth center gives
\[
C=r^2F\psi'+4\eta(F-1)F'=0.
\]
Advanced-coordinate smoothness at a horizon then demands \(q=4\eta F'(r_h)/r_h^2\). The exact rates are
\[
q_-=-2\eta,\qquad q_+=(25-11\sqrt5)\eta.
\]
They are incompatible for nonzero \(\eta\). This is a **scalar-equation** obstruction on a fixed prescribed metric, not proof that Hayward solves the full coupled theory.

## Reproducibility

From the repository root (Python 3.11+; SymPy 1.14):

~~~bash
python research/frontier-physics-attack003/attack003_exact.py
python research/frontier-physics-attack003/attack003_full_tensor.py
python research/frontier-physics-attack003/attack003_fraction_replay.py
~~~

All three programs passed in local execution on 12 November 2026. The full tensor derivation and exact model filter share SymPy; the **Fraction-only** checkpoint independently confirms \(P_{tr}=1/512\), \(P_{tt}=13/32768\), \(E_{tr}=0\), \(E_{tt}=999/8192\) for \(M=\eta=1,r=4M,q=1/2\). This is a local arithmetic check, **not** an independent general-purpose metric-variation engine. Hosted GitHub CI and inherited PHYSQED regressions have not been verified.

**Physical stability:** Not certified. Ghost/gradient analysis requires the quadratic coupled perturbation action around an actual solution of the full equations, not this rejected fixed-background ansatz.

## Relevant prior art and next direction

- Kobayashi & Tanahashi (2014), time-dependent Horndeski hair and \(E_{tr}\sim qJ^r/f\): https://academic.oup.com/ptep/article/2014/7/073E02/1564012
- Benkel, Sotiriou & Witek (2016), time-dependent scalar hair on Schwarzschild: https://doi.org/10.1103/PhysRevD.94.121503
- Babichev, Sawicki & Trombetta (2025), cosmological horizon matching obstruction: https://doi.org/10.1103/PhysRevD.111.L041502
- Glavan & Jaramillo-Garrido (August 2026), cosmological behavior and energy flux: https://doi.org/10.1103/q3nv-ccwn
- De Felice & Tsujikawa (July 2026), restricted time-independent regular-center no-go: https://arxiv.org/abs/2607.08228
- Bueno, Cano, Hennigar & Murcia (January 2026), nonpolynomial-gravity regular collapse: https://doi.org/10.1103/8f3j-zcxh

A sensible next attack is to test a **fully coupled** theory with an extra admissible operator, a noncanonical kinetic branch, or a cosmological rather than Minkowski asymptotic. Require a stable principal symbol, finite horizons and curvature, valid matter dynamics, radiative scrutiny, and empirical tests. The mechanism itself is established prior art; a new prediction or rigorously distinct theorem would require a more comprehensive novelty audit.
