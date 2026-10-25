"""PHYSQED v0.8: restricted conditional algebra / typed dimension gate.

Proves only a polynomial certificate C-D = W*(A-B) given a *single*
real-polynomial premise A=B. Text is accepted only in a controlled grammar
and must agree side-by-side with the supplied formal JSON expressions.
No physical dynamics, theorem originality, Lean kernel, or empirical validation.
"""
from __future__ import annotations
from fractions import Fraction
import hashlib
import json
import re
from engine import polynomial, unit_of, CertificationError, BASES
from controlled_semantics import (_parse_expression, _plus, _scale, _mult,
                                  ControlledLanguageRefusal)

VERSION='physqed-conditional-v0.8'
TAIL=' This checks only the conditional polynomial consequence; no physical law is established.'

class ConditionalRefusal(ValueError):
    pass


def _negative(p):
    return _scale(p, -1)


def _difference(a,b):
    return _plus(a,_negative(b))


def _formal(node,variables):
    try:
        return polynomial(node,variables)
    except (CertificationError,KeyError,TypeError,ValueError,OverflowError,RecursionError) as exc:
        raise ConditionalRefusal('invalid formal polynomial expression') from exc


def _dim_check(node,types):
    try:
        return unit_of(node,types)
    except (CertificationError,KeyError,TypeError,ValueError,OverflowError,RecursionError) as exc:
        raise ConditionalRefusal('dimension or formal-expression error') from exc


def _dim_equal(a,b,variables,types):
    da,db=_dim_check(a,types),_dim_check(b,types)
    pa,pb=_formal(a,variables),_formal(b,variables)
    # Literal polynomial zero has no intrinsic unit and is compatible with
    # the dimensional type of the other side. Non-zero constant 1 is not.
    if pa=={}: da=db
    if pb=={}: db=da
    if da!=db:raise ConditionalRefusal('incompatible physical dimensions')
    return da


def verify(contract):
    if not isinstance(contract,dict) or set(contract)!={'schema','statement','variables',
                                'dimensions','premise','conclusion','witness','provenance'}:
        raise ConditionalRefusal('invalid / incomplete v0.8 schema')
    if contract['schema']!=VERSION or contract['provenance']!='SYNTHETIC_SCOPED':
        raise ConditionalRefusal('unsupported schema or provenance class')
    variables=contract['variables']
    if (not isinstance(variables,list) or not 1<=len(variables)<=6 or
        any(not isinstance(v,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,18}',v)
            for v in variables) or len(set(variables))!=len(variables)):
        raise ConditionalRefusal('invalid variable declarations')
    types=contract['dimensions']
    if not isinstance(types,dict) or set(types)!=set(variables):
        raise ConditionalRefusal('dimension metadata must cover exactly declared variables')
    for name,d in types.items():
        if (not isinstance(d,dict) or any(b not in BASES for b in d) or
            any(type(k) is not int or abs(k)>16 for k in d.values())):
            raise ConditionalRefusal('invalid dimension declaration')
    prem,con=contract['premise'],contract['conclusion']
    if any(not isinstance(d,dict) or set(d)!={'lhs','rhs'} for d in (prem,con)):
        raise ConditionalRefusal('premise and conclusion each require exactly two sides')
    s=contract['statement']
    if not isinstance(s,str) or len(s)>4096:
        raise ConditionalRefusal('missing or excessive controlled text')
    prefix='For all real scalars '+', '.join(variables)+', if '
    if not s.startswith(prefix) or not s.endswith(TAIL):
        raise ConditionalRefusal('uncontrolled quantifier, scope or physical assertion')
    middle=s[len(prefix):-len(TAIL)]
    if middle.count(', then ')!=1:
        raise ConditionalRefusal('exactly one conditional implication required')
    antecedent,consequent=middle.split(', then ')
    if not consequent.endswith(' holds.'):
        raise ConditionalRefusal('unsupported consequent ending')
    consequent=consequent[:-len(' holds.')]
    if antecedent.count(' == ')!=1 or consequent.count(' == ')!=1:
        raise ConditionalRefusal('single premise and conclusion equality required')
    al,ar=antecedent.split(' == ')
    cl,cr=consequent.split(' == ')
    for formula,field in ((al,prem['lhs']),(ar,prem['rhs']),
                          (cl,con['lhs']),(cr,con['rhs'])):
        try:
            parsed=_parse_expression(formula,variables)
        except (ControlledLanguageRefusal,RecursionError,OverflowError,ZeroDivisionError) as exc:
            raise ConditionalRefusal('controlled expression parse refused') from exc
        if parsed!=_formal(field,variables):
            raise ConditionalRefusal('text-to-formal SIDE MISMATCH')
    dp=_dim_equal(prem['lhs'],prem['rhs'],variables,types)
    dc=_dim_equal(con['lhs'],con['rhs'],variables,types)
    pw=_formal(contract['witness'],variables)
    # Even though the statement is strict, the certificate is a sufficient
    # exact polynomial membership identity; one witness, one premise only.
    try:
        p=_difference(_formal(prem['lhs'],variables),_formal(prem['rhs'],variables))
        c=_difference(_formal(con['lhs'],variables),_formal(con['rhs'],variables))
        expanded_witness=_mult(p,pw)
    except ControlledLanguageRefusal as exc:
        raise ConditionalRefusal('polynomial expansion exceeded safe budget') from exc
    if len(p)==1 and tuple([0]*len(variables)) in p:
        raise ConditionalRefusal('inconsistent nonzero-constant premise')
    if not p and c:
        raise ConditionalRefusal('tautological premise cannot imply nonidentity')
    if expanded_witness!=c:
        raise ConditionalRefusal('invalid or missing polynomial implication witness')
    dw=_dim_check(contract['witness'],types)
    if tuple(a+b for a,b in zip(dp,dw))!=dc:
        # If both sides of implication are literal zero, dimension check remains
        # conservative rather than assigning a type to the zero polynomial.
        raise ConditionalRefusal('witness has incompatible dimensions')
    # A hash does not attest source authenticity or domain truth.
    digest=hashlib.sha256(json.dumps(contract,sort_keys=True,separators=(',',':'),
                        allow_nan=False).encode()).hexdigest()
    return {'status':'CONTROLLED_CONDITIONAL_POLYNOMIAL_IMPLICATION_PASSED__PHYSICS_UNVERIFIED',
            'contract_sha256':digest,'exact_single_premise_witness_verified':True,
            'controlled_text_formal_alignment_verified':True,
            'declared_dimensional_consistency_verified':True,
            'semantic_correctness_unrestricted':False,'physical_law_proven':False,
            'lean_kernel_verified':False,'experimental_evidence_verified':False,
            'limitations':'One exact polynomial premise, bounded grammar, self-declared units and model; not differential dynamics.'}
