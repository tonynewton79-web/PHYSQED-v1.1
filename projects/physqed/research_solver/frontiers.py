"""Additional bounded research subproblems: PDE residuals and exact linear systems."""
from __future__ import annotations

from fractions import Fraction as Q
import sympy as S

from v12.geometry import ScopeError, zero
from v12.typed_input import RestrictedExpression
from .backends import _base, _names, _expression


def _fraction(node):
    if type(node) is int and abs(node)<=10**40:
        return Q(node)
    if isinstance(node,dict) and set(node)=={"rational"}:
        a=node["rational"]
        if (not isinstance(a,list) or len(a)!=2 or
            any(type(v) is not int or abs(v)>10**40 for v in a) or a[1]==0):
            raise ScopeError("invalid exact rational matrix coefficient")
        return Q(*a)
    raise ScopeError("linear-system coefficients must be exact rationals")


def _rref(a,b,n):
    """Independent Python Fraction Gauss-Jordan elimination, no SymPy."""
    rows=[list(r)+[v] for r,v in zip(a,b)]
    nrows=len(rows)
    pivots=[]
    top=0
    for col in range(n):
        candidate=next((i for i in range(top,nrows) if rows[i][col]),None)
        if candidate is None:
            continue
        rows[top],rows[candidate]=rows[candidate],rows[top]
        pivot=rows[top][col]
        rows[top]=[v/pivot for v in rows[top]]
        for j in range(nrows):
            if j!=top and rows[j][col]:
                scale=rows[j][col]
                rows[j]=[u-scale*v for u,v in zip(rows[j],rows[top])]
        pivots.append(col)
        top+=1
        if top==nrows:
            break
    inconsistent=any(all(c==0 for c in row[:n]) and row[-1]!=0 for row in rows)
    solution=None
    if not inconsistent and len(pivots)==n:
        solution=[Q(0)]*n
        for i,col in enumerate(pivots):
            solution[col]=rows[i][-1]
    return {"rank":len(pivots),"inconsistent":inconsistent,"unique_solution":solution}


def rational_linear_system(model):
    if set(model)!={"variables","coefficients","rhs"}:
        raise ScopeError("exact linear system requires variables, coefficients and rhs")
    names=_names(model["variables"],upper=6)
    entries=model["coefficients"]
    rhs=model["rhs"]
    if (not isinstance(entries,list) or not 1<=len(entries)<=8 or
        any(not isinstance(row,list) or len(row)!=len(names) for row in entries)
        or not isinstance(rhs,list) or len(rhs)!=len(entries)):
        raise ScopeError("linear model requires bounded rectangular matrix and rhs")
    a=[[_fraction(v) for v in row] for row in entries]
    b=[_fraction(v) for v in rhs]
    A=S.Matrix([[S.Rational(x.numerator,x.denominator) for x in row] for row in a])
    B=S.Matrix([S.Rational(x.numerator,x.denominator) for x in b])
    independent=_rref(a,b,len(names))
    rank=A.rank()
    augmented=A.row_join(B).rank()
    consistency=(augmented==rank)
    agreement=(rank==independent["rank"] and
               consistency != independent["inconsistent"])
    checks=[{"gate":"Fraction_vs_SymPy_rref_rank","passed":agreement}]
    if not agreement:
        return _base("INCONCLUSIVE_ORACLE_DISAGREEMENT","unverified",{},
                     checks=checks,next_step="Resolve independent rational linear-algebra disagreement.")
    if independent["inconsistent"]:
        return _base("REFUTED_LINEAR_SYSTEM_FEASIBILITY","exact_two_route",
                     {"rank":rank,"augmented_rank":augmented,
                      "solution_exists":False},
                     checks=checks,independent=True,
                     next_step="Reject inconsistent equations or revise assumptions.")
    if independent["unique_solution"] is None:
        return _base("UNDERDETERMINED_LINEAR_SYSTEM","exact_two_route",
                     {"rank":rank,"unknowns":len(names),
                      "solution_exists":True,"unique":False},
                     checks=checks,independent=True,
                     next_step="Supply additional independent equations or a justified gauge choice.")
    vals=independent["unique_solution"]
    X=S.Matrix([S.Rational(v.numerator,v.denominator) for v in vals])
    residual=A*X-B
    passed=all(v==0 for v in residual)
    checks.append({"gate":"exact_direct_substitution","passed":passed})
    status="PROVED_SCOPED_UNIQUE_LINEAR_SOLUTION" if passed else "INCONCLUSIVE_ORACLE_DISAGREEMENT"
    return _base(status,"exact_two_route",
          {"rank":rank,"unique":True,
           "solution":{n:str(v) for n,v in zip(names,vals)},
           "direct_substitution_zero":passed},
          checks=checks,independent=passed,
          next_step="Check how the linear model follows from the original physical equations.")


def pde_ansatz_residual(model):
    required={"coordinates","ansatz","terms","source"}
    if not isinstance(model,dict) or set(model)!=required:
        raise ScopeError("PDE ansatz needs coordinates, ansatz, operator terms and source")
    coords=_names(model["coordinates"],upper=3)
    parser=RestrictedExpression(coords)
    x={name:parser.coordinates[name] for name in coords}
    u=_expression(parser,model["ansatz"])
    terms=model["terms"]
    if not isinstance(terms,list) or not 1<=len(terms)<=12:
        raise ScopeError("PDE requires 1..12 linear differential operator terms")
    out=0
    descriptions=[]
    for term in terms:
        if not isinstance(term,dict) or set(term)!={"coefficient","derivatives"}:
            raise ScopeError("PDE linear term must specify coefficient and derivatives")
        ds=term["derivatives"]
        if not isinstance(ds,list) or len(ds)>4 or any(
            not isinstance(k,str) or k not in x for k in ds):
            raise ScopeError("PDE derivatives must use declared coordinates, order <=4")
        c=_expression(parser,term["coefficient"])
        # Linear operator coefficients cannot depend on the field:
        # u is a fixed ansatz here, not a separately bound dynamical field.
        derived=S.diff(u,*(x[k] for k in ds)) if ds else u
        out+=c*derived
        descriptions.append({"coefficient":S.sstr(c),"derivatives":ds})
    source=_expression(parser,model["source"])
    residual=S.simplify(out-source)
    second=S.cancel(S.together(S.expand(out-source)))
    passed=zero(residual) and zero(second)
    # "nonzero" is algebraically decisive if SymPy returns an explicit value
    # or the finite sampled substitution gives a valid exact rational counterexample.
    witness=None
    if not passed:
        assignments=[
            {x[n]:S.Rational((i+j+1),i+2) for j,n in enumerate(coords)}
            for i in range(5)]
        for assignment in assignments:
            try:
                v=S.simplify(residual.subs(assignment))
                if v.is_finite is True and v.is_zero is False:
                    witness={"assignment":{str(k):str(vv) for k,vv in assignment.items()},
                             "residual":S.sstr(v)}
                    break
            except (ValueError,TypeError,ZeroDivisionError):
                pass
    status=("DERIVED_SCOPED_PDE_SOLUTION_ANSATZ" if passed else
            "REFUTED_PDE_ANSATZ_BY_COUNTEREXAMPLE" if witness else
            "INCONCLUSIVE_PDE_RESIDUAL")
    checks=[{"gate":"operator_symbolic_residual","passed":passed},
            {"gate":"second_algebraic_normal_form","passed":bool(zero(second))}]
    return _base(status,"symbolic_local_ansatz_check",
           {"ansatz":S.sstr(u),"operator_terms":descriptions,
            "residual":S.sstr(residual),"operator_order_bound":4,
            "global_pde_wellposedness_proven":False,
            "boundary_initial_data_verified":False},
           checks=checks,obstruction=witness,
           next_step="Check PDE coefficients, chart/boundary domain, Cauchy data and independent continuum well-posedness.")
