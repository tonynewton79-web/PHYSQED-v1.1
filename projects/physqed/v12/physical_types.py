"""Typed tensor signatures and geometric-length dimension checking.

Coordinate-aware *component* dimensions for zero-shift Einstein--Maxwell:
with ds having length L, x^a dimension L^(d_a), covariant metric g_ab
has L^(2-d_a-d_b), Maxwell potential A_a has L^(1-d_a), field strength
F_ab has L^(1-d_a-d_b), and Maxwell stress T_ab has L^(-d_a-d_b).
This is a geometrized-unit (c=G=...=1) length-dimension checker, NOT
a complete SI unit system or an arbitrary Einstein-summation type engine.
"""
from __future__ import annotations
from fractions import Fraction
from dataclasses import dataclass
import sympy as S
from .geometry import ScopeError

TENSOR_SIGNATURES = {
    "metric": ("dd", 2),
    "potential": ("d", 1),
    "field_strength": ("dd", 2),
    "stress": ("dd", 2),
    "lapse": ("", 0),
}
ZERO = None  # an exact zero may occupy a component of any dimension


def _power(value):
    if type(value) is not int or not -8 <= value <= 8:
        raise ScopeError("length dimensions require bounded integer exponents")
    return Fraction(value)


def _exact_zero(node):
    # Only literal zero, or rational numerator zero, receives a polymorphic
    # component zero dimension. Do not trust unsimplified arbitrary ASTs.
    return type(node) is int and node == 0 or (
        isinstance(node, dict) and set(node) == {"rational"} and
        isinstance(node["rational"], list) and len(node["rational"]) == 2 and
        type(node["rational"][0]) is int and node["rational"][0] == 0 and
        type(node["rational"][1]) is int and node["rational"][1] != 0)


@dataclass(frozen=True)
class TensorType:
    name: str
    variance: str
    rank: int

    def validate(self):
        expected = TENSOR_SIGNATURES.get(self.name)
        if expected is None or (self.variance, self.rank) != expected:
            raise ScopeError("tensor rank/index variance mismatch for " + self.name)
        return self


class GeometrizedDimensions:
    """One-base length L type checking with coordinate-aware components."""

    def __init__(self, coordinates, parameters, raw):
        if not isinstance(raw, dict) or set(raw) != {
            "system", "coordinates", "parameters"
        } or raw["system"] != "geometrized_length":
            raise ScopeError("explicit geometrized_length unit system required")
        cd = raw["coordinates"]
        pd = raw["parameters"]
        if not isinstance(cd, dict) or set(cd) != set(coordinates):
            raise ScopeError("every coordinate requires a length exponent")
        if not isinstance(pd, dict) or set(pd) != set(parameters):
            raise ScopeError("every parameter requires a length exponent")
        self.coord = {name: _power(cd[name]) for name in coordinates}
        self.param = {name: _power(pd[name]) for name in parameters}
        self.symbols = dict(self.coord)
        self.symbols.update(self.param)
        self.coordinates = tuple(coordinates)

    @staticmethod
    def _combine_add(dimensions):
        actual = {d for d in dimensions if d is not ZERO}
        if len(actual) > 1:
            raise ScopeError("dimensionally inconsistent addition")
        return next(iter(actual)) if actual else ZERO

    def dimension(self, node, depth=0):
        if depth > 18:
            raise ScopeError("dimensional AST recursion exceeds limit")
        if _exact_zero(node):
            return ZERO
        if type(node) is int:
            return Fraction(0)
        if type(node) is str:
            if node not in self.symbols:
                raise ScopeError("undeclared symbol in dimension checker")
            return self.symbols[node]
        if not isinstance(node, dict) or len(node) != 1:
            raise ScopeError("invalid dimensional expression")
        key, value = next(iter(node.items()))
        ch = lambda v: self.dimension(v, depth+1)
        if key == "rational":
            if (not isinstance(value, list) or len(value) != 2 or
                any(type(v) is not int for v in value) or value[1] == 0):
                raise ScopeError("invalid rational dimensions")
            return Fraction(0)
        if key in ("add", "mul"):
            if not isinstance(value, list) or not 2 <= len(value) <= 16:
                raise ScopeError("invalid add/mul dimensions")
            ds = [ch(v) for v in value]
            if key == "add":
                return self._combine_add(ds)
            if ZERO in ds:
                return ZERO
            return sum(ds, Fraction(0))
        if key == "neg":
            return ch(value)
        if key == "pow":
            if (not isinstance(value, list) or len(value) != 2
                or type(value[1]) is not int or not -8 <= value[1] <= 8):
                raise ScopeError("invalid power dimensions")
            d = ch(value[0])
            if d is ZERO:
                if value[1] < 0:
                    raise ScopeError("zero to negative power is undefined")
                return Fraction(0) if value[1] == 0 else ZERO
            return d * value[1]
        if key == "constant":
            if value != "pi":
                raise ScopeError("unknown dimensionless mathematical constant")
            return Fraction(0)
        if key == "func":
            if not isinstance(value, dict) or set(value) != {"name", "arg"}:
                raise ScopeError("invalid function dimension constructor")
            fun = value["name"]
            if not isinstance(fun, str):
                raise ScopeError("invalid function name")
            d = ch(value["arg"])
            if fun in ("sin", "cos", "exp"):
                if d is not ZERO and d != 0:
                    raise ScopeError(fun + " argument must be dimensionless")
                return Fraction(0)
            if fun == "sqrt":
                return ZERO if d is ZERO else d / 2
            raise ScopeError("unsupported dimensional function")
        raise ScopeError("unsupported dimensional AST constructor: " + str(key))

    def require(self, expr, required, label):
        d = self.dimension(expr)
        target = Fraction(required)
        if d is not ZERO and d != target:
            raise ScopeError(f"wrong physical length dimension for {label}: L^{d} expected L^{target}")
        return {"field": label, "dimension": "zero" if d is ZERO else str(d),
                "expected": str(target), "passed": True}

    def matrix(self, expression, kind):
        n = len(self.coordinates)
        if (not isinstance(expression, list) or len(expression) != n or
            any(not isinstance(row, list) or len(row) != n for row in expression)):
            raise ScopeError("typed " + kind + " matrix shape incorrect")
        tests = []
        for i in range(n):
            for j in range(n):
                dim = self.coord[self.coordinates[i]] + self.coord[self.coordinates[j]]
                expected = (2 - dim if kind == "metric" else
                            1 - dim if kind == "field_strength" else -dim)
                tests.append(self.require(expression[i][j], expected,
                                f"{kind}[{i},{j}]"))
        return tests

    def one_form(self, expression):
        n = len(self.coordinates)
        if not isinstance(expression, list) or len(expression) != n:
            raise ScopeError("one-form potential components required")
        return [self.require(expression[i],
                  1 - self.coord[self.coordinates[i]],f"A[{i}]")
                  for i in range(n)]

    def check_lapse(self, expression):
        return self.require(expression, 1 - self.coord[self.coordinates[0]], "lapse")

    def check_cosmological(self, expression):
        return self.require(expression, -2, "cosmological_constant")

    def check_coupling(self, expression):
        return self.require(expression, 0, "gravitational_coupling")


def check_tensor_signatures(raw):
    if (not isinstance(raw, dict) or set(raw) != set(TENSOR_SIGNATURES)):
        raise ScopeError("explicit metric/potential/F/stress/lapse tensor signatures required")
    results = []
    for name, (variance, rank) in TENSOR_SIGNATURES.items():
        obj = raw[name]
        if not isinstance(obj, dict) or set(obj) != {"variance", "rank"}:
            raise ScopeError("invalid typed tensor signature for " + name)
        TensorType(name, obj["variance"], obj["rank"]).validate()
        results.append({"name": name, "variance": variance, "rank": rank,
                        "passed": True})
    return results
