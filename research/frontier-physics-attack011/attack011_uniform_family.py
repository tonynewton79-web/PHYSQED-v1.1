"""Attack 011: parameter-uniform exact massless exterior/no-matching certificate.

Uses the previously verified nonlinear Green source and Fraction interval
classes from Attack010. Proves the result for EVERY 0<=C<=7/250, rather
than merely two individual parameter values.
"""
import sys
from pathlib import Path
from fractions import Fraction as Q
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"frontier-physics-attack010"))
import attack010_exterior_banach as old
I,D=old.I,old.D

def main():
    Cmax=Q(7,250);R=Q(1997,1000)
    old.C=I(0,Cmax);old.R=R
    C=old.C
    t=D(I(0,1/R))
    y=[D.var(I(-2,2),0),D.var(I(-2,2),1),
       D.var(I(Q(4,5),Q(6,5)),2),D.var(I(-2,2),3)]
    F,G,J,N,T=old.scaled(t,*y)
    ff,gg,jj=(z.v.mag() for z in (F,G,J))
    u_self=(ff+gg)/3;z_self=jj/5
    nt=N.v/T.v
    Imax=(C*C/old.EPS*T.v.mag()*old.weights[3]/(2*R**2)).hi
    q_self=max(abs(nt.lo-1),abs(nt.hi-1))+nt.mag()*Imax
    assert max(u_self/2,z_self/2,q_self/Q(1,5))<1
    lu=sum((F.der[j].mag()+G.der[j].mag())*old.weights[j] for j in range(4))/(3*old.weights[0])
    lz=sum(J.der[j].mag()*old.weights[j] for j in range(4))/(5*old.weights[3])
    du=(C*C/R**4/T.v.lo).hi
    dh=(N.v.mag()*C*C/R**3/T.v.lo**2).hi
    ih=(C**4/old.EPS*old.weights[3]/(5*R**5)).hi
    iz=(C*C/old.EPS*T.v.mag()/(2*R**2)).hi
    lq=((1+Imax)*(du*old.weights[0]+dh*old.weights[1])
        +nt.mag()*(ih*old.weights[1]+iz*old.weights[3]))/old.weights[2]
    assert max(lu,lz,lq)<Q(99,100)
    nmin=1-2*Cmax*Cmax/R**4
    amax=(1+2*Cmax*Cmax/R**3)/nmin
    vmax=Q(6,5)*Cmax/R**2
    assert nmin>0 and -nmin*nmin+(amax*vmax)**2<0
    # r=2 lies in [R,infty); earlier exact horizon BVP has V(2)>0.9908.
    assert Q(6,5)*Cmax/4==Q(21,2500)
    assert Q(21,2500)<Q(9908,10000)
    print("PASS each fixed amplitude 0<=C<=7/250 has a unique exact massless exterior")
    print("PASS strict uniform Green self-map and Lipschitz constant <99/100")
    print("PASS no Killing horizon on r>=1997/1000 for the entire family")
    print("PASS disjoint V(2): exterior <=21/2500 versus Attack007 >9908/10000")
    print("Certified row Lipschitz:",float(lu),float(lz),float(lq))
    print("SCOPE: no high-amplitude existence or all-C matching exclusion")

if __name__=="__main__":main()
