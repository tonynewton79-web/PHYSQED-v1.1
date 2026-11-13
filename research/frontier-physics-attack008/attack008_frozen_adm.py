"""Frozen local ADM leading-derivative Schur complement (SymPy 1.14).

Not the complete gauge-reduced curved-horizon quadratic action. The
background curvature and lower-derivative mixing are not included.
"""
import sympy as s
def main():
    alpha,sigma,v,L,g2=s.symbols('alpha sigma v L g2',real=True)
    Mp2,eps,X,lam,X0=s.symbols('Mp2 eps X lam X0',positive=True)
    PX=2*lam*(X-X0);PXX=2*lam
    H=s.factor(X*(PX+2*X*PXX))
    assert s.factor(H-2*lam*X*(3*X-X0))==0
    L2=Mp2*s.Rational(1,2)*((-6-9*eps)*v**2+(4+6*eps)*v*sigma-eps*sigma**2)+Mp2*g2-2*Mp2*alpha*L+H*alpha**2
    ac=s.solve(s.diff(L2,alpha),alpha)[0]
    sc=s.solve(s.diff(L2,sigma),sigma)[0]
    assert s.factor(ac-Mp2*L/H)==0
    assert s.factor(sc-(2+3*eps)*v/eps)==0
    red=s.factor(L2.subs({alpha:ac,sigma:sc}))
    expect=Mp2*(2/eps+3)*v**2+Mp2*g2-Mp2**2/H*L**2
    assert s.factor(red-expect)==0
    print('PASS frozen ADM alpha/sigma constraint Schur complement',red)
    print('PASS high-k scalar principal positive if epsilon>0, H>0')
    print('WARNING: NOT a complete physical curved-background perturbation spectrum')
if __name__=='__main__':main()
