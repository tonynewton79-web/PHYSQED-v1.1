# PHYSQED Frontier Physics — Attack 007

Tony Newton | Newton Astro Labs, London, UK | 12 November 2026

**Research-only exact local nonlinear BVP and Killing-horizon certificate.** This does NOT establish a global event horizon, asymptotic flatness, a finite-curvature center, physical scalar stability, a new theory of gravity, or a resolution of GR singularities.

## Governing action and exact normal form

Continue the Attack 005 preferred-foliation action (signature -+++):

S=integral sqrt(-g)[Mp²R/2+lambda(X−q²/2)²−gamma q²(div u)²/(2 Lambda²)] d⁴x,
X=−(grad phi)²/2, u_mu=−d_mu phi/sqrt(2X), phi=q t.

Set eps=gamma q²/(Mp² Lambda²)>0 and mu=lambda q⁴/Mp²>0. With

ds²=−N(r)²dt²+A(r)²(dr+V(r)dt)²+r²dOmega²,

define K=[V'+(A'/A)V+2V/r]/N and S0=−mu A²r(N²−1)/(2N⁴). The **exact reduced stationary spherical equations** are

N'=N(A²−1)/(2r)+A²[eps N K²r/4+KV−3V²/(2Nr)]+mu A²Nr(N^(−2)−1)²/8,

A'=A(S0−N'/N),

V'=NK−2V/r−(A'/A)V,

K'=2VS0/(eps Nr)=−mu A²V(N²−1)/(eps N⁵).

The derivative coefficient determinant for the independent lapse/radial pair is **4r²/A⁴ >0** for r,A>0. The exact first-order normal form is checked by substituting into all three original reduced Euler–Lagrange expressions, not by numerical integration.

## Exact local mixed boundary-value existence

Set eps=1/1000, mu=1 (for example q=Mp²=lambda=1 and gamma/Lambda²=1/1000). On I=[1.997,2.003] impose

N(1.997)=32009/32000, V(1.997)=1251/1250, A(2.003)=1, K(2.003)=3/4.

In the function box centered at c=(32009/32000,1,1251/1250,3/4) with radii rho=(1/2000,1/1000,1/100,1/20), define the Green/Picard map by integrating N,V from the left boundary and A,K backward from the right.

Using *only exact rational interval arithmetic* and the full four-by-four Jacobian of the nonlinear vector field, the verifier proves the self-map ratio <91/100 and weighted Lipschitz constant <3/4. Banach's fixed-point theorem gives **a unique smooth exact radial solution** of the mixed nonlinear BVP within that box. This is a LOCAL exact existence theorem, not a perturbative truncation.

For an explicit affine trial satisfying the same boundary conditions, with slope F(2,c), the operator defect is <17/250. Therefore the actual solution is within **271/1000** of that trial in the weighted supremum norm. This is an actual local residual-to-solution bound, but does NOT upgrade Attack 006's much larger [1.9,8] residual certificate.

## Nondegenerate local Killing horizon

Five rigorously outward-rounded interval refinements establish N,A,V>0, X=1/(2N²)>0, and

g_tt(1.997)>0, g_tt(2.003)<0, g_tt'<−2/5 everywhere on I.

Since g^rr=−g_tt/(N²A²), the surface g_tt=0 is a smooth locally nondegenerate Killing horizon with exact enclosure **1.9988<r_h<1.9995**. The metric remains nondegenerate in the scalar-adapted coordinates; smoothness of the first-order rational ODE implies finite local curvature on this compact annulus.

For q=Mp²=lambda=1, the *bare* scalar k-essence time-kinetic coefficient 6X−1>19/10. This is **not** the complete curved-background physical gauge-reduced kinetic condition; tensor/scalar stability, horizon causality for all modes, and the EFT strong-coupling cutoff are NOT certified.

## Covariant equation scope

The stationary spherical action varies all three independent time/radial metric components. For q≠0 and r>0, the angular metric and scalar equations follow from the diffeomorphism Noether identity under the regular spherical ansatz. The reduction has been checked algebraically but a second completely independent four-dimensional field-variation backend has not yet been implemented.

## Conditional asymptotic obstruction and inverse caveat

Two exact on-shell identities are

(ln NA)'=−mu A²r(N²−1)/(2N⁴) and K'=−mu A²V(N²−1)/(eps N⁵).

Under standard differentiable 1/r expansions N=1+n1/r+n2/r²+n3/r³+..., A=1+a1/r+..., and a nonzero leading pure-power shift V~c r^(−p), p>0, the momentum identity forces p=2. The log identity gives n1=n2=0 and a1=mu n3; the radial equation then gives a1=0. **Nonzero conventional ADM mass is incompatible with this restricted stationary scalar-clock power-tail class.** More general clock asymptotics are not excluded.

A separate exact inverse of the epsilon=0 **linearized** first-order radial operator with a(4)=b(4)=0 has conservative C1 operator norm <20 on [1.9,8]. It does NOT carry over uniformly to finite eps, where the shift equation gains an extra derivative and stiffness 1/eps.

## Reproduce

Run these programs from the repo root using Python 3.11+, SymPy 1.14.0 for the symbolic scripts:

- research/frontier-physics-attack007/attack007_normal_form.py — exact reduced EL to ODE equivalence.
- research/frontier-physics-attack007/attack007_bvp_certificate.py — standard-library-only rational contraction, solution-distance and horizon proof.
- research/frontier-physics-attack007/attack007_jacobian_replay.py — independent SymPy-versus-Fraction replay of 8 vector values and 32 Jacobian entries.
- research/frontier-physics-attack007/attack007_linear_inverse.py — scoped epsilon-zero inverse.
- research/frontier-physics-attack007/attack007_asymptotics.py — conditional power-tail obstruction.

Dedicated CI: .github/workflows/physqed-frontier-attack007.yml. The inherited full PHYSQED regression suite has NOT been verified as part of this result; the preexisting generalized-harmonic release hold remains in force.

## Literature and next test

All main ingredients intersect established work; no absolute novelty claim is made:
- Eling and Jacobson (2006), black holes in Einstein-aether: https://doi.org/10.1088/0264-9381/23/18/009
- Static spherical Einstein-aether black holes (2020): https://doi.org/10.1103/PhysRevD.102.064043
- Adam et al. (2022), rotating Einstein-aether black holes: https://arxiv.org/abs/2108.00005
- Kovachik and Sibiryakov (2025), khronometric black holes: https://doi.org/10.1103/PhysRevD.111.044042
- Estrada (2026), spherical Hořava and Einstein-aether solutions: https://doi.org/10.1016/j.physletb.2026.140798

**Attack 008** should continue or obstruct this certified local solution toward an admissible exterior with nonzero mass, and independently calculate physical perturbation characteristics and EFT validity. Nothing yet solves the central singularity.
