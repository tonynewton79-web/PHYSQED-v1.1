"""PHYSQED v1.2: classical fields and finite Gaussian perturbation theory.

Functional Euler--Lagrange here means a local first-derivative Lagrangian
on a coordinate chart. Gaussian/Wick calculations are finite-dimensional
formal expansions; they do not certify continuum QFT, regularisation,
renormalisation, spectral condition or nonperturbative existence.
"""
from __future__ import annotations
from functools import lru_cache
import sympy as S
from .geometry import ScopeError, zero


def euler_lagrange(lagrangian, fields, coordinates):
    """E_i=partial L/partial phi_i - d_mu(partial L/partial phi_i,mu)."""
    x=tuple(coordinates)
    phi=tuple(fields)
    if not 1<=len(x)<=4 or not 1<=len(phi)<=8:
        raise ScopeError("supported fields 1..8 and coordinates 1..4")
    if any(not isinstance(f,S.FunctionClass) and not (
         hasattr(f,"is_Function") and f.is_Function) for f in phi):
        raise ScopeError("fields must be evaluated SymPy functions")
    out=[]
    for f in phi:
        v=S.diff(lagrangian,f)
        for xi in x:
            v-=S.diff(S.diff(lagrangian,S.diff(f,xi)),xi)
        out.append(S.simplify(v))
    return tuple(out)


def canonical_stress(lagrangian, fields, coordinates):
    """Mixed canonical stress T^mu_nu=sum pi_i^mu d_nu phi_i-delta^mu_nu L."""
    x=tuple(coordinates)
    return S.Matrix(len(x),len(x),lambda mu,nu:S.simplify(
        sum(S.diff(lagrangian,S.diff(f,x[mu]))*S.diff(f,x[nu])
            for f in fields) - (lagrangian if mu==nu else 0)))


def translation_noether_residual(lagrangian, fields, coordinates):
    """d_mu T^mu_nu + sum_i EL_i d_nu phi_i, zero for x-independent L."""
    x=tuple(coordinates)
    t=canonical_stress(lagrangian,fields,x)
    el=euler_lagrange(lagrangian,fields,x)
    return tuple(S.simplify(sum(S.diff(t[mu,nu],x[mu])
                 for mu in range(len(x))) +
                 sum(el[i]*S.diff(fields[i],x[nu])
                     for i in range(len(fields))))
                 for nu in range(len(x)))


def noether_current(lagrangian, fields, variations, coordinates):
    if len(fields)!=len(variations):
        raise ScopeError("Noether generator dimension")
    return tuple(S.simplify(sum(
        S.diff(lagrangian,S.diff(f,x))*df
        for f,df in zip(fields,variations))) for x in coordinates)


def quadratic_propagator(kernel):
    K=S.Matrix(kernel)
    if K.rows!=K.cols or K.rows<1 or K.rows>12 or zero(K.det()):
        raise ScopeError("nondegenerate finite Gaussian kernel 1..12 required")
    if any(not zero(K[i,j]-K[j,i]) for i in range(K.rows)
           for j in range(K.cols)):
        raise ScopeError("Gaussian kernel must be symmetric")
    return K.inv().applyfunc(S.simplify)


def wick(indices, covariance):
    """Wick moment sum of all pairings for centered Gaussian variables."""
    C=S.Matrix(covariance)
    if C.rows!=C.cols or C.rows<1 or C.rows>12:
        raise ScopeError("covariance dimensions")
    ids=tuple(indices)
    if any(not isinstance(i,int) or i<0 or i>=C.rows for i in ids):
        raise ScopeError("invalid Wick field index")
    if len(ids)>12:
        raise ScopeError("Wick expansion order exceeds 12")
    if len(ids)%2:
        return S.S.Zero

    @lru_cache(None)
    def pair(seq):
        if not seq:
            return S.S.One
        return S.expand(sum(C[seq[0],seq[k]]*pair(
            seq[1:k]+seq[k+1:]) for k in range(1,len(seq))))
    return S.simplify(pair(ids))


def first_order_phi4_two_point(covariance, left, right, couplings):
    """O(lambda) normalized zero-dimensional phi^4 Euclidean 2pt correction.

    S = 1/2 phi K phi + sum_i lambda_i phi_i^4/24.
    Returns coefficient sum -lambda_i/24*(<phi_l phi_r phi_i^4>
        - <phi_l phi_r><phi_i^4>) using the free Gaussian.
    """
    C=S.Matrix(covariance)
    if len(couplings)!=C.rows or not (0<=left<C.rows and 0<=right<C.rows):
        raise ScopeError("phi4 indices and couplings")
    return S.simplify(-sum(couplings[k]/24*(
        wick([left,right]+[k]*4,C) - C[left,right]*wick([k]*4,C))
        for k in range(C.rows)))
