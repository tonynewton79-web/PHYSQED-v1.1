"""Scoped computational backends for the PHYSQED research problem router.

All untrusted symbolic values are parsed by v1.2 RestrictedExpression.
Distinct mathematics/physics scopes are never silently interchangeable.
"""
from __future__ import annotations

import re
from fractions import Fraction as Q
import sympy as S

from v12.geometry import Geometry, ScopeError, zero
from v12.typed_input import RestrictedExpression, execute_physics_input, replay_physics_input
from v12.fields import euler_lagrange, translation_noether_residual
from v12.quantum import commutator, is_hermitian, poisson_bracket
from .exact import (PolynomialScope, coefficient_difference, rational_counterexample,
                    polynomial_signature, compare_units)


def _names(value, lower=1, upper=8):
    if (not isinstance(value, list) or not lower <= len(value) <= upper or
        len(set(map(str, value))) != len(value) or
        any(not isinstance(s, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,30}", s)
            for s in value)):
        raise ScopeError("invalid or repeated bounded symbolic identifier")
    return tuple(value)


def _expression(parser, node):
    return parser.parse(node)


def _matrix(rows, parser, bound=4):
    if (not isinstance(rows, list) or not 1 <= len(rows) <= bound or
        any(not isinstance(row,list) or len(row)!=len(rows) for row in rows)):
        raise ScopeError("bounded square matrix required")
    return S.Matrix([[_expression(parser,item) for item in row] for row in rows])


def _to_text(expr):
    if isinstance(expr, S.MatrixBase):
        return [[S.sstr(v) for v in row] for row in expr.tolist()]
    if isinstance(expr, (tuple, list)):
        return [_to_text(x) for x in expr]
    return S.sstr(expr)


def _eq(a,b):
    if isinstance(a,S.MatrixBase) or isinstance(b,S.MatrixBase):
        x, y = S.Matrix(a), S.Matrix(b)
        return x.shape==y.shape and all(zero(e) for e in x-y)
    if isinstance(a,(tuple,list)) and isinstance(b,(tuple,list)):
        return len(a)==len(b) and all(_eq(x,y) for x,y in zip(a,b))
    return bool(zero(S.sympify(a)-S.sympify(b)))


def _base(status, evidence, result, *, checks=(), next_step="", obstruction=None, independent=False):
    return {"status":status, "evidence_level":evidence,
            "results":result, "checks":list(checks),
            "independent_exact_backend":bool(independent),
            "counterexample":obstruction,
            "recommended_next_step":next_step}


def exact_identity(model):
    if set(model)-{"variables","lhs","rhs","dimensions"}:
        raise ScopeError("unknown exact identity model fields")
    names = _names(model.get("variables"),upper=8)
    if "lhs" not in model or "rhs" not in model:
        raise ScopeError("lhs/rhs required")
    parser=RestrictedExpression(names)
    left,right=_expression(parser,model["lhs"]),_expression(parser,model["rhs"])
    if model.get("dimensions") is not None:
        units=compare_units(model["lhs"],model["rhs"],model["dimensions"],names)
    else:
        units={"checked":False,"reason":"no units declared"}
    try:
        difference=coefficient_difference(model["lhs"],model["rhs"],names)
    except PolynomialScope as exc:
        # Domain guard: x / x may be undefined at x=0; cancellation alone
        # does not prove an unrestricted equality on the declared domain.
        delta=left-right
        proof=bool(zero(delta))
        return _base("INCONCLUSIVE_SYMBOLIC_ONLY", "symbolic_diagnostic",
                {"lhs":S.sstr(left),"rhs":S.sstr(right),
                 "sympy_zero":proof,"units":units,
                 "scope_refusal":str(exc)},
                checks=[{"gate":"independent_polynomial_oracle","passed":False}],
                next_step="Supply a domain-certified analytic proof or a supported exact polynomial formulation.")
    delta=S.expand(left-right)
    try:
        sympoly=S.Poly(delta,*[parser.symbols[name] for name in names],domain=S.QQ)
        symdict={tuple(m):Q(int(c.p),int(c.q)) for m,c in sympoly.terms()}
        symdict={m:c for m,c in symdict.items() if c}
    except (S.PolynomialError,TypeError,ValueError,ZeroDivisionError) as exc:
        return _base("INCONCLUSIVE_ORACLE_DISAGREEMENT","unverified",
              {"reason":str(exc)},next_step="Investigate parser/oracle discrepancy.")
    agreement=symdict==difference
    checks=[{"gate":"independent_fraction_sparse_polynomial","passed":True},
            {"gate":"sympy_QQ_coefficient_reconstruction","passed":agreement},
            {"gate":"declared_dimensions","passed":bool(units["checked"]) if "dimensions" in model else None}]
    if not agreement:
        return _base("INCONCLUSIVE_ORACLE_DISAGREEMENT","unverified",
             {"sympy_coefficients":polynomial_signature(symdict),
              "fraction_coefficients":polynomial_signature(difference),"units":units},
             checks=checks,next_step="Investigate discrepancy; do not certify.")
    if not difference:
        # Explicit counterfactual perturbation ensures that the oracle
        # catches a simple altered conclusion in the same variable basis.
        mutated=S.Poly(delta-S.Integer(1),*[parser.symbols[n] for n in names],domain=S.QQ)
        checks.append({"gate":"altered_conclusion_negative_control",
                       "passed":not mutated.is_zero})
        return _base("PROVED_SCOPED_POLYNOMIAL_IDENTITY","exact_two_route",
              {"identity":f"{S.sstr(left)} = {S.sstr(right)}","units":units,
               "universal_over_formal_variables":True,
               "assumptions_physically_validated":False},
              checks=checks,independent=True,
              next_step="Audit how the formal symbols map to the intended physical variables and assumptions.")
    witness=rational_counterexample(difference,names)
    if witness is not None:
        assignment={parser.symbols[n]:S.Rational(v) for n,v in witness["assignment"].items()}
        symval=S.simplify(delta.subs(assignment))
        checks.append({"gate":"independently_replay_counterexample",
                       "passed":str(symval)==witness["residual"]})
    return _base("REFUTED_EXACT_POLYNOMIAL_IDENTITY","exact_two_route",
           {"nonzero_coefficients":polynomial_signature(difference),"units":units},
           checks=checks,obstruction=witness,independent=True,
           next_step="Revise the claimed identity or its formally stated premises.")


def hamiltonian_flow(model):
    if set(model)-{"positions","momenta","hamiltonian","expected_dq","expected_dp"}:
        raise ScopeError("unknown Hamiltonian model fields")
    qnames=_names(model.get("positions"),upper=4)
    pnames=_names(model.get("momenta"),upper=4)
    if len(qnames)!=len(pnames) or set(qnames)&set(pnames) or "hamiltonian" not in model:
        raise ScopeError("disjoint equal canonical q/p pairs and H required")
    parser=RestrictedExpression((),(),(),qnames,pnames)
    q=[parser.symbols[n] for n in qnames]
    p=[parser.symbols[n] for n in pnames]
    H=_expression(parser,model["hamiltonian"])
    dq=[S.simplify(S.diff(H,v)) for v in p]
    dp=[S.simplify(-S.diff(H,v)) for v in q]
    secondary=[poisson_bracket(v,H,q,p) for v in q+p]
    agreement=_eq(dq+dp,secondary)
    expected=None
    if "expected_dq" in model or "expected_dp" in model:
        if (not isinstance(model.get("expected_dq"),list) or
            not isinstance(model.get("expected_dp"),list) or
            len(model["expected_dq"])!=len(q) or len(model["expected_dp"])!=len(q)):
            raise ScopeError("expected Hamilton equations must be complete")
        expected=[_expression(parser,x) for x in model["expected_dq"]+model["expected_dp"]]
    matched=(None if expected is None else _eq(dq+dp,expected))
    checks=[{"gate":"canonical_poisson_gradient_comparison","passed":agreement}]
    if matched is not None:
        checks.append({"gate":"claimed_hamiltonian_equations","passed":matched})
    status=("INCONCLUSIVE_ORACLE_DISAGREEMENT" if not agreement else
            "REJECTED_MODEL_PREDICTION" if matched is False else
            "DERIVED_SCOPED_CANONICAL_EQUATIONS")
    return _base(status,"symbolic_model_derivation",
         {"H":S.sstr(H),"dq_dt":_to_text(dq),"dp_dt":_to_text(dp),
          "declared_equations_matched":matched},
         checks=checks,next_step="Check physical units, domain, constraints and initial/boundary data.")


def euler_lagrange_system(model):
    if set(model)-{"coordinates","fields","lagrangian","expected_eom","translation_noether"}:
        raise ScopeError("unknown field model fields")
    coords=_names(model.get("coordinates"),upper=4)
    fieldnames=_names(model.get("fields"),upper=4)
    if set(coords)&set(fieldnames) or "lagrangian" not in model:
        raise ScopeError("field and coordinate names must be disjoint; L required")
    parser=RestrictedExpression(coords,(),fieldnames)
    L=_expression(parser,model["lagrangian"])
    fields=[parser.fields[f] for f in fieldnames]
    eqs=euler_lagrange(L,fields,list(parser.coordinates.values()))
    expected=None
    if "expected_eom" in model:
        if not isinstance(model["expected_eom"],list) or len(model["expected_eom"])!=len(fields):
            raise ScopeError("one expected Euler-Lagrange equation per field")
        expected=[_expression(parser,x) for x in model["expected_eom"]]
    matched=None if expected is None else _eq(eqs,expected)
    noether=None
    if model.get("translation_noether") is True:
        res=translation_noether_residual(L,fields,list(parser.coordinates.values()))
        noether=_eq(res,(0,)*len(coords))
    elif model.get("translation_noether") not in (None,False):
        raise ScopeError("translation_noether must be boolean")
    checks=[{"gate":"euler_lagrange_expected","passed":matched},
            {"gate":"translation_noether_structural_identity","passed":noether}]
    return _base("REJECTED_MODEL_PREDICTION" if matched is False else
                  "DERIVED_SCOPED_EULER_LAGRANGE",
         "symbolic_model_derivation",
         {"lagrangian":S.sstr(L),"euler_lagrange":_to_text(eqs),
          "declared_equations_matched":matched,"translation_noether_zero":noether},
         checks=checks,next_step="Check action, boundary terms, field domain and independent variation.")


def quantum_commutator(model):
    if set(model)-{"a","b","expected_commutator","expected_hermitian"}:
        raise ScopeError("unknown quantum model fields")
    if "a" not in model or "b" not in model:
        raise ScopeError("two exact finite operators required")
    parser=RestrictedExpression(())
    A=_matrix(model["a"],parser,bound=5)
    B=_matrix(model["b"],parser,bound=5)
    if A.shape!=B.shape:
        raise ScopeError("operators must act on same finite Hilbert space")
    C=commutator(A,B)
    # Independent entrywise multiplication loop (no backend commutator call).
    independent=S.Matrix(A.rows,A.cols,lambda i,j:S.simplify(
        sum(A[i,k]*B[k,j]-B[i,k]*A[k,j] for k in range(A.rows))))
    agree=_eq(C,independent)
    expected=None
    if "expected_commutator" in model:
        expected=_matrix(model["expected_commutator"],parser,bound=5)
        if expected.shape!=C.shape:
            raise ScopeError("expected commutator shape mismatch")
    matched=None if expected is None else _eq(C,expected)
    hermiticity=(is_hermitian(A),is_hermitian(B))
    requested=model.get("expected_hermitian")
    if requested is not None and (
            not isinstance(requested,list) or len(requested)!=2 or
            any(type(x) is not bool for x in requested)):
        raise ScopeError("expected_hermitian must be a two-boolean list")
    hmatch=None if requested is None else tuple(requested)==hermiticity
    checks=[{"gate":"independent_entrywise_matrix_product","passed":agree},
            {"gate":"asserted_commutator","passed":matched},
            {"gate":"asserted_hermiticity","passed":hmatch}]
    status=("INCONCLUSIVE_ORACLE_DISAGREEMENT" if not agree else
            "REJECTED_MODEL_PREDICTION" if matched is False or hmatch is False else
            "DERIVED_SCOPED_FINITE_QUANTUM_ALGEBRA")
    return _base(status,"exact_finite_linear_algebra",
          {"dimension":A.rows,"commutator":_to_text(C),
           "trace_commutator":S.sstr(S.trace(C)),
           "operator_hermitian":list(hermiticity),
           "expected_commutator_matched":matched},
          checks=checks,independent=agree,
          next_step="Do not infer a continuum QFT, unitarity of dynamics or experimental observables.")


def metric_curvature(model):
    if set(model)-{"coordinates","metric","signature","expected_scalar_curvature","check_vacuum"}:
        raise ScopeError("unknown geometry model fields")
    coords=_names(model.get("coordinates"),upper=4)
    if "metric" not in model or not isinstance(model.get("signature"),str):
        raise ScopeError("metric and explicit chart signature required")
    sign=model["signature"]
    if len(sign)!=len(coords) or any(ch not in "+-" for ch in sign):
        raise ScopeError("signature must have a +/- sign per dimension")
    parser=RestrictedExpression(coords)
    g=_matrix(model["metric"],parser)
    if g.rows!=len(coords):
        raise ScopeError("coordinate/metric dimension mismatch")
    geom=Geometry(tuple(parser.coordinates.values()),g)
    scalar=geom.scalar
    expected=None
    if "expected_scalar_curvature" in model:
        expected=_expression(parser,model["expected_scalar_curvature"])
    scalar_match=None if expected is None else _eq(scalar,expected)
    bianchi=all(zero(v) for v in geom.contracted_bianchi_residual())
    first=all(zero(v) for v in geom.first_bianchi_residual())
    inverse=_eq(g*geom.g_inv,S.eye(len(coords)))
    vacuum=None
    if model.get("check_vacuum") is True:
        if len(coords)!=4:
            raise ScopeError("Einstein vacuum claim requires 3+1 spacetime")
        vacuum=all(zero(x) for x in geom.einstein)
    elif model.get("check_vacuum") not in (None,False):
        raise ScopeError("check_vacuum must be boolean")
    checks=[{"gate":"metric_inverse","passed":inverse},
            {"gate":"first_bianchi","passed":first},
            {"gate":"contracted_bianchi","passed":bianchi},
            {"gate":"claimed_scalar_curvature","passed":scalar_match},
            {"gate":"vacuum_einstein_chart","passed":vacuum}]
    bad=any(x["passed"] is False for x in checks)
    status=("REJECTED_MODEL_PREDICTION" if bad else "DERIVED_SCOPED_METRIC_CURVATURE")
    return _base(status,"symbolic_chart_local",
             {"scalar_curvature":S.sstr(scalar),"ricci":_to_text(geom.ricci),
              "einstein":_to_text(geom.einstein),
              "expected_scalar_matched":scalar_match,
              "vacuum_equations_satisfied":vacuum,
              "signature":sign,"signature_independently_verified":False},
             checks=checks,next_step="Prove chart domain, signature, matter equations and global causal/regularity conditions.")


def finite_statistical(model):
    if set(model)-{"energies","degeneracies","inverse_temperature"}:
        raise ScopeError("unknown finite statistical model fields")
    energies=model.get("energies")
    if not isinstance(energies,list) or not 1<=len(energies)<=12:
        raise ScopeError("1..12 exact energy levels required")
    degeneracies=model.get("degeneracies",[1]*len(energies))
    if (not isinstance(degeneracies,list) or len(degeneracies)!=len(energies)
        or any(type(x) is not int or not 1<=x<=10000 for x in degeneracies)):
        raise ScopeError("degeneracies must be bounded positive integers")
    beta=model.get("inverse_temperature","beta")
    bname=_names([beta])[0]
    parser=RestrictedExpression(())
    E=[]
    for val in energies:
        e=parser.parse(val)
        if e.free_symbols or e.is_Rational is not True:
            raise ScopeError("finite ensemble energy must be an exact real rational")
        E.append(e)
    b=S.Symbol(bname,positive=True,real=True)
    weights=[g*S.exp(-b*v) for g,v in zip(degeneracies,E)]
    Z=S.Add(*weights)
    mean=S.simplify(sum(v*w for v,w in zip(E,weights))/Z)
    variance=S.simplify(sum(v*v*w for v,w in zip(E,weights))/Z-mean**2)
    check1=zero(S.diff(Z,b)+mean*Z)
    check2=zero(S.diff(mean,b)+variance)
    checks=[{"gate":"thermodynamic_energy_derivative","passed":check1},
            {"gate":"finite_fluctuation_identity","passed":check2}]
    return _base("DERIVED_SCOPED_FINITE_CANONICAL_ENSEMBLE" if check1 and check2 else
                 "INCONCLUSIVE_ORACLE_DISAGREEMENT",
            "exact_finite_statistical_model",
            {"inverse_temperature":bname,"partition_function":S.sstr(Z),
             "mean_energy":S.sstr(mean),"energy_variance":S.sstr(variance),
             "ensemble_finite":True,"thermodynamic_limit_proven":False},
            checks=checks,
            next_step="Add physical calibration, thermodynamic limit, phase assumptions and independently validated input spectrum.")


def typed_obligations(model):
    if set(model)!={"contract"} or not isinstance(model["contract"],dict):
        raise ScopeError("typed adapter requires an existing v1.2 typed contract")
    given=model["contract"]
    receipt=execute_physics_input(given)
    replay=replay_physics_input(given,receipt)
    passed=receipt["status"].startswith("PASS_") and replay
    checks=[{"gate":"native_v12_typed_model","passed":receipt["status"].startswith("PASS_")},
            {"gate":"bytewise_full_replay","passed":replay}]
    return _base("PASS_SCOPED_TYPED_OBLIGATIONS" if passed else "REJECTED_MODEL_PREDICTION",
                 "existing_v12_scoped_receipt",
                 {"native_status":receipt["status"],
                  "native_receipt_sha256":receipt["receipt_sha256"],
                  "native_schema":receipt["schema"],
                  "native_physical_truth":False},
                 checks=checks,next_step="Audit assumptions and obtain an independent physics and numerical validation.")
