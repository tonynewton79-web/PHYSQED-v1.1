"""Four-dimensional Levi-Civita Einstein-tensor verification.

Different tensor formula route, but same SymPy engine as attack004_exact.py.
"""
import sympy as s

def einstein(g,x):
    n=len(x);gi=g.inv();C={}
    for a in range(n):
        for b in range(n):
            for c in range(b,n):
                z=s.simplify(sum(gi[a,d]*(s.diff(g[d,b],x[c])+s.diff(g[d,c],x[b])-s.diff(g[b,c],x[d])) for d in range(n))/2)
                if z!=0:C[a,b,c]=z;C[a,c,b]=z
    def gm(a,b,c):return C.get((a,b,c),s.S.Zero)
    R=s.zeros(n)
    for a in range(n):
        for b in range(n):
            R[a,b]=s.simplify(sum(
                s.diff(gm(k,a,b),x[k])-s.diff(gm(k,a,k),x[b])
                +sum(gm(k,k,l)*gm(l,a,b)-gm(k,b,l)*gm(l,a,k) for l in range(n))
                for k in range(n)))
    scalar=s.simplify(sum(gi[a,b]*R[a,b] for a in range(n) for b in range(n)))
    return s.simplify(R-g*scalar/2),scalar

def main():
    t,r,th,ph,M,H,Mp,V0=s.symbols("t r theta phi M H Mpl V0",positive=True)
    F=1-2*M/r
    schw=s.diag(-F,1/F,r*r,r*r*s.sin(th)**2)
    G,R=einstein(schw,(t,r,th,ph))
    assert G==s.zeros(4) and R==0
    a=s.exp(H*t)
    ds=s.diag(-1,a*a,a*a,a*a)
    G,R=einstein(ds,(t,r,th,ph))
    assert s.simplify(R-12*H**2)==0
    assert s.simplify(G[0,0]-3*H**2)==0
    assert all(s.simplify(G[i,i]+3*H**2*a*a)==0 for i in (1,2,3))
    T=-V0*ds
    assert all(s.simplify((Mp**2*G[i,i]-T[i,i]).subs(V0,3*Mp**2*H**2))==0 for i in range(4))
    print("PASS: 4D Schwarzschild Einstein tensor vanishes")
    print("PASS: 4D de Sitter Einstein tensor equals full k-essence source")
    print("No non-SymPy independent metric-variation backend is claimed.")

if __name__=="__main__":
    main()
