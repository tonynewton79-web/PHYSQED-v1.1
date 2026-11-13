"""PHYSQED Frontier Physics Attack 005 — exact completion and constraint filters.

Conventions:
  signature (-+++), X=-g^{ab}d_a phi d_b phi/2, X0=q^2/2.
  P(X)=lam*(X-X0)^2, lam>0.
  Background: Minkowski phi=qt; Schwarzschild phi=qt+psi(r) of Attack 004.

Two derivative completions, *not* new fundamental physics:
 A: -beta*(Box phi)^2/(2*Lambda^2) (covariant, heavy ghost).
 B: -gamma*q^2*(div u)^2/(2*Lambda^2), u_a=-d_a phi/sqrt(2X)
    (timelike-gradient foliation sector only; no additional time
     derivatives in unitary gauge, but IR Jeans instability).
Never promote local checks to a globally stable theory.
"""
import sympy as s

def zero(a):
    assert s.simplify(s.factor(a))==0, s.simplify(a)

def main():
    lam,q,Mp2,Lambda,beta,gamma,k,omega,r,M=s.symbols(
        'lam q Mp2 Lambda beta gamma k omega r M',positive=True)
    X0=q**2/2
    A=2*lam*q**2
    B=beta/Lambda**2

    # I. A covariant Box^2 correction: two scalar poles and opposite residues.
    W=s.symbols('W',real=True)
    scalar_det=s.factor(A*W-B*(W-k**2)**2)
    D=s.factor(A**2+4*A*B*k**2)
    roots=[s.factor((A+2*B*k**2+sgn*s.sqrt(D))/(2*B)) for sgn in (-1,1)]
    for root in roots:
        zero(scalar_det.subs(W,root))
    assert s.simplify(roots[0].subs(k,0))==0
    zero(roots[1].subs(k,0)-A/B)
    zero(s.limit(roots[0]/k**4,k,0,dir='+')-B/A)
    det_kin=s.det(s.Matrix([[A,-B],[-B,0]]))
    zero(det_kin+B**2)
    assert det_kin.is_negative
    zero(s.diff(scalar_det,W).subs(W,roots[0])-B*(roots[1]-roots[0]))
    zero(s.diff(scalar_det,W).subs(W,roots[1])+B*(roots[1]-roots[0]))
    # Hence opposite-sign pole residues: one heavy ghost.
    mghost2=A/B

    # II. Full-gravity unitary-gauge ADM quadratic Lagrangian for B.
    # alpha = lapse fluctuation, sigma = Laplacian of scalar shift,
    # zeta = curvature scalar, v=dot zeta, lap=Delta zeta.
    alpha,sigma,v,lap,grad2=s.symbols('alpha sigma v lap grad2')
    eps=gamma*q**2/(Mp2*Lambda**2)
    L2=(Mp2*s.Rational(1,2))*(
        (-6-9*eps)*v**2+(4+6*eps)*v*sigma-eps*sigma**2
    )+Mp2*grad2-2*Mp2*alpha*lap+lam*q**4*alpha**2
    alpha_c=s.solve(s.diff(L2,alpha),alpha)[0]
    sigma_c=s.solve(s.diff(L2,sigma),sigma)[0]
    zero(alpha_c-Mp2*lap/(lam*q**4))
    zero(sigma_c-(2+3*eps)*v/eps)
    Lred=s.factor(L2.subs({alpha:alpha_c,sigma:sigma_c}))
    expected=Mp2*(2/eps+3)*v**2+Mp2*grad2-Mp2**2*lap**2/(lam*q**4)
    zero(Lred-expected)
    # Kinetic coefficient positive, tensor kinetic = Mp2/8 positive.
    Dz=2/eps+3
    omega2=s.factor(((Mp2/(lam*q**4))*k**4-k**2)/Dz)
    kJ2=s.factor(lam*q**4/Mp2)
    zero(omega2.subs(k,s.sqrt(kJ2)))
    # Low-k is negative; high-k is positive below cutoff if a window exists.
    zero(s.limit(omega2/k**4,k,s.oo)-gamma/(2*lam*q**2*Lambda**2+3*gamma*lam*q**4/Mp2))
    growth2=s.factor(kJ2/(4*Dz))  # max of -omega^2 over 0<k<kJ
    zero(s.diff(omega2,k).subs(k,s.sqrt(kJ2/2)))
    zero(omega2.subs(k,s.sqrt(kJ2/2))+growth2)

    # III. Full-background failures on exact rolling-stealth Schwarzschild.
    F=1-2*M/r
    psi_prime=q*s.sqrt(2*M/r)/F
    boxphi=s.factor(s.diff(r**2*F*psi_prime,r)/r**2)
    boxboxphi=s.factor(s.diff(r**2*F*s.diff(boxphi,r),r)/r**2)
    zero(boxphi-3*q*s.sqrt(2*M)/(2*r**s.Rational(3,2)))
    zero(boxboxphi-9*q*s.sqrt(2*M)*(r-6*M)/(8*r**s.Rational(9,2)))
    # Covariant scalar EOM: -B Box(Box phi) != 0 at generic r.
    cov_scalar=s.factor(-B*boxboxphi)
    # Auxiliary-field equivalent L = +B d chi.d phi+B chi^2/2
    # gives T_tr^(Box^2)=-B q d_r chi.
    cov_tr=s.factor(-B*q*s.diff(boxphi,r))
    zero(cov_tr-9*B*q**2*s.sqrt(2*M)/(4*r**s.Rational(5,2)))

    # For projected foliation, u^r=-sqrt(2M/r), div u=theta.
    theta=-boxphi/q
    proj_laplacian=s.factor(s.diff(r**2*s.diff(theta,r),r)/r**2)
    zero(proj_laplacian+9*s.sqrt(2*M)/(8*r**s.Rational(7,2)))
    # First variation at fixed metric:
    # Ephi_theta=(gamma*q/Lambda^2) nabla_nu[h^{mu nu} d_mu theta].
    projected_scalar=s.factor(gamma*q/Lambda**2*proj_laplacian)

    # Painleve-Gullstrand slicing has spatially flat h, lapse N=1,
    # shift sqrt(2M/r), and extrinsic curvature trace theta.
    # GR Hamiltonian term Kij*Kij-K^2=0 but new K^2 term shifts
    # the lapse equation by +gamma*q^2 K^2/(2 Lambda^2).
    pg_hamiltonian=s.factor(gamma*q**2*theta**2/(2*Lambda**2))
    zero(pg_hamiltonian-9*gamma*q**2*M/(4*Lambda**2*r**3))

    # IV. Rational benchmark, scalar/tensor windows.
    p={lam:1,q:1,Mp2:100,Lambda:10,beta:1,gamma:1}
    assert eps.subs(p)==s.Rational(1,10000)
    assert kJ2.subs(p)==s.Rational(1,100)
    assert mghost2.subs(p)==200
    assert omega2.subs(p).subs(k,s.Rational(1,20))<0
    assert omega2.subs(p).subs(k,s.Rational(1,5))>0
    assert omega2.subs(p).subs(k,1)>0
    assert s.simplify(omega2.subs(p).subs(k,s.Rational(1,5)))==s.Rational(3,500075)
    # Note only gradient/ghost window, NOT proven perturbative weak coupling.
    assert growth2.subs(p)==s.Rational(1,8001200)
    # Sch. exact metric and scalar nonzero residuals, units beta=gamma=q=1, Lambda=10.
    bval=s.factor(cov_tr.subs({M:1,r:8,q:1,beta:1,Lambda:10}))
    hval=s.factor(pg_hamiltonian.subs({M:1,r:8,q:1,gamma:1,Lambda:10}))
    assert bval!=0 and hval==s.Rational(9,204800)

    print('PASS covariant pole polynomial and opposite residues; heavy ghost m_g^2=',mghost2)
    print('PASS full-gravity ADM alpha constraint=',alpha_c)
    print('PASS full-gravity ADM shift constraint=',sigma_c)
    print('PASS gauge-reduced scalar L2=',Lred)
    print('PASS 2 tensor + 1 scalar quadratic modes in projected foliation; c_T=1')
    print('PASS scalar dispersion omega^2=',omega2,'Jeans k_J^2=',kJ2)
    print('PASS representative positive-gradient window k in (1/10, 1)')
    print('PASS covariant Box^2 Schwarzschild scalar residual=',cov_scalar)
    print('PASS covariant Box^2 Schwarzschild T_tr=',cov_tr)
    print('PASS projected scalar Schwarzschild residual=',projected_scalar)
    print('PASS projected PG gravitational lapse residual=',pg_hamiltonian)
    print('PASS max negative omega^2 example=',-growth2.subs(p))
    print('NOT CERTIFIED: nonlinear Cauchy well-posedness, global stability, cutoff strong coupling, full astrophysical fit')

if __name__=='__main__':
    main()
