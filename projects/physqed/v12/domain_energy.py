"""Exact rational-polynomial domain energy certification (sufficient bounds).

For U_t + A^j U_j+B U=0, compute
R=S_t+sum_j d_j(S A^j)-S B-B^T S.
Exact multivariate Bernstein enclosures and Gershgorin row bounds certify
S >= s_* I and C S-R >=0 THROUGHOUT a rational spacetime rectangle.

Inputs are trusted, programmatic SymPy polynomials (not free-form text or
arbitrary source to evaluate). This is a sufficient, fail-closed checker.
INCONCLUSIVE does not imply a counterexample. Boundary flux and smooth
solution existence remain separate analytic hypotheses.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import product
from math import comb
from hashlib import sha256
import json
import sympy as sy


class DomainScopeError(ValueError):
    pass


def _rat(v):
    if type(v) is int or isinstance(v,Fraction):
        return Fraction(v)
    if isinstance(v,sy.Rational):
        return Fraction(int(v.p),int(v.q))
    if isinstance(v,str):
        try:
            return Fraction(v)
        except (ValueError,ZeroDivisionError) as exc:
            raise DomainScopeError("invalid exact rational input") from exc
    raise DomainScopeError("exact rational number required")


def _poly(v,coords):
    if isinstance(v,(str,float)) or (isinstance(v,sy.Expr) and v.has(sy.Float)):
        raise DomainScopeError("polynomial coefficients require exact typed expressions")
    v=sy.sympify(v)
    if not v.free_symbols.issubset(set(coords)):
        raise DomainScopeError("undeclared free polynomial symbols")
    try:
        p=sy.Poly(v,*coords,domain=sy.QQ)
    except (sy.PolynomialError,sy.CoercionFailed,ValueError) as exc:
        raise DomainScopeError("exact rational polynomial required") from exc
    if p.total_degree()>12 or len(p.terms())>700:
        raise DomainScopeError("polynomial complexity limit exceeded")
    return p


def bernstein_bounds(expression,box):
    """Return rigorous min/max Bernstein-coefficient enclosure.

    Transform x_j=a_j+(b_j-a_j)t_j to the unit box; monomials obey
    t^i=sum_{k>=i} product_j binom(k_j,i_j)/binom(n_j,i_j) B_{k,n}(t).
    Positivity and partition of unity of the Bernstein basis imply a
    global enclosure on the entire closed box.
    """
    coords=tuple(box)
    if not 1<=len(coords)<=4 or any(not isinstance(c,sy.Symbol) for c in coords):
        raise DomainScopeError("box requires 1..4 coordinate symbols")
    ends=[]
    for interval in box.values():
        if not isinstance(interval,(list,tuple)) or len(interval)!=2:
            raise DomainScopeError("rational closed intervals required")
        a,b=map(_rat,interval)
        if b<=a:
            raise DomainScopeError("box needs strictly positive widths")
        ends.append((a,b))
    _poly(expression,coords)
    us=sy.symbols("u0:"+str(len(coords)))
    repl={
        x:sy.Rational(a.numerator,a.denominator)+
          sy.Rational((b-a).numerator,(b-a).denominator)*u
        for x,(a,b),u in zip(coords,ends,us)}
    q=sy.Poly(sy.expand(sy.sympify(expression).subs(repl,simultaneous=True)),
              *us,domain=sy.QQ)
    if q.is_zero:
        return {"lower":Fraction(0),"upper":Fraction(0),
                "degree":(0,)*len(coords),"coefficient_count":1}
    degree=q.degree_list()
    if any(d>12 for d in degree) or sy.prod(d+1 for d in degree)>8000:
        raise DomainScopeError("Bernstein coefficient tensor too large")
    terms=[(powers,_rat(c)) for powers,c in q.terms()]
    values=[]
    for k in product(*(range(d+1) for d in degree)):
        total=Fraction(0)
        for powers,coeff in terms:
            if all(p<=kj for p,kj in zip(powers,k)):
                ratio=Fraction(1)
                for kj,p,n in zip(k,powers,degree):
                    ratio*=Fraction(comb(kj,p),comb(n,p))
                total+=coeff*ratio
        values.append(total)
    return {"lower":min(values),"upper":max(values),
            "degree":degree,"coefficient_count":len(values)}


def _checked_matrices(coords,S,A,B):
    coords=tuple(coords)
    if not 2<=len(coords)<=4 or len(set(coords))!=len(coords) or any(
        not isinstance(v,sy.Symbol) for v in coords):
        raise DomainScopeError("time and 1..3 distinct spatial symbols required")
    s=sy.Matrix(S)
    n=s.rows
    if not 1<=n<=6 or s.shape!=(n,n):
        raise DomainScopeError("square system of rank 1..6 required")
    a=[sy.Matrix(x) for x in A]
    b=sy.Matrix(B)
    if len(a)!=len(coords)-1 or b.shape!=(n,n) or any(m.shape!=(n,n) for m in a):
        raise DomainScopeError("coefficient matrix shapes disagree")
    for m in [s,b]+a:
        for entry in m:
            _poly(entry,coords)
    if any(sy.expand(v)!=0 for v in s-s.T):
        raise DomainScopeError("S not exactly symmetric")
    if any(any(sy.expand(v)!=0 for v in s*m-(s*m).T) for m in a):
        raise DomainScopeError("S A^i not symmetric")
    return s,a,b


def _gershgorin(matrix,box,threshold=Fraction(0)):
    n=matrix.rows
    bnds={}
    for i in range(n):
        for j in range(i,n):
            subtract=sy.Rational(threshold.numerator,threshold.denominator) if i==j else 0
            bnds[(i,j)]=bernstein_bounds(matrix[i,j]-subtract,box)
    rows=[]
    for i in range(n):
        diag=bnds[(i,i)]["lower"]
        off=sum((max(abs(bnds[min(i,j),max(i,j)]["lower"]),
                     abs(bnds[min(i,j),max(i,j)]["upper"]))
                 for j in range(n) if i!=j),Fraction(0))
        rows.append({"row":i,"diagonal_lower":str(diag),
                     "offdiag_abs_upper":str(off),
                     "gershgorin_margin":str(diag-off),
                     "passed":diag>=off})
    return rows


def certify_domain_energy(coords,box,symmetrizer,principal,lower_order,
                          *,coercivity,growth,boundary="unverified"):
    """Certify two interior matrix bounds on a finite rational rectangle."""
    coords=tuple(coords)
    if not isinstance(box,dict) or set(box)!=set(coords):
        raise DomainScopeError("box must give every declared coordinate exactly once")
    if boundary not in ("unverified","periodic_solution_assumed",
                        "nonnegative_outward_flux_assumed"):
        raise DomainScopeError("unsupported boundary status")
    c=_rat(growth);sigma=_rat(coercivity)
    if sigma<=0 or c<0:
        raise DomainScopeError("s_* positive and C nonnegative required")
    s,a,b=_checked_matrices(coords,symmetrizer,principal,lower_order)
    R=(s.diff(coords[0])+sum(((s*a[j]).diff(coords[j+1])
          for j in range(len(a))),sy.zeros(s.rows))
          -s*b-b.T*s).applyfunc(sy.expand)
    low=_gershgorin(s,box,sigma)
    high=_gershgorin((sy.Rational(c.numerator,c.denominator)*s-R).applyfunc(sy.expand),box)
    spatial_constant=all(all(sy.expand(sy.diff(v,x))==0 for x in coords[1:])
              for m in [s,b]+a for v in m)
    bounds_ok=all(v["passed"] for v in low+high)
    receipt={
       "schema":"physqed.domain-energy.v1",
       "status":("PASS_INTERIOR_DOMAIN_BOUNDS__PDE_HYPOTHESES_PENDING" if bounds_ok
                 else "INCONCLUSIVE_SUFFICIENT_BOUND_NOT_ESTABLISHED"),
       "intervals":{str(v):[str(_rat(x)) for x in box[v]] for v in coords},
       "coercivity_s":str(sigma),"growth_C":str(c),
       "coercivity_gershgorin":low,"growth_gershgorin":high,
       "coercivity_bound_proved":all(v["passed"] for v in low),
       "growth_bound_proved":all(v["passed"] for v in high),
       "coefficient_polynomial_regular_on_box":True,
       "symmetric_principal_matrices_proved":True,
       "boundary_kind":boundary,
       "spatial_coefficient_independence_proved":spatial_constant,
       "conditional_periodic_flux_applies":boundary=="periodic_solution_assumed" and spatial_constant,
       "boundary_flux_proven_from_input":False,
       "boundary_flux_assumed":boundary!="unverified",
       "source_free_assumed":True,
       "underlying_smooth_solution_existence_proven":False,
       "complete_einstein_constraints_proven":False,
       "energy_estimate_given_hypotheses":
           "E(t)<=exp(C*(t-t0))*E(t0) for smooth homogeneous solutions with nonnegative outward flux",
       "backend":"exact rational SymPy polynomial extraction + Fraction Bernstein/Gershgorin",
       "not_global_pde_proof":True}
    canonical=json.dumps(receipt,sort_keys=True,separators=(",",":"))
    receipt["receipt_sha256"]=sha256(canonical.encode()).hexdigest()
    return receipt


def replay_domain_energy(coords,box,symmetrizer,principal,lower_order,claimed,
                         *,coercivity,growth,boundary="unverified"):
    """Recompute all inequalities; refuse a modified proof receipt."""
    return isinstance(claimed,dict) and claimed==certify_domain_energy(
        coords,box,symmetrizer,principal,lower_order,
        coercivity=coercivity,growth=growth,boundary=boundary)
