"""PHYSQED v0.9: exact two-premise polynomial membership with affine independence.

Checks C-D = W1 (A-B) + W2 (E-F) over Q[x1,...,xn], against
bounded, controlled-language text. Premises must be affine-linear with
Q-linearly independent normals: an exact nonredundancy guarantee.
No ODE, free-language, Lean-kernel or empirical/physical certification.
"""
from __future__ import annotations
import ast
from fractions import Fraction
import hashlib
import json
import re

from engine import polynomial, unit_of, BASES, CertificationError

VERSION = 'physqed-two-premise-v0.9'
TAIL = ' This checks only a conditional polynomial consequence; no physical law is established.'

class MultiPremiseRefusal(ValueError):
    pass


def _read_formal(expr, names):
    try:
        return polynomial(expr, names)
    except (CertificationError, ValueError, TypeError, KeyError, OverflowError,
            ZeroDivisionError, RecursionError) as exc:
        raise MultiPremiseRefusal('unsupported formal polynomial') from exc


def _add(a, b):
    r = dict(a)
    for mon, coef in b.items():
        r[mon] = r.get(mon, Fraction(0)) + coef
    return {k:v for k,v in r.items() if v}


def _neg(a):
    return {k:-v for k,v in a.items()}


def _mul(a, b, budget=512):
    r = {}
    for ma,va in a.items():
        for mb,vb in b.items():
            idx = tuple(i+j for i,j in zip(ma,mb))
            r[idx] = r.get(idx,Fraction(0))+va*vb
            if len(r) > budget:
                raise MultiPremiseRefusal('polynomial monomial budget exceeded')
    return {k:v for k,v in r.items() if v}


def _controlled(text, names):
    if len(text) > 1024:
        raise MultiPremiseRefusal('expression text too long')
    try:
        tree = ast.parse(text, mode='eval')
    except (SyntaxError, TypeError, ValueError, MemoryError) as exc:
        raise MultiPremiseRefusal('invalid controlled expression') from exc
    zero = (0,)*len(names)
    def walk(n, depth=0):
        if depth>24:
            raise MultiPremiseRefusal('expression depth limit')
        if isinstance(n,ast.Constant) and type(n.value) is int and len(str(n.value))<=60:
            return {zero:Fraction(n.value)} if n.value else {}
        if isinstance(n,ast.Name) and n.id in names:
            return {tuple(int(i==names.index(n.id)) for i in range(len(names))):Fraction(1)}
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):
            return _neg(walk(n.operand,depth+1))
        if isinstance(n,ast.BinOp):
            a=walk(n.left,depth+1)
            if isinstance(n.op,ast.Pow):
                if not isinstance(n.right,ast.Constant) or type(n.right.value) is not int or not 0<=n.right.value<=8:
                    raise MultiPremiseRefusal('unsupported exponent')
                out={zero:Fraction(1)}
                for _ in range(n.right.value):out=_mul(out,a)
                return out
            b=walk(n.right,depth+1)
            if isinstance(n.op,ast.Add):return _add(a,b)
            if isinstance(n.op,ast.Sub):return _add(a,_neg(b))
            if isinstance(n.op,ast.Mult):return _mul(a,b)
        raise MultiPremiseRefusal('unsupported controlled expression syntax')
    try:return walk(tree.body)
    except (OverflowError,RecursionError,TypeError,ValueError) as exc:
        raise MultiPremiseRefusal('invalid or overbudget controlled expression') from exc


def _typed(node, dimensions):
    try:return unit_of(node,dimensions)
    except (CertificationError,TypeError,ValueError,KeyError,OverflowError,RecursionError) as exc:
        raise MultiPremiseRefusal('unproved or malformed dimensional typing') from exc


def _equality_dim(left,right,names,types):
    u,v=_typed(left,types),_typed(right,types)
    a,b=_read_formal(left,names),_read_formal(right,names)
    if not a:u=v
    if not b:v=u
    if u!=v:raise MultiPremiseRefusal('dimensional inconsistency in equality')
    return u


def _independent_affine(p,q,n):
    """Q-linear independent gradients imply both affine constraints are independent.

    For two nonparallel nonzero normals the map R^n -> R^2 is surjective.
    Thus both equations can be met simultaneously and neither follows from
    the other alone. This check intentionally rejects nonlinear premises.
    """
    def normal(r):
        if any(sum(ex)>1 for ex in r):
            raise MultiPremiseRefusal('independence not established for nonlinear premises')
        return [r.get(tuple(int(i==j) for i in range(n)),Fraction(0)) for j in range(n)]
    a,b=normal(p),normal(q)
    if not any(a) or not any(b):raise MultiPremiseRefusal('degenerate affine premise')
    if not any(a[i]*b[j]-a[j]*b[i] for i in range(n) for j in range(i+1,n)):
        raise MultiPremiseRefusal('two premises have dependent affine normals')
    return True


def verify(contract):
    required={'schema','statement','variables','dimensions','premises','conclusion','witnesses','provenance'}
    if not isinstance(contract,dict) or set(contract)!=required:
        raise MultiPremiseRefusal('incorrect two-premise schema')
    if contract['schema']!=VERSION or contract['provenance']!='SYNTHETIC_SCOPED':
        raise MultiPremiseRefusal('unsupported schema or provenance')
    names=contract['variables']
    if (not isinstance(names,list) or not 2<=len(names)<=8 or
        any(not isinstance(s,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,18}',s) for s in names) or
        len(set(names))!=len(names)):
        raise MultiPremiseRefusal('invalid variable list')
    types=contract['dimensions']
    if not isinstance(types,dict) or set(types)!=set(names):
        raise MultiPremiseRefusal('incomplete dimensional declarations')
    for unit in types.values():
        if (not isinstance(unit,dict) or any(k not in BASES for k in unit) or
            any(type(v) is not int or abs(v)>16 for v in unit.values())):
            raise MultiPremiseRefusal('invalid dimensional declaration')
    premises=contract['premises']; witnesses=contract['witnesses']; conclusion=contract['conclusion']
    if (not isinstance(premises,list) or len(premises)!=2 or
        not isinstance(witnesses,list) or len(witnesses)!=2 or
        any(not isinstance(p,dict) or set(p)!={'lhs','rhs'} for p in premises) or
        not isinstance(conclusion,dict) or set(conclusion)!={'lhs','rhs'}):
        raise MultiPremiseRefusal('exactly two premises, two witnesses and one conclusion required')
    statement=contract['statement']; prefix='For all real scalars '+', '.join(names)+', if '
    if (not isinstance(statement,str) or len(statement)>4096 or
        not statement.startswith(prefix) or not statement.endswith(TAIL)):
        raise MultiPremiseRefusal('uncontrolled scientific statement or quantifier')
    middle=statement[len(prefix):-len(TAIL)]
    if middle.count(', then ')!=1:raise MultiPremiseRefusal('unsupported implication syntax')
    antecedent,after=middle.split(', then ')
    if antecedent.count(' and ')!=1 or not after.endswith(' holds.'):
        raise MultiPremiseRefusal('exactly two assumptions connected with and required')
    antecedents=antecedent.split(' and ')
    consequent=after[:-len(' holds.')]
    for text,p in zip(antecedents+[consequent],premises+[conclusion]):
        if text.count(' == ')!=1:raise MultiPremiseRefusal('invalid controlled equality')
        left,right=text.split(' == ')
        if _controlled(left,names)!=_read_formal(p['lhs'],names) or _controlled(right,names)!=_read_formal(p['rhs'],names):
            raise MultiPremiseRefusal('controlled text-formal SIDE MISMATCH')
    dims=[_equality_dim(p['lhs'],p['rhs'],names,types) for p in premises]
    dc=_equality_dim(conclusion['lhs'],conclusion['rhs'],names,types)
    p=[_add(_read_formal(r['lhs'],names),_neg(_read_formal(r['rhs'],names))) for r in premises]
    _independent_affine(p[0],p[1],len(names))
    target=_add(_read_formal(conclusion['lhs'],names),_neg(_read_formal(conclusion['rhs'],names)))
    w=[_read_formal(x,names) for x in witnesses]
    calculated=_add(_mul(w[0],p[0]),_mul(w[1],p[1]))
    if calculated!=target:
        raise MultiPremiseRefusal('invalid two-premise ideal-membership certificate')
    for i in range(2):
        wd=_typed(witnesses[i],types)
        if tuple(a+b for a,b in zip(dims[i],wd)) !=dc:
            raise MultiPremiseRefusal('witness product has inconsistent dimensions')
    digest=hashlib.sha256(json.dumps(contract,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
    return {'status':'TWO_INDEPENDENT_AFFINE_PREMISE_CERTIFICATE_VALID__PHYSICS_UNVERIFIED',
            'contract_sha256':digest, 'exact_ideal_membership_identity':True,
            'affine_gradient_rank':2,'controlled_text_formal_alignment_verified':True,
            'declared_dimensions_consistent':True,'physical_law_proven':False,
            'lean_kernel_verified':False,'empirical_validation_verified':False,
            'unrestricted_semantic_correctness':False,
            'scope':'Two nonredundant affine polynomial premises; polynomial witnesses; declared SI units; synthetic controlled text only'}
