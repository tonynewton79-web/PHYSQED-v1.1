# Center–horizon incompatibility in a static shift-symmetric scalar–Gauss–Bonnet sector

**Tony Newton — Newton Astro Labs, London, UK**  
**PHYSQED Frontier Physics, Attack 002 — 12 November 2026**

## Scope

This research note is an exact, reproducible *restricted-model obstruction*, not a claim of new fundamental physics. It provides a scalar-equation-level necessary condition that remains applicable when the metric is dynamically determined, under the stated ansatz. It does not solve the coupled Einstein equations, certify collapse or global regularity, or establish originality against the cited literature.

Take the four-dimensional classical action, in geometrized units and mostly-plus signature,

\[
S=\int d^4x\sqrt{-g}\left[\frac{M_{\rm Pl}^2}{2}R-\frac12(\nabla\phi)^2+\eta\phi\mathcal G\right]+S_{\rm other}[g,\Psi],\quad
\mathcal G=R_{abcd}R^{abcd}-4R_{ab}R^{ab}+R^2,
\]

where other sectors do not couple directly to \(\phi\). The scalar equation is \(\Box\phi+\eta\mathcal G=0\). Restrict to static, spherical, areal coordinates and a time-independent radial scalar,

\[
 ds^2=-N(r)^2F(r)dt^2+\frac{dr^2}{F(r)}+r^2d\Omega^2,\qquad \phi=\phi(r),
\]

on a connected radial interval, with \(N\) finite and strictly positive at any regular center or considered horizon. The conditions below demand enough smoothness for the displayed curvature derivatives. These coordinates can have the usual coordinate singularity at a horizon; scalar regularity refers to its invariant value in a regular extension.

## Exact divergence and flux

A direct curvature calculation gives

\[
\mathcal G=\frac4{Nr^2}\frac d{dr}\left[N(F-1)\left(F'+2F\frac{N'}N\right)\right]. \tag{1}
\]

As \(\Box\phi=(Nr^2)^{-1}(Nr^2F\phi')'\), the scalar equation is equivalent to \(\mathcal C'=0\), where

\[
\boxed{\mathcal C=Nr^2F\phi'+4\eta N(F-1)\left(F'+2F\frac{N'}N\right).} \tag{2}
\]

One derivation of (1), independent of a 4D component contraction, uses the four orthonormal curvature combinations

\[
X=\tfrac12F''+\tfrac32(N'/N)F'+F N''/N,\quad
Y=(F'/2+FN'/N)/r,\quad Z=-F'/(2r),\quad W=(1-F)/r^2,
\]

with \(\mathcal G=-8(XW+2YZ)\). SymPy symbolically verifies the divergence equivalence. A second script builds the full four-dimensional Levi–Civita connection, Riemann and Ricci tensors and reconstructs \(\mathcal G=K-4R_{ab}R^{ab}+R^2\) on a nontrivial rational test metric, obtaining the identical exact value \(-137/450\) at \(r=1,\theta=\pi/2\). Both scripts use SymPy and thus do not provide complete cross-engine independence.

## Proposition: obstruction from a smooth center

Assume that at \(r=0\), \(F=1+O(r^2)\), \(N=N_0+O(r^2)\) with \(N_0>0\), and \(\phi\) is a smooth rotationally invariant scalar. Each term of (2) tends to zero, so \(\mathcal C=0\) on the connected domain.

Now assume a positive-radius horizon \(r_h\) at which \(F(r_h)=0\), \(0<N(r_h)<\infty\), and \(F\) has a finite-order zero \(F(r)=f_p(r-r_h)^p+O((r-r_h)^{p+1})\), \(f_p\ne0\), integer \(p\ge1\), with \(N'/N\) bounded nearby. Equation (2) with \(\mathcal C=0\) gives

\[
\phi'=-\frac{4\eta(F-1)}{r^2 F}\left(F'+2F\frac{N'}N\right)
=\frac{4\eta p}{r_h^2(r-r_h)}+O(1). \tag{3}
\]

For nonzero \(\eta\), the scalar has a logarithmic divergence approaching the horizon. **A smooth center and a smooth finite-order horizon cannot both occur within this ansatz and scalar sector.** The conclusion is independent of the gravitational field equations because it follows from one necessary equation of the fully coupled system; it is *not* a proof that some other covariant action has no regular black-hole solutions.

A separate useful obstruction is available with two distinct simple horizons \(r_-<r_+\), with \(F<0\) between them, \(N>0\) and the scalar regular at both. Evaluating (2) at each simple horizon demands

\[
\mathcal C=-4\eta N(r_-)F'(r_-)=-4\eta N(r_+)F'(r_+). \tag{4}
\]

Since \(F'(r_-)<0<F'(r_+)\), (4) is impossible for \(\eta\ne0\). This argument does not require a regular center. It uses the static scalar and both horizons' standard smoothness; it does not apply to time-dependent scalar hair.

## Exactly factorable Hayward control

Let \(F=1-2Mr^2/(r^3+2M\ell^2)\) and \(N=1\), a familiar regular-core effective geometry, not necessarily a solution of the action above. At \(M=1,\ell^2=1/2\), the horizon polynomial factorizes exactly:

\[
r^3-2r^2+1=(r-1)(r^2-r-1).
\]

The positive horizons are \(r_-=1\) and \(r_+=(1+\sqrt5)/2\). Their derivatives and horizon-regularity flux values are

\[
F'(r_-)=-\tfrac12,\quad F'(r_+)=\tfrac52-\sqrt5>0,
\]

\[
\mathcal C_- =2\eta,\qquad \mathcal C_+=(-10+4\sqrt5)\eta.
\]

They cannot equal one another for nonzero \(\eta\), and neither equals the smooth-center value \(0\). An extremal Hayward horizon occurs at \(r_h=4M/3\), \(\ell^2=16M^2/27\). Although \(F'(r_h)=0\), the order-two local formula (3) still forces a logarithmic divergence for a center-regular static scalar.

## Potential/source loophole and exact balance law

If one adds \(-V(\phi)\) to the Lagrangian, with scalar equation \(\Box\phi+\eta\mathcal G=V'(\phi)\), (2) becomes

\[
\mathcal C'=Nr^2 V'(\phi).
\]

For a smooth regular center and a regular **simple** horizon, necessarily

\[
\boxed{\int_0^{r_h}N(r)r^2V'(\phi(r))\,dr=-4\eta N(r_h)F'(r_h).} \tag{5}
\]

This is a *necessary integral compensation condition*, not proof of existence of a solution. For an outer horizon with \(F'(r_h)>0\) and \(\eta>0\), the integral must be negative. With \(V'(\phi)\ge0\) throughout the integration domain, no solution satisfies the stated boundary regularity. Nonlinear scalar–Gauss–Bonnet couplings \(f(\phi)\mathcal G\), derivative couplings, time-dependent scalars, additional scalar source terms, nonstandard horizons and horizonless spacetimes evade or modify this specific flux argument and require new audits.

## Scientific implication and priority boundary

This result prevents the basic shift-symmetric linear scalar–Gauss–Bonnet theory from being promoted as a *static regular-center black-hole mechanism*, even when one allows metric backreaction. The broader frontier task is not another regular metric ansatz. It is to specify a different, covariant and dynamically consistent theory, then check **all coupled field equations, propagator degrees of freedom, ghost/gradient instabilities, hyperbolicity, collapse, horizons, global completeness, quantum corrections and observational constraints**.

The result should be understood as a small, transparent diagnostic derivation within an extensively studied literature, **not a novel no-go theorem**. It aligns closely with work on topological scalar charge and analytic regular-black-hole obstructions. Care is required: a horizon-regular hairy black hole with a *singular center* does not contradict it, and a regular black-hole **exterior** is not the same as a regular-center solution.

## Reproduce

From repository root with SymPy:

```bash
python research/frontier-physics-attack002/attack002_exact.py
python research/frontier-physics-attack002/attack002_4d_oracle.py
```

Both scripts passed locally on 12 November 2026. GitHub Actions, independent non-SymPy curvature replay, the full inherited PHYSQED suite, and backreacted dynamical evolution have **not** been certified. PHYSQED's separate generalized-harmonic release hold remains unchanged.

## Related literature, prior-art boundary

1. Saravani and Sotiriou, *Classification of shift-symmetric Horndeski theories and hairy black holes*, Phys. Rev. D **99**, 124004 (2019), https://doi.org/10.1103/PhysRevD.99.124004.
2. Sotiriou and Zhou, *Black hole hair in generalized scalar-tensor gravity: An explicit example*, Phys. Rev. D **90**, 124063 (2014), https://doi.org/10.1103/PhysRevD.90.124063.
3. Babichev, Sawicki and Trombetta, *Black-hole hair in scalar-Gauss-Bonnet gravity is altered by cosmology*, Phys. Rev. D **111**, L041502 (2025), https://doi.org/10.1103/PhysRevD.111.L041502.
4. Ballester and collaborators, *Nonclosed scalar charge in four-dimensional Einstein-scalar-Gauss-Bonnet black hole thermodynamics*, Phys. Rev. D **113**, 084039 (2026), https://doi.org/10.1103/1hz8-zn5h.
5. De Felice and Tsujikawa, *Static regular black holes in Horndeski theories: analytic no-go and nonanalytic obstructions*, arXiv:2607.08228v2 (July 2026), https://arxiv.org/abs/2607.08228.
6. Boonserm, De Felice, Nakarachinda, Tsujikawa and Wongjun, *Perturbations and stability of black holes with static scalar hair in general GLPV theories*, arXiv:2609.00664 (September 2026), https://arxiv.org/abs/2609.00664.

These citations identify closely related work, **not** a comprehensive priority audit or proof that the local derivation was absent from the literature.
