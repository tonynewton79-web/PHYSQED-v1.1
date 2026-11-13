# PHYSQED Frontier Physics — Attack 010

Tony Newton | Newton Astro Labs | London, United Kingdom | 13 November 2026

**Mathematical research only.** The exact preferred-foliation action and stationary spherical scalar-clock radial equations from Attacks 005–009 are unchanged. This attack proves existence of **nontrivial zero-ADM-mass asymptotically flat exterior solutions on infinite half-lines**. It also proves a **specific** nonmatching to the Attack 007 local horizon, and identifies a **factorially divergent quadratic-amplitude** inverse-radius expansion. No global massless black hole, nonzero-mass black hole, singularity cure, physical mode stability, or fundamental novelty is claimed.

## Exact radial system and nonlinear Green integral

Use the same areal-radius unitary gauge phi=q t with

ds²=−N²dt² +A²(dr+Vdt)²+r²dOmega²,
eps=gamma q²/(Mp² Lambda²)>0, mu=lambda q⁴/Mp²>0,

and K=[V'+(A'/A)V+2V/r]/N.

For mu=1, put u=r(N−1), h=NA−1, T=NA. The exact stationary reduced field equations are equivalent to

u'=h+F, h'=−u+G,
K'=−A²V(N²−1)/(eps N⁵),
(Ar²V)'=Tr²K,

where

F=(T−N)²/(2N)+A²[eps N K²r²/4+KVr−3V²/(2N)]
  +A²Nr²(N^(−2)−1)²/8,

G=u−TA²r(N²−1)/(2N⁴).

For a specified asymptotic shift datum C=lim_(r→infinity) Ar²V, exclude the free homogeneous oscillator and prescribe K(infinity)=0. The exact nonlinear integral equations are

(u,h)(r) = −integral_r^infty
 [[cos(s−r),−sin(s−r)],[sin(s−r),cos(s−r)]] (F,G)(s) ds,

K(r)=eps^(−1) integral_r^infty A²V(N²−1)/N⁵ ds,

Ar²V=C−integral_r^infty Tr²K dr (with integration variable s).

Each is absolutely convergent in the certified function box and differentiates back to the exact stationary radial equations.

## Rigorous nonlinear exterior existence theorem

Set eps=1/1000, mu=1, t=1/r and

u=C²r^(−3)U, h=C²r^(−3)H,
V=Cr^(−2)Q, K=C³ eps^(−1) r^(−5)Z.

On the closed weighted function box |U|,|H|,|Z|<=2 and |Q−1|<=1/5, define the normalized nonlinear Green operator. **Pure Python Fraction interval arithmetic** encloses its exact rational sources and all sixteen derivatives over the *entire* t interval [0,1/R]. The weighted sup norm uses weights (2,2,1/5,2).

Two fully certified regimes:

- R=100, C=1/10: self-map sup bounds |U|,|H|<0.721, |Q−1|<0.0011, |Z|<0.961; weighted contraction <0.57.
- R=1997/1000, C=1/100: self-map sup bounds |U|,|H|<0.741, |Q−1|<0.026, |Z|<0.961; weighted contraction <0.57.

Banach's theorem supplies a unique *exact* solution of the reduced nonlinear stationary equations in each specified box. The solutions are smooth with N,A,X>0 and nonzero V~C/r². They have N−1=O(r^(−4)), A−1=O(r^(−3)), hence **m_ADM=0**. The same interval enclosures establish g_tt=−N²+A²V²<0 on the whole certified half-line, so neither has a local Killing horizon there.

### Exact scoped horizon mismatch

At r=2, the small-amplitude exact exterior has **0.002<=V(2)<=0.003**. The exact Attack 007 local horizon BVP, in the same gauge and at the same eps,mu, has **0.9908<=V(2)<=1.0108**. The two specific solutions therefore cannot be matched smoothly as one scalar-clock geometry. Other exterior C values, nonstandard clocks, and time-dependent solutions are not excluded.

## Factorial divergence does not prevent exact existence

Extract the term quadratic in the exterior shift amplitude C, N=1+C² n2(r)+O(C⁴), V=C/r²+O(C³). Exact symbolic algebra gives

n2''+2n2'/r+mu n2=6/r⁶.

The no-homogeneous-oscillation solution is

n2(r)=6/(sqrt(mu) r) integral_r^infty sin(sqrt(mu)(s−r))/s⁵ ds.

Its inverse-radius Poincare expansion has coefficients

a_j=6(−1)^j (5)_(2j)/mu^(j+1), with powers r^(−6−2j).

The coefficient ratio |a_(j+1)/a_j|=(5+2j)(6+2j)/mu grows without bound. Thus the **C² inverse-radius Taylor series has zero radius**; a nontrivial amplitude family with that response cannot be jointly analytic in (C,1/r) at zero. This is NOT a proof that the entire nonlinear series diverges at every fixed C!=0.

For every finite truncation m, integration by parts yields the exact error bound

|n2−sum_(j<m) a_j r^(−6−2j)|
<=12(5)_(2m)/(mu^(m+1) r^(6+2m)).

Independent mpmath incomplete-gamma and oscillatory quadrature agree for n2(12)=0.00000169659195233085846... . These diagnostics supplement, but are **not inputs to**, the rigorous Fraction Banach certificate.

## Reproduce and limitations

From repository root:

    python research/frontier-physics-attack010/attack010_exterior_banach.py
    python research/frontier-physics-attack010/attack010_symbolic_replay.py
    python research/frontier-physics-attack010/attack010_helmholtz.py

Scripts: Fraction-only nonlinear exterior Banach/horizon mismatch; independent SymPy exact radial-to-Green identity and C² equation; exact factorial recurrence plus two high-precision integral evaluations. The dedicated workflow is .github/workflows/physqed-frontier-attack010.yml. The complete PHYSQED inherited suite is NOT independently rerun, and the generalized-harmonic release hold remains unchanged.

The model-specific Banach existence theorem must undergo independent mathematical review; the full unrestricted four-dimensional covariant variation and curved-background gauge-reduced physical perturbation operator have NOT been independently reverified here. Existing work on ghost-condensate black-hole accretion, Hořava/khronometric spherical solutions, and asymptotic expansions is substantial prior art. See Frolov, Phys Rev D 70 (2004) 061501; Eling–Jacobson, CQG 23 (2006); Graham–Jha, PRD 89 (2014), erratum (2015); NIST DLMF 2.7. No absolute novelty claim is made.

**Next research gate:** establish whether a much larger-amplitude massless exterior can be connected to the certified local horizon, or exclude such matches by a global invariant or validated interval continuation; independently derive full physical scalar/tensor perturbations and an EFT cutoff. A smooth massless exterior is not yet a physically viable black hole.
