"""Independent Fraction arithmetic checkpoints (no SymPy)."""
from fractions import Fraction as Q

def main():
    M=Q(1);r=Q(8);q=Q(2);lam=Q(3);X0=Q(2)
    F=1-2*M/r
    k=Q(1,2) # sqrt(2M/r) at r=8M
    psi=q*k/F
    X=(q*q/F-F*psi*psi)/2
    assert (F,psi,X)==(Q(3,4),Q(4,3),X0)
    assert psi-q/F==-q/(1+k)==Q(-4,3)
    P=lam*(X-X0)**2
    Px=2*lam*(X-X0)
    Pxx=2*lam
    assert P==Px==0
    kin=Px+2*X*Pxx
    assert kin==24 and Px/kin==0
    ut=-q/F; ur=F*psi
    Ztt=-Pxx*ut*ut
    Ztr=-Pxx*ut*ur
    Zrr=-Pxx*ur*ur
    assert (Ztt,Ztr,Zrr)==(Q(-128,3),Q(16),Q(-6))
    assert Ztt*Zrr-Ztr**2==0
    assert Px*q*psi==0 # complete off-diagonal source
    # Hayward mass M=1, ell^2=1/2, r=1
    rh=Q(1);ell2=Q(1,2)
    D=rh**3+2*M*ell2
    mp=6*M*M*ell2*rh**2/D**2
    mpp=24*M*M*ell2*rh*(M*ell2-rh**3)/D**3
    Gtt=-2*mp/rh**2;Gth=-mpp/rh
    assert (Gtt,Gth,Gtt-Gth)==(Q(-3,2),Q(3,4),Q(-9,4))
    # de Sitter: Mpl=2, V0=3
    Mp=Q(2);V0=Q(3)
    H2=V0/(3*Mp*Mp)
    assert H2==Q(1,4)
    assert 12*H2==3 and 24*H2**2==Q(3,2)
    assert (V0+Q(1,4))/(3*Mp*Mp)-H2==Q(1,48)
    # Bounce point X=1/2, P(X)=X^2-3X/2, Mpl=1
    xb=Q(1,2); pb=xb**2-Q(3,2)*xb
    pxb=2*xb-Q(3,2); kinb=pxb+4*xb
    assert (2*xb*pxb-pb,-xb*pxb,kinb,pxb/kinb)==(0,Q(1,4),Q(3,2),Q(-1,3))
    print("PASS exact Fraction replay: X constant, rank-one scalar characteristic, T_tr=0")
    print("PASS Hayward Gtt-Gtheta=-9/4, de Sitter H^2=1/4, bounce cs^2=-1/3")
    print("No full independent nonlinear symbolic backend is claimed.")

if __name__=="__main__":
    main()
