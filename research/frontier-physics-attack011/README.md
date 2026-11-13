# PHYSQED Frontier Physics — Attack 011

**Tony Newton — Newton Astro Labs — London, UK | 13 November 2026**

**Research-only mathematics.** Exact scope: the *unchanged* preferred-foliation action and regular stationary spherical scalar-clock chart of Attacks 005–010. This note proves a horizon rigidity/no-regular-center theorem and a parameter-uniform small-amplitude nonmatching theorem, and gives a separately labeled **nonrigorous** high-amplitude massless-horizon candidate. It does **not** establish a globally asymptotically flat horizon solution, a stable higher-derivative physical spectrum, a regular black-hole center, a cutoff, or an original fundamental theory.

## 1. Governing action and exact radial equations

Use signature (-+++), X=−(grad phi)^2/2, q>0, u_mu=−∇_mu phi/sqrt(2X), and

S=integral sqrt(−g) [ Mpl² R/2 +lambda(X−q²/2)² −gamma q²(div u)²/(2Lambda²)] d⁴x.

Set epsilon=gamma q²/(Mpl² Lambda²)>0, mu=lambda q⁴/Mpl²>0. In scalar-clock gauge phi=q t,

ds²=−N(r)²dt² +A(r)²(dr+V(r)dt)²+r²dOmega²,

with N,A>0, r>0, and K=[V'+(A'/A)V+2V/r]/N. Define

S0=−mu A²r(N²−1)/(2N⁴).

The exact stationary spherical field equations are

N'=N(A²−1)/(2r)+A²[epsilon N K²r/4 +KV−3V²/(2Nr)]+mu A²Nr(N^(−2)−1)²/8,

A'=A(S0−N'/N),

V'=NK−2V/r−(A'/A)V,

K'=2VS0/(epsilon Nr).

The equivalence of these first-order ODEs and the original reduced Euler–Lagrange system was proved and checked in Attack007. The result does not assert a complete gauge-reduced dynamic perturbation theory.

## 2. Exact Killing-horizon rigidity and uniqueness (winner)

Define G=g_tt=−N²+A²V². A metric Killing horizon in this chart is a root G(r_h)=0, equivalently V_h=±N_h/A_h. Differentiate G along the *complete nonlinear radial equations*, substitute either root condition, and simplify:

G'(r_h)=−N_h² A_h² [1/r_h +epsilon K_h² r_h/2 +mu r_h(N_h^(−2)−1)²/4] <0.

This is valid for **both** signs of V at the horizon, for positive r,N,A,epsilon,mu. Therefore all roots are simple, all change from G>0 on their inner side to G<0 on their outer side, and a connected regular chart contains **at most one metric Killing horizon**. A second horizon would necessarily require an upcrossing, contradicting the exact negative derivative. Degenerate metric Killing horizons are excluded in this sector.

For the *positive ingoing* shift V_h=N_h/A_h, the Killing surface gravity with chi=partial_t is

kappa_h=(N_h A_h/2)[1/r_h+epsilon K_h²r_h/2+mu r_h(N_h^(−2)−1)²/4]>0.

For outgoing V_h<0 the signed kappa (fixed chi orientation) reverses; the displayed expression is its positive **magnitude**. This sign distinction does not affect the theorem.

The same equations give a useful radial quasi-local spatial mass derivative identity, for m_s(r)=r(1-A^(−2))/2:

m_s'=3V²/(2N²)−rKV/N−epsilon r²K²/4−mu r²(N²−1)(N²+3)/(8N⁴).

For V!=0 the ratio y=r N K/V obeys

y'=y(3−y)/r+(y+2/epsilon)S0.

These identities are independently checked exactly and may support a stronger global matching invariant.

## 3. Exact regular-center no-go and preferred-foliation horizon caution

At a smooth spherical center in a nondegenerate globally regular stationary foliation, N→N0>0, A=1+O(r²), and V=O(r). Hence G(0)=−N0²<0. If a positive-radius Killing horizon occurred, the *innermost* one would have to cross G from negative to positive when moving outward, because every horizon demands G>0 immediately to its interior. This contradicts Section 2. Equivalently, the unique-root/downcrossing theorem forbids any stationary metric Killing horizon on a connected regular-center domain.

**Conditional theorem:** A globally smooth stationary spherical regular center with positive finite scalar-clock lapse and the exact action cannot coexist with a metric Killing horizon. It may fail if the foliation breaks down, N or X becomes singular, the topology changes, a time-dependent sector becomes necessary, or one modifies the action. No broad no-go for other Einstein-aether or Horndeski models is claimed.

Further, the unit normal obeys chi^mu u_mu=−N. Hence the usual universal-horizon condition chi.u=0 is not met anywhere in the regular N>0 scalar-clock patch. This does not exclude a universal horizon beyond the patch where the clock foliation breaks down.

## 4. Continuum exact small-amplitude exterior and nonmatching (runner-up)

The Attack010 exact Green/Banach system uses mu=1, epsilon=1/1000 and asymptotic parameter C=lim_(r→infinity) Ar²V. Attack010 individually certified C=1/100, and separately a domain r>=100 for C=1/10.

**New uniform parameter theorem:** On r>=1997/1000, the **same exact rational interval enclosure** holds simultaneously for every C in [0,7/250]. The Banach self-map and full four-component weighted Jacobian bounds are uniform with maximum contraction <99/100 (actual checked maximum about 0.98528). The proof uses exact interval arithmetic simultaneously over t=1/r∈[0,1000/1997], state box |U|,|H|,|Z|<=2 and |Q−1|<=1/5, and amplitude C∈[0,7/250]. Each fixed C has a unique exact smooth massless exterior in that box; for C>0, V!=0. Every solution has N,A>0 and G<0 throughout its certified exterior.

At r=2 these exteriors obey V(2)<=21/2500=0.0084, versus the exact Attack007 horizon BVP V(2)>0.9908, so **none of the entire continuous family matches that specified horizon**. This excludes C≤0.028 *within the same bounded Green class*; the conclusion does not extend to larger C, unusual oscillatory asymptotic branches, or time-dependent solutions. The C=0 member is the exact trivial Minkowski vacuum.

Reproduction: attack011_uniform_family.py imports Attack010's Fraction interval class and normalized Green source, without numerical sampling.

## 5. Large-amplitude massless-horizon candidate: numerical only

Use epsilon=1/1000, mu=1 and the **high-order FORMAL asymptotic coefficients** (including C⁴/epsilon terms absent from the shorter initial tail). Initialize the exact four-state radial ODE at r=2000 or 4000 and integrate inward to r=2.

Representative R=4000 DOP853 diagnostics:

C=7000: G(2)≈−0.01187114;
C=7500: G(2)≈+0.02334470;
C=8000: G(2)≈+0.05740875.

Root of the *finite-start numerical shooting condition* G(2)=0 occurs near C≈7166.6277. The associated numerical state is

(N,A,V,K)(2)≈(1.00027826,1.00673384,0.99358761,0.74107511).

Corrected higher asymptotic coefficients and comparison of R=2000 versus R=4000 agree closely. A separate DOP853/Radau comparison gives consistent signs. This is **strong numerical evidence** for a possible nontrivial zero-mass Killing-horizon branch, but no infinity-anchored interval validation has been performed for these enormous C values. The known formal series is divergent already at order C², so truncating it and increasing the start radius is **not an exact boundary condition at infinity**. The numerical root is not a theorem or certified black hole.

The numerical candidate is disjoint from the **specific** Attack007 horizon BVP: its A(2)≈1.006734 whereas the latter has A(2)≈1.000008. These approximate numerical comparisons do not exclude matching a different local horizon solution.

A future rigorous candidate construction should combine an infinity-anchored nonlinear Green manifold with directed-rounding Taylor-model finite-radius continuation and a validated matching zero. This resembles the methods used in Goldstein's 2026 computer-assisted Einstein–Weyl black-hole existence proof, but our field equations and asymptotic scalar clock are different.

## 6. Strict scalar stability: an exact compact-support witness

The **fully constrained flat** scalar dispersion from Attack005 and Attack009 is

omega²(k)=[k⁴/mu−k²]/D, D=2/epsilon+3>0.

The selfadjoint flat spatial scalar operator is H0=(Delta²/mu+Delta)/D. Its Fourier spectrum is the interval [−mu/(4D),infinity). In particular **no strict positive spectral bound is possible in the flat vacuum**.

A more explicit finite-energy witness is the compactly supported radial function

f(x)=(1−|x−x0|²/L²)^3 for |x−x0|<L; f=0 otherwise, L=6/sqrt(mu).

Direct polynomial integration in three dimensions gives

||grad f||²/||f||²=27/(2L²),
||Delta f||²/||f||²=585/(2L⁴),

hence

<f,H0 f>/||f||² = −43 mu/[288D] <0.

This witness belongs to the H² quadratic-form domain and can be translated into a ball arbitrarily far outside a compact object. For a curved exterior, the same negative band follows **conditionally** if its full gauge-reduced physical scalar operator has a selfadjoint asymptotically flat realization whose quadratic form converges suitably to H0 on translated compact tests. That convergence and the complete curved scalar/tensor constraint reduction **have not yet been demonstrated**. The known flat Jeans instability is prior art, not a new mechanism.

## 7. Reproducibility and trust boundary

From the GitHub repository root, Python 3.11+ with SymPy 1.14 and SciPy:

    python research/frontier-physics-attack011/attack011_horizon_rigidity.py
    python research/frontier-physics-attack011/attack011_uniform_family.py
    python research/frontier-physics-attack011/attack011_spectral_witness.py
    python research/frontier-physics-attack011/attack011_large_C_shoot.py

Dedicated hosted scoped workflow: .github/workflows/physqed-frontier-attack011.yml.

The first three scripts check **exact algebra or Fraction interval theorems**; the fourth is **nonrigorous numerical evidence only**. Neither the original full PHYSQED regression suite nor a completely independent four-dimensional functional-variation backend was run here. The earlier generalized-harmonic release hold remains unchanged.

## 8. Literature and originality audit

Regular-center spherical black holes generally require inner and outer horizons, a standard phenomenon rather than novelty; see Sean Hayward (2006), DOI:10.1103/PhysRevLett.96.031103, and Bonanno–Khosravi–Saueressig (2021), DOI:10.1103/PhysRevD.103.124027.

Preferred-foliation causal horizons and their relation to the scalar clock are established: Bhattacharyya–Colombo–Sotiriou (2016), *Causality and black holes in spacetimes with a preferred foliation*; Eling–Jacobson (2006), *Black holes in Einstein-aether theory*. A recent exact preferred-foliation discussion is Arata et al. (2026), arXiv:2610.12559.

A directly relevant *computer-assisted horizon-to-infinity* prior-art method is Kevin Goldstein (2026), arXiv:2609.21797, *A computer assisted existence proof for a non-Schwarzschild black hole in Einstein--Weyl gravity*. Those proof techniques are established and must not be presented as original merely for using them.

No absolute originality claim is made for the horizon-uniqueness or regular-center exclusion; both are specialized results that require expert prior-art audit and independent checking against the covariant equations.

## 9. Next decisive research obligation

**Attack012:** Construct a validated large-C infinity manifold, continue it with interval Taylor models to r≈2, and search for a signed matching determinant with a locally exact horizon solution. First establish **global mathematical existence**; then compute the full physical gauge-reduced curved scalar and tensor spectrum and the EFT strong-coupling limit. The negative flat scalar essential spectrum already puts a strict global stability requirement under serious pressure. If any stationary solution has a metric horizon, the present exact regular-center theorem prevents that solution from curing the central singularity while the clock remains globally regular. The appropriate next physical lane may therefore be a time-dependent scalar clock.
