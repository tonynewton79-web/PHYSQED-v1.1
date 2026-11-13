"""Independent Fraction-only Attack009 necessary-condition replay."""
from fractions import Fraction as Q
def main():
    C=Q(1);e=Q(1,1000);mu=Q(1)
    a4=Q(3,2)*C*C;n6=6*C*C/mu;k7=12*C**3/(7*e)
    v6=-(Q(3,2)+3/(7*e))*C**3
    a6=-36*C*C/mu;n8=-180*C*C/mu**2
    assert Q(3,2)*C*C-a4==0
    assert mu*n6-Q(3,2)*C*C-3*a4==0
    assert 3*C**3-2*C*a4-2*C*mu*n6-2*k7-8*v6==0
    assert 2*C*mu*n6-7*e*k7==0
    assert a6+6*n6==0 and -5*a6+mu*n8==0
    D=2/e+3
    def w2(k):return (k**4/mu-k*k)/D
    assert w2(Q(1,4))<0 and w2(Q(1))==0 and w2(Q(2))>0
    assert mu/(4*D)==Q(1,8012)
    print('PASS independent formal asymptotic coefficient identities')
    print('PASS exact rational flat Jeans window and maximum growth rate')
    print('WARNING no nonlinear massless horizon exterior or full curved mode')

if __name__=='__main__':main()
