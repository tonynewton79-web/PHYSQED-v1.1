"""PHYSQED v1.2: finite Lie-algebra and local Yang--Mills checks.

A_a are Lie-algebra coefficient columns. The structure constants are exact;
no numerical 'approximately Jacobi' acceptance is permitted.
"""
from __future__ import annotations
from itertools import product
import sympy as S
from .geometry import ScopeError, zero


class LieAlgebra:
    def __init__(self, structure):
        f = S.MutableDenseNDimArray(structure)
        if f.rank() != 3 or len(set(f.shape)) != 1:
            raise ScopeError("structure constants must be a cubic tensor")
        self.dim = f.shape[0]
        if not 1 <= self.dim <= 8:
            raise ScopeError("supported Lie algebra dimension: 1..8")
        self.f = f
        if not self.check_antisymmetry() or not self.check_jacobi():
            raise ScopeError("structure constants violate antisymmetry/Jacobi")

    def check_antisymmetry(self):
        return all(zero(self.f[a,b,c]+self.f[b,a,c])
                   for a,b,c in product(range(self.dim),repeat=3))

    def check_jacobi(self):
        n=self.dim
        return all(zero(sum(
            self.f[a,b,e]*self.f[e,c,d] +
            self.f[b,c,e]*self.f[e,a,d] +
            self.f[c,a,e]*self.f[e,b,d]
            for e in range(n)))
            for a,b,c,d in product(range(n),repeat=4))

    @classmethod
    def u1(cls):
        return cls(S.MutableDenseNDimArray.zeros(1,1,1))

    @classmethod
    def so3(cls):
        return cls([[[S.LeviCivita(a,b,c) for c in range(3)]
                     for b in range(3)] for a in range(3)])

    @classmethod
    def lorentz(cls):
        f = S.MutableDenseNDimArray.zeros(6,6,6)
        for i,j,k in product(range(3),repeat=3):
            eps=S.LeviCivita(i,j,k)
            f[i,j,k]=eps
            f[i,j+3,k+3]=eps
            f[i+3,j,k+3]=eps
            f[i+3,j+3,k]=-eps
        return cls(f)

    def bracket(self, a, b):
        if len(a)!=self.dim or len(b)!=self.dim:
            raise ScopeError("Lie vector dimension")
        return S.Matrix([S.simplify(sum(self.f[i,j,k]*a[i]*b[j]
                       for i,j in product(range(self.dim),repeat=2)))
                         for k in range(self.dim)])

    def representation_valid(self, generators):
        if len(generators)!=self.dim:
            raise ScopeError("representation generator count")
        t=[S.Matrix(a) for a in generators]
        if any(a.shape!=t[0].shape or a.rows!=a.cols for a in t):
            raise ScopeError("representation matrices must be square/equal")
        return all(zero(v) for a,b in product(range(self.dim),repeat=2)
                   for v in t[a]*t[b]-t[b]*t[a] -
                   sum((self.f[a,b,c]*t[c] for c in range(self.dim)),
                       S.zeros(t[0].rows)))


class GaugeField:
    def __init__(self, algebra, coordinates, potentials):
        self.lie=algebra
        self.x=tuple(coordinates)
        self.n=len(self.x)
        if not 1 <= self.n <= 4 or len(potentials)!=self.n:
            raise ScopeError("gauge chart must have 1..4 dimensions")
        self.A=[S.Matrix(a) for a in potentials]
        if any(a.shape!=(algebra.dim,1) for a in self.A):
            raise ScopeError("gauge connection coefficient count")
        self._field=None

    @property
    def field(self):
        if self._field is None:
            n=self.n
            f=[[S.zeros(self.lie.dim,1) for _ in range(n)]
               for _ in range(n)]
            for mu in range(n):
                for nu in range(mu+1,n):
                    f[mu][nu]=(self.A[nu].diff(self.x[mu]) -
                               self.A[mu].diff(self.x[nu]) +
                               self.lie.bracket(self.A[mu],self.A[nu])
                               ).applyfunc(S.simplify)
                    f[nu][mu]=-f[mu][nu]
            self._field=f
        return self._field

    def covariant(self, mu, vector):
        return (S.Matrix(vector).diff(self.x[mu]) +
                self.lie.bracket(self.A[mu],vector)).applyfunc(S.simplify)

    def bianchi_residual(self):
        F=self.field
        return tuple((self.covariant(mu,F[nu][rho]) +
                      self.covariant(nu,F[rho][mu]) +
                      self.covariant(rho,F[mu][nu])).applyfunc(S.simplify)
                     for mu,nu,rho in product(range(self.n),repeat=3))

    def yang_mills_residual(self, spacetime_metric, current=None):
        """D_mu(sqrt(|g|) F^{mu nu})/sqrt(|g|)-j^nu=0."""
        g=S.Matrix(spacetime_metric)
        if g.shape!=(self.n,self.n) or zero(g.det()):
            raise ScopeError("nonsingular spacetime metric required")
        inv=g.inv()
        volume=S.sqrt(S.Abs(S.simplify(g.det())))
        F=self.field
        current=current or [S.zeros(self.lie.dim,1) for _ in range(self.n)]
        if len(current)!=self.n:
            raise ScopeError("current must have one Lie vector per direction")
        out=[]
        for nu in range(self.n):
            acc=S.zeros(self.lie.dim,1)
            for mu in range(self.n):
                fup=sum((inv[mu,rho]*inv[nu,sigma]*F[rho][sigma]
                     for rho,sigma in product(range(self.n),repeat=2)),
                     S.zeros(self.lie.dim,1))
                acc+=self.covariant(mu,volume*fup)
            out.append((acc/volume-S.Matrix(current[nu])).applyfunc(S.simplify))
        return tuple(out)


def matrix_curvature(coords, connections):
    """Representation-valued F_mu nu = d_mu A_nu - d_nu A_mu + [A_mu,A_nu]."""
    x=tuple(coords)
    A=[S.Matrix(m) for m in connections]
    n=len(x)
    if len(A)!=n or any(m.shape!=A[0].shape or m.rows!=m.cols for m in A):
        raise ScopeError("matrix-valued connection shape")
    return [[(A[nu].diff(x[mu])-A[mu].diff(x[nu])+
              A[mu]*A[nu]-A[nu]*A[mu]).applyfunc(S.simplify)
             for nu in range(n)] for mu in range(n)]


def transformed_connection(coords, connections, transformation):
    """Local gauge law: A' = U A U^-1 - (dU) U^-1."""
    U=S.Matrix(transformation)
    if U.rows != U.cols or zero(U.det()):
        raise ScopeError("gauge transformation not invertible")
    inv=U.inv()
    return [(U*S.Matrix(A)*inv-U.diff(x)*inv).applyfunc(S.simplify)
            for x,A in zip(coords,connections)]


def transformation_residual(coords, connections, transformation):
    U=S.Matrix(transformation)
    F=matrix_curvature(coords,connections)
    Fp=matrix_curvature(coords,transformed_connection(
        coords,connections,U))
    inv=U.inv()
    return tuple((Fp[mu][nu]-U*F[mu][nu]*inv).applyfunc(S.simplify)
                 for mu,nu in product(range(len(coords)),repeat=2))
