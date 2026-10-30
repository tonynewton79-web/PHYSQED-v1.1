"""One-model Einstein--Maxwell/ADM + domain-energy + boundary compatibility.

Strict coupling of the existing 18-node shifted-Einstein--Maxwell
contract with source-preserving domain-wide lapse/metric/energy/boundary
proofs. Boundary maximal-nonnegative rank is checked via the
characteristic inertia of the ADM constraint principal symbol.

This is an algebraic compatibility and conditional energy uniqueness
certificate for the constraint subsystem. In particular, it does NOT
prove nonlinear Einstein initial-boundary well-posedness, Lopatinski
conditions, solution existence for arbitrary data or that the
Einstein-evolution boundary conditions induce the declared constraint
trace spaces.
"""
from __future__ import annotations
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
import sympy as S

from .rational_energy import (_validate_box, _exact_zero, _rational_interval,
                              DomainScopeError)
from .typed_adm_domain import (certify_typed_adm_domain, _frame_matrix,
                               _strict_positive, parse_rational_sources)
from .typed_input import RestrictedExpression, execute_physics_input
from .variable_energy import adm_constraint_matrices

SCHEMA = "physqed.linked-adm-boundary.v1"


def _face_rank(frame, normal_variable, normal_value, face_box):
    """Prove full column rank by one exact strictly nonzero minor."""
    k=frame.cols
    if k<1 or k>frame.rows:
        return {"passed":False,"reason":"INVALID_FRAME_SIZE","minor":None}
    for rows in combinations(range(frame.rows),k):
        minor=S.together(frame.extract(list(rows),list(range(k))).det())
        minor=S.together(minor.subs(normal_variable,normal_value))
        proof=_strict_positive(minor**2,face_box,"rank_minor_squared")
        if proof["proved"]:
            return {"passed":True,"rows":list(rows),"minor":proof}
    return {"passed":False,"reason":"NO_UNIFORMLY_NONZERO_MINOR_FOUND",
            "minor":None}


def _face_inertia(coords,box,h,lapse,shift,axis,side):
    """Prove a fixed noncharacteristic wave pair and advective signs.

    A_n eigenvalues: -b_n ± N sqrt(h^ij n_i n_j), -b_n (twice).
    With N^2 h^nn-b_n^2 > 0 the pair has signs (+,-).
    Advective modes have sign opposite to b_n, or zero if b_n==0.
    """
    x=coords[axis+1]
    outward=-1 if side=="lower" else 1
    value=box[x][0 if side=="lower" else 1]
    face_box={c:box[c] for c in coords if c!=x}
    bn=S.together(outward*shift[axis]).subs(x,S.Rational(
        value.numerator,value.denominator))
    inverse=h.inv().applyfunc(S.together)
    hnn=S.together(inverse[axis,axis].subs(
        x,S.Rational(value.numerator,value.denominator)))
    N=S.together(lapse.subs(x,S.Rational(
        value.numerator,value.denominator)))
    difference=S.together(N*N*hnn-bn*bn)
    cone=_strict_positive(difference,face_box,"normal_wave_pair_gap")
    if _exact_zero(bn,tuple(face_box)):
        sign="zero"
    else:
        bound=_rational_interval(bn,face_box,"outward_shift_component")
        values=bound["bounds"]
        if values is None:
            sign="undetermined"
        elif Fraction(values["lower"])>0:
            sign="positive"
        elif Fraction(values["upper"])<0:
            sign="negative"
        else:
            sign="undetermined"
    count={"positive":1,"negative":3,"zero":3}.get(sign)
    # positive b_n: two negative transport modes -> 1 nonnegative
    # negative b_n: two positive transport modes -> 3 nonnegative
    # b_n == 0: two zero modes -> 3 nonnegative
    expected={"positive":1,"negative":3,"zero":3}.get(sign)
    return {"axis":str(x),"side":side,"outward_shift_sign":sign,
            "wave_pair_gap":cone,
            "noncharacteristic_wave_pair_proven":cone["proved"],
            "constant_boundary_inertia_proven":
                cone["proved"] and expected is not None,
            "expected_maximal_nonnegative_dimension":expected,
            "inertia_statement":
                "one positive and one negative wave speed; two advection speeds of sign -outward_beta",
            "characteristic_boundary":sign=="zero"}


def certify_linked_adm_boundary(model):
    if not isinstance(model,dict) or set(model)!={
            "schema","field_model","domain_model"} or model["schema"]!=SCHEMA:
        raise DomainScopeError("linked model requires schema, field_model and domain_model")
    fields=model["field_model"]
    domain=model["domain_model"]
    if not isinstance(fields,dict) or not isinstance(domain,dict):
        raise DomainScopeError("field and domain inputs must be typed JSON objects")
    if fields.get("kind")!="einstein_maxwell_shift":
        raise DomainScopeError("only 18-node shifted Einstein-Maxwell model supported")
    if fields.get("parameters",[]) or fields.get("parameter_values",{}):
        raise DomainScopeError("linked contract requires source-free declared parameters")
    if fields.get("coordinates")!=domain.get("coordinates"):
        raise DomainScopeError("coordinate declarations disagree")
    for key in ("spatial_metric","lapse","shift"):
        # Deliberately compare exact source ASTs, not simplified SymPy;
        # otherwise cancelled original domain poles could be hidden.
        if fields.get(key)!=domain.get(key):
            raise DomainScopeError("field and domain original source AST differs: "+key)
    # Original electromagnetic potential and constant coupling syntax also
    # carry denominator-domain restrictions, distinct from ADM geometry.
    # Capture these BEFORE the field backend may simplify a cancelled pole.
    extras=list(fields.get("potential",()))
    if len(extras)!=4:
        raise DomainScopeError("electromagnetic 4-potential is required")
    extras.extend((fields.get("cosmological_constant",0),
                   fields.get("coupling",2)))
    source=parse_rational_sources(fields["coordinates"],extras)
    coords=tuple(S.Symbol(x,real=True) for x in fields["coordinates"])
    box=_validate_box(coords,{x:domain["box"][str(x)] for x in coords})
    source_guards=[_strict_positive(g*g,box,"matter_source_guard_"+str(i))
                   for i,g in enumerate(source["guard_expressions"])]
    # Call the trusted typed source compiler for all 18 nodes, so
    # the domain certificate is not issued for an unrelated metric.
    shift=execute_physics_input(fields)
    shifted=shift["shifted_contract"]
    if len(shifted["nodes"])!=18:
        raise DomainScopeError("shifted node schema mismatch")
    domain_result=certify_typed_adm_domain(domain)
    source_ok=all(g["proved"] for g in source_guards)
    matter_evidence={"passed":source_ok,
        "guard_count":len(source_guards),
        "original_guard_ast":list(source["guard_sources"]),
        "guard_sign_checks":source_guards}
    if not domain_result["interior_domain_bounds_proven"] or not source_ok:
        return _receipt(model,shift,domain_result,None,False,matter_evidence)
    parser=RestrictedExpression(fields["coordinates"])
    h=S.Matrix([[parser.parse(v) for v in row] for row in domain["spatial_metric"]])
    N=parser.parse(domain["lapse"])
    beta=[parser.parse(v) for v in domain["shift"]]
    Sm,A,B=adm_constraint_matrices(coords,h,N,beta)
    boundary=domain_result["boundary_flux"]
    if domain["boundary_mode"]!="trace_subspaces_assumed":
        # Purely assumed periodic boundary traces are not a verified
        # frame-by-frame maximal nonnegative compatibility result.
        return _receipt(model,shift,domain_result,{"passed":False,
             "reason":"BOUNDARY_FRAME_COMPATIBILITY_NOT_REQUESTED"},False,matter_evidence)
    faces=[]
    all_compatible=True
    for axis in range(3):
        x=coords[axis+1]
        for side in ("lower","upper"):
            inertia=_face_inertia(coords,box,h,N,beta,axis,side)
            name=f"{x}_{side}"
            face_box={c:box[c] for c in coords if c!=x}
            value=box[x][0 if side=="lower" else 1]
            frame,_=_frame_matrix(domain["boundary_frames"][name],parser,4)
            rank=_face_rank(frame,x,S.Rational(value.numerator,value.denominator),
                            face_box)
            expected=inertia["expected_maximal_nonnegative_dimension"]
            size_ok=(expected is not None and frame.cols==expected)
            flux=next((f for f in boundary.get("faces",())
                       if f.get("name")==name),None)
            flux_ok=flux is not None and flux.get("passed") is True
            compatible=(inertia["constant_boundary_inertia_proven"]
                        and rank["passed"] and size_ok and flux_ok)
            faces.append({"name":name,"passed":bool(compatible),
                          "inertia":inertia,"frame_columns":frame.cols,
                          "expected_maximal_dimension":expected,
                          "dimension_matched":size_ok,
                          "rank_certificate":rank,"flux_positive_semidefinite":flux_ok})
            all_compatible=all_compatible and compatible
    return _receipt(model,shift,domain_result,{
        "passed":bool(all_compatible),"faces":faces,
        "all_six_face_inertias_verified":all(
            f["inertia"]["constant_boundary_inertia_proven"] for f in faces),
        "all_six_maximal_nonnegative_subspaces_verified":all_compatible,
        "compatibility_scope":"pointwise maximal nonnegative boundary subspaces of homogeneous constraint principal system; NOT nonlinear Einstein-IBVP compatibility",
        "nonlinear_Einstein_boundary_conditions_verified":False,
        "strong_Lopatinski_condition_verified":False,
        "corner_compatibility_verified":False,
        "smooth_constraint_solution_existence_verified":False}, all_compatible,matter_evidence)


def _receipt(model,shift,domain,compatibility,ok,matter_evidence):
    nodes=shift["shifted_contract"]["nodes"]
    required={
       "normal_unit","normal_orthogonal","maxwell_bianchi",
       "maxwell_equations","matter_conservation","einstein_full",
       "spatial_einstein_evolution","trace_reversed_spatial_evolution",
       "hamilton_constraint","momentum_constraint",
       "gauss_hamiltonian_bridge","codazzi_momentum_bridge",
       "einstein_stress_bianchi_bridge","hamiltonian_propagation_bridge",
       "momentum_propagation_bridge",
       "hamiltonian_hyperbolic_propagation_bridge",
       "momentum_hyperbolic_propagation_bridge",
       "principal_symbol_symmetrizer"}
    field_ok=(len(nodes)==18 and set(v["name"] for v in nodes)==required
              and all(v["passed"] for v in nodes)
              and shift["shifted_contract"]["oracle_passed"]
              and shift["shifted_contract"]["trace_reversed_hyperbolic_constraint_closure_passed"])
    interior_ok=bool(domain.get("interior_domain_bounds_proven"))
    boundary_ok=bool(domain.get("conditional_boundary_flux_algebra_proven"))
    full=field_ok and interior_ok and boundary_ok and ok and matter_evidence["passed"]
    result={"schema":"physqed.linked-adm-boundary-result.v1",
        "field_model_claim_id":shift["claim_id"],
        "field_contract":shift,
        "domain_contract":domain,
        "matter_source_domain":matter_evidence,
        "compatibility":compatibility,
        "all_18_field_nodes_passed":bool(field_ok),
        "uniform_interior_energy_bounds_passed":interior_ok,
        "all_face_flux_forms_passed":boundary_ok,
        "maximal_nonnegative_constraint_trace_spaces_passed":bool(ok),
        "status":("PASS_LINKED_EXACT_MODEL_AND_CONDITIONAL_CONSTRAINT_ENERGY"
                  if full else "REJECTED_OR_INCONCLUSIVE_LINKED_OBLIGATIONS"),
        "conditional_energy_statement":
            "For any existing smooth homogeneous constraint solution on the specified box satisfying its declared trace subspaces and corner compatibility: E(t)<=exp(C*(t-t0))*E(t0)",
        "smooth_constraint_solution_existence_proven":False,
        "nonlinear_Einstein_IBVP_well_posedness_proven":False,
        "corner_compatibility_proven":False,
        "global_Einstein_existence_proven":False,
        "claim_limit":"Exact supplied spacetime Einstein-Maxwell checks and conditional constraint-system energy; not an existence or full boundary-value theorem",
        "input_sha256":sha256(json.dumps(model,sort_keys=True,
                                    separators=(",",":")).encode()).hexdigest()}
    result["receipt_sha256"]=sha256(json.dumps(result,sort_keys=True,
                                  separators=(",",":")).encode()).hexdigest()
    return result


def replay_linked_adm_boundary(model,stored):
    return isinstance(stored,dict) and stored==certify_linked_adm_boundary(model)
