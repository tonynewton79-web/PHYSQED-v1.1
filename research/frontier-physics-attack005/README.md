# PHYSQED Frontier Physics — Attack 005

Tony Newton — Newton Astro Labs, London, UK | 12 November 2026

**Research only. This is NOT a new gravity theory, a singularity cure, a complete stability result, or experimental confirmation.**

## 1. Governing actions

Signature (-+++), X = -(grad phi)^2/2, P(X) = lambda (X-X0)^2, lambda>0, q=sqrt(2X0)>0, reduced Planck mass squared Mp2>0.

**Completion A:** L = Mp2 R/2 + P(X) - beta (Box phi)^2/(2 Lambda^2), beta>0.

**Completion B:** L = Mp2 R/2 + P(X) - gamma q^2 theta^2/(2 Lambda^2), gamma>0, theta=div u, u_mu=-partial_mu phi/sqrt(2X). B requires X>0 and a preferred timelike foliation. Both are previously studied classes of operators.

## 2. Complete A equations and two-scalar ghost

Set B0=beta/Lambda^2. The equivalent auxiliary-field Lagrangian is L_A=Mp2 R/2+P(X)+B0 grad chi.grad phi+B0 chi^2/2, with chi=Box phi. Its *complete* field equations are

Mp2 G_ab = P_X partial_a phi partial_b phi +P g_ab -2 B0 partial_(a chi partial_b) phi + B0 g_ab (grad chi.grad phi+chi^2/2),

div(P_X grad phi)-B0 Box chi=0, chi=Box phi.

About flat phi=qt, scalar kinetic Hessian H=[[A,-B0],[-B0,0]], where A=2lambda q^2>0. det H=-B0^2<0: two scalar modes, one ghost. Einstein gravity adds two tensors. The fixed-metric scalar characteristic is A W-B0(W-k^2)^2=0 (W=omega^2), with

W_plus/minus=[A+2 B0 k^2 +/- sqrt(A^2+4 A B0 k^2)]/(2 B0).

W_minus=(B0/A)k^4+O(k^6); W_plus=A/B0+2k^2+O(k^4), with opposite-sign pole residues. Ghost m_g^2=A/B0 must lie outside the EFT domain to treat this as a low-energy expansion; no fundamental ghost-free theory is obtained.

## 3. Complete B field equations

Set C=gamma q^2/(2Lambda^2), h^ab=g^ab+u^a u^b, a=u^rho grad_rho theta. Varying the *full covariant action* gives

Mp2 G_ab = P_X partial_a phi partial_b phi+P g_ab+Ttheta_ab,

Ttheta_ab = -4C u_(a grad_b)theta -2C a u_a u_b +2C (a+theta^2/2)g_ab,

E_phi = div(P_X grad phi)+2C div[(h^ab/sqrt(2X))grad_a theta]=0.

All terms from metric and normalization variation are retained. Flat spacetime with phi=qt has X=X0, theta=0 and satisfies both full equations.

## 4. Gauge-reduced full-gravity scalar quadratic action

In unitary gauge phi=qt, set N=1+alpha, shift N_i=partial_i beta_s, spatial metric h_ij=e^(2zeta)delta_ij, sigma=spatial Laplacian(beta_s), v=dot zeta, and L=spatial Laplacian(zeta). Define epsilon=gamma q^2/(Mp2 Lambda^2)>0.

The quadratic scalar Lagrangian (after integrating boundaries) is

L2 = Mp2/2 [(-6-9epsilon)v^2 +(4+6epsilon)v sigma -epsilon sigma^2] + Mp2 (grad zeta)^2 -2 Mp2 alpha L +lambda q^4 alpha^2.

Lapse and scalar shift have no independent time derivatives; for nonzero spatial momentum their constraints are

alpha=Mp2 L/(lambda q^4), sigma=(2+3epsilon)v/epsilon.

The EXACT GAUGE-REDUCED scalar action is

Lred = Mp2(2/epsilon+3)dot(zeta)^2 +Mp2(grad zeta)^2 -Mp2^2/(lambda q^4)(Laplacian zeta)^2.

This shows a positive scalar time-kinetic coefficient and one scalar mode at quadratic order. The transverse-traceless metric has Mp2/8[dot(gamma_ij)^2-(grad gamma_ij)^2], hence two tensor modes and c_T=1. A full nonlinear Hamiltonian constraint count has not been carried out.

Scalar dispersion:

omega^2 = [Mp2 k^4/(lambda q^4)-k^2]/(2/epsilon+3).

It has a POSITIVE k^4 term but an IR Jeans instability when 0<k<kJ, with kJ^2=lambda q^4/Mp2 and maximal growth rate squared Gamma_max^2=kJ^2/[4(2/epsilon+3)]. Positive omega^2 for k>kJ is not proof of full perturbative weak coupling or hyperbolicity over arbitrary spacetimes.

## 5. Exact representative window (illustrative, NOT fitted data)

Set lambda=gamma=beta=q=1, Mp2=100, Lambda=10, illustrative momentum cutoff kcut=1. Then epsilon=1/10000, kJ=1/10, denominator 2/epsilon+3=20003, and omega^2(k=1/5)=3/500075>0, omega^2(k=1)=99/20003>0. But omega^2<0 for 0<k<1/10, and Gamma_max^2=1/8001200. A's heavy pole mass squared is 200, well above kcut^2. The illustrative cutoff does not substitute for a derived strong-coupling scale or observational bound.

## 6. Exact full Schwarzschild-background failures

For F=1-2M/r, rolling scalar phi=qt+psi(r), psi'=q sqrt(2M/r)/F, X=q^2/2:

Completion A has chi=Box phi=3q sqrt(2M)/(2r^(3/2)); Box chi=9q sqrt(2M)(r-6M)/(8r^(9/2)). Its scalar residual Ephi=-B0 Box chi is generically nonzero, and the full metric stress has T_tr=-B0 q chi'=9B0 q^2 sqrt(2M)/(4r^(5/2)) !=0, whereas Schwarzschild G_tr=0.

Completion B has theta=-3 sqrt(2M)/(2r^(3/2)) and the exact scalar residual Ephi=-9gamma q sqrt(2M)/(8Lambda^2 r^(7/2)). In Painleve-Gullstrand coordinates T=phi/q, h_ij is flat, lapse N=1, radial shift sqrt(2M/r); the GR Hamiltonian constraint term vanishes, but the B completion contributes the nonzero normal/lapse constraint residual

C_N=gamma q^2 theta^2/(2Lambda^2)=9gamma q^2 M/(4Lambda^2 r^3)>0.

Thus neither action retains the exact rolling Schwarzschild solution. Full modified black-hole metric backreaction remains unsolved. Schwarzschild's singular center is not removed.

## 7. Reproducibility

From the PHYSQED repo root, Python 3.11+ and SymPy 1.14.0:

    python research/frontier-physics-attack005/attack005_exact.py
    python research/frontier-physics-attack005/attack005_fraction_replay.py

The SymPy check derives exact pole roots, ADM algebraic constraints, dispersion and scalar/metric residuals. Fraction independently checks rational components, not the entire tensor functional variation. The scoped hosted GitHub workflow runs both programs. Existing generalized-harmonic release hold and the unverified inherited full regression suite remain separate.

## 8. Prior art and observational boundary

- Arkani-Hamed, Cheng, Luty & Mukohyama (2004), Ghost Condensation: https://doi.org/10.1088/1126-6708/2004/05/074
- Motohashi & Mukohyama (2020), scordatura: https://doi.org/10.1088/1475-7516/2020/01/030
- Takahashi & Motohashi (2021), DHOST perturbations: https://doi.org/10.1088/1475-7516/2021/08/013
- De Felice, Mukohyama & Takahashi (2022/2023), approximately stealth BH: https://arxiv.org/abs/2212.13031
- Gao & Hu (2020), covariant-spatial correspondence: https://doi.org/10.1103/PhysRevD.102.084006
- LVK July 2026, GWTC-5 tests: https://ligo.org/science-summaries/o4b_tgr/

The mechanism, including the gravitational Jeans scale and apparent high-frequency ghost, is established prior art. No new phenomenological prediction or observational likelihood comparison has been achieved.

## 9. Attack 006 research target

Solve the full spherical Einstein–scalar foliation equations at finite coupling gamma with physically specified asymptotics; control error relative to a Schwarzschild-like metric, monitor the Jeans growth time versus black-hole evolution, check full nonlinear hyperbolicity and EFT strong-coupling, and search for a bounded-curvature interior. A positive k^4 coefficient is necessary in this lane, but cannot substitute for a complete stable and regular solution.
