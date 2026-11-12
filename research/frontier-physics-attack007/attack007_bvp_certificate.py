"""Attack 007: rational interval Banach certificate for an exact mixed spherical BVP.

Only Python standard library. Fraction interval arithmetic and forward-mode
Jacobian AD certify a unique solution and nondegenerate local Killing horizon.
See README for the normal form and trust boundary.
"""
from fractions import Fraction as Q

class I:
    def __init__(self,a,b=None):
        if isinstance(a,I):self.lo,self.hi=a.lo,a.hi;return
        self.lo,self.hi=Q(a),Q(a if b is None else b)
        assert self.lo<=self.hi
    def __add__(self,y):
        if isinstance(y,D):return NotImplemented
        y=I(y);return I(self.lo+y.lo,self.hi+y.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,y):
        if isinstance(y,D):return NotImplemented
        return self+(-I(y))
    def __rsub__(self,y):
        if isinstance(y,D):return NotImplemented
        return I(y)-self
    def __mul__(self,y):
        if isinstance(y,D):return NotImplemented
        y=I(y);a,b,c,d=self.lo,self.hi,y.lo,y.hi
        return I(min(a*c,a*d,b*c,b*d),max(a*c,a*d,b*c,b*d))
    __rmul__=__mul__
    def inv(self):
        assert self.lo>0 or self.hi<0
        return I(1/self.hi,1/self.lo)
    def __truediv__(self,y):
        if isinstance(y,D):return NotImplemented
        return self*I(y).inv()
    def __rtruediv__(self,y):return I(y)*self.inv()
    def __pow__(self,n):
        assert isinstance(n,int)
        if n<0:return (self**(-n)).inv()
        if not n:return I(1)
        if n%2:return I(self.lo**n,self.hi**n)
        return I(0 if self.lo<=0<=self.hi else min(self.lo**n,self.hi**n),max(self.lo**n,self.hi**n))
    def mag(self):return max(abs(self.lo),abs(self.hi))

class D:
    def __init__(self,v,g=None):
        self.v=I(v);self.g=[I(0) for _ in range(4)] if g is None else g
    @staticmethod
    def var(v,j):
        g=[I(0) for _ in range(4)];g[j]=I(1);return D(v,g)
    def __add__(self,y):
        y=dd(y);return D(self.v+y.v,[a+b for a,b in zip(self.g,y.g)])
    __radd__=__add__
    def __neg__(self):return D(-self.v,[-a for a in self.g])
    def __sub__(self,y):return self+(-dd(y))
    def __rsub__(self,y):return dd(y)-self
    def __mul__(self,y):
        y=dd(y);return D(self.v*y.v,[a*y.v+b*self.v for a,b in zip(self.g,y.g)])
    __rmul__=__mul__
    def inv(self):
        z=self.v.inv();return D(z,[-g*z*z for g in self.g])
    def __truediv__(self,y):return self*dd(y).inv()
    def __rtruediv__(self,y):return dd(y)*self.inv()
    def __pow__(self,n):
        assert isinstance(n,int)
        if n<0:return (self**(-n)).inv()
        z=D(1)
        for _ in range(n):z=z*self
        return z

def dd(x):return x if isinstance(x,D) else D(x)

def rhs(r,vals,eps=Q(1,1000),mu=Q(1)):
    N,A,V,K=vals
    S=-mu*A*A*r*(N*N-1)/(2*N**4)
    NP=N*(A*A-1)/(2*r)+A*A*(eps*N*K*K*r/4+K*V-3*V*V/(2*N*r))+mu*A*A*N*r*(N**(-2)-1)**2/8
    AP=A*(S-NP/N)
    VP=N*K-2*V/r-AP*V/A
    KP=2*V*S/(eps*N*r)
    return [NP,AP,VP,KP]

def floor_grid(x,S=10**12):return Q(x.numerator*S//x.denominator,S)
def ceil_grid(x,S=10**12):return -floor_grid(-x,S)

def main():
    center=Q(2);d=Q(3,1000);L=2*d
    rr=I(center-d,center+d)
    anchors=(Q(32009,32000),Q(1),Q(1251,1250),Q(3,4))
    widths=(Q(5,10000),Q(1,1000),Q(1,100),Q(1,20))
    box=[I(c-w,c+w) for c,w in zip(anchors,widths)]
    assert rr.lo>0 and box[0].lo>0 and box[1].lo>0
    f=rhs(D(rr),[D.var(b,j) for j,b in enumerate(box)])
    selfmap=[L*f[i].v.mag()/widths[i] for i in range(4)]
    contraction=[L*sum(f[i].g[j].mag()*widths[j]/widths[i] for j in range(4)) for i in range(4)]
    assert max(selfmap)<Q(91,100)
    assert max(contraction)<Q(3,4)
    print('PASS strict self-map <91/100 and contraction <3/4: unique exact nonlinear mixed-BVP solution')
    # Explicit affine boundary-compatible trial; its exact operator defect
    # and contraction yield a genuine solution-distance certificate.
    slopes=[z.v.lo for z in rhs(D(I(center)),[D.var(I(c),j) for j,c in enumerate(anchors)])]
    trial=[I(c+min(0,L*s),c+max(0,L*s)) for c,s in zip(anchors,slopes)]
    for v,b in zip(trial,box):assert b.lo<=v.lo<=v.hi<=b.hi
    tf=rhs(rr,trial)
    defect=max(L*(z-I(s)).mag()/widths[i] for i,(z,s) in enumerate(zip(tf,slopes)))
    assert defect<Q(17,250)
    assert 4*defect<Q(271,1000)
    print('PASS explicit affine trial ||T trial-trial||_weighted <17/250')
    print('PASS ||exact - affine trial||_weighted <271/1000')
    # Five rigorous a-priori bootstrap enclosures, outward-rounded to a
    # fixed 10^-12 rational grid. The exact solution remains inside each.
    xs=box
    for _ in range(5):
        f=rhs(rr,xs);refined=[]
        for i,z in enumerate(f):
            if i in (0,2):dv=I(L*min(z.lo,0),L*max(z.hi,0))
            else:dv=I(-L*max(z.hi,0),-L*min(z.lo,0))
            new=I(anchors[i])+dv
            new=I(floor_grid(new.lo),ceil_grid(new.hi))
            assert xs[i].lo<=new.lo<=new.hi<=xs[i].hi
            refined.append(new)
        xs=refined
    n,a,v,k=xs
    n_p,a_p,v_p,k_p=rhs(rr,xs)
    a_left=I(anchors[1])-I(L)*a_p
    n_right=I(anchors[0])+I(L)*n_p
    v_right=I(anchors[2])+I(L)*v_p
    g_left=-I(anchors[0])**2+a_left**2*I(anchors[2])**2
    g_right=-n_right**2+v_right**2 # A(right)=1
    gprime=-2*n*n_p+2*a*a_p*v*v+2*a*a*v*v_p
    assert g_left.lo>0 and g_right.hi<0 and gprime.hi<-Q(2,5)
    assert g_left.lo>(-gprime.lo)*Q(9,5000)
    assert g_left.hi<(-gprime.hi)*Q(1,400)
    assert n.lo>1 and a.lo>Q(99,100) and v.lo>0
    X=I(1)/(2*n**2)
    assert X.lo>0 and (6*X-I(1)).lo>Q(19,10)
    print('PASS unique local nondegenerate Killing horizon: 1.9988<r_h<1.9995')
    print('PASS smooth positive N,A, timelike scalar X>0, bare k-essence kinetic>1.9')
    print('PASS g_tt derivative uniformly <-0.4, horizon is regular in ADM chart')
    print('LIMIT: no global event horizon, center regularity, physical-mode stability or AF claim')

if __name__=='__main__':main()
