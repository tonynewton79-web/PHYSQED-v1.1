"""PHYSQED v1.2: bounded, typed JSON physics-input and obligation planner.

No eval, exec, Python-source parsing, arbitrary SymPy sympify, or permissive
unknown expression constructors. Input is a restricted JSON expression tree.
Symbolic verification relies on current v1.2 backends; a passed component
claim is NOT a theorem about general/global physical systems.
"""
from __future__ import annotations
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import sympy as S

from .geometry import Geometry, ScopeError, zero
from .fields import euler_lagrange, translation_noether_residual
from .gauge import LieAlgebra, GaugeField
from .quantum import poisson_bracket, poisson_jacobi_residual
from .receipts import certify

SCHEMA = "physqed.typed-input.v1"
_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,31}$")
MAX_BYTES = 60000
MAX_NODES = 400
MAX_DEPTH = 18
KINDS = {
    "metric": ("metric_compatibility", "first_bianchi", "contracted_bianchi",
               "vacuum_einstein", "einstein_source"),
    "lagrangian": ("euler_lagrange", "translation_noether"),
    "hamiltonian": ("hamilton_equations", "poisson_jacobi"),
    "gauge": ("gauge_bianchi", "yang_mills_vacuum", "flat_connection"),
}
FIELDS = ("claim_id", "schema", "kind", "source", "assumptions", "coordinates",
          "parameters", "fields", "positions", "momenta", "metric", "stress",
          "cosmological_constant", "coupling", "lagrangian", "expected_eom",
          "hamiltonian", "expected_dq", "expected_dp", "jacobi_test",
          "algebra", "connection", "claims")


def _keys(data, allowed, required=()):
    if not isinstance(data, dict) or not set(required) <= set(data):
        raise ScopeError("missing required fields for typed physics contract")
    extras = set(data) - set(allowed)
    if extras:
        raise ScopeError("unrecognised typed physics fields: " + ",".join(sorted(map(str, extras))))


def _names(seq, *, limit=8):
    if not isinstance(seq, list) or not 1 <= len(seq) <= limit:
        raise ScopeError("expected nonempty bounded list of identifiers")
    if any(not isinstance(s, str) or not _ID.fullmatch(s) for s in seq):
        raise ScopeError("invalid identifier")
    if len(set(seq)) != len(seq):
        raise ScopeError("duplicate identifiers")
    return tuple(seq)


def _matrix(value, n, parser):
    if (not isinstance(value, list) or len(value) != n or
        any(not isinstance(row, list) or len(row) != n for row in value)):
        raise ScopeError("typed matrix shape mismatch")
    return S.Matrix([[parser.parse(cell) for cell in row] for row in value])


class RestrictedExpression:
    """Construct exact SymPy expressions from a small explicit JSON grammar."""
    def __init__(self, coordinates, parameters=(), fields=(), positions=(), momenta=()):
        names = tuple(coordinates) + tuple(parameters) + tuple(fields) + tuple(positions) + tuple(momenta)
        if len(set(names)) != len(names):
            raise ScopeError("symbol/field name collision")
        self.symbols = {
            name: S.Symbol(name, real=True)
            for name in tuple(coordinates) + tuple(parameters) + tuple(positions) + tuple(momenta)
        }
        self.coordinates = {name: self.symbols[name] for name in coordinates}
        self.fields = {
            name: S.Function(name)(*tuple(self.coordinates.values()))
            for name in fields
        }
        self.count = 0

    def parse(self, node, depth=0):
        self.count += 1
        if self.count > MAX_NODES or depth > MAX_DEPTH:
            raise ScopeError("expression size/depth limit reached")
        if type(node) is int:
            if abs(node) > 10**40:
                raise ScopeError("integer magnitude exceeded")
            return S.Integer(node)
        if type(node) is str:
            if node in self.symbols:
                return self.symbols[node]
            if node in self.fields:
                return self.fields[node]
            raise ScopeError("undeclared symbol or raw expression string")
        if not isinstance(node, dict) or len(node) != 1:
            raise ScopeError("expression must be a single-tag typed AST node")
        key, value = next(iter(node.items()))
        child = lambda obj: self.parse(obj, depth + 1)
        if key == "rational":
            if (not isinstance(value, list) or len(value) != 2 or
                any(type(v) is not int or abs(v) > 10**40 for v in value) or
                value[1] == 0):
                raise ScopeError("rational requires exact bounded integer numerator/denominator")
            return S.Rational(*value)
        if key in ("add", "mul"):
            if not isinstance(value, list) or not (2 <= len(value) <= 16):
                raise ScopeError("add/mul needs 2..16 arguments")
            args = [child(v) for v in value]
            return S.Add(*args) if key == "add" else S.Mul(*args)
        if key == "neg":
            return -child(value)
        if key == "pow":
            if (not isinstance(value, list) or len(value) != 2 or
                type(value[1]) is not int or not -8 <= value[1] <= 8):
                raise ScopeError("power requires bounded integer exponent")
            return child(value[0]) ** value[1]
        if key == "func":
            _keys(value, ("name", "arg"), ("name", "arg"))
            funcs = {"sin": S.sin, "cos": S.cos, "exp": S.exp, "sqrt": S.sqrt}
            if value["name"] not in funcs:
                raise ScopeError("unsupported function constructor")
            return funcs[value["name"]](child(value["arg"]))
        if key == "derivative":
            if (not isinstance(value, list) or len(value) not in (2,3)
                    or value[0] not in self.fields or
                    value[1] not in self.coordinates):
                raise ScopeError("derivative must name a declared field and coordinate")
            order = value[2] if len(value) == 3 else 1
            if type(order) is not int or not 1 <= order <= 4:
                raise ScopeError("field derivative order outside 1..4")
            return S.diff(self.fields[value[0]], self.coordinates[value[1]], order)
        raise ScopeError("unsupported expression AST tag: " + str(key))


@dataclass(frozen=True)
class PhysicsInput:
    claim_id: str
    kind: str
    source: str
    assumptions: tuple
    claims: tuple
    coordinates: tuple
    parameters: tuple
    raw: dict


def load_physics_input(payload: Any) -> PhysicsInput:
    """Strict typed JSON/dict loader; cannot execute source text."""
    if isinstance(payload, (str, bytes)):
        if len(payload) > MAX_BYTES:
            raise ScopeError("typed input exceeds byte limit")
        try:
            payload = json.loads(payload, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        except (ValueError, TypeError) as exc:
            raise ScopeError("invalid JSON physics input") from exc
    if not isinstance(payload, dict):
        raise ScopeError("typed input must be a JSON object")
    try:
        encoded = json.dumps(payload, allow_nan=False)
    except (ValueError, TypeError) as exc:
        raise ScopeError("not a finite JSON physics input") from exc
    if len(encoded) > MAX_BYTES:
        raise ScopeError("typed input exceeds byte limit")
    _keys(payload, FIELDS, ("schema", "claim_id", "kind", "source",
                           "assumptions", "coordinates", "claims"))
    if payload["schema"] != SCHEMA:
        raise ScopeError("unsupported typed input schema version")
    kind = payload["kind"]
    if kind not in KINDS:
        raise ScopeError("unsupported physics kind")
    if not isinstance(payload["claim_id"], str) or not _ID.fullmatch(payload["claim_id"]):
        raise ScopeError("invalid claim ID")
    if not isinstance(payload["source"], str) or not payload["source"].strip():
        raise ScopeError("explicit provenance required")
    assumptions = payload["assumptions"]
    if (not isinstance(assumptions, list) or not assumptions or
        any(not isinstance(a, str) or not a.strip() for a in assumptions)):
        raise ScopeError("nonempty assumption strings required")
    coords = _names(payload["coordinates"], limit=4)
    params = tuple() if "parameters" not in payload else _names(payload["parameters"])
    claims = payload["claims"]
    if (not isinstance(claims, list) or not claims or
        len(set(claims)) != len(claims) or any(x not in KINDS[kind] for x in claims)):
        raise ScopeError("unsupported or repeated theorem request")
    # Ensure a JSON literal strictly determines a model; refuse unknown
    # kind-specific fields instead of silently dropping them.
    common = {"schema", "claim_id", "kind", "source", "assumptions",
              "coordinates", "parameters", "claims"}
    specific = {
        "metric": {"metric", "stress", "cosmological_constant", "coupling"},
        "lagrangian": {"fields", "lagrangian", "expected_eom"},
        "hamiltonian": {"positions", "momenta", "hamiltonian",
                        "expected_dq", "expected_dp", "jacobi_test"},
        "gauge": {"algebra", "connection", "metric"},
    }
    _keys(payload, common | specific[kind])
    _names(list(coords) + list(params), limit=12)
    return PhysicsInput(payload["claim_id"], kind, payload["source"],
                        tuple(assumptions), tuple(claims), coords, params, payload)


def plan_physics_obligations(spec: PhysicsInput) -> tuple:
    """Plan obligations without interpreting them as proven physical laws."""
    if not isinstance(spec, PhysicsInput):
        raise ScopeError("typed PhysicsInput required")
    return tuple({
        "claim": c,
        "category": ("asserted_dynamics" if c in (
            "vacuum_einstein", "einstein_source", "euler_lagrange",
            "hamilton_equations", "yang_mills_vacuum", "flat_connection")
            else "structural_identity"),
        "comparison": "exact symbolic components; no global theorem",
    } for c in spec.claims)


def _obligations(spec, parser):
    x = tuple(parser.coordinates.values())
    raw = spec.raw
    kind = spec.kind
    obligations = []
    if kind == "metric":
        if "metric" not in raw:
            raise ScopeError("metric kind requires metric")
        geom = Geometry(x, _matrix(raw["metric"], len(x), parser))
        for claim in spec.claims:
            if claim == "metric_compatibility":
                relation = [(geom.covariant_derivative(
                    geom.g.tolist(), "dd", k), S.MutableDenseNDimArray.zeros(geom.n,geom.n))
                    for k in range(geom.n)]
            elif claim == "first_bianchi":
                relation = [(geom.first_bianchi_residual(), tuple(
                    S.S.Zero for _ in range(geom.n**4)))]
            elif claim == "contracted_bianchi":
                relation = [(geom.contracted_bianchi_residual(), (0,) * geom.n)]
            elif claim == "vacuum_einstein":
                relation = [(geom.einstein, S.zeros(geom.n))]
            elif claim == "einstein_source":
                if "stress" not in raw:
                    raise ScopeError("einstein_source requires supplied stress")
                stress = _matrix(raw["stress"], geom.n, parser)
                if any(not zero(stress[i,j]-stress[j,i])
                       for i in range(geom.n) for j in range(geom.n)):
                    raise ScopeError("covariant stress must be symmetric")
                coupling = parser.parse(raw.get("coupling", 1))
                cosmological = parser.parse(raw.get("cosmological_constant",0))
                relation = [(geom.einstein_residual(stress,cosmological,coupling),
                             S.zeros(geom.n))]
            else:
                raise ScopeError("internal unsupported geometry claim")
            obligations.append((claim,relation))
    elif kind == "lagrangian":
        fields = _names(raw.get("fields"), limit=8)
        if set(fields) & (set(spec.coordinates) | set(spec.parameters)):
            raise ScopeError("field/coordinate name collision")
        local = RestrictedExpression(spec.coordinates,spec.parameters,fields)
        L=local.parse(raw["lagrangian"])
        components=tuple(local.fields[name] for name in fields)
        for claim in spec.claims:
            if claim == "euler_lagrange":
                expected = raw.get("expected_eom")
                if not isinstance(expected,list) or len(expected)!=len(fields):
                    raise ScopeError("Euler-Lagrange claim needs an expected equation per field")
                target=[local.parse(a) for a in expected]
                relation=[(euler_lagrange(L,components,x), tuple(target))]
            elif claim == "translation_noether":
                # Explicit coordinate dependence yields an external force:
                # the structural identity must be checked rather than assumed.
                relation=[(translation_noether_residual(L,components,x),
                           (0,)*len(x))]
            else:
                raise ScopeError("internal unsupported field claim")
            obligations.append((claim,relation))
    elif kind == "hamiltonian":
        positions = _names(raw.get("positions"))
        momenta = _names(raw.get("momenta"))
        if len(positions)!=len(momenta):
            raise ScopeError("canonical position and momentum dimensions differ")
        local=RestrictedExpression(spec.coordinates,spec.parameters,(),positions,momenta)
        q=[local.symbols[n] for n in positions]
        p=[local.symbols[n] for n in momenta]
        H=local.parse(raw["hamiltonian"])
        for claim in spec.claims:
            if claim=="hamilton_equations":
                expectedq=raw.get("expected_dq")
                expectedp=raw.get("expected_dp")
                if not isinstance(expectedq,list) or not isinstance(expectedp,list) or (
                    len(expectedq)!=len(q) or len(expectedp)!=len(p)):
                    raise ScopeError("Hamilton claim needs expected dq/dt and dp/dt")
                eq=(tuple(poisson_bracket(v,H,q,p) for v in q) +
                    tuple(poisson_bracket(v,H,q,p) for v in p))
                target=tuple(local.parse(v) for v in expectedq+expectedp)
                relation=[(eq,target)]
            elif claim=="poisson_jacobi":
                given=raw.get("jacobi_test")
                if not isinstance(given,list) or len(given)!=3:
                    raise ScopeError("Poisson Jacobi requires three typed observables")
                f,g,h=[local.parse(v) for v in given]
                relation=[(poisson_jacobi_residual(f,g,h,q,p),0)]
            else:
                raise ScopeError("internal unsupported Hamiltonian claim")
            obligations.append((claim,relation))
    elif kind == "gauge":
        if "connection" not in raw:
            raise ScopeError("gauge kind requires Lie-valued connection")
        algebra_name=raw.get("algebra")
        constructors={"u1":LieAlgebra.u1,"so3":LieAlgebra.so3,
                      "lorentz":LieAlgebra.lorentz}
        if algebra_name not in constructors:
            raise ScopeError("unsupported Lie algebra; no arbitrary structure constants")
        lie=constructors[algebra_name]()
        connection=raw["connection"]
        if (not isinstance(connection,list) or len(connection)!=len(x) or
            any(not isinstance(v,list) or len(v)!=lie.dim for v in connection)):
            raise ScopeError("Lie-valued connection coefficient shape mismatch")
        potential=[[parser.parse(expr) for expr in v] for v in connection]
        gf=GaugeField(lie,x,potential)
        for claim in spec.claims:
            if claim=="gauge_bianchi":
                relation=[(gf.bianchi_residual(), tuple(
                    S.zeros(lie.dim,1) for _ in range(len(x)**3)))]
            elif claim=="flat_connection":
                relation=[(gf.field[a][b], S.zeros(lie.dim,1))
                          for a in range(len(x)) for b in range(a+1,len(x))]
            elif claim=="yang_mills_vacuum":
                if "metric" not in raw:
                    raise ScopeError("Yang-Mills vacuum requires explicit spacetime metric")
                metric=Geometry(x,_matrix(raw["metric"],len(x),parser))
                relation=[(gf.yang_mills_residual(metric.g),
                           tuple(S.zeros(lie.dim,1) for _ in x))]
            else:
                raise ScopeError("internal unsupported gauge claim")
            obligations.append((claim,relation))
    else:
        raise ScopeError("unsupported kind")
    return obligations


def execute_physics_input(payload: Any) -> dict:
    """Run all requested obligations and preserve result separation.

    A passing math component does not establish physical correctness,
    validity of arbitrary chart domains, quantum field theory or novelty.
    """
    spec=load_physics_input(payload)
    raw=spec.raw
    parser=RestrictedExpression(spec.coordinates,spec.parameters,
          raw.get("fields",()) if spec.kind=="lagrangian" else (),
          raw.get("positions",()) if spec.kind=="hamiltonian" else (),
          raw.get("momenta",()) if spec.kind=="hamiltonian" else ())
    obligations=_obligations(spec,parser)
    checks=[]
    for name,eqs in obligations:
        proof=certify(spec.claim_id+"_"+name,
                      {"metric":"tensor","lagrangian":"field",
                       "hamiltonian":"canonical","gauge":"gauge"}[spec.kind],
                      eqs, assumptions=spec.assumptions, source=spec.source)
        checks.append({"obligation":name,
                       "passed":proof["status"].startswith("EXACT_"),
                       "symbolic_receipt":proof})
    original=json.dumps(raw,sort_keys=True,separators=(",",":"))
    result={
        "schema":"physqed.typed-result.v1",
        "claim_id":spec.claim_id,
        "kind":spec.kind,
        "planner":plan_physics_obligations(spec),
        "checks":checks,
        "status":("PASS_SCOPED_SYMBOLIC_OBLIGATIONS__PHYSICS_UNVERIFIED"
                  if all(v["passed"] for v in checks) else
                  "REJECTED_UNSATISFIED_PHYSICS_OBLIGATION"),
        "input_sha256":hashlib.sha256(original.encode()).hexdigest(),
        "implementation_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "physical_truth_proven":False,
        "global_theorem_proven":False,
        "lean_kernel_verified":False,
        "arbitrary_expressions_supported":False,
        "independent_symbolic_backend_verified":False,
        "boundaries":"exact specified chart/finite model obligations only; no input statement becomes a law by assertion",
    }
    canon=json.dumps(result,sort_keys=True,separators=(",",":"))
    result["receipt_sha256"]=hashlib.sha256(canon.encode()).hexdigest()
    return result


def replay_physics_input(payload: Any, claimed_result: dict) -> bool:
    """Full rerun and canonical comparison to an alleged stored certificate."""
    if not isinstance(claimed_result,dict):
        return False
    actual=execute_physics_input(payload)
    return (json.dumps(actual,sort_keys=True,separators=(",",":")) ==
            json.dumps(claimed_result,sort_keys=True,separators=(",",":")))
