"""Connect safe JSON units/index types to shifted ADM propagation verification.

Scope: 4D Einstein--Maxwell, geometrized length dimensions, positive
lapse/spatial metric at exact witnesses. Does not prove global existence
or uniqueness of the Einstein Cauchy problem.
"""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
import json
import sympy as S
from .geometry import ScopeError
from .physical_types import GeometrizedDimensions,check_tensor_signatures
from .typed_input import RestrictedExpression
from .typed_em_bridge import _numeric_parameter_values,_witnesses
from .adm_shift import ShiftedEinsteinMaxwellSpec,evaluate_shifted_einstein_maxwell

SHIFTED_NODE_NAMES=(
    "normal_unit","normal_orthogonal",
    "maxwell_bianchi","maxwell_equations","matter_conservation",
    "einstein_full","spatial_einstein_evolution",
    "trace_reversed_spatial_evolution",
    "hamilton_constraint","momentum_constraint",
    "gauss_hamiltonian_bridge","codazzi_momentum_bridge",
    "einstein_stress_bianchi_bridge",
    "hamiltonian_propagation_bridge","momentum_propagation_bridge",
    "hamiltonian_hyperbolic_propagation_bridge",
    "momentum_hyperbolic_propagation_bridge",
    "principal_symbol_symmetrizer",
)


def _check_shift_type(value):
    if (not isinstance(value,dict) or set(value)!={"variance","rank"}
            or value["variance"]!="u" or type(value["rank"]) is not int
            or value["rank"]!=1):
        raise ScopeError("shift is a contravariant spatial rank-one vector")
    return {"name":"shift","variance":"u","rank":1,"passed":True}


def run_typed_shifted_adm(spec):
    if getattr(spec,"kind",None)!="einstein_maxwell_shift":
        raise ScopeError("typed Einstein-Maxwell shift model required")
    raw=spec.raw
    required=("spatial_metric","potential","lapse","shift","shift_type",
              "units","tensor_types","witnesses","parameter_values")
    if any(key not in raw for key in required):
        raise ScopeError("typed shifted ADM input missing required data")
    if len(spec.coordinates)!=4 or spec.claims!=("linked_shifted_adm_propagation",):
        raise ScopeError("shifted Einstein-Maxwell requires four coordinates and one linked claim")
    units=GeometrizedDimensions(spec.coordinates,spec.parameters,raw["units"])
    types=check_tensor_signatures(raw["tensor_types"])
    types.append(_check_shift_type(raw["shift_type"]))
    h=raw["spatial_metric"]
    if (not isinstance(h,list) or len(h)!=3 or
        any(not isinstance(row,list) or len(row)!=3 for row in h)):
        raise ScopeError("shifted ADM requires a 3x3 spatial metric")
    if not isinstance(raw["shift"],list) or len(raw["shift"])!=3:
        raise ScopeError("spatial shift requires three components")
    checks=[]
    for i in range(3):
        for j in range(3):
            d=2-units.coord[spec.coordinates[i+1]]-units.coord[spec.coordinates[j+1]]
            checks.append(units.require(h[i][j],d,f"spatial_metric[{i},{j}]"))
    for i in range(3):
        d=units.coord[spec.coordinates[i+1]]-units.coord[spec.coordinates[0]]
        checks.append(units.require(raw["shift"][i],d,f"shift_contravariant[{i}]"))
    checks.extend(units.one_form(raw["potential"]))
    checks.append(units.check_lapse(raw["lapse"]))
    cosmological=raw.get("cosmological_constant",0)
    kappa=raw.get("coupling",2)
    checks.append(units.check_cosmological(cosmological))
    checks.append(units.check_coupling(kappa))

    compiler=RestrictedExpression(spec.coordinates,spec.parameters)
    subs=_numeric_parameter_values(spec.parameters,raw["parameter_values"],compiler)
    def expr(v):
        return S.simplify(compiler.parse(v).subs(subs))
    coords=tuple(compiler.coordinates[a] for a in spec.coordinates)
    hg=S.Matrix([[expr(h[i][j]) for j in range(3)] for i in range(3)])
    beta=tuple(expr(v) for v in raw["shift"])
    A=tuple(expr(v) for v in raw["potential"])
    N=expr(raw["lapse"])
    witnesses=_witnesses(raw["witnesses"],spec.coordinates,compiler,subs)

    model=ShiftedEinsteinMaxwellSpec(
        claim_id=spec.claim_id,coordinates=coords,spatial_metric=hg,
        lapse=N,shift=beta,potential=A,witnesses=witnesses,
        assumptions=spec.assumptions,source=spec.source,
        cosmological_constant=expr(cosmological),
        gravitational_coupling=expr(kappa),
    )
    linked=evaluate_shifted_einstein_maxwell(model)
    actual=tuple(v["name"] for v in linked["nodes"])
    if actual!=SHIFTED_NODE_NAMES:
        raise ScopeError("shifted ADM backend node contract changed")
    accepted=linked["status"]=="PASS_SCOPED_SHIFTED_EINSTEIN_MAXWELL"
    original=json.dumps(raw,sort_keys=True,separators=(",",":"))
    result={
        "schema":"physqed.typed-shifted-adm.v1",
        "claim_id":spec.claim_id,"kind":spec.kind,
        "input_sha256":sha256(original.encode()).hexdigest(),
        "implementation_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
        "physical_unit_system":"geometrized_length",
        "unit_component_checks":checks,
        "index_type_checks":types,
        "linked_obligations":list(SHIFTED_NODE_NAMES),
        "shifted_contract":linked,
        "status":("PASS_TYPED_SHIFTED_ADM__SCOPED" if accepted
                  else "REJECTED_TYPED_SHIFTED_ADM"),
        "global_constraint_propagation_theorem_proven":False,
        "pde_well_posedness_proven":False,
        "physical_model_proven":False,
        "domain_assumptions_proven":False,
        "full_SI_units_supported":False,
        "note":"off-shell Bianchi propagation identities; no global PDE solution/uniqueness proof",
    }
    payload=json.dumps(result,sort_keys=True,separators=(",",":"))
    result["receipt_sha256"]=sha256(payload.encode()).hexdigest()
    return result
