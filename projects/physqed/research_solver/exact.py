"""Exact rational polynomial oracle independent of the SymPy expression engine.

Controlled JSON AST -> sparse Q[x] using Python fractions only.
This oracle proves/contradicts a *formal polynomial identity*, not a physical law.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import product

MAX_TERMS = 2048
MAX_DEGREE = 16
MAX_NODES = 600


class PolynomialScope(ValueError):
    """The bounded exact-polynomial backend cannot certify this input."""


def _clean(p):
    return {e: c for e, c in p.items() if c}


def _add(a, b):
    out = dict(a)
    for e, c in b.items():
        out[e] = out.get(e, Q(0)) + c
    return _clean(out)


def _neg(a):
    return {e: -c for e, c in a.items()}


def _mul(a, b):
    out = {}
    for e, c in a.items():
        for f, d in b.items():
            h = tuple(x + y for x, y in zip(e, f))
            if sum(h) > MAX_DEGREE:
                raise PolynomialScope("polynomial total-degree bound exceeded")
            out[h] = out.get(h, Q(0)) + c * d
            if len(out) > MAX_TERMS:
                raise PolynomialScope("polynomial term budget exceeded")
    return _clean(out)


def independent_polynomial(tree, variables):
    """No SymPy, no eval, no expression text, no unbounded powers."""
    if not isinstance(variables, (list, tuple)) or not 1 <= len(variables) <= 8:
        raise PolynomialScope("expected 1..8 controlled variables")
    names = tuple(variables)
    zero = (0,) * len(names)
    count = [0]

    def walk(node, depth=0):
        count[0] += 1
        if depth > 24 or count[0] > MAX_NODES:
            raise PolynomialScope("AST size or depth budget exceeded")
        if type(node) is int:
            if abs(node) > 10**40:
                raise PolynomialScope("integer coefficient exceeds bound")
            return {zero: Q(node)} if node else {}
        if isinstance(node, str):
            if node not in names:
                raise PolynomialScope("undeclared variable")
            e = tuple(int(node == name) for name in names)
            return {e: Q(1)}
        if not isinstance(node, dict) or len(node) != 1:
            raise PolynomialScope("unknown AST node")
        op, arg = next(iter(node.items()))
        if op == "rational":
            if (not isinstance(arg, list) or len(arg) != 2 or
                any(type(v) is not int or abs(v) > 10**40 for v in arg) or
                arg[1] == 0):
                raise PolynomialScope("invalid exact rational")
            val = Q(*arg)
            return {zero: val} if val else {}
        if op == "neg":
            return _neg(walk(arg, depth + 1))
        if op in ("add", "mul"):
            if not isinstance(arg, list) or not 2 <= len(arg) <= 16:
                raise PolynomialScope("expected 2..16 operands")
            result = {} if op == "add" else {zero: Q(1)}
            for item in arg:
                piece = walk(item, depth + 1)
                result = _add(result, piece) if op == "add" else _mul(result, piece)
            return result
        if op == "pow":
            if (not isinstance(arg, list) or len(arg) != 2 or
                type(arg[1]) is not int or not 0 <= arg[1] <= 8):
                raise PolynomialScope("only nonnegative integer powers <= 8")
            base = walk(arg[0], depth + 1)
            result = {zero: Q(1)}
            for _ in range(arg[1]):
                result = _mul(result, base)
            return result
        # pi, trigonometry, radicals and negative powers are not polynomials
        # in Q[variables]; another trusted backend must handle them.
        raise PolynomialScope("not a bounded rational polynomial AST")
    return _clean(walk(tree))


def coefficient_difference(lhs, rhs, variables):
    return _add(independent_polynomial(lhs, variables),
                _neg(independent_polynomial(rhs, variables)))


def evaluate(poly, values):
    result = Q(0)
    for mon, coefficient in poly.items():
        term = coefficient
        for x, power in zip(values, mon):
            term *= Q(x) ** power
        result += term
    return result


def rational_counterexample(poly, names):
    """Find a witness; nonzero coefficients alone already disprove equality."""
    if not poly:
        return None
    n = len(names)
    points = (Q(0), Q(1), Q(-1), Q(2), Q(3), Q(-2), Q(5))
    # Deterministic independent evaluations; bounded even in 8 variables.
    for d in range(min(n, 4) + 1):
        for values in product(points[:5], repeat=d):
            assignment = tuple(values) + (Q(0),) * (n - d)
            residual = evaluate(poly, assignment)
            if residual:
                return {"assignment": {name: str(x) for name, x in zip(names, assignment)},
                        "residual": str(residual)}
    for t in points:
        assignment = tuple(t * Q(i + 1) for i in range(n))
        residual = evaluate(poly, assignment)
        if residual:
            return {"assignment": {name: str(x) for name, x in zip(names, assignment)},
                    "residual": str(residual)}
    return None


def polynomial_signature(poly):
    return [{"powers": list(exps), "coefficient": str(coeff)}
            for exps, coeff in sorted(poly.items())]


def independent_units(node, dimensions, bases=("M", "L", "T", "Q")):
    """Check externally declared dimensions; this does not validate declarations.

    A literal zero is polymorphic; a nonzero numeric constant is dimensionless.
    """
    bases = tuple(bases)
    zero = (Q(0),) * len(bases)
    def walk(tree):
        if type(tree) is int:
            return None if tree == 0 else zero
        if isinstance(tree, str):
            if tree not in dimensions:
                raise PolynomialScope("missing dimension for variable")
            v = dimensions[tree]
            if not isinstance(v, dict) or set(v) - set(bases):
                raise PolynomialScope("invalid base-unit dimensions")
            if any(type(x) is not int or abs(x) > 12 for x in v.values()):
                raise PolynomialScope("out-of-range unit exponent")
            return tuple(Q(v.get(k, 0)) for k in bases)
        if not isinstance(tree, dict) or len(tree) != 1:
            raise PolynomialScope("invalid dimension expression")
        op, a = next(iter(tree.items()))
        if op == "rational":
            if (not isinstance(a, list) or len(a) != 2 or
                    any(type(x) is not int for x in a) or a[1] == 0):
                raise PolynomialScope("invalid rational dimension value")
            return None if a[0] == 0 else zero
        if op == "neg":
            return walk(a)
        if op == "add":
            values = [walk(z) for z in a]
            present = set(x for x in values if x is not None)
            if len(present) > 1:
                raise PolynomialScope("dimensionally inconsistent addition")
            return next(iter(present)) if present else None
        if op == "mul":
            vals = [walk(z) for z in a]
            if None in vals:
                return None
            return tuple(sum(x[i] for x in vals) for i in range(len(bases)))
        if op == "pow":
            if (not isinstance(a, list) or len(a) != 2 or
                type(a[1]) is not int or not -8 <= a[1] <= 8):
                raise PolynomialScope("bad dimension power")
            v = walk(a[0])
            if v is None:
                if a[1] < 0:
                    raise PolynomialScope("zero to a negative power")
                return zero if a[1] == 0 else None
            return tuple(x * a[1] for x in v)
        if op == "func":
            if not isinstance(a, dict) or set(a) != {"name", "arg"}:
                raise PolynomialScope("bad function AST")
            d = walk(a["arg"])
            if a["name"] in ("sin", "cos", "exp"):
                if d is not None and d != zero:
                    raise PolynomialScope("function argument has units")
                return zero
            if a["name"] == "sqrt":
                return None if d is None else tuple(x / 2 for x in d)
        if op == "constant" and a == "pi":
            return zero
        raise PolynomialScope("unsupported AST dimensional rule")
    return walk(node)


def compare_units(lhs, rhs, dimensions, names):
    if not isinstance(dimensions, dict) or set(dimensions) != set(names):
        raise PolynomialScope("all variables need declared dimensions")
    a, b = independent_units(lhs, dimensions), independent_units(rhs, dimensions)
    if a is not None and b is not None and a != b:
        raise PolynomialScope("left and right units differ")
    return {"checked": True, "dimension": [str(x) for x in (a or b or (Q(0),)*4)],
            "source": "caller-declared variable dimensions"}
