"""Attack012: uniform high-order centered exact infinity tail for C in [7000,8000].

All assertions use exact SymPy algebra and Python Fraction interval arithmetic.
For eps=1/1000, mu=1 prove unique exact nonlinear Green solution
within |u-u0|,|h-h0|<=10^23/r^9,
|W-W0|<=2.8e28/r^8, |K-K0|<=1.8e29/r^11, on r>=50000,
where u=r(N-1), h=NA-1, W=Ar^2 V.
No continuation below r=50000 or Killing horizon is certified.
"""
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
import sys
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'frontier-physics-attack010'))
from attack010_exterior_banach import I

C,z=s.symbols('C z');u,h,W,K=s.symbols('u h W K')
U,H,WW,ZZ=s.symbols('U H WW ZZ')
eps=s.Rational(1,1000);R=50000
CI=I(7000,8000);ZI=I(0,Q(1,R))
alpha=beta=10**23;gamma=280000*10**23;delta=1800000*10**23

def polybox(expr):
    out=I(0)
    for (pz,pc),a in s.Poly(s.expand(expr),z,C).terms():
        out+=I(Q(a))*ZI**pz*CI**pc
    return out

def center():
    a4=s.Rational(3,2)*C**2;a6=-36*C**2
    a8=-3*C**2*(3*C**2*eps+8*C**2-3840*eps)/(8*eps)
    n6=6*C**2;n8=-180*C**2
    n10=-12*C**2*(3*C**2*eps+2*C**2-840*eps)/eps
    v6=-3*C**3*(7*eps+2)/(14*eps)
    v8=4*C**3*(27*eps+5)/(3*eps)
    v10=3*C**3*(693*C**2*eps**2+808*C**2*eps+124*C**2
       -295680*eps**2-47040*eps)/(616*eps**2)
    k7=12*C**3/(7*eps);k9=-40*C**3/eps
    k11=-6*C**3*(63*C**2*eps+62*C**2-23520*eps)/(77*eps**2)
    N0=1+n6*z**6+n8*z**8+n10*z**10
    A0=1+a4*z**4+a6*z**6+a8*z**8
    V0=C*z**2+v6*z**6+v8*z**8+v10*z**10
    K0=k7*z**7+k9*z**9+k11*z**11
    return N0,A0,V0,K0

@lru_cache(None)
def eval_expr(ex):
    if ex.is_Number:return I(Q(ex))
    if ex.is_Symbol:return boxes[ex]
    if ex.is_Add:return sum((eval_expr(x) for x in ex.args),I(0))
    if ex.is_Mul:
        v=I(1)
        for x in ex.args:v=v*eval_expr(x)
        return v
    if ex.is_Pow and ex.exp.is_Integer:return eval_expr(ex.base)**int(ex.exp)
    raise TypeError(('Unrecognized rational expression',str(ex)))

def main():
    global boxes
    N0,A0,V0,K0=center()
    b0u,b0h,b0w,b0k=[polybox(s.expand(q)) for q in (
       (N0-1)/z**6,(N0*A0-1)/z**4,A0*V0/z**2,K0/z**7)]
    boxes={z:ZI,
      U:I(b0u.lo-Q(alpha,R**4),b0u.hi+Q(alpha,R**4)),
      H:I(b0h.lo-Q(beta,R**5),b0h.hi+Q(beta,R**5)),
      WW:I(b0w.lo-Q(gamma,R**8),b0w.hi+Q(gamma,R**8)),
      ZZ:I(b0k.lo-Q(delta,R**4),b0k.hi+Q(delta,R**4))}
    # Exact transformed ODE: u'=h+F, h'=-u+G, W'=Tr^2K.
    N=1+u*z;T=1+h;A=T/N
    F=((h-u*z)**2/(2*N)+eps*A*A*N*K*K/(4*z*z)
       +A*W*K*z-s.Rational(3,2)*W*W*z**4/N
       +A*A*u*u*(2+u*z)**2/(8*N**3))
    G=u-T*A*A*u*(2+u*z)/(2*N**4)
    KP=-A*W*u*(2+u*z)*z**3/(eps*N**5)
    WP=T*K/z**2
    sub={u:z**5*U,h:z**4*H,W:WW,K:z**7*ZZ}
    derivatives=[
      ('Fu',s.diff(F,u),5),('Fh',s.diff(F,h),4),
      ('FW',s.diff(F,W),4),('FK',s.diff(F,K),1),
      ('Gu',s.diff(G,u),4),('Gh',s.diff(G,h),5),
      ('Kpu',s.diff(KP,u),3),('Kph',s.diff(KP,h),8),
      ('KpW',s.diff(KP,W),8),('Wph',s.diff(WP,h),5)]
    bounds={}
    for name,der,power in derivatives:
        expr=s.factor(der.subs(sub)/z**power)
        eval_expr.cache_clear()
        bounds[name]=eval_expr(expr).mag()
    # Both components of the oscillator Green kernel receive F AND G.
    L_osc=(Q(alpha)*bounds['Fu']/(13*R**4)
       +Q(beta)*bounds['Fh']/(12*R**3)
       +Q(gamma)*bounds['FW']/(11*R**2)
       +Q(delta)*bounds['FK']/(11*R**2)
       +Q(alpha)*bounds['Gu']/(12*R**3)
       +Q(beta)*bounds['Gh']/(13*R**4))/alpha
    LT=I(1)+ZI**4*boxes[H];LN=I(1)+ZI**6*boxes[U]
    assert LN.lo>0 and LT.lo>0 and boxes[WW].lo>0
    LA=LT/LN
    LW=(Q(beta)*bounds['Wph']/(13*R**5)
       +Q(delta)*LT.mag()/8)/gamma
    LK=(Q(alpha)*bounds['Kpu']/11
       +Q(beta)*bounds['Kph']/(16*R**5)
       +Q(gamma)*bounds['KpW']/(15*R**4))/delta
    # Residual of the polynomial centre in the full nonlinear ODE.
    rr=1/z
    S=-A0*A0*rr*(N0*N0-1)/(2*N0**4)
    NP=(N0*(A0*A0-1)/(2*rr)
       +A0*A0*(eps*N0*K0*K0*rr/4+K0*V0-3*V0*V0/(2*N0*rr))
       +A0*A0*N0*rr*(N0**(-2)-1)**2/8)
    AP=A0*(S-NP/N0)
    VP=N0*K0-2*V0/rr-AP*V0/A0
    KPP=2*V0*S/(eps*N0*rr)
    denconst=(145711104,1165688832,269274120192,1232)
    denpow=(3,4,4,5)
    bR=[]
    for i,(f,rhs,power) in enumerate(((N0,NP,11),(A0,AP,11),
                                     (V0,VP,13),(K0,KPP,14))):
        rat=s.cancel((-z*z*s.diff(f,z)-rhs)/z**power)
        nu,de=s.fraction(rat)
        assert s.factor(de-denconst[i]*(-N0)**denpow[i])==0
        num=polybox(nu);nd=polybox(N0)
        denominator=I(denconst[i])*(-nd)**denpow[i]
        bR.append((num/denominator).mag())
    RN,RA,RV,RK=bR
    # Green defects: Ru=r RN, Rh=A RN+N RA,
    # RW=A r^2 RV+V r^2 RA and RK=RK.
    defect_u=RN/(9*alpha)
    defect_h=(LA.mag()*RN+LN.mag()*RA)/(10*beta*R)
    defect_W=(LA.mag()*RV+(boxes[WW]/LA).mag()*RA)/(10*gamma*R**2)
    defect_K=RK/(13*delta*R**2)
    row_osc=L_osc+defect_u+defect_h
    row_W=LW+defect_W;row_K=LK+defect_K
    assert max(L_osc,LW,LK)<Q(81,100)
    assert max(row_osc,row_W,row_K)<Q(81,100)
    assert boxes[U].lo>0 and boxes[H].lo>0
    print('PASS uniform centered exact infinity Banach for every C in [7000,8000]')
    print('PASS exact nonlinear solutions with weighted error bounds on r>=50000')
    print('PASS all contraction AND self-map rows <81/100')
    print('Lipschitz oscillator,W,K:',*[float(v) for v in (L_osc,LW,LK)])
    print('Selfmap oscillator,W,K:',*[float(v) for v in (row_osc,row_W,row_K)])
    print('Exact normalized residual coefficients:',*[float(v) for v in bR])
    print('Error: |u-u0|,|h-h0|<=10^23/r^9, |W-W0|<=2.8e28/r^8, |K-K0|<=1.8e29/r^11')
    # Overlap with the coarse Attack010 unique infinity solution.
    zi=I(0,Q(1,800100));ci=CI
    oldU=zi**2*boxes[U]/(ci**2)
    oldH=zi*boxes[H]/(ci**2)
    newN=I(1)+zi**6*boxes[U];newT=I(1)+zi**4*boxes[H]
    newA=newT/newN;Qflow=boxes[WW]/(ci*newA)
    oldZ=I(Q(1,1000))*zi**2*boxes[ZZ]/ci**3
    assert oldU.mag()<2 and oldH.mag()<2 and oldZ.mag()<2
    assert Qflow.lo>Q(4,5) and Qflow.hi<Q(6,5)
    print('PASS same infinity-selected exact branch as all-amplitude coarse theorem')
    print('NOT CERTIFIED: r<50000 validated continuation or a horizon match')
if __name__=='__main__':main()
