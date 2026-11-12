"""4D coordinate tensor check, independent derivation route (same SymPy engine)."""
import sympy as s
r,th,t,ph=s.symbols('r theta t phi',real=True)
x=(t,r,th,ph)
F=1-r**2/s.Integer(5)+r**4/s.Integer(30)
N=1+r**2/s.Integer(7)
g=s.diag(-N**2*F,1/F,r**2,r**2*s.sin(th)**2)
inv=s.diag(-1/(N**2*F),F,1/r**2,1/(r**2*s.sin(th)**2))
# Exact sample r=1,theta=pi/2 with no floating arithmetic.
p={r:s.Integer(1),th:s.pi/2}
Gamma={}
for i in range(4):
 for j in range(4):
  for k in range(j,4):
   v=s.Rational(1,2)*sum(inv[i,l]*(s.diff(g[l,k],x[j])+s.diff(g[l,j],x[k])-s.diff(g[j,k],x[l])) for l in range(4))
   if v != 0:
    Gamma[i,j,k]=Gamma[i,k,j]=s.factor(v)
def gam(i,j,k):return Gamma.get((i,j,k),s.S.Zero)
G0={q:s.simplify(v.subs(p)) for q,v in Gamma.items()}
D0={}
for q,v in Gamma.items():
 for k in (1,2):
  D0[q,k]=s.simplify(s.diff(v,x[k]).subs(p))
def der(i,j,k,l):return D0.get(((i,j,k),l),s.S.Zero)
def gamma0(i,j,k):return G0.get((i,j,k),s.S.Zero)
Riem={}
for i in range(4):
 for j in range(4):
  for k in range(4):
   for l in range(4):
    val=der(i,j,l,k)-der(i,j,k,l)+sum(gamma0(i,m,k)*gamma0(m,j,l)-gamma0(i,m,l)*gamma0(m,j,k) for m in range(4))
    # R^i_{jkl}=∂_k Γ^i_{lj}-∂_l Γ^i_{kj}+Γ^i_{km}Γ^m_{lj}-Γ^i_{lm}Γ^m_{kj}
    if val!=0:Riem[i,j,k,l]=s.factor(val)
def rt(i,j,k,l):return Riem.get((i,j,k,l),s.S.Zero)
gv=[s.simplify(g[i,i].subs(p)) for i in range(4)]
Ric=s.zeros(4)
for j in range(4):
 for l in range(4):
  Ric[j,l]=s.factor(sum(rt(i,j,i,l) for i in range(4)))
scalar=s.factor(sum(Ric[i,i]/gv[i] for i in range(4)))
Ric2=s.factor(sum(Ric[i,j]*Ric[i,j]/(gv[i]*gv[j]) for i in range(4) for j in range(4)))
K=s.factor(sum(gv[i]*rt(i,j,k,l)**2/(gv[j]*gv[k]*gv[l]) for i in range(4) for j in range(4) for k in range(4) for l in range(4)))
GB=s.factor(K-4*Ric2+scalar**2)
expected=s.factor(4*s.diff(N*(F-1)*(s.diff(F,r)+2*F*s.diff(N,r)/N),r)/(N*r**2)).subs(r,1)
assert s.simplify(GB-expected)==0, (GB,expected,s.factor(GB-expected))
print('PASS: independent 4D Levi-Civita -> Riemann/Ricci/K/Gauss-Bonnet rational oracle')
print('Coordinate evaluation r=1 theta=pi/2: GB =',GB,'expected:',expected)
