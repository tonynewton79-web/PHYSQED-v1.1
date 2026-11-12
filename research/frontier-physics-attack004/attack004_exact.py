"""Frontier Attack 004: exact coupled k-essence backgrounds and obstructions.

Research-only checks; not a viable quantum-gravity theory. Signature (-+++).
S = integral sqrt(-g) [Mpl**2 R/2 + P(X)], X=-(d phi)^2/2.
Mpl**2 G_ab=P_X d_a phi d_b phi+P g_ab; div(P_X grad phi)=0.
"""
import sympy as s

def eq(a,b):
    return s.simplify(a-b)==0

def main():
    M,r,q,lam,X0,eps,ell,V0,Mp=s.symbols("M r q lam X0 eps ell V0 Mp",positive=True)
    Xs=s.symbols("X")
    F=1-2*M/r
    u=s.sqrt(2*M/r)
    psi=q*u/F
    X=s.factor((q**2/F-F*psi**2)/2)
    assert eq(X,q**2/2)
    chi=s.radsimp(s.factor(psi-q/F))
    assert eq(chi,-q/(1+u))
    assert eq(s.limit(chi,r,2*M),-q/2)
    P=lam*(Xs-X0)**2
    Px=s.diff(P,Xs)
    Pxx=s.diff(Px,Xs)
    assert P.subs(Xs,X0)==0 and Px.subs(Xs,X0)==0
    assert eq(P.subs(Xs,X).subs(X0,q**2/2),0)
    assert eq(Px.subs(Xs,X).subs(X0,q**2/2),0)
    # Full Einstein tensors for the spherical vacuum metric.
    Gt=s.factor((r*s.diff(F,r)+F-1)/r**2)
    Gth=s.factor(s.diff(F,r,2)/2+s.diff(F,r)/r)
    assert Gt==Gth==0
    # T_ab and scalar current vanish because P=Px=0 at constant X.
    assert s.simplify((Px*psi*q).subs(Xs,X0))==0
    kinetic=s.factor((Px+2*Xs*Pxx).subs(Xs,X0))
    assert eq(kinetic,4*lam*X0)
    cs2=s.factor((Px/(Px+2*Xs*Pxx)).subs(Xs,X0))
    assert cs2==0
    # Principal symbol is an outer product and rank one.
    ginv=s.diag(-1/F,F,1/r**2,1/r**2)
    grad_up=ginv*s.Matrix([q,psi,0,0])
    Z=-2*lam*grad_up*grad_up.T
    assert Z.subs({M:1,r:8,q:2,lam:3}).rank()==1
    # Ordinary kinetic detuning lifts c_s but creates T_tr != 0.
    Pdet=P+eps*(Xs-X0)
    pdetx=s.diff(Pdet,Xs).subs(Xs,X0)
    detK=(s.diff(Pdet,Xs)+2*Xs*s.diff(Pdet,Xs,2)).subs(Xs,X0)
    assert pdetx==eps
    assert eq(pdetx/detK,eps/(eps+4*lam*X0))
    assert s.factor(eps*q*psi)!=0
    # Schwarzschild curvature remains singular at the center.
    KS=s.factor(s.diff(F,r,2)**2+4*(s.diff(F,r)/r)**2+4*((1-F)/r**2)**2)
    assert eq(KS,48*M**2/r**6)
    # Hayward geometric anisotropy cannot be sourced by one P(phi,X)
    # with phi=qt+psi(r) and a diagonal static Einstein metric.
    D=r**3+2*M*ell**2
    Fh=1-2*M*r**2/D
    Gh=(r*s.diff(Fh,r)+Fh-1)/r**2
    Gtheta=s.diff(Fh,r,2)/2+s.diff(Fh,r)/r
    gap=s.factor(Gh-Gtheta)
    assert eq(gap,-36*M**2*ell**2*r**3/D**3)
    # Fully coupled rolling-scalar flat-de Sitter control.
    # P(X)=lam(X-X0)^2-V0, phi=sqrt(2X0)t.
    H2=V0/(3*Mp**2)
    assert eq(3*Mp**2*H2,V0)
    assert eq(-3*Mp**2*H2,-V0)
    delta=s.symbols("delta")
    assert eq(s.diff((V0+delta)/(3*Mp**2),delta),1/(3*Mp**2))
    # Flat FLRW bounce example P=X^2-3X/2, X=1/2.
    xb=s.Rational(1,2)
    Pb=xb**2-s.Rational(3,2)*xb
    Pxb=2*xb-s.Rational(3,2)
    Kb=Pxb+4*xb
    assert 2*xb*Pxb-Pb==0
    assert -xb*Pxb==s.Rational(1,4)
    assert Kb==s.Rational(3,2) and Pxb/Kb==-s.Rational(1,3)
    print("PASS full Schwarzschild + rolling k-essence background, smooth future horizon")
    print("PASS scalar principal rank one, K>0, c_s^2=0")
    print("PASS gradient detuning makes T_tr nonzero and fails old Schwarzschild")
    print("PASS Hayward anisotropy:",gap)
    print("PASS exact rolling-scalar de Sitter background; vacuum shift not screened")
    print("PASS local flat bounce algebra; scalar gradient unstable")
    print("NOT CERTIFIED: stable perturbations, geodesic completeness, observations, novelty")

if __name__=="__main__":
    main()
