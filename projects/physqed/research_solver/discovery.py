"""Bounded discovery mode: systematically generate and certify symmetry candidates.

Discovery is not novelty. Search completeness holds ONLY in the finite declared
polynomial/matrix grammar. Independent arithmetic replays use Fraction.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import product
import sympy as S

from v12.geometry import ScopeError
from v12.typed_input import RestrictedExpression
from .backends import _names, _matrix, _base
from .exact import independent_polynomial, _mul, _add, _neg


def _monomials(n,degree):
    return [ex for d in range(1,degree+1)
            for ex in product(range(d+1),repeat=n) if sum(ex)==d]


def _derivative(poly,i):
    out={}
    for powers,c in poly.items():
        if powers[i]:
            e=list(powers);e[i]-=1;e=tuple(e)
            out[e]=out.get(e,Q(0))+c*powers[i]
    return {k:v for k,v in out.items() if v}


def _poisson_fraction(f,h,dim):
    n=2*dim
    result={}
    for i in range(dim):
        result=_add(result,_mul(_derivative(f,i),_derivative(h,dim+i)))
        result=_add(result,_neg(_mul(_derivative(f,dim+i),_derivative(h,i))))
    return result


def _rational_poly(expr,symbols):
    try:
        p=S.Poly(S.expand(expr),*symbols,domain=S.QQ)
        return {tuple(m):Q(int(c.p),int(c.q)) for m,c in p.terms() if c}
    except (S.PolynomialError,TypeError,ValueError) as exc:
        raise ScopeError("discovery requires rational polynomial coefficients") from exc


def classical_conservation_search(model):
    required={"positions","momenta","hamiltonian","max_degree"}
    if not isinstance(model,dict) or set(model)!=required:
        raise ScopeError("classical search requires positions,momenta,H,max_degree")
    qnames=_names(model["positions"],upper=3)
    pnames=_names(model["momenta"],upper=3)
    if len(qnames)!=len(pnames) or set(qnames)&set(pnames):
        raise ScopeError("independent matched canonical coordinates required")
    degree=model["max_degree"]
    if type(degree) is not int or not 1<=degree<=3:
        raise ScopeError("supported conservation grammar degree 1..3")
    names=qnames+pnames
    exps=_monomials(len(names),degree)
    if len(exps)>80:
        raise ScopeError("too many polynomial monomials for bounded search")
    parser=RestrictedExpression((),(),(),qnames,pnames)
    symbols=tuple(parser.symbols[name] for name in names)
    H=parser.parse(model["hamiltonian"])
    Hpoly=independent_polynomial(model["hamiltonian"],names)
    if any(sum(m)>4 for m in Hpoly):
        raise ScopeError("Hamiltonian polynomial degree must be <=4")
    features=[]
    for exp in exps:
        mon=S.prod(z**d for z,d in zip(symbols,exp))
        lie=S.expand(sum(S.diff(mon,symbols[i])*S.diff(H,symbols[len(qnames)+i])
                     - S.diff(mon,symbols[len(qnames)+i])*S.diff(H,symbols[i])
                     for i in range(len(qnames))))
        features.append(_rational_poly(lie,symbols))
    rows=sorted(set().union(*(set(p) for p in features)))
    C=S.Matrix([[S.Rational(features[j].get(exp,Q(0)).numerator,
                             features[j].get(exp,Q(0)).denominator)
                 for j in range(len(exps))] for exp in rows]) if rows else S.zeros(0,len(exps))
    vectors=C.nullspace()
    if len(vectors)>32:
        raise ScopeError("candidate basis budget exceeded")
    certified=[]
    for vec in vectors:
        candidate=S.expand(sum(vec[j]*S.prod(z**d for z,d in zip(symbols,exp))
                               for j,exp in enumerate(exps)))
        exact=_rational_poly(candidate,symbols)
        resid=_poisson_fraction(exact,Hpoly,len(qnames))
        if resid:
            raise ScopeError("discovery oracle found a nonconserved basis element")
        certified.append({"candidate":S.sstr(candidate),
                          "candidate_degree":S.Poly(candidate,*symbols).total_degree(),
                          "fraction_poisson_bracket_zero":True})
    positive=(len(certified)>0)
    return _base("CANDIDATES_EXACTLY_CERTIFIED_IN_BOUNDED_CLASS" if positive else
                 "NO_CANDIDATE_WITHIN_BOUNDED_GRAMMAR",
                 "exact_candidate_search_two_route",
                 {"hamiltonian":S.sstr(H),"polynomial_degree_cap":degree,
                  "monomials_searched":len(exps),
                  "nonconstant_integral_basis_dimension":len(certified),
                  "basis":certified,
                  "discovery_novelty_proven":False,
                  "complete_integrability_proven":False,
                  "global_flows_established":False},
                 checks=[{"gate":"independent_fraction_poisson_replay","passed":True},
                         {"gate":"exact_nullspace_matrix","passed":all(C*v==S.zeros(C.rows,1) for v in vectors)}],
                 independent=True,
                 next_step="Test larger polynomial grammars, functional independence, global regularity and prior art.")


def _matrix_fractions(matrix):
    return [[Q(int(x.p),int(x.q)) for x in row] for row in matrix.tolist()]


def _independent_commutator_zero(matrix,h):
    a,b=_matrix_fractions(matrix),_matrix_fractions(h)
    n=len(a)
    for i in range(n):
        for j in range(n):
            if sum(a[i][k]*b[k][j]-b[i][k]*a[k][j] for k in range(n)) != 0:
                return False
    return True


def finite_quantum_symmetry_search(model):
    if not isinstance(model,dict) or set(model)!={"hamiltonian"}:
        raise ScopeError("finite commutant search requires a Hamiltonian matrix")
    parser=RestrictedExpression(())
    H=_matrix(model["hamiltonian"],parser,bound=4)
    if H.rows<2 or any(z.is_Rational is not True for z in H) or H!=H.T:
        raise ScopeError("real symmetric rational Hamiltonian of order 2..4 required")
    n=H.rows
    matrix_units=[]
    for i in range(n):
        for j in range(n):
            E=S.zeros(n)
            E[i,j]=1
            matrix_units.append(E)
    # [Q,H] is a linear map on the n^2-dimensional matrix algebra.
    constraints=S.Matrix.hstack(*[
        S.Matrix(n*n,1,list(E*H-H*E)) for E in matrix_units])
    null=constraints.nullspace()
    if len(null)>16:
        raise ScopeError("commutant search budget exceeded")
    mats=[]
    hermitian=[]
    for v in null:
        Qmat=sum((v[i]*matrix_units[i] for i in range(n*n)),S.zeros(n))
        if not _independent_commutator_zero(Qmat,H):
            raise ScopeError("Fraction oracle detected an invalid commutant candidate")
        mats.append({"matrix":[[str(z) for z in row] for row in Qmat.tolist()],
                     "commutator_zero":True})
        R=(Qmat+Qmat.T)/2
        if R!=S.zeros(n) and _independent_commutator_zero(R,H):
            hermitian.append([[str(z) for z in row] for row in R.tolist()])
    ev=H.eigenvals()
    distinct=len(ev)
    return _base("CANDIDATES_EXACTLY_CERTIFIED_IN_BOUNDED_CLASS",
                 "exact_candidate_search_two_route",
                 {"matrix_dimension":n,"commutant_dimension":len(null),
                  "distinct_eigenvalues":distinct,
                  "commutant_exceeds_polynomial_H_dimension":len(null)>distinct,
                  "commuting_matrices":mats,
                  "real_symmetric_candidate_generators":hermitian,
                  "symmetry_physical_significance_proven":False,
                  "discovery_novelty_proven":False},
                 checks=[{"gate":"independent_Fraction_commutator_for_every_generator","passed":True},
                         {"gate":"SymPy_exact_adjoint_nullspace","passed":all(
                             constraints*v==S.zeros(n*n,1) for v in null)}],
                 independent=True,
                 next_step="Classify irreducible symmetry algebras and test perturbative stability, locality and physical realization.")
