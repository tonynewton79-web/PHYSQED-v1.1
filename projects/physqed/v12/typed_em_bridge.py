"""Bridge safe typed JSON inputs to the established 16-node Einstein--Maxwell/ADM contract.

The compiler checks length dimensions and declared tensor index variance
*before* any curved-spacetime derivative is evaluated. It then constructs
one EinsteinMaxwellSpec, runs all linked obligations and independent
four-/three-dimensional rational 2-jet curvature comparisons, and returns
one deterministic scoped receipt. It cannot prove the caller's domain
assumptions, action normalization or an unrestricted physical theory.
"""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
import json
import sympy as S
from .geometry import ScopeError
from .contracts import EinsteinMaxwellSpec, evaluate_contract
from .physical_types import GeometrizedDimensions, check_tensor_signatures
from .typed_input import RestrictedExpression

LINKED_NODE_NAMES = (
    "normal_unit",
    "field_potential_consistency",
    "maxwell_stress_constitutive",
    "electromagnetic_bianchi",
    "maxwell_euler_lagrange",
    "matter_noether_divergence",
    "stress_conservation",
    "einstein_field_equation",
    "einstein_contracted_bianchi",
    "einstein_stress_divergence_bridge",
    "hamiltonian_constraint",
    "momentum_constraints",
    "hamiltonian_gauss_bridge",
    "momentum_codazzi_bridge",
    "claimed_hamiltonian_agreement",
    "claimed_momentum_agreement",
)


def _required(data):
    fields=("metric", "potential", "lapse", "units", "tensor_types",
            "witnesses", "parameter_values")
    missing=[k for k in fields if k not in data]
    if missing:
        raise ScopeError("typed Einstein-Maxwell missing required: "+", ".join(missing))
    if len(data["coordinates"])!=4:
        raise ScopeError("Einstein-Maxwell/ADM requires four coordinates")
    if data["claims"] != ["linked_einstein_maxwell_adm"]:
        raise ScopeError("Einstein-Maxwell bridge requires one exact linked claim")


def _square(raw, dim, compiler):
    if (not isinstance(raw,list) or len(raw)!=dim or
        any(not isinstance(row,list) or len(row)!=dim for row in raw)):
        raise ScopeError("declared four-dimensional tensor must be a 4x4 array")
    return S.Matrix([[compiler.parse(v) for v in row] for row in raw])


def _array(raw, dim, compiler):
    if not isinstance(raw,list) or len(raw)!=dim:
        raise ScopeError("one-form or constraint array must match its declared rank")
    return tuple(compiler.parse(v) for v in raw)


def _numeric_parameter_values(params, values, compiler):
    if not isinstance(values,dict) or set(values)!=set(params):
        raise ScopeError("each declared physical parameter needs one exact value")
    subs={}
    for name in params:
        parsed=compiler.parse(values[name])
        if parsed.free_symbols or parsed.is_Rational is not True:
            raise ScopeError("Einstein-Maxwell parameter values must be exact rational")
        subs[compiler.symbols[name]]=parsed
    return subs


def _witnesses(raw, coordinates, compiler, substitutions):
    if not isinstance(raw,list) or not 1<=len(raw)<=4:
        raise ScopeError("1..4 curvature witnesses required")
    result=[]
    for item in raw:
        if not isinstance(item,dict) or set(item)!=set(coordinates):
            raise ScopeError("witness must provide every declared coordinate")
        entry={}
        for name in coordinates:
            expression=S.simplify(compiler.parse(item[name]).subs(substitutions))
            if expression.free_symbols or expression.is_real is not True:
                raise ScopeError("curvature witness must be exact real, without free symbols")
            entry[compiler.coordinates[name]]=expression
        result.append(entry)
    return tuple(result)


def _optional_matrix(raw, key, units, kind, compiler, substitutions):
    if key not in raw:
        return None, []
    tests=units.matrix(raw[key],kind)
    return _square(raw[key],4,compiler).subs(substitutions),tests


def run_typed_einstein_maxwell(spec):
    """Execute the linked 16-node contract from a user-declared typed model."""
    if getattr(spec,"kind",None)!="einstein_maxwell":
        raise ScopeError("expected typed Einstein-Maxwell input kind")
    raw=spec.raw
    _required(raw)
    # The only physics-unit system supported here is geometrized length.
    units=GeometrizedDimensions(spec.coordinates,spec.parameters,raw["units"])
    indices=check_tensor_signatures(raw["tensor_types"])
    dim_checks=units.matrix(raw["metric"],"metric")
    dim_checks.extend(units.one_form(raw["potential"]))
    dim_checks.append(units.check_lapse(raw["lapse"]))
    cosmological=raw.get("cosmological_constant",0)
    coupling=raw.get("coupling",2)
    dim_checks.append(units.check_cosmological(cosmological))
    dim_checks.append(units.check_coupling(coupling))

    # Safe parser never invokes eval, Python source, arbitrary sympify text,
    # undeclared functions or uncontrolled expression macros.
    compiler=RestrictedExpression(spec.coordinates,spec.parameters)
    substitutions=_numeric_parameter_values(
        spec.parameters,raw["parameter_values"],compiler)
    coords=tuple(compiler.coordinates[name] for name in spec.coordinates)
    metric=_square(raw["metric"],4,compiler).subs(substitutions)
    potential=tuple(expr.subs(substitutions) for expr in
                    _array(raw["potential"],4,compiler))
    lapse=S.simplify(compiler.parse(raw["lapse"]).subs(substitutions))
    declared_stress,stress_checks=_optional_matrix(
        raw,"declared_stress",units,"stress",compiler,substitutions)
    declared_F,F_checks=_optional_matrix(
        raw,"declared_field_strength",units,"field_strength",compiler,substitutions)
    dim_checks.extend(stress_checks)
    dim_checks.extend(F_checks)
    declared_H=None
    declared_M=None
    if "declared_hamiltonian" in raw:
        dim_checks.append(units.require(raw["declared_hamiltonian"],
                                        -2,"declared_hamiltonian"))
        declared_H=S.simplify(compiler.parse(raw["declared_hamiltonian"]).subs(substitutions))
    if "declared_momentum" in raw:
        m=raw["declared_momentum"]
        if not isinstance(m,list) or len(m)!=3:
            raise ScopeError("ADM declared momentum has exactly three components")
        for i,item in enumerate(m):
            required=-1-units.coord[spec.coordinates[i+1]]
            dim_checks.append(units.require(item, required,
                                            f"declared_momentum[{i}]"))
        declared_M=tuple(S.simplify(a.subs(substitutions))
                         for a in _array(m,3,compiler))
    witnesses=_witnesses(raw,spec.coordinates,compiler,substitutions)
    contract=EinsteinMaxwellSpec(
        claim_id=spec.claim_id,coordinates=coords,metric=metric,
        potential=potential,lapse=lapse,witnesses=witnesses,
        assumptions=spec.assumptions,
        source=spec.source,
        cosmological_constant=S.simplify(
            compiler.parse(cosmological).subs(substitutions)),
        gravitational_coupling=S.simplify(
            compiler.parse(coupling).subs(substitutions)),
        declared_stress=declared_stress,
        declared_field_strength=declared_F,
        declared_hamiltonian=declared_H,
        declared_momentum=declared_M,
    )
    result=evaluate_contract(contract)
    names=tuple(v["name"] for v in result["nodes"])
    if names != LINKED_NODE_NAMES:
        raise ScopeError("the coupled backend contract-node version has changed")
    passed=(result["status"]=="PASS_LOCAL_TYPED_COUPLED_SYMBOLIC_CONTRACT"
            and len(dim_checks)>0 and len(indices)==5)
    model=json.dumps(raw,sort_keys=True,separators=(",",":"))
    receipt={
        "schema":"physqed.typed-einstein-maxwell-result.v1",
        "claim_id":spec.claim_id,
        "kind":"einstein_maxwell",
        "input_sha256":sha256(model.encode()).hexdigest(),
        "implementation_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
        "physical_type_sha256":sha256(
            Path(__file__).with_name("physical_types.py").read_bytes()).hexdigest(),
        "dimension_system":"geometrized_length",
        "physical_dimension_checks":dim_checks,
        "tensor_index_signature_checks":indices,
        "linked_obligations":list(LINKED_NODE_NAMES),
        "coupled_contract":result,
        "status":("PASS_TYPED_EINSTEIN_MAXWELL_ADM__SCOPED"
                  if passed else "REJECTED_LINKED_PHYSICS_OBLIGATIONS"),
        "physical_truth_proven":False,
        "global_theorem_proven":False,
        "lean_kernel_verified":False,
        "domain_assumptions_proven":False,
        "full_SI_units_supported":False,
        "arbitrary_index_contractions_supported":False,
        "independent_symbolic_proof":False,
        "note":"16-node chart-local symbolic comparison with separately computed rational 2-jet curvature at declared points",
    }
    canon=json.dumps(receipt,sort_keys=True,separators=(",",":"))
    receipt["receipt_sha256"]=sha256(canon.encode()).hexdigest()
    return receipt
