"""Independent exact-Fraction replay of Attack 003's r=4M checkpoint.

No SymPy; canonical Schwarzschild coordinates, Riemann convention R^a_bcd=
partial_c Gamma^a_db - partial_d Gamma^a_cb + Gamma*Gamma - Gamma*Gamma.
It checks two tensor component contractions from Christoffel-derived closed forms,
not a separate full nonlinear Einstein/Gauss-Bonnet verifier.
"""
from fractions import Fraction as Q


def run():
    M=eta=Q(1)
    r=Q(4)
    q=eta/(2*M**3)
    F=1-2*M/r
    Fp=2*M/r**2
    Fpp=-4*M/r**3
    # 4D Schwarzschild components from the Levi-Civita connection.
    Rtrrt=-Fpp/2
    Rtrtr=Fpp/2
    Rtthth=M*F/r
    assert Rtrrt == Q(1,32) and Rtrtr == -Q(1,32)
    assert Rtthth == Q(1,8)
    psi_p=16*eta*M**2/(r**5*F)
    psi_pp=psi_p*(-5/r-Fp/F)
    uprr=F**2*(psi_pp+Fp*psi_p/(2*F))
    uptheta=F*psi_p/r**3
    # Hess^rt = -Hess_rt due g^tt g^rr = -1.
    uprt=Fp*q/(2*F)
    Ptr=Rtrrt*uprt
    Ptt=Rtrtr*uprr+2*Rtthth*uptheta
    assert psi_p==Q(1,32)
    assert psi_pp==-Q(3,64)
    assert uprr==-Q(11,1024)
    assert uptheta==Q(1,4096)
    assert Ptr==Q(1,512)
    assert Ptt==Q(13,32768)
    Ttr=q*psi_p
    Ttt=(q*q+F*F*psi_p*psi_p)/2
    Etr=Ttr-8*eta*Ptr
    Ett=Ttt-8*eta*Ptt
    assert Etr==0
    assert Ttt==Q(1025,8192)
    assert Ett==Q(999,8192)
    assert Ett>0
    # Future-horizon EF radial derivative and finite X (M=eta=1).
    q_h=Q(1,2)
    chi_h=-5*q_h
    X_h=-q_h*chi_h
    assert chi_h==-Q(5,2)
    assert X_h==Q(5,4)
    print('PASS Fraction-only curvature/hessian contraction checkpoint M=eta=1, r=4M')
    print('P_tr=',Ptr,'P_tt=',Ptt)
    print('off-diagonal residual E_tr=',Etr)
    print('time-time residual E_tt=',Ett,'(nonzero)')
    print('future-horizon chi_prime=',chi_h,'X_h=',X_h)
    print('SCOPE: local independent rational replay of a fixed-background residual, not full coupled solver')


if __name__=='__main__':run()
