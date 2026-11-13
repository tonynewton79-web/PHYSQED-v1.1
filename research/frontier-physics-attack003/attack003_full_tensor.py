import sympy as s
M,eta,q=s.symbols('M eta q', nonzero=True,positive=True)
t,r,th,ph=s.symbols('t r th ph', real=True)
x=(t,r,th,ph)
F=1-2*M/r
metric=s.diag(-F,1/F,r**2,r**2*s.sin(th)**2)
ginv=s.diag(-1/F,F,1/r**2,1/(r**2*s.sin(th)**2))
C={}
for a in range(4):
 for b in range(4):
  for c in range(b,4):
   v=s.simplify(sum(ginv[a,k]*(s.diff(metric[k,b],x[c])+s.diff(metric[k,c],x[b])-s.diff(metric[b,c],x[k])) for k in range(4))/2)
   if v!=0: C[a,b,c]=v; C[a,c,b]=v
def conn(a,b,c):return C.get((a,b,c),0)
def curv(a,b,c,d):return s.simplify(s.diff(conn(a,d,b),x[c])-s.diff(conn(a,c,b),x[d])+sum(conn(a,c,k)*conn(k,d,b)-conn(a,d,k)*conn(k,c,b) for k in range(4)))
psi_p=16*eta*M*M/(r**5*F)
psi_pp=s.diff(psi_p,r)
vec=s.Matrix([q,psi_p,0,0])
H=s.zeros(4)
for a in range(4):
 for b in range(4):
  H[a,b]=s.simplify((s.diff(vec[b],x[a]) if a==1 and b==1 else 0)-sum(conn(k,a,b)*vec[k] for k in range(4)))
raised=ginv*H*ginv
Rlo={}
def fullR(a,b,c,d):
 key=(a,b,c,d)
 if key not in Rlo:
  Rlo[key]=s.simplify(metric[a,a]*curv(a,b,c,d))
 return Rlo[key]
def P(a,b): return s.factor(sum(fullR(a,rho,b,sig)*raised[rho,sig] for rho in range(4) for sig in range(4)))
Ptt=P(0,0);Ptr=P(0,1)
gradnorm=s.factor((vec.T*ginv*vec)[0]);Ttt=s.factor(vec[0]**2-metric[0,0]*gradnorm/2); Ttr=q*psi_p
Ett=s.factor(Ttt-8*eta*Ptt)
Etr=s.factor(Ttr-8*eta*Ptr)
print('Ptt=',Ptt)
print('Ptr=',Ptr)
print('Ttt=',Ttt)
print('Ett=',Ett)
print('Etr=',Etr)
print('Ett at infinity',s.limit(Ett,r,s.oo))
print('q rolling horizon', eta/(2*M**3))
print('Ett horizon for regular q',s.simplify(s.limit(Ett.subs(q,eta/(2*M**3)),r,2*M)))
assert s.simplify(Ett-(5888*M**4*eta**2-3072*M**3*eta**2*r+q**2*r**10)/(2*r**10))==0
assert Etr==0
assert s.factor(Ett.subs({q:eta/(2*M**3),r:4*M})) == s.Rational(999,8192)*eta**2/M**6
print('PASS 4D Christoffel/Riemann/Hessian exact metric-source residual checks')
