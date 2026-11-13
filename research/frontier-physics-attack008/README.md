# PHYSQED Frontier Physics — Attack 008

**Tony Newton — Newton Astro Labs, London, UK — 13 November 2026**

**Research-only theorem and verification.** The current action is unchanged. We establish a conditional mass-rigidity result for conventional stationary scalar-clock exteriors. We do **not** produce a globally asymptotically flat nonzero-mass black hole, certify the complete curved perturbation spectrum, remove the central singularity, or establish experimental novelty.

## 1. Field equations and exact on-shell identities

Use the Attack 005–007 covariant preferred-foliation scalar–tensor action with signature (−+++):

\[
S=\int\sqrt{-g}\left[\frac{M_{\rm Pl}^2}{2}R+
\lambda(X-q^2/2)^2-\frac{\gamma q^2}{2\Lambda^2}(\nabla_\mu u^\mu)^2\right]d^4x,
\qquad X=-\tfrac12(\nabla\phi)^2,\quad
u_\mu=-\nabla_\mu\phi/\sqrt{2X}.
\]

Set \(\epsilon=\gamma q^2/(M_{\rm Pl}^2\Lambda^2)>0\), \(\mu=\lambda q^4/M_{\rm Pl}^2>0\). In stationary spherical scalar-clock gauge \(\phi=qt\),

\[
ds^2=-N(r)^2dt^2+A(r)^2(dr+V(r)dt)^2+r^2d\Omega^2,
\]

where \(r>0\), \(N,A>0\), and

\[
K=\frac{V'+(A'/A)V+2V/r}{N},\quad
S_0=-\frac{\mu A^2r(N^2-1)}{2N^4}.
\]

The full reduced radial Euler–Lagrange system was derived and exactly checked in Attack 007. Three exact consequences are

\[
(\log NA)'=S_0,\qquad
K'=\frac{2V S_0}{\epsilon Nr},\qquad
(Ar^2V)'=ANr^2K.
\]

The fourth relevant equation is the exact lapse normal form

\[
N'=\frac{N(A^2-1)}{2r}
+A^2\left(\frac{\epsilon NK^2r}{4}+KV-\frac{3V^2}{2Nr}\right)
+\frac{\mu A^2Nr}{8}(N^{-2}-1)^2.
\]

No truncation in \(\epsilon\) is used in this attack.

## 2. New conditional mass-rigidity theorem without a scalar power-law hypothesis

**Theorem.** Let \((N,A,V,K)\) be a \(C^1\) exact solution of the above radial system on \([R,\infty)\), with \(R>0\), \(N,A>0\), and fixed \(\epsilon,\mu>0\). Assume

\[
N=1+O(r^{-1}),\quad A=1+O(r^{-1}),\quad
N',A'=O(r^{-2}),\quad g_{tt}=-1+O(r^{-1})
\]

as \(r\to\infty\). If the conventional spherical spatial ADM mass

\[
m=\lim_{r\to\infty}\frac r2(1-A(r)^{-2})
\]

exists and is finite, then **\(m=0\)**. Even without assuming the existence of that mass limit, the equations imply

\[
N-1=O(r^{-3}),\quad K=O(r^{-5/2}),\quad
V=O(r^{-3/2}),\quad g_{tt}=-1+O(r^{-3}).
\]

In particular, there is no ordinary \(1/r\) stationary Killing potential within this class.

**Proof.**

1. Since \(g_{tt}=-N^2+A^2V^2=-1+O(r^{-1})\), and \(N,A=1+O(r^{-1})\), necessarily \(V^2=O(r^{-1})\), so \(V=O(r^{-1/2})\). The specified differentiable falloff gives \(S_0=(\ln NA)'=O(r^{-2})\).
2. The exact momentum identity gives \(K'=2VS_0/(\epsilon Nr)=O(r^{-7/2})\). Thus \(K(r)\) has a finite limit \(K_\infty\) and \(K=K_\infty+O(r^{-5/2})\).
3. If \(K_\infty\ne0\), the exact transport identity \((Ar^2V)'=ANr^2K\) implies \(Ar^2V\sim (K_\infty/3)r^3\) and hence \(V\sim K_\infty r/3\), contradicting \(V=O(r^{-1/2})\). So \(K_\infty=0\), giving \(K=O(r^{-5/2})\).
4. The same transport identity now gives \((Ar^2V)'=O(r^{-1/2})\). Integrating from a fixed \(R\) implies \(Ar^2V=O(r^{1/2})\), hence \(V=O(r^{-3/2})\).
5. Reinsert \(S_0=O(r^{-2})\) in its algebraic expression. Since \(\mu>0\), \(A,N\to1\), we obtain \(N^2-1=O(r^{-3})\), and so \(N-1=O(r^{-3})\). Consequently \(g_{tt}+1=-(N^2-1)+A^2V^2=O(r^{-3})\).
6. Every remaining term in the exact lapse equation is \(O(r^{-4})\) or smaller, so
\[
N'=\frac{N(A^2-1)}{2r}+O(r^{-4}).
\]
If the stated ADM limit exists, \(A=1+m/r+o(r^{-1})\), which gives \(N'=m/r^2+o(r^{-2})\). Integrating from infinity and using \(N(\infty)=1\) yields \(N-1=-m/r+o(r^{-1})\), contradicting \(N-1=O(r^{-3})\) unless \(m=0\). QED.

**Critical scope:** No analytic expansion, pure power, or specified leading asymptotic for \(V\) was assumed. However we DO assume a positive timelike scalar clock, stationary spherical areal coordinates, positive fixed couplings, the stated \(C^1\) asymptotic-flatness falloff, and an ADM mass limit for its vanishing. The theorem does not exclude generalized weak/polyhomogeneous asymptotics that violate these conditions, nonstationary scalar clocks, other sources, other actions, or all Einstein-æther theories. Conventional ADM mass must be interpreted using admissible spatial infinity falloff; Painlevé–Gullstrand time slices of GR by themselves are not necessarily in the standard ADM energy class.

**Implication for Attack 007:** Its exact local nondegenerate Killing-horizon solution cannot extend to an isolated conventional asymptotically flat **nonzero-mass** exterior while preserving this stationary scalar-clock ansatz and all theorem hypotheses. The theorem does not demonstrate a global breakdown at a finite radius or exclude a massless alternative exterior.

## 3. Independent symbolic identity and adversarial asymptotic replay

The exact SymPy test in attack008_exterior_rigidity.py directly replays the three on-shell transport identities and verifies a formal coefficient stress test: for an illustrative asymptotic substitution \(N=1+\nu/r^3,\ A=1+m/r,\ V=v/r^{3/2},\ K=k/r^{5/2}\), the log identity gives \(m=\mu\nu\), while the lapse equation gives \(m=0\). **The proof above is stronger:** it does not rely on these formal substitutions.

## 4. Numerical continuation: cross-solver diagnostic, NOT global certification

To see how the particular Attack 007 local solution behaves beyond its strictly certified interval, solve the same mixed BVP with SciPy and extend from \(r=2.003\) to \(r=80\), using both DOP853 and Radau integrators. The solvers agree within \(7.7\times10^{-10}\) in the four state components on the sampled radii. The local numerical Killing-horizon root is approximately \(r_h=1.999135731067\), consistent with the **independently rigorous** Attack 007 bracket \(1.9988<r_h<1.9995\).

| r | N | A | V | finite-radius slice mass r(1−A^(−2))/2 |
|---|---:|---:|---:|---:|
| 4 | 1.000048419 | 0.999467965 | 0.707222213 | −0.002129839 |
| 10 | 1.000018661 | 0.998471323 | 0.448942269 | −0.015321894 |
| 20 | 0.999999685 | 0.997720505 | 0.320583228 | −0.045746261 |
| 40 | 1.000000669 | 0.996964141 | 0.232683238 | −0.121989598 |
| 80 | 1.000000283 | 0.996213619 | 0.174818605 | −0.304639633 |

The finite-radius mass diagnostic is **not the ADM mass at infinity**, the plotted trend is not a mathematical asymptotic proof, and numerically integrating beyond the local certificate does **not** certify the existence of the ODE solution throughout that outer domain. This exercise is useful for identifying poor asymptotic matching and solver sensitivity, but only the theorem in Section 2 supplies the rigorous global exclusion.

## 5. Perturbative scalar and tensor tests: what can be certified

Take the exact local horizon solution of Attack 007 with \(q=M_{\rm Pl}^2=\lambda=1\), \(\epsilon=1/1000\). Its rigorous interval bounds imply \(1<N<1.001\), \(X=1/(2N^2)>0\), and a positive *bare* k-essence kinetic coefficient

\[
{\cal K}_{\rm bare}=P_X+2XP_{XX}
=\frac{3}{N^2}-1>1.99.
\]

But \(N>1\) implies \(P_X=N^{-2}-1<0\), so the fixed-metric scalar has a negative quadratic spatial-gradient coefficient. The projected-extrinsic-curvature term contributes a **positive quartic** spatial derivative and can stabilize sufficiently short wavelengths.

A fixed-metric local proper-frame, frozen-coefficient approximation has
\[
\omega_{\rm test}^2
=\frac{P_X k^2+(\gamma N^2/\Lambda^2)k^4}{{\cal K}_{\rm bare}}
+\text{background derivative corrections}.
\]

The exact rational code checks these signs for positive rational lapses within the certified local range, without pretending that this is the physical curved mode.

One can also freeze the local ADM coefficients and eliminate lapse and longitudinal shift at the leading high-spatial-derivative level. With \(H=X(P_X+2XP_{XX})\) and \(D=2/\epsilon+3\), the corresponding leading scalar quadratic form is

\[
{\cal L}^{(2)}_{\rm UV,frozen}
=M_{\rm Pl}^2 D\,\dot\zeta^2
+M_{\rm Pl}^2(\nabla\zeta)^2
-\frac{M_{\rm Pl}^4}{H}(\nabla^2\zeta)^2
+\text{terms involving background curvature and gradients}.
\]

The frozen high-\(k\) quartic term and time-kinetic coefficient are positive for the tested local interval. The TT tensor leading kinetic and gradient still come from Einstein–Hilbert: the \(\theta^2\) term does not alter TT principal time derivatives at the tracefree level.

**Crucial refusal:** This is **NOT** the full curved-background gauge-reduced physical quadratic action, nor a theorem of strictly healthy scalar/tensor modes throughout the exterior. Background extrinsic curvature, spatial gradients, coupled constraints, lower-frequency Jeans behavior, scalar horizons, strong coupling, EFT cutoff, and any possible constraint degeneracy still require a fully covariant perturbation and mode analysis. The gradient warning and UV positivity cannot, on their own, decide physical viability.

## 6. Reproduction and scientific release boundary

From PHYSQED repo root, Python 3.11+:

    python research/frontier-physics-attack008/attack008_exterior_rigidity.py
    python research/frontier-physics-attack008/attack008_local_wkb.py
    python research/frontier-physics-attack008/attack008_frozen_adm.py
    python research/frontier-physics-attack008/attack008_outer_diagnostic.py

SymPy 1.14.0 supports exact on-shell identities and Schur complement, Python Fraction checks local principal coefficient signs, and NumPy/SciPy independently integrate the **numerical diagnostic only**. The dedicated scoped CI lives in .github/workflows/physqed-frontier-attack008.yml.

The inherited full PHYSQED regression suite remains unverified by this attack, and its existing generalized-harmonic release hold remains unchanged. This is an exact mathematical model filter, not a new phenomenologically viable gravity model.

## 7. Literature and originality limitations

Our model is a highly restricted kinetic-sector plus trace-extrinsic-curvature preferred-foliation action. Nearby prior art includes:

- Eling & Jacobson, *Black holes in Einstein-aether theory* (2006): https://doi.org/10.1088/0264-9381/23/18/009.
- Barausse, Jacobson & Sotiriou, *Black holes in Einstein-aether and Hořava-Lifshitz gravity* (2011): https://doi.org/10.1103/PhysRevD.83.124043.
- Franchini, Herrero-Valea & Barausse, *Relation between general relativity and a class of Hořava gravity theories* (2021): https://doi.org/10.1103/PhysRevD.103.084012.
- Kovachik & Sibiryakov, *Slowly moving black holes in khronometric model* (2025): https://doi.org/10.1103/PhysRevD.111.044042.
- Ghost-condensate accretion around black holes (2005): https://doi.org/10.1103/PhysRevD.71.104019.
- De Felice, Mukohyama & Takahashi, *Approximately stealth black hole* (2023): https://arxiv.org/abs/2212.13031.

The theorem uses familiar asymptotic and ODE methods. We have **not completed the detailed current prior-art audit** necessary to claim the zero-mass obstruction is original, and it should not be described as a universal Einstein-æther/khronometric no-go: richer coupling choices do admit asymptotically flat black holes.

## 8. Next attack: change the boundary-value problem, not the validation standard

Attack 009 should first test whether the massless stationary exterior option is genuinely realizable, and whether its curvature/horizon and perturbation properties can be physically acceptable. Otherwise the most relevant route is a **time-dependent scalar clock** or a model that relaxes one of the specific asymptotic hypotheses while maintaining genuine ADM energy and a stable Cauchy problem.

For any candidate, require an independently checked full physical curved-background quadratic action (scalar and tensor constraints, all angular modes), a validated nonlinear exterior continuation, a physically derived strong-coupling/cutoff window, and observationally distinguishable predictions. The Attack 007 local exact existence theorem remains valid, but this Attack 008 mass-rigidity theorem blocks the conventional isolated, nonzero-mass completion in the same stationary scalar-clock sector.
