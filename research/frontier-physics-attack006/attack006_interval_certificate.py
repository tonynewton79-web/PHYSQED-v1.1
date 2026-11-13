"""Exact rational interval/Taylor residual certificate for Attack 006.

All proof inequalities use Fraction + integer isqrt, never floating point.
r in [19/10,8], eps=1/1000, M=mu=1, reference radius=4.
"""
from fractions import Fraction as F
from math import isqrt

def f(x):return x if isinstance(x,F) else F(x)
class I:
    def __init__(self,a,b=None):
        if isinstance(a,I):self.lo,self.hi=a.lo,a.hi;return
        self.lo,self.hi=f(a),f(a if b is None else b)
        assert self.lo<=self.hi
    def __add__(self,y):
        if isinstance(y,J):return NotImplemented
        y=I(y);return I(self.lo+y.lo,self.hi+y.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,y):
        if isinstance(y,J):return NotImplemented
        return self+(-I(y))
    def __rsub__(self,y):
        if isinstance(y,J):return NotImplemented
        return I(y)+(-self)
    def __mul__(self,y):
        if isinstance(y,J):return NotImplemented
        y=I(y);p=[self.lo*y.lo,self.lo*y.hi,self.hi*y.lo,self.hi*y.hi]
        return I(min(p),max(p))
    __rmul__=__mul__
    def inv(self):
        assert self.lo>0 or self.hi<0,'zero in denominator interval'
        return I(1/self.hi,1/self.lo)
    def __truediv__(self,y):
        if isinstance(y,J):return NotImplemented
        return self*I(y).inv()
    def __rtruediv__(self,y):
        if isinstance(y,J):return NotImplemented
        return I(y)*self.inv()
    def __pow__(self,n):
        assert isinstance(n,int)
        if n<0:return (self**(-n)).inv()
        if n==0:return I(1)
        if n%2==0:
            p=[self.lo**n,self.hi**n]
            return I(0 if self.lo<=0<=self.hi else min(p),max(p))
        return I(self.lo**n,self.hi**n)
    def mag(self):return max(abs(self.lo),abs(self.hi))

class J:
    """Second-order automatic differentiation in epsilon with interval values."""
    def __init__(self,a,b=0,c=0):self.a,self.b,self.c=I(a),I(b),I(c)
    def __add__(self,y):
        y=jj(y);return J(self.a+y.a,self.b+y.b,self.c+y.c)
    __radd__=__add__
    def __neg__(self):return J(-self.a,-self.b,-self.c)
    def __sub__(self,y):return self+(-jj(y))
    def __rsub__(self,y):return jj(y)-self
    def __mul__(self,y):
        y=jj(y)
        return J(self.a*y.a,self.b*y.a+self.a*y.b,
                 self.c*y.a+2*self.b*y.b+self.a*y.c)
    __rmul__=__mul__
    def inv(self):
        z=self.a.inv()
        return J(z,-self.b*z**2,2*self.b**2*z**3-self.c*z**2)
    def __truediv__(self,y):return self*jj(y).inv()
    def __rtruediv__(self,y):return jj(y)*self.inv()
    def __pow__(self,n):
        assert isinstance(n,int)
        if n<0:return (self**(-n)).inv()
        y=J(1)
        for _ in range(n):y=y*self
        return y
def jj(a):return a if isinstance(a,J) else J(a)

def log_bound(x,terms=16):
    """Enclose ln(x) exactly using 2 arctanh((x-1)/(x+1))."""
    assert F(19,40)<=x<=2
    z=(x-1)/(x+1)
    series=2*sum(z**(2*j+1)/F(2*j+1) for j in range(terms))
    rem=2*abs(z)**(2*terms+1)/(F(2*terms+1)*(1-z*z))
    return I(series-rem,series+rem)

def sqrt_bound(x,scale=10**12):
    assert x>0
    k=isqrt((x.numerator*scale**2)//x.denominator)
    return I(F(k,scale),F(k+1,scale))

def functions(rr):
    ell=I(log_bound(rr.lo/4).lo,log_bound(rr.hi/4).hi)
    root=I(sqrt_bound(F(2)/rr.hi).lo,sqrt_bound(F(2)/rr.lo).hi)
    n=F(9,8)/rr**2
    np=-F(9,4)/rr**3
    a=-F(9,8)*ell-F(9,8)*(1/rr**2-F(1,16))
    ap=-F(9,8)/rr+F(9,4)/rr**3
    app=F(9,8)/rr**2-F(27,4)/rr**4
    b=F(9,16)*ell+F(9,16)*(rr*ell-rr+4)+F(9,16)*(1/rr-F(1,4))+F(9,8)*(1/rr**2-F(1,16))-F(9,256)*(rr-4)
    bp=F(9,16)/rr+F(9,16)*ell-F(9,16)/rr**2-F(9,4)/rr**3-F(9,256)
    bpp=-F(9,16)/rr**2+F(9,16)/rr+F(9,8)/rr**3+F(27,4)/rr**4
    return root,n,np,a,ap,app,b,bp,bpp

def profile(rr,eps):
    root,n,np,a,ap,app,b,bp,bpp=functions(rr)
    N=1+eps*n;A=1+eps*a;V=root*(1+eps*b)
    return N,A,V,-N**2+A**2*V**2

def second_derivatives(rr,ep_range):
    root,n,np,a,ap,app,b,bp,bpp=functions(rr);r=rr
    e=J(ep_range,1)
    N=J(1)+e*n;Np=e*np
    A=J(1)+e*a;Ap=e*ap;App=e*app
    V=J(root)*(J(1)+e*b)
    Vp=J(root)*(-(J(1)+e*b)/(2*r)+e*bp)
    Vpp=J(root)*(F(3,4)*(J(1)+e*b)/r**2-e*bp/r+e*bpp)
    U=Vp+(Ap/A)*V
    Up=Vpp+(App/A-(Ap/A)**2)*V+(Ap/A)*Vp
    Ksum=U+2*V/r
    Q=U**2+2*(V/r)**2-(J(1)+e)*Ksum**2
    W=-2*e*U-4*(J(1)+e)*V/r
    Wp=-2*e*Up-4*(J(1)+e)*(Vp/r-V/r**2)
    R3=2*(J(1)-A**(-2))/r**2+4*Ap/(A**3*r)
    P=(N**(-2)-J(1))**2/F(4)
    PN=-(N**(-2)-J(1))/(N**3)
    # Exact Euler-Lagrange components of the full reduced 1D action.
    EN=A*r**2*(R3-Q/N**2)/2+A*r**2*(P+N*PN)
    EA=N*(J(1)-A**(-2))-2*r*Np/A**2+r**2/(2*N)*(
        Q-W*U-V*Wp-W*V*(2/r-Np/N))+N*r**2*P
    EV=A*r**2/(2*N)*(4*V/r**2-4*(J(1)+e)*Ksum/r-Wp-W*(2/r-Np/N))
    return EN.c,EA.c,EV.c

def main():
    eps=F(1,1000)
    coefficients=[F(0),F(0),F(0)]
    lowerN=lowerA=lowerV=F(10)
    for j in range(61):
        rr=I(F(19,10)+F(j,10),F(19,10)+F(j+1,10))
        N,A,V,_=profile(rr,I(eps))
        lowerN=min(lowerN,N.lo)
        lowerA=min(lowerA,A.lo)
        lowerV=min(lowerV,V.lo)
        dd=second_derivatives(rr,I(0,eps))
        coefficients=[max(x,y.mag()/2) for x,y in zip(coefficients,dd)]
    bounds=[x*eps**2 for x in coefficients]
    # Exact symbolic derivation (attack006_radial.py) proves
    # E_i(0)=dE_i/d eps(0)=0; Taylor's theorem gives these bounds.
    assert bounds[0]<F(1,100000)
    assert bounds[1]<F(1,50000)
    assert bounds[2]<F(1,100000)
    assert lowerN>F(99,100) and lowerA>F(99,100) and lowerV>0
    _,_,_,kl=profile(I(F(199,100)),I(eps))
    _,_,_,kr=profile(I(F(201,100)),I(eps))
    assert kl.lo>0 and kr.hi<0
    print('PASS exact rational interval Taylor certificate, r in [19/10,8], eps=1/1000')
    print('61 cells; rigorous log/sqrt brackets; NO float calculations in assertions')
    print('Certified: |E_N|<1e-5, |E_A|<2e-5, |E_V|<1e-5')
    print('Certified N>0, A>0, V>0 and approximate Killing norm crosses zero in (1.99,2.01)')
    print('Taylor constants:',*[float(x) for x in coefficients])
    print('Residual bound magnitudes:',*[float(x) for x in bounds])
    print('Not an existence theorem or complete physical-mode stability result')

if __name__=='__main__':main()
