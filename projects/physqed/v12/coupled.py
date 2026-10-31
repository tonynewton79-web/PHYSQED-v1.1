"""PHYSQED v1.2: textbook Einstein–Maxwell coupling and conservation.

Conventions: signature (-,+,+,+), S = int sqrt(-g) (R - F_{ab}F^{ab}),
G_ab = 2 [F_ac F_b{}^c - g_ab F_cd F^{cd}/4], in geometrized units.
A supplied Maxwell 2-form is not automatically asserted globally exact.
This is a chart-local symbolic check, not a theory of arbitrary matter.
"""
from __future__ import annotations
import sympy as S
from .geometry import Geometry, ScopeError, zero


def _antisymmetric_field(field, dimension):
    F = S.Matrix(field)
    if F.shape != (dimension, dimension):
        raise ScopeError("electromagnetic two-form dimension mismatch")
    if any(not zero(F[i,j]+F[j,i])
           for i in range(dimension) for j in range(dimension)):
        raise ScopeError("Maxwell field tensor must be antisymmetric")
    return F


def maxwell_from_potential(coordinates, potential):
    """Local F_ab=partial_a A_b - partial_b A_a."""
    x = tuple(coordinates)
    n = len(x)
    if n < 2 or n > 4 or len(potential) != n:
        raise ScopeError("Maxwell potential/chart dimension mismatch")
    return S.Matrix(n, n, lambda a,b: S.simplify(
        S.diff(potential[b], x[a]) - S.diff(potential[a], x[b])))


def maxwell_bianchi(field, coordinates):
    x = tuple(coordinates)
    F = _antisymmetric_field(field, len(x))
    return tuple(S.simplify(S.diff(F[b,c],x[a]) +
                           S.diff(F[c,a],x[b]) + S.diff(F[a,b],x[c]))
                 for a in range(len(x)) for b in range(len(x))
                 for c in range(len(x)))


def maxwell_stress(geometry, field):
    """Maxwell stress T_ab=F_ac F_b{}^c - (1/4)g_ab F_cd F^cd."""
    F = _antisymmetric_field(field, geometry.n)
    inv = geometry.g_inv
    raised = (inv * F * inv.T).applyfunc(S.simplify)
    invariant = S.simplify(sum(F[a,b]*raised[a,b]
                   for a in range(geometry.n) for b in range(geometry.n)))
    return (F*inv*F.T - geometry.g*invariant/4).applyfunc(S.simplify)


def maxwell_equations(geometry, field, source=None):
    """Return nabla_a F^{ab} - J^b, using the full Levi-Civita connection.

    The divergent tensor identity avoids explicit sqrt(abs(det g)), which
    can otherwise obscure local chart-sign assumptions.
    """
    F=_antisymmetric_field(field,geometry.n)
    n=geometry.n
    C=geometry.connection
    raised=(geometry.g_inv*F*geometry.g_inv.T).applyfunc(S.simplify)
    if source is None:
        source=[S.S.Zero for _ in range(n)]
    if len(source)!=n:
        raise ScopeError("Maxwell source vector dimension mismatch")
    return tuple(S.simplify(
        sum(S.diff(raised[a,b],geometry.x[a]) +
            sum(C[a][a][c]*raised[c,b] + C[b][a][c]*raised[a,c]
                for c in range(n)) for a in range(n)) - source[b])
        for b in range(n))


def covariant_divergence_stress(geometry, stress):
    """Return nabla^a T_ab, directly from a covariant (0,2) tensor."""
    T=S.Matrix(stress)
    n=geometry.n
    if T.shape!=(n,n):
        raise ScopeError("stress dimension mismatch")
    inv=geometry.g_inv
    C=geometry.connection
    result = []
    for b in range(n):
        divergence = S.S.Zero
        for a in range(n):
            for k in range(n):
                covariant_part = S.diff(T[a,b], geometry.x[k]) - sum(
                    C[c][k][a]*T[c,b] + C[c][k][b]*T[a,c]
                    for c in range(n)
                )
                divergence += inv[a,k] * covariant_part
        result.append(S.simplify(divergence))
    return tuple(result)


def einstein_maxwell_residual(geometry, field):
    """Return the full G_ab-2*T_ab residual with stated action convention."""
    T=maxwell_stress(geometry,field)
    return (geometry.einstein - 2*T).applyfunc(S.simplify)


def check_einstein_maxwell(geometry, field, *, require_nonzero=True):
    """Structured multi-equation component suite; no blanket physics proof.

    Includes Maxwell Bianchi and source-free equation, Einstein equation,
    covariant stress conservation and vanishing Maxwell stress trace.
    """
    if not isinstance(geometry, Geometry) or geometry.n!=4:
        raise ScopeError("Einstein-Maxwell benchmark requires four-dimensional Geometry")
    F=_antisymmetric_field(field,4)
    if require_nonzero and all(zero(v) for v in F):
        raise ScopeError("nontrivial electromagnetic field required for benchmark")
    T=maxwell_stress(geometry,F)
    conditions={
        "maxwell_bianchi": maxwell_bianchi(F,geometry.x),
        "maxwell_equation": maxwell_equations(geometry,F),
        "einstein_equation": einstein_maxwell_residual(geometry,F),
        "stress_conservation": covariant_divergence_stress(geometry,T),
        "stress_trace": S.simplify(S.trace(geometry.g_inv*T)),
    }
    return {name: all(zero(v) for v in (value if isinstance(value,tuple)
           else list(value) if isinstance(value,S.MatrixBase) else (value,)))
            for name,value in conditions.items()}
