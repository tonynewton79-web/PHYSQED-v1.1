"""Source-preserving rational AST and finite-box ADM geometry/flux proof gates.

No eval/exec or text-to-SymPy parsing: accept only typed JSON AST via
RestrictedExpression. Every negative-power operand is captured *before*
SymPy cancellation and audited as a nonvanishing denominator guard.
The finite-box matrix and flux tests use the existing exact
Bernstein/Gershgorin rational domain verifier.

A pass proves only the explicitly tested local coefficient, lapse,
spatial SPD and boundary-quadratic inequalities over the box.
It never proves that a PDE solution satisfies the asserted boundary
trace conditions, nor that nonlinear Einstein evolution exists.
"""
from __future__ import annotations
import json
from hashlib import sha256
from fractions import Fraction
from itertools import product
from pathlib import Path
import sympy as S
from .typed_input import RestrictedExpression
from .rational_energy import (
    certify_rational_domain_energy, _rational_interval,
    _gershgorin_from_bounds, _rational_parts, _exact_zero,
    DomainScopeError, _validate_box)
from .domain_energy import _rat
from .variable_energy import adm_constraint_matrices

SCHEMA = "physqed.typed-adm-domain.v1"


def _check_ast(node, parser, source, guards, depth=0):
    """Visit the source first; do NOT lose cancelled negative powers."""
    if depth>18:
        raise DomainScopeError("expression AST exceeds depth cap")
    if type(node) is int or type(node) is str:
        return
    if not isinstance(node,dict) or len(node)!=1:
        raise DomainScopeError("source must be restricted JSON expression AST")
    key,value=next(iter(node.items()))
    if key=="rational":
        if (not isinstance(value,list) or len(value)!=2
            or any(type(v) is not int for v in value) or value[1]==0):
            raise DomainScopeError("invalid exact rational literal")
        return
    if key in ("add","mul"):
        if not isinstance(value,list) or not 2<=len(value)<=16:
            raise DomainScopeError("invalid sum/product arity")
        for v in value:
            _check_ast(v,parser,source,guards,depth+1)
        return
    if key=="neg":
        _check_ast(value,parser,source,guards,depth+1)
        return
    if key=="pow":
        if (not isinstance(value,list) or len(value)!=2 or
            type(value[1]) is not int or not -8<=value[1]<=8):
            raise DomainScopeError("power must have a bounded integer exponent")
        base=value[0]
        _check_ast(base,parser,source,guards,depth+1)
        if value[1]<0:
            # Capture exact operand before evaluating the full expression.
            expression=parser.parse(base)
            guards.append({"source":json.dumps(base,sort_keys=True,
                                               separators=(",",":")),
                           "expression":expression,
                           "exponent":value[1]})
        return
    # Rational proof mode deliberately refuses sqrt, sin, exp,
    # derivatives or constants whose domain/branch is not handled.
    raise DomainScopeError("unsupported rational source AST node: "+str(key))


def parse_rational_sources(coordinates,expressions,parameters=()):
    """Return exact SymPy values and source-denominator provenance.

    expressions is a flat list of JSON AST nodes. A source-free
    computed SymPy coefficient never receives this provenance flag.
    """
    if not isinstance(expressions,list) or len(expressions)>90:
        raise DomainScopeError("1..90 typed rational source expressions required")
    parser=RestrictedExpression(coordinates,parameters)
    values=[]
    guards=[]
    for i,tree in enumerate(expressions):
        _check_ast(tree,parser,str(i),guards)
        expr=parser.parse(tree)
        _rational_parts(expr,tuple(parser.coordinates.values()))
        values.append(expr)
    if len(guards)>50:
        raise DomainScopeError("too many source-level denominators")
    return {"values":tuple(values),
            "guard_expressions":tuple(v["expression"] for v in guards),
            "guard_sources":tuple(v["source"] for v in guards),
            "guard_exponents":tuple(v["exponent"] for v in guards),
            "provenance_complete_for_supplied_AST":True}


def _strict_positive(expr,box,label):
    r=_rational_interval(expr,box,label)
    bounds=r["bounds"]
    return {"name":label,"denominator_certified":
            r["denominator_nonzero_certified"],
            "lower":bounds["lower"] if bounds else None,
            "upper":bounds["upper"] if bounds else None,
            "proved":bounds is not None and Fraction(bounds["lower"])>0,
            "proof":r}


def _certify_geometry_cell(box,N,h,lap_floor,metric_floor):
    tests=[]
    tests.append(_strict_positive(N-S.Rational(lap_floor.numerator,lap_floor.denominator),
                                  box,"lapse_minus_floor_strict"))
    for k in (1,2,3):
        minor=S.together(h[:k,:k].det())
        tests.append(_strict_positive(minor,box,f"h_leading_minor_{k}"))
    # The strict Sylvester inequalities establish h positive on box.
    # A requested numerical floor h>=mu I is proved separately by a
    # non-strict Gershgorin inequality.
    margin=_gershgorin_from_bounds(
        h-S.eye(3)*S.Rational(metric_floor.numerator,metric_floor.denominator),
        box,Fraction(0),"metric_uniform_floor")
    regular=all(t["proved"] for t in tests)
    return {"lapse_and_sylvester_tests":tests,"metric_floor":margin,
            "passed":regular and margin["passed"]}


def _face_box(box,spatial,k,side):
    x=spatial[k]
    value=box[x][0 if side=="lower" else 1]
    return {coord:box[coord] for coord in box if coord!=x},x,value


def _frame_matrix(raw,parser,n):
    if not isinstance(raw,list) or not raw or len(raw)>n:
        raise DomainScopeError("boundary trace frame needs 1..n columns")
    if any(not isinstance(col,list) or len(col)!=n for col in raw):
        raise DomainScopeError("boundary trace frame columns must have state dimension")
    values=[]
    guards=[]
    for col in raw:
        result=parse_rational_sources(tuple(parser.coordinates),col)
        values.append(result["values"])
        guards.extend(result["guard_expressions"])
    return S.Matrix.hstack(*(S.Matrix(col) for col in values)),tuple(guards)


def _boundary_cell(box,coords,s,A,mode,frames,parser):
    """Certify nonnegative outward flux on every declared trace subspace."""
    if mode=="unverified":
        return {"passed":False,"reason":"BOUNDARY_NOT_DECLARED",
                "trace_condition_verified_on_actual_solution":False,
                "faces":[]}
    if mode=="periodic_assumed":
        faces=[]
        for i in range(3):
            _,x,lo=_face_box(box,coords[1:],i,"lower")
            _,_,hi=_face_box(box,coords[1:],i,"upper")
            equal=all(_exact_zero(S.together(v.subs(x,lo)-v.subs(x,hi)),
                tuple(vv for vv in coords if vv!=x))
                for m in [s]+A for v in m)
            faces.append({"axis":str(x),"coefficient_faces_match":bool(equal)})
        ok=all(f["coefficient_faces_match"] for f in faces)
        return {"passed":ok,"reason":("PERIODIC_COEFFICIENT_FACES_MATCH"
                  if ok else "PERIODIC_COEFFICIENT_MISMATCH"),
                "trace_condition_verified_on_actual_solution":False,
                "faces":faces}
    if mode!="trace_subspaces_assumed":
        raise DomainScopeError("boundary mode unsupported")
    if not isinstance(frames,dict) or set(frames)!={
            f"{coords[k+1]}_{side}" for k in range(3) for side in ("lower","upper")}:
        raise DomainScopeError("supply one trace subspace for every spatial face")
    faces=[]
    ok=True
    for k in range(3):
        for side in ("lower","upper"):
            remaining,x,value=_face_box(box,coords[1:],k,side)
            key=f"{x}_{side}"
            frame,guards=_frame_matrix(frames[key],parser,s.rows)
            sign=-1 if side=="lower" else 1
            normal=(sign*(s*A[k])).applyfunc(S.together)
            restricted=(frame.T*normal*frame).applyfunc(S.together)
            if any(not _exact_zero(v,tuple(coords)) for v in restricted-restricted.T):
                raise DomainScopeError("flux matrix is not symmetric")
            # Source frame denominator signs and nonzero requirements
            source_guards=[_strict_positive(S.together(g.subs(x,S.Rational(
                       value.numerator,value.denominator)))**2,remaining,
                      f"{key}_source_guard_{j}") for j,g in enumerate(guards)]
            bounded=_gershgorin_from_bounds(
                restricted.subs(x,S.Rational(value.numerator,value.denominator)),
                remaining,Fraction(0),key+"_outward_flux")
            good=bounded["passed"] and all(t["proved"] for t in source_guards)
            faces.append({"name":key,"passed":good,
                          "flux":bounded,"source_guards":source_guards,
                          "trace_basis_columns":frame.cols})
            ok=ok and good
    return {"passed":ok,"reason":("ALL_FACE_TRACE_FLUX_NONNEGATIVE"
                if ok else "ONE_OR_MORE_FACE_FLUXES_INCONCLUSIVE"),
            "trace_condition_verified_on_actual_solution":False,
            "faces":faces}


def certify_typed_adm_domain(model):
    """Certify source AST, lapse, 3-metric, energy and boundary flux.

    The boundary-subspace condition and any field solution remain caller
    assumptions. Result contains exact matrix/box evidence, no PDE theorem.
    """
    if not isinstance(model,dict) or set(model)!={
         "schema","coordinates","box","spatial_metric","lapse","shift",
         "lapse_floor","metric_floor","energy_coercivity","energy_growth",
         "boundary_mode","boundary_frames"}:
        raise DomainScopeError("unexpected/missing typed ADM-domain fields")
    if model["schema"]!=SCHEMA:
        raise DomainScopeError("typed ADM domain schema mismatch")
    names=model["coordinates"]
    if (not isinstance(names,list) or len(names)!=4 or
            any(not isinstance(n,str) for n in names) or len(set(names))!=4):
        raise DomainScopeError("four distinct typed coordinate names required")
    hraw=model["spatial_metric"]
    if not isinstance(hraw,list) or len(hraw)!=3 or any(
            not isinstance(row,list) or len(row)!=3 for row in hraw):
        raise DomainScopeError("spatial metric requires a 3x3 source AST")
    if not isinstance(model["shift"],list) or len(model["shift"])!=3:
        raise DomainScopeError("shift requires three source AST components")
    raw=[node for row in hraw for node in row]+[model["lapse"]]+model["shift"]
    parsed=parse_rational_sources(names,raw)
    values=parsed["values"]
    h=S.Matrix(3,3,lambda i,j:values[i*3+j])
    N=values[9];beta=values[10:13]
    coords=tuple(S.Symbol(name,real=True) for name in names)
    boxraw=model["box"]
    if not isinstance(boxraw,dict) or set(boxraw)!=set(names):
        raise DomainScopeError("box must give all coordinate names")
    box=_validate_box(coords,{x:boxraw[str(x)] for x in coords})
    nfloor=_rat(model["lapse_floor"])
    hfloor=_rat(model["metric_floor"])
    energy_floor=_rat(model["energy_coercivity"])
    growth=_rat(model["energy_growth"])
    if min(nfloor,hfloor,energy_floor)<=0 or growth<0:
        raise DomainScopeError("positive geometric and energy floors required")
    if any(not _exact_zero(v,coords) for v in h-h.T):
        raise DomainScopeError("spatial metric not symmetric")
    # Short precheck of source denominator nonvanishing on whole box.
    guards=[]
    for idx,g in enumerate(parsed["guard_expressions"]):
        cert=_strict_positive(g*g,box,f"source_denominator_squared_{idx}")
        guards.append(cert)
    guards_ok=all(v["proved"] for v in guards)
    geo=_certify_geometry_cell(box,N,h,nfloor,hfloor)
    energy={"status":"NOT_EXECUTED_UNSAFE_GEOMETRY_OR_GUARDS"}
    boundary={"passed":False,"reason":"NOT_EXECUTED"}
    if guards_ok and geo["passed"]:
        Senergy,A,B=adm_constraint_matrices(coords,h,N,beta)
        energy=certify_rational_domain_energy(
            coords,box,Senergy,A,B,
            coercivity=energy_floor,growth=growth,
            denominator_guards=parsed["guard_expressions"],
            original_expression_denominators_complete=True)
        parser=RestrictedExpression(names)
        boundary=_boundary_cell(box,coords,Senergy,A,
            model["boundary_mode"],model["boundary_frames"],parser)
    interior=guards_ok and geo["passed"] and energy.get("interior_coercivity_proven",False) and energy.get("interior_growth_proven",False)
    result={
        "schema":"physqed.typed-adm-domain-result.v1",
        "input_sha256":sha256(json.dumps(model,sort_keys=True,
             separators=(",",":")).encode()).hexdigest(),
        "source_guards_extracted_before_simplification":
             parsed["provenance_complete_for_supplied_AST"],
        "source_guard_count":len(guards),
        "source_guard_original_ast":list(parsed["guard_sources"]),
        "source_guard_exponents":list(parsed["guard_exponents"]),
        "source_guard_sign_evidence":guards,
        "all_source_guards_certified":guards_ok,
        "geometric_bounds":geo,
        "constraint_energy_bounds":energy,
        "boundary_flux":boundary,
        "interior_domain_bounds_proven":bool(interior),
        "conditional_boundary_flux_algebra_proven":bool(boundary["passed"]),
        "boundary_trace_conditions_satisfied_by_solution_proven":False,
        "evolution_solution_existence_proven":False,
        "global_constraint_propagation_theorem_proven":False,
        "status":("PASS_INTERIOR_AND_CONDITIONAL_BOUNDARY_ALGEBRA__PDE_ASSUMPTIONS_PENDING"
                  if interior and boundary["passed"] else
                  "INCONCLUSIVE_OR_UNVERIFIED_DOMAIN_OBLIGATIONS"),
        "backend_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
        "limitations":"exact rational 4D box, restricted AST, source guards; finite matrix inequalities. No field/boundary/PDE existence proof."
    }
    result["receipt_sha256"]=sha256(json.dumps(result,sort_keys=True,
         separators=(",",":")).encode()).hexdigest()
    return result


def replay_typed_adm_domain(model,stored):
    return isinstance(stored,dict) and stored==certify_typed_adm_domain(model)
