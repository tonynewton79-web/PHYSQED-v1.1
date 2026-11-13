"""PHYSQED Frontier Attack 001: exact restricted f(R) and regular-core checks.

This is a *model filter*, not an argument for a UV-complete theory. Uses
SymPy exact symbolic arithmetic, with separate algebraic consistency checks.
Units: G=c=1; GR Einstein equation G_ab = 8*pi*T_ab.
"""
import sympy as s


def main():
    R, alpha, beta, lam, kap, rho = s.symbols('R alpha beta Lambda_bare kappa rho_vac', real=True)
    f=R+alpha*R**2-2*lam
    trace=s.factor(R*s.diff(f,R)-2*f)
    assert trace == -R+4*lam
    curvature=s.solve(s.Eq(trace,-4*kap*rho),R)
    assert curvature==[4*kap*rho+4*lam]
    # General analytic f(R) with f(0)=0: every Ricci-flat spacetime remains
    # a vacuum solution. For R=0 constant, all derivative terms vanish.
    f_generic=R+alpha*R**2+beta*R**3
    assert f_generic.subs(R,0)==0
    assert s.diff(f_generic,R).subs(R,0)==1

    M, ell, r=s.symbols('M ell r',positive=True)
    F_schw=1-2*M/r
    def K(F):
        return s.factor(s.diff(F,r,2)**2+4*(s.diff(F,r)/r)**2+4*((1-F)/r**2)**2)
    assert s.simplify(K(F_schw)-48*M**2/r**6)==0

    m=M*r**3/(r**3+2*M*ell**2)
    F=s.factor(1-2*m/r)
    d=m.diff(r)
    rho_eff=s.factor(d/(4*s.pi*r**2))
    pr=s.factor(-rho_eff)
    pt=s.factor(-m.diff(r,2)/(8*s.pi*r))
    assert s.simplify(rho_eff-3*M**2*ell**2/(2*s.pi*(r**3+2*M*ell**2)**2))==0
    assert s.simplify(pt-3*M**2*ell**2*(r**3-M*ell**2)/(s.pi*(r**3+2*M*ell**2)**3))==0
    nec_t=s.factor(rho_eff+pt)
    assert s.simplify(nec_t-9*M**2*ell**2*r**3/(2*s.pi*(r**3+2*M*ell**2)**3))==0
    assert s.factor(rho_eff+pr)==0
    assert s.factor(rho_eff-pt)==s.factor(3*M**2*ell**2*(4*M*ell**2-r**3)/(2*s.pi*(r**3+2*M*ell**2)**3))
    Ric=s.factor(-F.diff(r,2)-4*F.diff(r)/r+2*(1-F)/r**2)
    assert s.limit(Ric,r,0)==12/ell**2
    Kcore=K(F)
    assert s.limit(Kcore,r,0)==24/ell**4
    assert s.limit(F,r,s.oo)==1
    assert s.limit((1-F)*r,r,s.oo)==2*M
    # The strong energy condition is violated near r=0 because p_t < 0.
    assert s.limit(pt,r,0)==-3/(8*s.pi*ell**2)
    assert s.limit(rho_eff,r,0)==3/(8*s.pi*ell**2)
    # g^t_t horizon discriminant, with degenerate root r=4M/3.
    poly=r**3-2*M*r**2+2*M*ell**2
    r_ext=s.Rational(4,3)*M
    ell2_ext=s.solve(poly.subs(r,r_ext),ell**2)[0]
    assert ell2_ext == s.Rational(16,27)*M**2
    assert s.factor(s.diff(poly,r).subs(r,r_ext))==0

    print('PASS: constant-curvature quadratic f(R) trace =',trace)
    print('PASS: curvature response R =',curvature[0])
    print('PASS: Schwarzschild K =',K(F_schw))
    print('PASS: Hayward rho =',rho_eff)
    print('PASS: Hayward p_r =',pr)
    print('PASS: Hayward p_t =',pt)
    print('PASS: Hayward rho+p_t =',nec_t)
    print('PASS: Hayward DEC tangential margin rho-p_t =',s.factor(rho_eff-pt))
    print('PASS: Hayward curvature R(0) =',s.limit(Ric,r,0),'K(0) =',s.limit(Kcore,r,0))
    print('PASS: extremality ell^2 =',ell2_ext,'; Schwarzschild asymptotics')
    print('SCOPE: known restricted-model mathematics; not a new gravity theory')

if __name__=='__main__':
    main()
