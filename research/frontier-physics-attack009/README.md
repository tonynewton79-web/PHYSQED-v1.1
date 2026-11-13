# PHYSQED Frontier Physics — Attack 009

**Tony Newton | Newton Astro Labs, London, UK | 13 November 2026**

This is a scoped research result for the unchanged preferred-foliation action of Attacks 005–008, NOT a new black hole, fundamental physics solution, global viability theorem or a certified physical curved-background spectrum.

## Mathematical question

Does the stationary scalar-clock theory admit any massless asymptotically flat states, and can the exact local Killing horizon of Attack 007 be joined to a *nontrivial* massless asymptotic exterior with a controlled spectrum?

Define X=−(grad phi)^2/2, phi=q t, u=−grad phi/sqrt(2X), epsilon=gamma q^2/(Mpl^2 Lambda^2)>0, mu=lambda q^4/Mpl^2>0 and

S=integral sqrt(−g)[Mpl² R/2+lambda(X−q²/2)²−gamma q²(div u)²/(2Lambda²)].

For ds²=−N²dt²+A²(dr+Vdt)²+r²dOmega², K=[V'+(A'/A)V+2V/r]/N, the exact radial normal form is in Attacks 007–008.

## Exact result: the massless sector contains Minkowski but not a stable black hole

N=A=1, V=K=0, phi=q t is an **exact coupled** mass-zero solution with X=q²/2 and zero stress/current, no horizon. The previously derived **fully gauge-constrained flat** scalar quadratic dispersion is

omega²=[k⁴/mu−k²]/(2/epsilon+3).

Thus omega²<0 for 0<k<sqrt(mu); the maximum growth rate squared is Gamma_max²=mu/[4(2/epsilon+3)] at k²=mu/2. At epsilon=1/1000, mu=1, Gamma_max²=1/8012. This is the established ghost-condensate Jeans instability, not a novel effect; the exact Minkowski massless solution **fails strict all-wavelength mode stability**. Acceptability of an EFT with a slow Jeans band depends on the actual cutoff and time scale; neither is certified for astrophysical black holes.

This does NOT prove every curved massless exterior is unstable, because the full gauge-reduced coupled curved perturbation operator and essential-spectrum analysis remain open.

## New exact necessary formal asymptotic coefficient hierarchy

Assume an **unproved formal** inverse-radius expansion around a nontrivial massless end with V=C/r² and no nondecaying oscillatory homogeneous terms. Algebraic substitution into the exact *nonlinear* radial field equations gives

A=1+3C²/(2r⁴)−36C²/(mu r⁶)+...,
N=1+6C²/(mu r⁶)−180C²/(mu² r⁸)+...,
V=C/r²−(3/2+3/(7epsilon))C³/r⁶+...,
K=12C³/(7epsilon r⁷)+....

All coefficients were checked by SymPy from the exact radial ODE and independently by Python Fraction algebra. They are only **necessary coefficient identities for a formal series**. No convergence, analytic solution, massless-horizon connection, regular center, or stable perturbation spectrum has been proved. The 1/epsilon terms show a nonuniform zero-coupling expansion and may make horizon-to-exterior matching a singular perturbation.

## Curved-background operator: rigorous partial structural advance only

In time-dependent spherical unitary gauge with phi=q t, metric

ds²=−N(t,r)²dt²+A(t,r)²(dr+V(t,r)dt)²+r²dOmega²,

the exact reduced ADM action is the Attack006 stationary radial action with

U=V'+(A'/A)V−dot(A)/A

in the extrinsic-curvature term, retaining the same spatial curvature and lapse condensate potential. Its *unreduced* time-gradient Hessians are

partial² L / partial(dot A)²=−epsilon r²/(NA),
partial² L / [partial(dot A) partial(V')]=epsilon r²/N,

after dividing out the overall 4pi Mpl² factor.

Since the lapse and radial shift must be eliminated using their full differential/algebraic constraints, **these bare coefficients are NOT the physical kinetic eigenvalues**. Even the complete monopole reduction is not the full angularly resolved even/odd-parity perturbation spectrum. We expressly do NOT certify physical stability, all characteristics, the exact strong-coupling cutoff or gauge-reduced curved quadratic action. Relevant prior work: Mukohyama et al., *Spherical black hole perturbations in EFT of scalar-tensor gravity with timelike scalar profile*, JCAP 05 (2025) 084, DOI:10.1088/1475-7516/2025/05/084.

## Relation to exact earlier findings

- Attack002: restricted static scalar–Gauss–Bonnet center/horizon scalar flux obstruction.
- Attack003: ingoing-regular rolling scalar solves scalar and tr metric equation on Schwarzschild, but not the full tt gravitational equation.
- Attack004: exact coupled stealth k-essence Schwarzschild but gradient-degenerate physical scalar; Hayward source obstruction.
- Attack005: covariant Box² gives a heavy ghost, preferred foliation gives positive k⁴ and IR Jeans band.
- Attack006: first-order spherical metric backreaction with uniform rational residual certificate on [1.9,8].
- Attack007: **exact local nonlinear mixed-BVP existence** and nondegenerate Killing horizon in (1.9988,1.9995), NOT a global event horizon.
- Attack008: **C1 exterior mass rigidity**; any conventional differentiable stationary scalar-clock AF exterior has m_ADM=0 if its mass limit exists. No shift power law is assumed.

## Paper

Combined scholarly manuscript (14 pages, nine numbered main sections, five vector figures, title/affiliation footnote and current prior-art references):

*Stationary Scalar Clocks in a Minimal Preferred-Foliation Theory: Local Horizon Existence, Exterior Rigidity, and Perturbative Obstructions*.

The PDF, standalone LaTeX source and reproducibility archive are supplied as downloadable artifacts with the conversation. The native GitHub PR is research-only and remains draft.

## Reproduction

Run from the repository root, Python 3.11+ and SymPy 1.14:

    python research/frontier-physics-attack009/attack009_tail_jeans.py
    python research/frontier-physics-attack009/attack009_fraction_replay.py

The inherited PHYSQED generalized-harmonic release hold is unchanged, and the full repository regression suite has NOT been rerun. Passing scoped tests is not the same as an independent derivation of the full 4D covariant action or physical EFT validity.

## Prior-art / novelty boundary

Ghost-condensate k⁴/Jeans: Arkani-Hamed et al., JHEP05(2004)074. Stealth/scordatura: Motohashi–Mukohyama JCAP01(2020)030. Full spherical scalar-clock perturbations: Mukohyama, Takahashi, Tomikawa and Yingcharoenrat JCAP05(2025)084. Current classical black-hole context: De Felice–Tsujikawa arXiv:2607.08228, Kovachik–Sibiryakov PRD111(2025)044042, and Arata–Liberati–Neri PRD114(2026)084071.

Absolute originality of the particular local/rigidity combination requires an independent literature and referee audit. **No global nonsingular/stable black hole or solution of quantum gravity has been obtained.**
