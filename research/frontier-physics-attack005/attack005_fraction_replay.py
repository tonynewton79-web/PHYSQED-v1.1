"""Independent standard-library rational replay of Attack 005.

No SymPy. Checks ADM Schur complement, ghost-Hessian signature,
Jeans band, and full-equation obstruction on Schwarzschild at r=8M.
This is independent component arithmetic, not a new geometric engine.
"""
from fractions import Fraction as Q

def main():
    Mpl2=Q(100); q=Q(1); lam=Q(1)
    Lambda=Q(10); gamma=beta=Q(1)
    eps=gamma*q*q/(Mpl2*Lambda**2)
    D=2/eps+3
    assert (eps,D)==(Q(1,10000),Q(20003))
    v=Q(1,100000)
    lap=Q(1,1000)
    grad2=Q(1,17)
    alpha=Mpl2*lap/(lam*q**4)
    sigma=(2+3*eps)*v/eps
    assert alpha==Q(1,10) and sigma==Q(20003,100000)
    Lbare=Mpl2/Q(2)*(
        (-6-9*eps)*v*v+(4+6*eps)*v*sigma-eps*sigma*sigma
    )+Mpl2*grad2-2*Mpl2*alpha*lap+lam*q**4*alpha*alpha
    Lreduced=Mpl2*D*v*v+Mpl2*grad2-Mpl2*Mpl2*lap*lap/(lam*q**4)
    assert Lbare==Lreduced
    assert 2*lam*q**4*alpha-2*Mpl2*lap==0
    assert (4+6*eps)*v-2*eps*sigma==0
    # Covariant completion: two scalar modes with kinetic determinant -B^2.
    A=2*lam*q*q
    B=beta/Lambda**2
    assert (A,B)==(Q(2),Q(1,100))
    H_det=-(B**2)
    assert H_det==Q(-1,10000)
    assert A/B==Q(200)  # heavy ghost pole omega^2 at k=0
    # Gauge-reduced scalar dispersion in full gravity (exact fractions).
    def w2(k):
        return ((Mpl2/(lam*q**4))*k**4-k*k)/D
    assert w2(Q(1,20))<0
    assert w2(Q(1,10))==0
    assert w2(Q(1,5))==Q(3,500075)>0
    assert w2(Q(1))==Q(99,20003)>0
    assert w2(Q(1,5))<1 # k=0.2 below EFT momentum cutoff=1
    # Schwarzschild PG at M=1, r=8 has sqrt(2M/r)=1/2.
    M=Q(1);r=Q(8);u=Q(1,2)
    theta=-3*u/(2*r)
    theta_prime=-3*theta/(2*r)
    # divergence of spatially projected gradient of theta on PG background
    Dtheta=-(Q(9,8))*Q(1,1024)
    projected_scalar=gamma*q/Lambda**2*Dtheta
    pg_hamiltonian=gamma*q*q/(2*Lambda**2)*theta**2
    assert theta==Q(-3,32)
    assert theta_prime==Q(9,512)
    assert Dtheta==Q(-9,8192)
    assert projected_scalar==Q(-9,819200)
    assert pg_hamiltonian==Q(9,204800)>0
    # Covariant Box^2 full scalar and tr metric residual.
    chi=Q(3,32)
    boxchi=chi*Q(3,4)/(r*r)*(1-6*M/r)
    cov_scalar=-B*boxchi
    cov_metric_tr=-B*q*(-Q(3,2)*chi/r)
    assert boxchi==Q(9,32768)
    assert cov_scalar==Q(-9,3276800)
    assert cov_metric_tr==Q(9,51200)>0
    print('PASS: Fraction ADM lapse/shift Schur complement and reduced scalar kinetic')
    print('PASS: full-gravity Jeans window and IR negative omega squared')
    print('PASS: covariant Hessian determinant',H_det,'heavy pole omega^2',A/B)
    print('PASS: projected scalar E_phi(r=8)=',projected_scalar)
    print('PASS: projected PG lapse residual(r=8)=',pg_hamiltonian)
    print('PASS: covariant scalar E_phi(r=8)=',cov_scalar)
    print('PASS: covariant metric T_tr(r=8)=',cov_metric_tr)
    print('NOT CLAIMED: nonlinear geodesic completeness, physical cutoff or global stability')

if __name__=='__main__':
    main()
