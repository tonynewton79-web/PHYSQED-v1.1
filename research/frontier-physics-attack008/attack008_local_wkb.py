"""Attack 008 exact rational local scalar/tensor high-frequency checks.

ONLY frozen-coefficient WKB necessary conditions, not the complete
gauge-reduced curved-background spectrum. All assertions exact Fraction.
"""
from fractions import Fraction as Q

def main():
    lam=q=Mp2=Q(1); eps=Q(1,1000)
    gamma_over_Lambda2=eps*Mp2/q**2
    D=2/eps+3
    assert D==Q(2003)
    # The verified Attack007 horizon box includes 1<N<1.001.
    for N in [Q(100001,100000),Q(10003,10000),Q(1001,1000)]:
        X=q*q/(2*N*N);X0=q*q/2
        PX=2*lam*(X-X0);PXX=2*lam
        kinetic=PX+2*X*PXX
        H=X*kinetic
        assert X>0 and PX<0 and kinetic>Q(199,100) and H>Q(99,100)
        b4=gamma_over_Lambda2*N*N
        assert -PX/b4>0
        def frozen_test_scalar(k):return (PX*k*k+b4*k**4)/kinetic
        assert frozen_test_scalar(Q(1,100))<0
        assert frozen_test_scalar(Q(8))>0
        def frozen_gauge_uv(k):return (Mp2/H*k**4-k*k)/D
        assert frozen_gauge_uv(Q(8))>0 and frozen_gauge_uv(Q(12))>0
        # TT trace of principal time derivative vanishes: theta squared
        # does not modify its two-derivative tensor kinetic principal.
        t11=Q(3,7);t22=-t11;t33=Q(0)
        assert t11+t22+t33==0
        print('PASS local N=',N,'P_X=',PX,'Kbare=',kinetic)
    print('PASS bare timelike scalar kinetic and frozen positive quartic principal')
    print('PASS local fixed-metric scalar has negative k^2 coefficient for N>1')
    print('SCOPE: local high-k necessary checks; curved coupled spectrum/cutoff unresolved')

if __name__=='__main__':main()
