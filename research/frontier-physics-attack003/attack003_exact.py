"""PHYSQED Frontier Physics Attack 003: exact rolling scalar tests.

Assumptions: canonical shift-symmetric scalar, linear eta*phi*GB coupling;
Schwarzschild fixed background for exact residuals; static spherical geometry.
Signature -+++ and Riemann R^a_{bcd}=d_c Gamma^a_db -d_d Gamma^a_cb+...
Metric equation: G_ab/kappa = Tcanon_ab -8 eta P_{a rho b sigma} nabla^rho nabla^sigma phi.
On Ricci-flat Schwarzschild P = Riemann.
No coupled gravitational solution or stability theorem is claimed.
"""
import sympy as s


def run():
    r, M, eta, q, C = s.symbols('r M eta q C', positive=True)
    F = 1 - 2*M/r
    Fp = s.diff(F,r)
    GB=48*M**2/r**6
    psi_p=(C +16*eta*M**2/r**3)/(r**2*F)
    assert s.simplify(s.diff(r**2*F*psi_p,r)+eta*r**2*GB)==0
    rh=2*M
    horizon_balance =s.simplify((r**2*F*psi_p).subs(r,rh)-q*rh**2)
    assert horizon_balance == C+2*eta/M-4*M**2*q
    q0=eta/(2*M**3)
    assert s.simplify(horizon_balance.subs({C:0,q:q0}))==0
    psi0=s.factor(psi_p.subs(C,0))
    chi_p=s.factor(psi0-q0/F)
    chi_expected=-q0*sum((2*M/r)**k for k in range(5))
    assert s.simplify(chi_p-chi_expected)==0
    assert s.simplify(chi_p.subs(r,rh)+5*q0)==0
    X=s.factor((q0**2/F-F*psi0**2)/2)
    assert s.simplify(s.limit(X,r,rh)-5*q0**2)==0

    # Fully explicit Schwarzschild 4D curvature and scalar Hessian entries:
    # R_{trrt}=2M/r^3; R_{trtr}=-2M/r^3; R_{t theta t theta}=MF/r.
    # Schwarzschild P=R and eta*phi*GB metric term equals -8 eta P.Hessian.
    cov_tr=-Fp*q/(2*F)
    hess_rt_up=s.factor(-cov_tr)
    P_tr=s.factor((2*M/r**3)*hess_rt_up)
    T_tr=s.factor(q*psi0)
    E_tr=s.factor(T_tr-8*eta*P_tr)
    assert E_tr==0
    # Arbitrary integration C produces a residual q C/(r^2 F) (static metric).
    E_tr_general=s.factor(q*psi_p-8*eta*P_tr)
    assert s.simplify(E_tr_general-q*C/(r**2*F))==0

    pp=s.diff(psi0,r)
    hess_rr_up=F**2*(pp+Fp*psi0/(2*F))
    hess_th_up=F*psi0/r**3
    P_tt=s.factor((-2*M/r**3)*hess_rr_up + 2*(M*F/r)*hess_th_up)
    assert s.simplify(P_tt-32*M**3*eta*(6*r-11*M)/r**10)==0
    T_tt=s.factor((q**2+F**2*psi0**2)/2)
    E_tt=s.factor(T_tt-8*eta*P_tt)
    expected=(q**2*r**10 + 5888*M**4*eta**2 -3072*M**3*eta**2*r)/(2*r**10)
    assert s.simplify(E_tt-expected)==0
    assert s.limit(E_tt,r,s.oo)==q**2/2
    E_tt_at_4M=s.factor(E_tt.subs({q:q0,r:4*M}))
    assert E_tt_at_4M==s.Rational(999,8192)*eta**2/M**6
    # No vacuum Einstein equation: G_tt =0 on Schwarzschild but E_tt !=0.
    assert E_tt_at_4M!=0

    # Asymptotically flat no-go: if phi=qt+o(r) with radial gradient -> 0,
    # canonical scalar stress tends q^2/2, while curvature correction decays.
    # Even Lambda cannot cancel both tt and rr Minkowski components.
    L=s.symbols('Lambda')
    tt_res=-L-q**2/2
    rr_res=L-q**2/2
    assert s.solve([tt_res,rr_res],[L,q**2])=={L:0,q**2:0}

    # Hayward M=1, ell^2=1/2: finite-center C=0 forces distinct q at
    # the two nondegenerate horizons for the *same* ingoing orientation.
    rplus=(1+s.sqrt(5))/2
    Fh=1-2*r**2/(r**3+1)
    assert s.factor(s.together(Fh))==s.factor((r-1)*(r**2-r-1)/(r**3+1))
    qminus=s.simplify(4*eta*s.diff(Fh,r).subs(r,1))
    qplus=s.simplify(s.radsimp(4*eta*s.diff(Fh,r).subs(r,rplus)/rplus**2))
    assert qminus==-2*eta
    assert s.simplify(qplus-eta*(25-11*s.sqrt(5)))==0
    assert s.simplify(qplus-qminus)!=0

    print('PASS scalar equation, arbitrary flux C and future-horizon condition')
    print('PASS zero-flux horizon-regular rolling q=',q0,'; EF chi_prime(2M)=',-5*q0)
    print('PASS finite scalar kinetic invariant at horizon X=',5*q0**2)
    print('PASS off-diagonal field equation: E_tr= q*C/(r^2*F); vanishes for C=0')
    print('PASS independent Ricci-flat curvature/Hessian contractions for P_tr and P_tt')
    print('PASS Schwarzschild tt effective source E_tt =',E_tt)
    print('PASS nonzero tt residual at r=4M with q=q0:',E_tt_at_4M)
    print('PASS asymptotic obstruction E_tt(infinity)=q^2/2; Lambda cannot cancel isotropic stiff gradient')
    print('PASS Hayward rolling rates incompatible: q_minus=',qminus,'q_plus=',qplus)
    print('VERDICT: scalar horizon escape YES; full Einstein equations NO; asymptotically flat rolling vacuum NO')


if __name__=='__main__':run()
