"""Separate tensor-path sanity check for the static spherical ansatz.
This shares SymPy with frontier_filters and is *not* a second math engine.
"""
import sympy as s
r,theta=s.symbols('r theta',positive=True)
t,phi=s.symbols('t phi')
F=s.Function('F')(r)
x=(t,r,theta,phi)
g=s.diag(-F,1/F,r**2,r**2*s.sin(theta)**2)
gi=s.diag(-1/F,F,r**-2,1/(r**2*s.sin(theta)**2))
G={}
for i in range(4):
    for j in range(4):
        for k in range(4):
            v=s.Rational(1,2)*sum(gi[i,l]*(s.diff(g[l,j],x[k])+s.diff(g[l,k],x[j])-s.diff(g[j,k],x[l])) for l in range(4))
            if v!=0: G[i,j,k]=s.simplify(v)
def ga(i,j,k): return G.get((i,j,k),s.S.Zero)
Ricc=s.zeros(4)
for i in range(4):
    for j in range(4):
        Ricc[i,j]=s.simplify(sum(
            s.diff(ga(k,i,j),x[k])-s.diff(ga(k,i,k),x[j])+
            sum(ga(k,k,l)*ga(l,i,j)-ga(k,j,l)*ga(l,i,k) for l in range(4)) for k in range(4)))
scalar=s.simplify(sum(gi[k,k]*Ricc[k,k] for k in range(4)))
Ein=s.simplify(gi*Ricc-s.eye(4)*scalar/2)
expected=(s.diff(F,r)*r+F-1)/r**2
assert s.simplify(Ein[0,0]-expected)==0
assert s.simplify(Ein[1,1]-expected)==0
assert s.simplify(Ein[2,2]-(s.diff(F,r,2)/2+s.diff(F,r)/r))==0
assert s.simplify(Ein[3,3]-Ein[2,2])==0
print('PASS independent tensor-formula route: 4D mixed Einstein components match static spherical expressions')
