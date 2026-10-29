"""PHYSQED v1.2: finite-dimensional quantum and canonical verification.

Matrix calculations are exact where inputs are exact. No finite matrix
representation of the canonical Heisenberg commutation relation exists.
Field-theoretic constraints here are local symbolic checks, not a Dirac
quantization or an interacting QFT existence proof.
"""
from __future__ import annotations
from itertools import product
import sympy as S
from .geometry import ScopeError, zero


def commutator(a,b):
    A,B=S.Matrix(a),S.Matrix(b)
    if A.shape!=B.shape or A.rows!=A.cols:
        raise ScopeError("commutator requires equally sized square matrices")
    return (A*B-B*A).applyfunc(S.simplify)


def anticommutator(a,b):
    A,B=S.Matrix(a),S.Matrix(b)
    if A.shape!=B.shape or A.rows!=A.cols:
        raise ScopeError("anticommutator requires equally sized square matrices")
    return (A*B+B*A).applyfunc(S.simplify)


def is_hermitian(a):
    A=S.Matrix(a)
    return A.rows==A.cols and all(zero(v) for v in A-A.conjugate().T)


def quantum_expectation(observable, density):
    O,rho=S.Matrix(observable),S.Matrix(density)
    if O.shape!=rho.shape or rho.rows!=rho.cols:
        raise ScopeError("operator/density dimensions")
    if not zero(S.trace(rho)-1) or not is_hermitian(rho):
        raise ScopeError("density must be Hermitian and trace one")
    ev=rho.eigenvals()
    if any(S.ask(S.Q.nonnegative(S.simplify(e))) is not True for e in ev):
        raise ScopeError("density positivity not established exactly")
    return S.simplify(S.trace(rho*O))


def heisenberg_residual(observable, hamiltonian, hbar=1):
    if zero(hbar):
        raise ScopeError("nonzero Planck constant required")
    return (S.I/hbar*commutator(hamiltonian,observable)).applyfunc(S.simplify)


def robertson_residual(a,b,density,hbar=1):
    """Var(A)Var(B) - |<[A,B]>|^2/4, with exact density gate."""
    if not is_hermitian(a) or not is_hermitian(b):
        raise ScopeError("Robertson requires Hermitian observables")
    A,B=S.Matrix(a),S.Matrix(b)
    ea=quantum_expectation(A,density)
    eb=quantum_expectation(B,density)
    va=S.simplify(quantum_expectation(A*A,density)-ea**2)
    vb=S.simplify(quantum_expectation(B*B,density)-eb**2)
    c=quantum_expectation(commutator(A,B),density)
    return S.simplify(va*vb - S.conjugate(c)*c/4)


def clifford_residual(gammas, inverse_metric):
    """Check {gamma^mu,gamma^nu}=2 g^{mu nu} I."""
    g=S.Matrix(inverse_metric)
    n=len(gammas)
    G=[S.Matrix(m) for m in gammas]
    if g.shape!=(n,n) or any(m.shape!=G[0].shape or m.rows!=m.cols for m in G):
        raise ScopeError("Clifford representation dimensions")
    eye=S.eye(G[0].rows)
    return tuple((anticommutator(G[a],G[b])-2*g[a,b]*eye
                 ).applyfunc(S.simplify) for a,b in product(range(n),repeat=2))


def finite_ccr_obstruction(x,p,hbar=1):
    """Return trace obstruction; [X,P]=ihbar I cannot hold in finite dim."""
    X,P=S.Matrix(x),S.Matrix(p)
    if X.shape!=P.shape or X.rows!=X.cols or zero(hbar):
        raise ScopeError("invalid finite-dimensional canonical pair")
    return S.simplify(S.trace(commutator(X,P)-S.I*hbar*S.eye(X.rows)))


def poisson_bracket(f,g,positions,momenta):
    q,p=list(positions),list(momenta)
    if len(q)!=len(p) or not q or len(set(q+p))!=2*len(q):
        raise ScopeError("independent canonical coordinate pairs required")
    return S.simplify(sum(S.diff(f,qi)*S.diff(g,pi)-
                          S.diff(f,pi)*S.diff(g,qi)
                          for qi,pi in zip(q,p)))


def poisson_jacobi_residual(f,g,h,positions,momenta):
    return S.simplify(
        poisson_bracket(f,poisson_bracket(g,h,positions,momenta),positions,momenta)
        +poisson_bracket(g,poisson_bracket(h,f,positions,momenta),positions,momenta)
        +poisson_bracket(h,poisson_bracket(f,g,positions,momenta),positions,momenta))


def constraint_closure(constraints, coefficients, positions, momenta):
    """Verify supplied first-class certificates {C_i,C_j}=sum f_ij^k C_k.

    Coefficients are symbolic certificate witnesses provided by the caller.
    This does not assert global regularity of the constraint surface.
    """
    cs=list(constraints)
    if not cs or len(coefficients)!=len(cs):
        raise ScopeError("constraint certificate dimensions")
    n=len(cs)
    if any(len(row)!=n or any(len(v)!=n for v in row) for row in coefficients):
        raise ScopeError("closure coefficient array shape")
    return tuple(S.simplify(poisson_bracket(cs[i],cs[j],positions,momenta) -
                            sum(coefficients[i][j][k]*cs[k] for k in range(n)))
                 for i,j in product(range(n),repeat=2))


def adm_scalar_constraint(spatial_metric, canonical_momentum, scalar_curvature):
    """ADM vacuum scalar constraint density, 16 pi G = 1.

    H = (pi^ij pi_ij - pi^2/(d-1))/sqrt(h) - sqrt(h) R(h).
    No lapse, shift or full smeared functional constraint algebra is inferred.
    """
    h=S.Matrix(spatial_metric)
    p=S.Matrix(canonical_momentum)
    d=h.rows
    if d<2 or d>3 or h.shape!=(d,d) or p.shape!=(d,d):
        raise ScopeError("ADM spatial dimension 2..3 and square matrices required")
    if not h.is_symmetric() or not p.is_symmetric():
        raise ScopeError("ADM spatial metric and momentum must be symmetric")
    det=S.simplify(h.det())
    if zero(det):
        raise ScopeError("ADM metric degenerate")
    pi=S.simplify(S.trace(h*p))
    square=S.simplify(S.trace(h*p*h*p))
    return S.simplify((square-pi**2/(d-1))/S.sqrt(det) -
                      S.sqrt(det)*scalar_curvature)
