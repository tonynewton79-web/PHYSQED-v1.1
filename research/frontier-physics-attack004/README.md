# PHYSQED Frontier Physics — Attack 004

**Fully coupled noncanonical scalar backgrounds and exact stability obstructions.**  
Research only; this is not a new fundamental gravitational theory, a quantum-gravity construction, or a removal of spacetime singularities.

## Governing theory

With signature (-+++), X = -(grad phi)^2/2 and

S = integral sqrt(-g) [Mpl^2 R/2 + P(X)]

the coupled equations are Mpl^2 G_ab = P_X (partial_a phi)(partial_b phi) + P g_ab and div(P_X grad phi)=0.

## Exact full-background positive control

For P(X)=lambda (X-X0)^2 with lambda,X0>0, Schwarzschild F=1-2M/r and scalar phi=q t+psi(r) solve the **complete coupled background equations** when

q^2=2X0, psi'=q sqrt(2M/r)/F.

Then X=X0, P=P_X=0, so the exact scalar stress and shift current vanish. Advanced-coordinate chi'=psi'-q/F=-q/(1+sqrt(2M/r)) is smooth at the future horizon: chi'(2M)=-q/2. However Schwarzschild retains K=48M^2/r^6 at r=0.

## Perturbation obstruction and failed simple detuning

K_scalar=P_X+2X P_XX=4lambda X0>0; c_s^2=P_X/K_scalar=0. The scalar principal tensor

Z^ab=P_X g^ab-P_XX (grad^a phi)(grad^b phi)

is a rank-one outer product. The two-derivative scalar system lacks a nondegenerate spatial principal part, so a healthy propagating scalar is not certified. Adding epsilon(X-X0) makes c_s^2=epsilon/(epsilon+4lambda X0)>0, but produces T_tr=epsilon q psi' != 0; old static Schwarzschild fails the off-diagonal Einstein equation and needs new backreaction.

## Regular-center obstruction for this matter sector

For Hayward m(r)=Mr^3/(r^3+2M ell^2), G^t_t=G^r_r but

G^t_t-G^theta_theta = -36 M^2 ell^2 r^3/(r^3+2M ell^2)^3 != 0.

A single minimally coupled P(phi,X) scalar of the form phi=q t+psi(r) cannot source the **exact** diagonal Hayward metric: the zero mixed Einstein component requires P_X q psi'=0, forcing one of three diagonal stress equalities incompatible with these Einstein components. This is not a theorem for modified curvature couplings or arbitrary matter.

## Cosmological control and bounce refusal

For P(X)=lambda(X-X0)^2-V0 with V0>0, the flat-patch de Sitter metric a(t)=exp(Ht) and phi=sqrt(2X0)t solve the coupled equations with H^2=V0/(3Mpl^2), finite R=12H^2 and Kretschmann=24H^4. However scalar c_s^2=0 remains degenerate, and vacuum-energy shifts are unscreened: dH^2/d rho_vac=1/(3Mpl^2). No global smooth scalar extension/geodesic-completeness claim is made.

For flat FLRW Einstein+k-essence, 3Mpl^2 H^2=2X P_X-P and -Mpl^2 dot H=X P_X. A smooth bounce H=0, dot H>0 with X>0 needs P_X<0. If the scalar time-kinetic K_scalar>0, then c_s^2=P_X/K_scalar<0: a gradient instability. For P=X^2-3X/2 and X=1/2, the exact local bounce has rho=0, dot H=1/4 (Mpl=1), K_scalar=3/2, and c_s^2=-1/3. A short numerical integration preserves the Friedmann constraint but does not cure that instability.

## Reproduction and limitations

From the repository root:

    python research/frontier-physics-attack004/attack004_exact.py
    python research/frontier-physics-attack004/attack004_tensor.py
    python research/frontier-physics-attack004/attack004_fraction_replay.py
    python research/frontier-physics-attack004/attack004_flrw_numeric.py

The analytic checks and four-dimensional tensor route share SymPy. The Fraction script replays exact rational local cases without SymPy; SciPy numerically integrates the **gradient-unstable** local bounce. Local corresponding calculations passed 12 November 2026. Hosted GitHub CI and inherited PHYSQED regressions remain **unverified**; GH release hold is unchanged. These are theoretical/numerical consistency tests, not observed gravitational-wave fits.

The minimal Einstein–Hilbert tensor sector has c_T=1, compatible with the GW170817 tensor-propagation bound, but this does not validate the new scalar. July 2026 LVK GWTC-5.0 tests found no departure from GR, so matching Schwarzschild at the background level produces no new discriminatory observation: https://ligo.org/science-summaries/o4b_tgr/.

## Prior art and next gate

Stealth scalar solutions and strong-coupling warnings are established:
- Kobayashi–Tanahashi (2014): https://academic.oup.com/ptep/article/2014/7/073E02/1564012
- Minamitsuji–Motohashi (2018): https://doi.org/10.1103/PhysRevD.98.084027
- de Rham–Zhang (2019): https://doi.org/10.1103/PhysRevD.100.124023
- Motohashi–Mukohyama (2020) scordatura: https://doi.org/10.1088/1475-7516/2020/01/030
- DHOST review (2025): https://link.springer.com/article/10.1140/epjc/s10052-025-13983-8
- GW170817: https://arxiv.org/abs/1710.05834

**Next Attack 005:** Include a carefully cutoff-controlled higher-derivative EFT operator, derive its full field equations, test whether the exact stealth solution persists or backreacts, and independently certify the physical dispersion relation, degrees of freedom, hyperbolicity, ghost/gradient constraints and observational predictions. A k^4 dispersion term must not be assumed healthy until its sign and cutoff domain are proved.
