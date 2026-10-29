"""PHYSQED v1.2: independent exact coordinate-curvature oracle.

Uses Python fractions and elementary matrix operations only. The input is the
2-jet (metric, first derivatives, second derivatives) at a fixed chart point:
    first[k][i][j] = partial_k g_ij
    second[k][l][i][j] = partial_k partial_l g_ij.
Returns connection, Riemann, Ricci, scalar and Einstein components. The oracle
does not import SymPy or PHYSQED's geometry backend.

R^a_(b c d) = partial_c Gamma^a_(d b) - partial_d Gamma^a_(c b)
                + Gamma^a_(c e)Gamma^e_(d b)
                - Gamma^a_(d e)Gamma^e_(c b).
A jet is local data; no claims of global chart regularity are inferred.
"""
from fractions import Fraction


def _f(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, Fraction)):
        raise ValueError("oracle requires exact integer, string or Fraction input")
    return Fraction(value)


def _inverse(matrix):
    n = len(matrix)
    rows = [list(matrix[i]) + [Fraction(int(i == j)) for j in range(n)]
            for i in range(n)]
    for k in range(n):
        pivot = next((j for j in range(k, n) if rows[j][k]), None)
        if pivot is None:
            raise ValueError("degenerate metric jet")
        rows[k], rows[pivot] = rows[pivot], rows[k]
        v = rows[k][k]
        rows[k] = [u / v for u in rows[k]]
        for i in range(n):
            if i == k:
                continue
            v = rows[i][k]
            rows[i] = [a - v*b for a, b in zip(rows[i], rows[k])]
    return tuple(tuple(row[n:]) for row in rows)


def curvature_from_jet(metric, first, second):
    """Independent exact local Riemann calculation using only rational jets."""
    n = len(metric)
    if not 1 <= n <= 4:
        raise ValueError("oracle requires chart dimension 1..4")
    try:
        g = tuple(tuple(_f(metric[i][j]) for j in range(n))
                  for i in range(n))
        dg = tuple(tuple(tuple(_f(first[k][i][j]) for j in range(n))
                         for i in range(n)) for k in range(n))
        ddg = tuple(tuple(tuple(tuple(_f(second[k][l][i][j])
                         for j in range(n)) for i in range(n))
                         for l in range(n)) for k in range(n))
    except (IndexError, TypeError, KeyError) as exc:
        raise ValueError("bad metric 2-jet dimensions") from exc
    if (any(len(row) != n for row in metric) or len(first) != n
        or len(second) != n):
        raise ValueError("bad metric 2-jet dimensions")
    for i in range(n):
        for j in range(n):
            if g[i][j] != g[j][i]:
                raise ValueError("metric jet is not symmetric")
            for k in range(n):
                if dg[k][i][j] != dg[k][j][i]:
                    raise ValueError("first metric jet is not symmetric")
                for l in range(n):
                    if ddg[k][l][i][j] != ddg[k][l][j][i] or ddg[k][l][i][j] != ddg[l][k][i][j]:
                        raise ValueError("second metric jet inconsistent")
    inv = _inverse(g)
    # derivative of inverse: d_k g^{-1} = -g^{-1} (d_k g) g^{-1}.
    dinv = [[[-sum(inv[a][i] * dg[k][i][j] * inv[j][h]
                   for i in range(n) for j in range(n))
              for h in range(n)] for a in range(n)] for k in range(n)]
    # C_hbc = d_b g_hc + d_c g_hb - d_h g_bc.
    c = lambda h, b, d: dg[b][h][d] + dg[d][h][b] - dg[h][b][d]
    dc = lambda k, h, b, d: (ddg[k][b][h][d] +
                             ddg[k][d][h][b] - ddg[k][h][b][d])
    half = Fraction(1, 2)
    gamma = [[[
        half * sum(inv[a][h] * c(h,b,d) for h in range(n))
        for d in range(n)] for b in range(n)] for a in range(n)]
    dgamma = [[[[
        half * sum(dinv[k][a][h] * c(h,b,d) +
                   inv[a][h] * dc(k,h,b,d) for h in range(n))
        for d in range(n)] for b in range(n)]
        for a in range(n)] for k in range(n)]
    riemann = [[[[
        dgamma[c][a][d][b] - dgamma[d][a][c][b] +
        sum(gamma[a][c][h]*gamma[h][d][b] -
            gamma[a][d][h]*gamma[h][c][b] for h in range(n))
        for d in range(n)] for c in range(n)] for b in range(n)]
        for a in range(n)]
    ricci = [[sum(riemann[a][b][a][d] for a in range(n))
              for d in range(n)] for b in range(n)]
    scalar = sum(inv[b][d]*ricci[b][d]
                 for b in range(n) for d in range(n))
    einstein = [[ricci[b][d]-Fraction(1,2)*scalar*g[b][d]
                 for d in range(n)] for b in range(n)]
    return {
        "dimension": n,
        "inverse": tuple(tuple(row) for row in inv),
        "connection": gamma,
        "riemann": riemann,
        "ricci": ricci,
        "scalar": scalar,
        "einstein": einstein,
    }
