"""Exact rational-function energy bounds on a rational spacetime box.

Conservative Bernstein numerator/denominator signs with exact Fraction
arithmetic, Gershgorin PSD bounds, deterministic dyadic cell refinement.
Only trusted SymPy inputs; original cancelled singularities must be
supplied in denominator_guards. No claim of global PDE well-posedness.
"""
from __future__ import annotations
from fractions import Fraction
from hashlib import sha256
import json
import sympy as S
from .domain_energy import bernstein_bounds, _rat, DomainScopeError


def _rational_parts(expr,coords):
    if isinstance(expr,(str,float)) or (isinstance(expr,S.Basic) and expr.has(S.Float)):
        raise DomainScopeError('exact SymPy rational expressions required')
    z=S.sympify(expr)
    if z.free_symbols-set(coords):
        raise DomainScopeError('undeclared free symbols')
    try:
        numerator,denominator=S.fraction(S.together(z))
        n=S.Poly(numerator,*coords,domain=S.QQ)
        d=S.Poly(denominator,*coords,domain=S.QQ)
    except (S.PolynomialError, S.CoercionFailed, ValueError, TypeError) as exc:
        raise DomainScopeError('rational function must have rational polynomial numerator and denominator') from exc
    if d.is_zero:
        raise DomainScopeError('identically zero denominator')
    if max(n.total_degree(),d.total_degree())>10 or len(n.terms())+len(d.terms())>400:
        raise DomainScopeError('rational numerator or denominator complexity limit')
    return n.as_expr(),d.as_expr()


def _exact_zero(z,coords):
    n,_=_rational_parts(z,coords)
    return S.Poly(n,*coords,domain=S.QQ).is_zero


def _boxed_fraction(bounds):
    return {"lower":str(bounds['lower']),"upper":str(bounds['upper']),
            "degree":list(bounds['degree']),"coefficient_count":bounds['coefficient_count']}


def _rational_interval(expr,box,label):
    coords=tuple(box)
    n,d=_rational_parts(expr,coords)
    n_bounds=bernstein_bounds(n,box)
    d_bounds=bernstein_bounds(d,box)
    lower,upper=d_bounds['lower'],d_bounds['upper']
    sign='positive' if lower>0 else 'negative' if upper<0 else None
    entry={"name":label,"numerator":S.srepr(n),"denominator":S.srepr(d),
           "numerator_Bernstein":_boxed_fraction(n_bounds),
           "denominator_Bernstein":_boxed_fraction(d_bounds),
           "denominator_sign":sign,"denominator_nonzero_certified":bool(sign)}
    if not sign:
        entry['bounds']=None
        return entry
    quotients=[a/b for a in (n_bounds['lower'],n_bounds['upper'])
               for b in (d_bounds['lower'],d_bounds['upper'])]
    entry['bounds']={"lower":str(min(quotients)),"upper":str(max(quotients))}
    return entry


def _gershgorin_from_bounds(matrix,box,threshold,label):
    n=matrix.rows
    details={}
    for i in range(n):
        for j in range(i,n):
            expr=S.together(matrix[i,j]-(S.Rational(threshold.numerator,threshold.denominator)
                        if i==j else 0))
            details[(i,j)]=_rational_interval(expr,box,f'{label}[{i},{j}]')
    if not all(row['denominator_nonzero_certified'] for row in details.values()):
        return {"passed":False,"reason":"DENOMINATOR_NOT_CERTIFIED",
                "rows":[],"entries":list(details.values())}
    rows=[]
    for i in range(n):
        diag=Fraction(details[(i,i)]['bounds']['lower'])
        off=Fraction(0)
        for j in range(n):
            if j==i: continue
            bounds=details[min(i,j),max(i,j)]['bounds']
            off+=max(abs(Fraction(bounds['lower'])),abs(Fraction(bounds['upper'])))
        rows.append({"index":i,"diagonal_lower":str(diag),
                     "off_diagonal_abs_upper":str(off),
                     "margin":str(diag-off),"passed":diag>=off})
    return {"passed":all(row['passed'] for row in rows),
            "reason":("PASSED" if all(row['passed'] for row in rows)
                      else "SUFFICIENT_GERSHGORIN_INCONCLUSIVE"),
            "rows":rows,"entries":list(details.values())}


def _matrices(coords,Sp,principal,lower_order):
    coords=tuple(coords)
    if not 2<=len(coords)<=4 or len(set(coords))!=len(coords) or any(
            not isinstance(x,S.Symbol) for x in coords):
        raise DomainScopeError('1 temporal and 1..3 distinct spatial symbols required')
    s=S.Matrix(Sp)
    if s.rows!=s.cols or not 1<=s.rows<=6:
        raise DomainScopeError('square 1..6 symmetric matrix required')
    A=[S.Matrix(v) for v in principal]
    B=S.Matrix(lower_order)
    if len(A)!=len(coords)-1 or B.shape!=s.shape or any(a.shape!=s.shape for a in A):
        raise DomainScopeError('coefficient matrix shape mismatch')
    for entry in [v for m in [s,B]+A for v in m]:
        _rational_parts(entry,coords)
    if any(not _exact_zero(v,coords) for v in s-s.T):
        raise DomainScopeError('symmetrizer must be symmetric as rational identity')
    if any(not _exact_zero(v,coords) for a in A for v in s*a-(s*a).T):
        raise DomainScopeError('S A^i must be symmetric as rational identity')
    return s,A,B


def _validate_box(coords,box):
    if not isinstance(box,dict) or set(box)!=set(coords):
        raise DomainScopeError('closed rational box must assign every coordinate')
    domain={}
    for x in coords:
        value=box[x]
        if not isinstance(value,(tuple,list)) or len(value)!=2:
            raise DomainScopeError('box endpoints must be pairs')
        a,b=map(_rat,value)
        if a>=b:
            raise DomainScopeError('positive box interval width required')
        domain[x]=(a,b)
    return domain


def _cell(box,guards,source_entries,Smat,Qmat,coords):
    guard_results=[]
    for i,guard in enumerate(guards):
        # A guard represents a *source-level denominator factor*; it must
        # have a certified strict sign, independent of rational cancellation.
        g=_rational_interval(guard,box,f'original_guard[{i}]')
        guard_results.append(g)
    input_signs=all(g['denominator_nonzero_certified'] for g in guard_results)
    guard_signs=[]
    for idx,guard in enumerate(guards):
        n,d=_rational_parts(guard,coords)
        if not input_signs:
            guard_signs.append({"name":f'original_guard[{idx}]',"passed":False})
            continue
        numerator=bernstein_bounds(n,box)
        sg='positive' if numerator['lower']>0 else 'negative' if numerator['upper']<0 else None
        guard_signs.append({"name":f'original_guard[{idx}]',"passed":bool(sg),
                            "sign":sg,"numerator_Bernstein":_boxed_fraction(numerator)})
    source_guard_ok=all(v['passed'] for v in guard_signs)
    # Every received coefficient must be regular before algebraic
    # cancellations in S*A, R, or C*S-R can hide original poles.
    source_checks=[_rational_interval(value,box,label)
                   for label,value in source_entries]
    source_regular=all(v['denominator_nonzero_certified']
                       for v in source_checks)
    low=_gershgorin_from_bounds(Smat,box,Fraction(0),'coercivity')
    high=_gershgorin_from_bounds(Qmat,box,Fraction(0),'growth')
    reasons=[]
    if not source_guard_ok: reasons.append('SOURCE_DENOMINATOR_SIGN_NOT_CERTIFIED')
    if not source_regular: reasons.append('INPUT_COEFFICIENT_DENOMINATOR_SIGN_NOT_CERTIFIED')
    if not low['passed']: reasons.append('COERCIVITY_'+low['reason'])
    if not high['passed']: reasons.append('GROWTH_'+high['reason'])
    return {"box":{str(x):[str(v) for v in box[x]] for x in coords},
            "passed":not reasons,"reason_codes":reasons,
            "original_denominator_guards":guard_results,
            "original_guard_signs":guard_signs,
            "source_denominator_checks":source_checks,
            "coercivity":low,"growth":high}


def certify_rational_domain_energy(coords,box,symmetrizer,principal,lower_order,
        *,coercivity,growth,denominator_guards=(),max_depth=0,
        boundary='unverified',original_expression_denominators_complete=False):
    """Exact sufficient pointwise interior matrix inequalities on a box.

    Original expression domain holes lost to external simplification must
    be declared in denominator_guards; provenance is caller-attested.
    """
    coords=tuple(coords)
    domain=_validate_box(coords,box)
    c=_rat(growth);lower=_rat(coercivity)
    if lower<=0 or c<0:
        raise DomainScopeError('coercivity must be positive, growth nonnegative')
    if type(max_depth) is not int or not 0<=max_depth<=4:
        raise DomainScopeError('dyadic subdivision depth must be 0..4')
    if boundary not in ('unverified','periodic_solution_assumed',
                        'nonnegative_outward_flux_assumed'):
        raise DomainScopeError('unknown boundary treatment')
    if type(original_expression_denominators_complete) is not bool:
        raise DomainScopeError('domain provenance assertion must be boolean')
    if not isinstance(denominator_guards,(tuple,list)) or len(denominator_guards)>24:
        raise DomainScopeError('at most 24 explicit denominator guards')
    s,A,B=_matrices(coords,symmetrizer,principal,lower_order)
    guards=tuple(denominator_guards)
    for g in guards:_rational_parts(g,coords)
    R=(s.diff(coords[0])+sum(((s*A[j]).diff(coords[j+1])
           for j in range(len(A))),S.zeros(s.rows))-s*B-B.T*s).applyfunc(S.together)
    P=(s-S.eye(s.rows)*S.Rational(lower.numerator,lower.denominator)).applyfunc(S.together)
    Q=(s*S.Rational(c.numerator,c.denominator)-R).applyfunc(S.together)
    for v in list(P)+list(Q):_rational_parts(v,coords)
    source_entries=[(f'S[{i}]',v) for i,v in enumerate(s)]
    source_entries.extend((f'A[{k},{i}]',v)
             for k,a in enumerate(A) for i,v in enumerate(a))
    source_entries.extend((f'B[{i}]',v) for i,v in enumerate(B))
    cells=[]
    def check(cell,depth):
        item=_cell(cell,guards,source_entries,P,Q,coords)
        item['depth']=depth
        if not item['passed'] and depth<max_depth:
            k=depth%len(coords)
            v=coords[k]
            a,b=cell[v]
            mid=(a+b)/2
            if len(cells)>=256:
                raise DomainScopeError('dyadic cell budget exceeded')
            children=[]
            for interval in ((a,mid),(mid,b)):
                child=dict(cell);child[v]=interval
                children.append(check(child,depth+1))
            return all(children)
        cells.append(item)
        return item['passed']
    proved=check(domain,0)
    spatial_constant=all(all(_exact_zero(S.diff(z,x),coords)
        for x in coords[1:]) for m in [s,B]+A for z in m)
    result={
       'schema':'physqed.rational-domain-energy.v1',
       'status':('PASS_RATIONAL_INTERIOR_BOUNDS__PDE_HYPOTHESES_PENDING' if proved else
                 'INCONCLUSIVE_RATIONAL_DOMAIN_BOUNDS'),
       'domain':{str(x):[str(v) for v in domain[x]] for x in coords},
       'coercivity_s':str(lower),'growth_C':str(c),
       'interior_coercivity_proven':proved,
       'interior_growth_proven':proved,
       'all_received_coefficient_denominators_certified':all(
           all(v['denominator_nonzero_certified'] for v in cell['source_denominator_checks'])
           for cell in cells),
       'all_required_original_denominator_guards_certified':all(
           all(v['passed'] for v in cell['original_guard_signs']) for cell in cells),
       'verified_cells':len(cells),'refinement_depth_limit':max_depth,
       'cells':cells,
       'symmetrizer_symmetric_proven':True,
       'principal_symmetrized_proven':True,
       'source_expression_denominator_completeness_asserted':original_expression_denominators_complete,
       'source_expression_denominator_completeness_independently_verified':False,
       'original_denominator_guard_count':len(guards),
       'boundary_kind':boundary,
       'boundary_flux_control_proven':False,
       'smooth_solution_exists_proven':False,
       'global_Einstein_Cauchy_theorem_proven':False,
       'conditional_energy_estimate':'E(t) <= exp(C*(t-t0))*E(t0) for smooth homogeneous solutions with controlled outward flux',
       'backend':'rational-function SymPy QQ extraction; exact Fraction Bernstein/Gershgorin; dyadic cell coverage'
    }
    result['receipt_sha256']=sha256(json.dumps(result,sort_keys=True,
         separators=(',',':')).encode()).hexdigest()
    return result


def replay_rational_domain_energy(coords,box,symmetrizer,principal,lower_order,
        receipt,*,coercivity,growth,denominator_guards=(),max_depth=0,
        boundary='unverified',original_expression_denominators_complete=False):
    if not isinstance(receipt,dict):return False
    return receipt==certify_rational_domain_energy(
        coords,box,symmetrizer,principal,lower_order,
        coercivity=coercivity,growth=growth,
        denominator_guards=denominator_guards,max_depth=max_depth,
        boundary=boundary,
        original_expression_denominators_complete=original_expression_denominators_complete)
