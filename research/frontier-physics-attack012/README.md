# PHYSQED Frontier Physics — Attack 012

Tony Newton — Newton Astro Labs, London, UK — 13 November 2026

**Research-only, verified exact exterior theorems.** This report does NOT certify an exterior-to-horizon matching zero, a global black hole, a regular interior, or the complete physical scalar/tensor spectrum and EFT cutoff.

## 1. Unchanged action and mathematical question

Retain the covariant scalar-clock preferred-foliation action and stationary spherical normal form from Attacks 005–011, with signature (−+++):

S=∫√−g [Mp²R/2+λ(X−q²/2)²−γq²(div u)²/(2Λ²)] d⁴x,

X=−(grad φ)²/2, u_μ=−∇_μφ/√(2X), φ=qt. Set μ=λq⁴/Mp²=1 and ε=γq²/(Mp²Λ²)=1/1000. In areal coordinates ds²=−N²dt²+A²(dr+Vdt)²+r²dΩ², let K=[V'+(A'/A)V+2V/r]/N.

The four-component nonlinear stationary spherical equations are EXACTLY transformed under

u=r(N−1), h=NA−1, W=Ar²V,

into an oscillator plus transports:

u'=h+F, h'=−u+G, W'=(1+h)r²K,
K'=−A W u(2+u/r)/(ε N⁵ r³),

where N=1+u/r, A=(1+h)/N, and the full nonlinear F,G have already been derived from the radial Einstein–scalar action and are replayed in attack012_exact_replay.py. The desired infinity Green branch excludes independent nondecaying oscillator modes and prescribes W(∞)=C>0, K(∞)=0.

## 2. Exact all-amplitudes far-exterior existence

**Theorem.** For every real C>0 there is a unique exact stationary spherical zero-ADM-mass exterior in the specified Green function box on r≥100(1+C).

**Proof.** Put t=1/r and s=C/r. On r≥100(1+C), both t and s belong to [0,1/100]. With the same exact normalized four-variable Green operator and weighted box of Attack010, namely |U|,|H|,|Z|≤2 and |Q−1|≤1/5, independently enclose t and s over that rectangle. The normalized rational source functions and all 16 state Jacobian entries are enclosed with Python Fraction arithmetic (no float calculations enter assertions). The exact self-map ratios are <0.401 in the U/H rows, <0.481 for Z, and <0.501 for Q. The exact row Lipschitz bounds are <0.168, <0.561 and <0.501, respectively. Thus the uniform contraction is <561/1000. Banach's theorem establishes the unique fixed point in this box. It differentiates to the exact radial equations and has N,A,X>0, V~C/r²≠0, g_tt<0 on the entire certified half-line, and m_ADM=0 from N−1=O(C²r^(−4)), A−1=O(C²r^(−3)). The existence statement concerns each fixed C on the stated amplitude-dependent half-line; it does not assert a common fixed radius for arbitrarily large amplitudes.

This eliminates the concern that arbitrarily large prescribed asymptotic C must fail to define an exterior. It does NOT prove a large-C horizon.

## 3. Uniform exact centered large-C infinity manifold

**Theorem.** For every C∈[7000,8000], the same infinity-selected nonlinear exact solution admits a considerably sharper a posteriori enclosure for all r≥50000. Let (N0,A0,V0,K0) be the explicit high-order formal ansatz from Attack011, with N through r^(−10), A through r^(−8), V through r^(−10), and K through r^(−11). Set u0=r(N0−1), h0=N0A0−1, W0=A0r²V0. Then

|u−u0| ≤ 10^23/r^9,  |h−h0| ≤ 10^23/r^9,
|W−W0| ≤ 2.8×10^28/r^8,  |K−K0| ≤ 1.8×10^29/r^11.

**Proof.** Apply the exact Green operator to the error about the polynomial trial. The trial's full nonlinear normal-form residuals have uniform exact rational interval bounds on C∈[7000,8000], r≥50000:

|r^11 E_N| ≤ 2.034×10^21, |r^11 E_A| ≤1.073×10^21,
|r^13 E_V| ≤7.905×10^24, |r^14 E_K| ≤3.091×10^28.

These decimals are UPWARD rounded summaries; proof assertions use exact Fraction values. Derive the Green defects from Ru=r E_N, Rh=A E_N+N E_A, RW=Ar²E_V+Vr²E_A, RK=E_K. Using rational interval Jacobian bounds over the entire uniform weighted error box, including BOTH oscillator source components in both Green rows, the Lipschitz row maxima are respectively less than 0.769, 0.804 and 0.809. Adding the exact residual defects gives strict self-map bounds <0.771, <0.804 and <0.809. Every bound is strictly below 81/100, proving the a posteriori Banach theorem and uniqueness within the weighted error box. On the shared far region r≥800100 the centered solution satisfies the earlier coarse Green-box bounds, so uniqueness identifies it with the exact all-C infinity-selected exterior branch.

At r=50000 the errors are |N−N0|≤1.024×10^(−24), |h−h0|≤5.12×10^(−20), |W−W0|≤7.168×10^(−10), and |K−K0|≤3.6864×10^(−23). This is a genuine solution-distance theorem, not just an ODE residual estimate.

## 4. Matching diagnostic versus a proof

Independent shooting in cancellation-safe variables u,h,W,K from high-order formal initial conditions at r=4000, 10000 and 50000 gives consistent NONRIGOROUS values at r=2:

C=7000: g_tt(2)≈−0.0118711361
C=7167: g_tt(2)≈+0.0000263679
C=7500: g_tt(2)≈+0.0233447041

This strongly supports the previous C≈7166.628 finite-start horizon candidate. However the initial-condition enclosure proven above is only at and beyond r=50000. We have NOT yet propagated that enclosure rigorously down to r=2 with directed-rounding Taylor models or established a validated Poincaré–Miranda/interval Newton matching zero. These finite-start numerical roots CANNOT be promoted into exact horizon existence.

For a free local horizon family, a certified sign change in g_tt(2) for two infinity-anchored amplitudes would imply at least one metric Killing horizon, provided a continuous regular radial continuation and all constraints are validated. The earlier exact horizon slope identity then guarantees nondegeneracy and uniqueness on its connected positive-lapse domain. Neither missing validation hypothesis has been discharged.

## 5. Physical and originality boundary

The previously proved stationary smooth-regular-center no-go still holds for the unchanged positive-lapse scalar clock. The full gauge-reduced curved scalar/tensor perturbation operator, hyperbolicity, and EFT strong-coupling cutoff remain unverified. The negative flat Jeans band and its compact-support Rayleigh witness already obstruct strict all-wavelength stability in the vacuum.

**Established methodological precedent:** Kevin Goldstein and Vishnu Jejjala, *A computer assisted existence proof for a non-Schwarzschild black hole in Einstein--Weyl gravity*, arXiv:2609.21797v2 (2026), uses a convergent horizon series, validated Taylor-model core, exact infinity stable manifold and a Poincaré--Miranda matching test. These methods do NOT prove our model's matching conjecture. The exact Green/Banach technique and interval fixed-point argument are established mathematical methods. An independent substantial originality and physics literature audit remains necessary before describing the present model-specific tail theorem as new in the literature.

## 6. Reproduce

Run from PHYSQED repo root (Python 3.11+, SymPy 1.14):

    python research/frontier-physics-attack012/attack012_all_amplitudes.py
    python research/frontier-physics-attack012/attack012_centered_tail.py
    python research/frontier-physics-attack012/attack012_exact_replay.py

The first test is pure Python Fraction+forward interval AD and proves the all-amplitudes half-line bound. The second test performs exact symbolic cancellation, bivariate rational interval polynomial enclosures and complete interval Jacobian bounds. The third independently derives the radial-to-Green coordinate identities. The dedicated CI is .github/workflows/physqed-frontier-attack012.yml. No full inherited PHYSQED regression suite was run for this attack. The original generalized-harmonic release hold remains intact.

## 7. Next mathematical gate

The immediate missing calculation is a **validated infinity-to-compact-core propagation** from the sharpened r=50000 large-C solution-distance boxes to r≈2. A Taylor-model/interval Lohner-type method should control the oscillatory (u,h) pair without uncontrolled wrapping, preserve positivity of N,A and track derivatives with respect to C. Only then may endpoint sign changes or a matching determinant be certified. If this fails, document a rigorous obstruction or a precise continuation singularity, rather than inferring physical black-hole existence from ordinary numerical shooting.
