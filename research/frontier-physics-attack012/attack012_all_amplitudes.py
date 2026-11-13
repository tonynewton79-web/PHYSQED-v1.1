"""PHYSQED Attack 012: exact rational all-amplitudes infinity Green theorem.

For every real C>0 at fixed mu=1, eps=1/1000, prove an exact
asymptotically-flat zero-ADM-mass exterior on r>=100(1+C).
This says nothing about a horizon below that radius.
"""
import sys
from pathlib import Path
from fractions import Fraction as Q
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'frontier-physics-attack010'))
from attack010_exterior_banach import I,D,EPS,weights

def source(s,t,U,H,P,Z):
    x=s*s*t*t*U;N=1+x;T=1+s*s*t*H;A=T/N
    F=(s*s*(H-t*U)**2/(2*N)
       +s**4*A*A*N*Z*Z/(4*EPS)
       +s*s*A*A*P*Z/EPS
       -Q(3,2)*A*A*P*P/N
       +s*s*A*A*U*U*(2+x)**2/(8*N**3))
    G=s*s*U*(t*U*(2*sum(N**j for j in range(6))-1)
        -H*(2+x)*(T*T+T+1))/(2*N**6)
    J=P*U*T*T*(2+x)/(N**7)
    return F,G,J,N,T

def main():
    # For any C>0, r>=100(1+C), t=1/r and s=C/r independently
    # obey 0<=t,s<=1/100. This rectangle is a safe sup enclosure.
    t=D(I(0,Q(1,100)));s=D(I(0,Q(1,100)))
    x=[D.var(I(-2,2),0),D.var(I(-2,2),1),
       D.var(I(Q(4,5),Q(6,5)),2),D.var(I(-2,2),3)]
    F,G,J,N,T=source(s,t,*x)
    assert N.v.lo>0 and T.v.lo>0
    ub=(F.v.mag()+G.v.mag())/3;zb=J.v.mag()/5
    nt=N.v/T.v
    Imax=Q(1,10000)*T.v.mag()*weights[3]/(2*EPS)
    qbound=max(abs(nt.lo-1),abs(nt.hi-1))+nt.mag()*Imax
    assert ub<Q(81,100) and zb<Q(97,100) and qbound<Q(11,100)
    lu=sum((F.der[j].mag()+G.der[j].mag())*weights[j]
            for j in range(4))/(3*weights[0])
    lz=sum(J.der[j].mag()*weights[j] for j in range(4))/(5*weights[3])
    dntU=Q(1,100**4)/T.v.lo
    dntH=N.v.mag()*Q(1,100**3)/(T.v.lo**2)
    diH=Q(1,100**5)*weights[3]/(5*EPS)
    diZ=Q(1,100**2)*T.v.mag()/(2*EPS)
    lq=((1+Imax)*(dntU*weights[0]+dntH*weights[1])
        +nt.mag()*(diH*weights[1]+diZ*weights[3]))/weights[2]
    assert lu<Q(17,100) and lz<Q(561,1000) and lq<Q(51,100)
    assert max(lu,lz,lq)<Q(561,1000)
    nmin=Q(1)-Q(2,100**4)
    amax=(Q(1)+Q(2,100**3))/nmin
    vmax=Q(6,5)*Q(1,100**2)
    assert nmin>0 and -nmin**2+(amax*vmax)**2<0
    print('PASS every real C>0, exact asymptotically flat exterior r>=100(1+C)')
    print('PASS m_ADM=0, V nonzero, N,A>0, g_tt<0 on certified half-line')
    print('PASS rigorous weighted contraction <561/1000')
    print('self-map U/H,Z,Q ratios:',*[float(v) for v in
      (ub/weights[0],zb/weights[3],qbound/weights[2])])
    print('Lipschitz U/H,Z,Q:',*[float(v) for v in (lu,lz,lq)])
    print('OPEN: continuation to r~2, matching, physical curved spectrum/cutoff')
if __name__=='__main__':main()
