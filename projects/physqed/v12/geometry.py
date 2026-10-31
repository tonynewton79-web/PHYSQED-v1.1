"""PHYSQED v1.2: coordinate tensor and curvature backend.

Conventions: R^a_{bcd} = d_c Gamma^a_{db} - d_d Gamma^a_{cb}
+ Gamma^a_{ce} Gamma^e_{db} - Gamma^a_{de} Gamma^e_{cb}.
The signature is supplied by the caller, not inferred. This is a finite symbolic
coordinate-chart verifier, not a global theorem prover.
"""
from __future__ import annotations

from itertools import product
import sympy as S


class ScopeError(ValueError):
    """Unsupported scope or unverifiable input; no certificate is issued."""


def zero(x):
    """Conservative exact symbolic zero test including trig identities.

    The second pass expands angle-multiple identities (e.g. sin(2x))
    before trigonometric simplification. Without it, correctly conserved
    Maxwell stress may be falsely refused in spherical coordinates.
    """
    try:
        if S.simplify(S.cancel(S.together(x))) == 0:
            return True
        return S.simplify(S.cancel(S.together(
            S.trigsimp(S.expand_trig(x))))) == 0
    except (TypeError, ValueError, ZeroDivisionError, NotImplementedError):
        return False


class Geometry:
    def __init__(self, coordinates, metric):
        self.x = tuple(coordinates)
        self.n = len(self.x)
        if not 1 <= self.n <= 4 or len(set(self.x)) != self.n:
            raise ScopeError("chart must have 1..4 distinct coordinates")
        if any(not isinstance(c, S.Symbol) for c in self.x):
            raise ScopeError("coordinates must be SymPy symbols")
        self.g = S.Matrix(metric)
        if self.g.shape != (self.n, self.n):
            raise ScopeError("metric/coordinate dimensions disagree")
        if any(not zero(self.g[i, j] - self.g[j, i])
               for i in range(self.n) for j in range(self.n)):
            raise ScopeError("metric is not symmetric")
        det = S.simplify(self.g.det())
        if zero(det):
            raise ScopeError("degenerate metric")
        self.g_inv = self.g.inv().applyfunc(S.simplify)
        self._connection = None
        self._riemann = None
        self._ricci = None

    @property
    def connection(self):
        if self._connection is None:
            n, x, g, inv = self.n, self.x, self.g, self.g_inv
            self._connection = [[[
                S.simplify(S.Rational(1, 2) * sum(
                    inv[a, h] * (S.diff(g[h, b], x[c]) +
                                 S.diff(g[h, c], x[b]) -
                                 S.diff(g[b, c], x[h]))
                    for h in range(n)))
                for c in range(n)] for b in range(n)] for a in range(n)]
        return self._connection

    @property
    def riemann(self):
        if self._riemann is None:
            n, x, C = self.n, self.x, self.connection
            self._riemann = [[[[
                S.simplify(S.diff(C[a][d][b], x[c]) -
                           S.diff(C[a][c][b], x[d]) +
                           sum(C[a][c][h] * C[h][d][b] -
                               C[a][d][h] * C[h][c][b]
                               for h in range(n)))
                for d in range(n)] for c in range(n)]
                for b in range(n)] for a in range(n)]
        return self._riemann

    @property
    def ricci(self):
        if self._ricci is None:
            R = self.riemann
            self._ricci = S.Matrix(self.n, self.n, lambda b, d:
                S.simplify(sum(R[a][b][a][d] for a in range(self.n))))
        return self._ricci

    @property
    def scalar(self):
        return S.simplify(S.trace(self.g_inv * self.ricci))

    @property
    def einstein(self):
        return (self.ricci - self.g * self.scalar / 2).applyfunc(S.simplify)

    def einstein_residual(self, stress, cosmological=0, coupling=1):
        T = S.Matrix(stress)
        if T.shape != self.g.shape:
            raise ScopeError("stress tensor shape mismatch")
        return (self.einstein + cosmological*self.g - coupling*T).applyfunc(S.simplify)

    def covariant_derivative(self, tensor, variance, derivative_index):
        """Derivative of arbitrary finite-rank tensor; 'u' upper, 'd' lower."""
        if any(c not in "ud" for c in variance) or len(variance) > 5:
            raise ScopeError("tensor rank limit is five")
        if not 0 <= derivative_index < self.n:
            raise ScopeError("derivative index out of range")
        shape = (self.n,) * len(variance)
        T = S.MutableDenseNDimArray(tensor, shape) if variance else None
        if not variance:
            return S.diff(S.sympify(tensor), self.x[derivative_index])
        C = self.connection
        out = S.MutableDenseNDimArray.zeros(*shape)
        for idx in product(range(self.n), repeat=len(variance)):
            expr = S.diff(T[idx], self.x[derivative_index])
            for pos, kind in enumerate(variance):
                for h in range(self.n):
                    other = idx[:pos] + (h,) + idx[pos+1:]
                    if kind == "u":
                        expr += C[idx[pos]][derivative_index][h] * T[other]
                    else:
                        expr -= C[h][derivative_index][idx[pos]] * T[other]
            out[idx] = S.simplify(expr)
        return out

    def contracted_bianchi_residual(self):
        """Return nabla_a G^a_b via a mixed-index covariant derivative."""
        mixed = self.g_inv * self.einstein
        C = self.connection
        return tuple(S.simplify(sum(
            S.diff(mixed[a, b], self.x[a]) +
            sum(C[a][a][h]*mixed[h, b] - C[h][a][b]*mixed[a, h]
                for h in range(self.n))
            for a in range(self.n))) for b in range(self.n))

    def first_bianchi_residual(self):
        """Algebraic R^a_[bcd]=0 for the Levi-Civita connection."""
        R = self.riemann
        return tuple(S.simplify(R[a][b][c][d] + R[a][c][d][b] +
                                R[a][d][b][c])
                     for a,b,c,d in product(range(self.n), repeat=4))

    def geodesic_residual(self, curves, parameter):
        if len(curves) != self.n:
            raise ScopeError("curve dimension mismatch")
        C = self.connection
        result = []
        for a in range(self.n):
            value = S.diff(curves[a], parameter, 2)
            for b,c in product(range(self.n), repeat=2):
                value += C[a][b][c].subs(dict(zip(self.x, curves))) * (
                    S.diff(curves[b], parameter) *
                    S.diff(curves[c], parameter))
            result.append(S.simplify(value))
        return tuple(result)


def tetrad_metric(coframe, internal_metric):
    E, eta = S.Matrix(coframe), S.Matrix(internal_metric)
    if E.rows != eta.rows or eta.rows != eta.cols:
        raise ScopeError("incompatible tetrad and internal metric")
    return (E.T * eta * E).applyfunc(S.simplify)


def cartan_torsion(coframe, spin_connection, coordinates):
    """T^I_{mu nu}=d_mu e^I_nu-d_nu e^I_mu+
       omega^I_{J mu}e^J_nu-omega^I_{J nu}e^J_mu."""
    E = S.Matrix(coframe)
    n = len(coordinates)
    if E.shape != (n,n) or len(spin_connection) != n:
        raise ScopeError("tetrad/spin connection dimensions")
    w = [S.Matrix(a) for a in spin_connection]
    if any(a.shape != (n,n) for a in w):
        raise ScopeError("spin connection matrix shape")
    return [[[
        S.simplify(S.diff(E[i,nu],coordinates[mu]) -
                   S.diff(E[i,mu],coordinates[nu]) +
                   sum(w[mu][i,j]*E[j,nu] - w[nu][i,j]*E[j,mu]
                       for j in range(n)))
        for nu in range(n)] for mu in range(n)] for i in range(n)]
