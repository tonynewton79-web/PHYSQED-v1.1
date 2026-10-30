"""Link a shifted Einstein--Maxwell exact field to a moving-wall Maxwell control.

Only the flat, constant-shift, zero-electromagnetic-potential reference
family is accepted. It uses the same exact source fields as the existing
18-node shifted Einstein--Maxwell model, but a *moving inertial-box*
Maxwell boundary (not the fixed-coordinate ADM constraint boundary).
No GR evolution-to-constraint boundary intertwiner is claimed.
"""
from __future__ import annotations
from hashlib import sha256
import json
import sympy as S
from .typed_input import load_physics_input,RestrictedExpression,execute_physics_input
from .maxwell_ibvp_control import verify_maxwell_shifted_boundary


def verify_linked_maxwell_positive_control(raw):
    if not isinstance(raw,dict) or raw.get("kind")!="einstein_maxwell_shift":
        raise ValueError("requires typed shifted Einstein-Maxwell source")
    if raw.get("parameters",[]) or raw.get("parameter_values",{}):
        raise ValueError("reference control has no free parameters")
    coords=raw.get("coordinates")
    if coords!=["t","x","y","z"]:
        raise ValueError("fixed reference Cartesian source coordinates required")
    parser=RestrictedExpression(coords)
    def expr(v):
        return S.simplify(parser.parse(v))
    h=raw.get("spatial_metric")
    beta=raw.get("shift")
    potential=raw.get("potential")
    if not isinstance(h,list) or len(h)!=3 or any(not isinstance(r,list) or len(r)!=3 for r in h):
        raise ValueError("regular 3x3 metric required")
    if any(expr(h[i][j])!=int(i==j) for i in range(3) for j in range(3)):
        raise ValueError("positive control requires flat unit spatial metric")
    if expr(raw.get("lapse"))!=1:
        raise ValueError("positive control requires unit lapse")
    if not isinstance(beta,list) or len(beta)!=3:
        raise ValueError("reference shift requires three components")
    b=[expr(v) for v in beta]
    if b[1:]!=[0,0] or b[0].free_symbols or b[0].is_Rational is not True:
        raise ValueError("constant x-only rational shift required")
    if not isinstance(potential,list) or len(potential)!=4 or any(expr(v)!=0 for v in potential):
        raise ValueError("Maxwell reference control requires zero potential")
    if expr(raw.get("cosmological_constant",0))!=0:
        raise ValueError("reference control requires zero cosmological constant")
    field=execute_physics_input(raw)
    shifted=field["shifted_contract"]
    field_ok=(field["status"]=="PASS_TYPED_SHIFTED_ADM__SCOPED"
              and len(shifted["nodes"])==18
              and all(n["passed"] for n in shifted["nodes"])
              and shifted["oracle_passed"])
    maxwell=verify_maxwell_shifted_boundary(str(b[0]))
    good=field_ok and maxwell["all_six_maximal_nonnegative"]
    result={"schema":"physqed.linked-Maxwell-moving-boundary.v1",
            "claim_id":field["claim_id"],
            "field_contract":field,
            "moving_wall_Maxwell_control":maxwell,
            "same_shifted_spacetime_source_used":True,
            "all_18_Einstein_Maxwell_nodes_passed":bool(field_ok),
            "Maxwell_moving_wall_energy_flux_and_Gauss_verified":
                bool(maxwell["all_six_maximal_nonnegative"]),
            "constraint_energy_boundary_from_GR_evolution_proven":False,
            "GR_and_Maxwell_boundaries_identical_spacetime_domain":False,
            "Einstein_initial_boundary_well_posedness_proven":False,
            "status":("PASS_FIELD_AND_MAXWELL_POSITIVE_CONTROL__GR_BOUNDARY_LINK_OPEN"
                      if good else "REJECTED_FIELD_OR_MAXWELL_CONTROL"),
            "source_sha256":sha256(json.dumps(raw,sort_keys=True,separators=(",",":")).encode()).hexdigest()}
    result["receipt_sha256"]=sha256(json.dumps(result,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return result


def replay_linked_maxwell_positive_control(raw,stored):
    return isinstance(stored,dict) and stored==verify_linked_maxwell_positive_control(raw)
