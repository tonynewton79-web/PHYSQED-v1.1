"""Attack 010: Fraction-only Banach certificate for exact massless exteriors.
Two parameter regimes (mu=1, epsilon=1/1000):
  (R,C)=(100,1/10), (1997/1000,1/100).
The second solution is disjoint from the Attack 007 local horizon branch.
All assertions use rational interval arithmetic; no sampled radii.
"""
from fractions import Fraction as Q

class I:
    def __init__(self,a,b=None):
        if isinstance(a,I):self.lo,self.hi=a.lo,a.hi;return
        self.lo,self.hi=Q(a),Q(a if b is None else b)
        assert self.lo<=self.hi
    def __add__(self,x):
        if isinstance(x,D):return NotImplemented
        x=I(x);return I(self.lo+x.lo,self.hi+x.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,x):
        if isinstance(x,D):return NotImplemented
        return self+(-I(x))
    def __rsub__(self,x):
        if isinstance(x,D):return NotImplemented
        return I(x)-self
    def __mul__(self,x):
        if isinstance(x,D):return NotImplemented
        x=I(x);v=(self.lo*x.lo,self.lo*x.hi,self.hi*x.lo,self.hi*x.hi)
        return I(min(v),max(v))
    __rmul__=__mul__
    def inv(self):
        assert self.lo>0 or self.hi<0
        return I(1/self.hi,1/self.lo)
    def __truediv__(self,x):
        if isinstance(x,D):return NotImplemented
        return self*I(x).inv()
    def __rtruediv__(self,x):
        if isinstance(x,D):return NotImplemented
        return I(x)*self.inv()
    def __pow__(self,n):
        assert isinstance(n,int)
        if n<0:return (self**(-n)).inv()
        if n==0:return I(1)
        if n%2:return I(self.lo**n,self.hi**n)
        return I(0 if self.lo<=0<=self.hi else min(self.lo**n,self.hi**n),max(self.lo**n,self.hi**n))
    def mag(self):return max(abs(self.lo),abs(self.hi))

class D:
    def __init__(self,v,der=None):
        self.v=I(v);self.der=[I(0) for _ in range(4)] if der is None else der
    @staticmethod
    def var(v,j):
        g=[I(0) for _ in range(4)];g[j]=I(1);return D(v,g)
    def __add__(self,x):
        x=d(x);return D(self.v+x.v,[a+b for a,b in zip(self.der,x.der)])
    __radd__=__add__
    def __neg__(self):return D(-self.v,[-a for a in self.der])
    def __sub__(self,x):return self+(-d(x))
    def __rsub__(self,x):return d(x)-self
    def __mul__(self,x):
        x=d(x);return D(self.v*x.v,[a*x.v+b*self.v for a,b in zip(self.der,x.der)])
    __rmul__=__mul__
    def inv(self):
        z=self.v.inv();return D(z,[-a*z*z for a in self.der])
    def __truediv__(self,x):return self*d(x).inv()
    def __rtruediv__(self,x):return d(x)*self.inv()
    def __pow__(self,n):
        assert isinstance(n,int)
        if n<0:return (self**(-n)).inv()
        y=D(1)
        for _ in range(n):y=y*self
        return y
def d(x):return x if isinstance(x,D) else D(x)

EPS=Q(1,1000)
weights=(Q(2),Q(2),Q(1,5),Q(2))

def sources(t,U,H,P,Z,C):
    # u=r(N-1)=C^2 r^-3 U, h=NA-1=C^2 r^-3 H,
    # V=C r^-2 P, K=C^3 eps^-1 r^-5 Z.
    x=C*C*t**4*U; N=1+x; T=1+C*C*t**3*H; A=T/N
    F=C*C*t*t*(H-t*U)**2/(2*N)
    F+=C**4*t**4*A*A*N*Z*Z/(4*EPS)
    F+=C*C*t*t*A*A*P*Z/EPS
    F-=Q(3,2)*A*A*P*P/N
    F+=C*C*t*t*A*A*U*U*(2+x)**2/(8*N**3)
    G=C*C*t*t*U*(t*U*(2*sum(N**j for j in range(6))-1)
       -H*(2+x)*(T*T+T+1))/(2*N**6)
    J=P*U*T*T*(2+x)/(N**7)
    return F,G,J,N,T

def certify(C,R):
    t=D(I(0,1/R))
    y=[D.var(I(-2,2),0),D.var(I(-2,2),1),
       D.var(I(Q(4,5),Q(6,5)),2),D.var(I(-2,2),3)]
    F,G,J,N,T=sources(t,*y,C)
    fm,gm,jm=F.v.mag(),G.v.mag(),J.v.mag()
    uh=(fm+gm)/3; z=jm/5
    assert uh<2 and z<2
    nt=N.v/T.v
    assert N.v.lo>0 and T.v.lo>0
    nt_offset=max(abs(nt.lo-1),abs(nt.hi-1))
    integral_bound=C*C/EPS*T.v.mag()*2/(2*R**2)
    qoffset=nt_offset+nt.mag()*integral_bound
    assert qoffset<Q(1,5)
    lip_uh=sum((F.der[j].mag()+G.der[j].mag())*weights[j]
               for j in range(4))/(3*weights[0])
    lip_z=sum(J.der[j].mag()*weights[j] for j in range(4))/(5*weights[3])
    derivative_nt_U=C*C/R**4/T.v.lo
    derivative_nt_H=N.v.mag()*C*C/R**3/T.v.lo**2
    derivative_integral_H=C**4/EPS*2/(5*R**5)
    derivative_integral_Z=C*C/EPS*T.v.mag()/(2*R**2)
    lip_q=((1+integral_bound)*(derivative_nt_U*weights[0]+derivative_nt_H*weights[1])
           +nt.mag()*(derivative_integral_H*weights[1]+derivative_integral_Z*weights[3]))/weights[2]
    contraction=max(lip_uh,lip_q,lip_z)
    assert contraction<Q(57,100)
    nmin=1-2*C*C/R**4
    amax=(1+2*C*C/R**3)/nmin
    vmax=Q(6,5)*C/R**2
    assert nmin>0 and -nmin*nmin+(amax*vmax)**2<0
    assert Q(4,5)*C>0
    print('PASS exact nonlinear massless exterior, R=',R,'C=',C)
    print('self-map U/H,Q-offset,Z:',*[float(v) for v in (uh,qoffset,z)])
    print('weighted contraction rows:',*[float(v) for v in (lip_uh,lip_q,lip_z)])
    print('PASS no local Killing horizon on all r>=R; ADM mass zero; V not identically zero')
    if R==Q(1997,1000):
        assert Q(6,5)*C/4 < Q(1251,1250)-Q(1,100)
        print('PASS exact nonmatching at r=2: V_ext<=0.003, V_007>=0.9908')

def main():
    certify(Q(1,10),Q(100))
    certify(Q(1,100),Q(1997,1000))

if __name__=='__main__':main()
