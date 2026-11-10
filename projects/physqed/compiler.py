"""PHYSQED 0.2 structured physics-statement compiler (experimental).

Design contract: checks a *declared formalisation*, not the meaning of English
or the truth of a physical assumption. Full scientific certification is excluded.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path

from engine import BASES, CertificationError, canonical, dimension, digest, polynomial, unit_of
from replay import ReplayError, verify_identity

SCHEMA = 'physqed-contract-0.2'
IDENT = re.compile(r'^[A-Za-z][A-Za-z0-9_]*$')
RESERVED = {'by','theorem','end','namespace','open','import','Mathlib','axiom',
            'sorry','admit','notation','instance','attribute','variable','section',
            'class','where','do','let','if','then','else','in','fun','match','with',
            'exact','ring','linear_combination','Type','Prop','True','False','self'}

# Fixed, publicly auditable unit and meaning registry. No caller may redefine it.
SI_UNITS = {
    '1': {}, 'kg': {'M':1}, 'm':{'L':1}, 's':{'T':1},
    'm/s':{'L':1,'T':-1}, 'm/s^2':{'L':1,'T':-2},
    'N':{'M':1,'L':1,'T':-2}, 'N/m':{'M':1,'T':-2},
    'J':{'M':1,'L':2,'T':-2}, 'W':{'M':1,'L':2,'T':-3},
    'Hz':{'T':-1},
}
ROLE_UNITS = {
    'dimensionless': '1', 'mass': 'kg', 'position':'m', 'velocity':'m/s',
    'acceleration':'m/s^2', 'time':'s', 'force':'N', 'stiffness':'N/m',
    'energy':'J', 'energy_rate':'W', 'frequency':'Hz',
}
CONTEXT_FIELDS = ('domain','frame','regime','regularity','boundary_conditions','gauge')

class ContractError(CertificationError):
    pass

def expect_keys(data, expected, label):
    if not isinstance(data, dict) or set(data) != set(expected):
        raise ContractError(f'{label}: expected exactly {list(expected)}')

def nonblank(x, label, limit=2000):
    if not isinstance(x, str) or not x.strip() or len(x) > limit:
        raise ContractError(f'{label}: required nonblank bounded text')
    return x

def identifier(x, label):
    if not isinstance(x, str) or len(x) > 45 or not IDENT.fullmatch(x) or x in RESERVED or x.startswith('h_'):
        raise ContractError(f'{label}: invalid or reserved identifier')
    return x

def sum_expr(args):
    return {'op':'add','args':args}

def mul_expr(args):
    return {'op':'mul','args':args}

def sub_expr(left,right):
    return sum_expr([left,mul_expr([{'const':'-1'},right])])

def poly_sub(left,right,names):
    lp,rp=polynomial(left,names),polynomial(right,names)
    delta=dict(lp)
    for k,v in rp.items():
        delta[k]=delta.get(k,Fraction(0))-v
    return {k:v for k,v in delta.items() if v}

def check_metadata(contract):
    expect_keys(contract,('contract_version','id','statement','provenance','context',
                          'symbols','assumptions','conclusions','proofs','mapping'), 'contract')
    if contract['contract_version'] != SCHEMA:
        raise ContractError('unknown contract schema version')
    identifier(contract['id'],'claim id')
    nonblank(contract['statement'],'statement')
    expect_keys(contract['provenance'], ('source_uri','origin_kind'),'provenance')
    nonblank(contract['provenance']['source_uri'],'source URI')
    if contract['provenance']['origin_kind'] not in ('synthetic','published','unpublished','experiment'):
        raise ContractError('unknown provenance origin (not authenticated)')
    expect_keys(contract['context'], CONTEXT_FIELDS,'physics context')
    for field in CONTEXT_FIELDS:
        nonblank(contract['context'][field],'context.'+field)
    expect_keys(contract['mapping'],('statement_conclusion_ids','explanation'),'mapping')
    nonblank(contract['mapping']['explanation'],'self-declared semantic mapping')
    if not isinstance(contract['symbols'],list) or not 1 <= len(contract['symbols']) <= 6:
        raise ContractError('1-6 typed symbols required')
    variables={}
    for symbol in contract['symbols']:
        expect_keys(symbol,('name','role','unit','meaning'),'symbol')
        name=identifier(symbol['name'],'symbol name')
        nonblank(symbol['meaning'],'symbol meaning')
        if name in variables:
            raise ContractError('duplicate symbol name')
        role=symbol['role']
        if role not in ROLE_UNITS or symbol['unit'] != ROLE_UNITS[role]:
            raise ContractError(f'symbol {name}: unit does not match controlled physical role')
        variables[name]=SI_UNITS[symbol['unit']]
    return variables

def check_equation(eq, variables, kind):
    fields=('id','meaning','lhs','rhs','source') if kind == 'assumption' else ('id','meaning','lhs','rhs')
    expect_keys(eq,fields,kind)
    id_=identifier(eq['id'],f'{kind} id')
    nonblank(eq['meaning'],f'{kind} meaning')
    if kind=='assumption':
        nonblank(eq['source'],'assumption source')
    a,b=unit_of(eq['lhs'],variables),unit_of(eq['rhs'],variables)
    # Zero is dimension-polymorphic, provided it is the literal exact 0.
    if eq['lhs'] == {'const':'0'} or eq['lhs'] == {'const':0}:
        a=b
    if eq['rhs'] == {'const':'0'} or eq['rhs'] == {'const':0}:
        b=a
    if a!=b:
        raise ContractError(f'{id_}: inconsistent SI dimensions {a} != {b}')
    # Full syntax and complexity check separate from unit lint.
    names=list(variables)
    delta=poly_sub(eq['lhs'],eq['rhs'],names)
    if kind == 'assumption' and len(delta)==1 and all(k==0 for k in next(iter(delta))):
        raise ContractError(f'{id_}: explicitly contradictory constant assumption')
    return id_,delta,a

def render_lean_expr(node):
    if 'const' in node:
        r=Fraction(node['const'])
        return f'({r.numerator} : ℝ)' if r.denominator==1 else f'(({r.numerator} : ℝ) / ({r.denominator} : ℝ))'
    if 'var' in node:
        return node['var']
    if node['op']=='pow':
        return f'({render_lean_expr(node["arg"])} ^ {node["exp"]})'
    sep=' + ' if node['op']=='add' else ' * '
    return '(' + sep.join(render_lean_expr(a) for a in node['args']) + ')'

def compile_contract(contract):
    variables=check_metadata(contract)
    assumptions=contract['assumptions']
    conclusions=contract['conclusions']
    proofs=contract['proofs']
    if not isinstance(assumptions,list) or len(assumptions)>12:
        raise ContractError('invalid assumptions array')
    if not isinstance(conclusions,list) or not 1<=len(conclusions)<=10:
        raise ContractError('1-10 conclusions required')
    if not isinstance(proofs,list) or len(proofs)!=len(conclusions):
        raise ContractError('every conclusion requires exactly one proof obligation')
    names=list(variables)
    prior={}
    cons={}
    units={}
    for eq in assumptions:
        name,delta,u=check_equation(eq,variables,'assumption')
        if name in prior:
            raise ContractError('duplicate assumption id')
        prior[name]=delta
        units[name]=u
    for eq in conclusions:
        name,delta,u=check_equation(eq,variables,'conclusion')
        if name in cons or name in prior:
            raise ContractError('duplicate/colliding equation id')
        cons[name]=delta
        units[name]=u
    targets=contract['mapping']['statement_conclusion_ids']
    if not isinstance(targets,list) or len(targets)!=len(cons) or len(set(targets))!=len(targets) or set(targets)!=set(cons):
        raise ContractError('claim-to-equation mapping must enumerate exactly all conclusions')
    # Reject a direct replay of an assumption as a purported derived theorem.
    for cid,cvalue in cons.items():
        if cvalue and any(cvalue==a or cvalue=={k:-v for k,v in a.items()} for a in prior.values()):
            raise ContractError(f'{cid}: conclusion merely restates an assumption')
    results=[]
    lean_parts=['import Mathlib',
                '/- Auto-generated by PHYSQED 0.2; all physical premises are explicit hypotheses. -/',
                '', 'namespace PHYSQEDGenerated','']
    seen=set()
    for p in proofs:
        expect_keys(p,('conclusion_id','method','multipliers'),'proof obligation')
        id_=identifier(p['conclusion_id'],'proof conclusion')
        if id_ not in cons or id_ in seen:
            raise ContractError('missing/duplicate/undeclared conclusion proof')
        seen.add(id_)
        method=p['method']
        if method not in ('polynomial_identity','assumption_combination'):
            raise ContractError(f'{id_}: unsupported proof method')
        witnesses=p['multipliers']
        if not isinstance(witnesses,dict) or (method=='polynomial_identity' and witnesses) or (method=='assumption_combination' and (not witnesses or len(witnesses)>len(prior))):
            raise ContractError(f'{id_}: malformed or missing witnesses')
        if any(x not in prior for x in witnesses):
            raise ContractError(f'{id_}: witness cites non-assumption or other conclusion')
        # An explicit and independently replayed exact polynomial equality:
        # conclusion(lhs - rhs) == sum_i witness_i*(assumption_i lhs - rhs).
        terms=[]
        for aid,witness in sorted(witnesses.items()):
            polynomial(witness,names)
            au=units[aid]
            cu=units[id_]
            wu=unit_of(witness,variables)
            if tuple(x+y for x,y in zip(au,wu))!=cu:
                raise ContractError(f'{id_}: witness {aid} has wrong physical dimensions')
            eq=next(e for e in assumptions if e['id']==aid)
            terms.append(mul_expr([witness,sub_expr(eq['lhs'],eq['rhs'])]))
        target=next(e for e in conclusions if e['id']==id_)
        candidate=sum_expr(terms+[{'const':'0'}]) if terms else {'const':'0'}
        left=sub_expr(target['lhs'],target['rhs'])
        try:
            same=poly_sub(left,candidate,names)=={}
            replay=verify_identity(left,candidate,names,max_grid=5000)
        except (CertificationError,ReplayError) as exc:
            results.append({'conclusion_id':id_,'passed':False,'reason':str(exc)})
            continue
        valid=same and replay['verified']
        results.append({'conclusion_id':id_,'method':method,'passed':valid,'replay':replay,
                        'assumptions_used':sorted(witnesses),'unit_dimension':list(units[id_]),
                        'scope':'conditional polynomial consequence, not physical verification'})
        if valid:
            hypotheses=[e for e in assumptions if e['id'] in witnesses]
            all_symbols=' '.join(names)
            args=' '.join(f'(h_{e["id"]} : {render_lean_expr(e["lhs"])} = {render_lean_expr(e["rhs"])})' for e in hypotheses)
            lean_parts.append(f'theorem {id_} ({all_symbols} : ℝ) {args} :')
            lean_parts.append(f'    {render_lean_expr(target["lhs"])} = {render_lean_expr(target["rhs"])} := by')
            if method=='polynomial_identity':
                lean_parts.append('  ring')
            else:
                linear=' + '.join(f'({render_lean_expr(witnesses[e["id"]])}) * h_{e["id"]}' for e in hypotheses)
                lean_parts.append(f'  linear_combination {linear}')
            lean_parts.append('')
    if seen!=set(cons):
        raise ContractError('missing proof obligations')
    passed=all(x['passed'] for x in results)
    lean_parts.append('end PHYSQEDGenerated')
    lean='\n'.join(lean_parts)+'\n' if passed else None
    out={
      'contract_version':SCHEMA,'claim_id':contract['id'],
      'status':'DERIVATION_CHECKED__SEMANTIC_REVIEW_REQUIRED' if passed else 'REJECTED',
      'physical_law_proven':False,'lean_kernel_verified':False,
      'semantic_alignment_verified':False,'physics_assumptions_established':False,
      'human_statement':contract['statement'],
      'structured_conclusions':sorted(cons),
      'declared_assumptions':sorted(prior),
      'declared_context':contract['context'],
      'mapping_statement':'Mapping to natural language is SELF-DECLARED and NOT verified.',
      'claims_of_nature':'No empirical data or physical model adequacy assessed.',
      'proof_checks':results,
      'source_provenance':contract['provenance'],
      'input_sha256':digest(canonical(contract)),
      'compiler_sha256':digest(Path(__file__).read_bytes()),
      'engine_sha256':digest(Path(__file__).with_name('engine.py').read_bytes()),
      'replay_sha256':digest(Path(__file__).with_name('replay.py').read_bytes()),
      'lean_source_sha256':digest(lean.encode('utf-8')) if lean else None,
      'security_note':'Hashes prove file identity only; neither source authentication nor correctness of translation.',
    }
    out['report_sha256']=digest(canonical(out))
    return out,lean

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input',type=Path)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--lean-output',type=Path)
    ns=ap.parse_args()
    try:
        claim=json.loads(ns.input.read_text(encoding='utf-8'),
            parse_float=lambda _: (_ for _ in ()).throw(ContractError('floating-point JSON literals forbidden')),
            parse_constant=lambda _: (_ for _ in ()).throw(ContractError('nonfinite literals forbidden')))
        report,lean=compile_contract(claim)
    except (ValueError,OSError,KeyError,TypeError,OverflowError,RecursionError) as exc:
        ap.exit(2,f'PHYSQED COMPILER REFUSED: {exc}\n')
    body=json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+'\n'
    if ns.output:
        ns.output.write_text(body,encoding='utf-8')
    else:
        print(body,end='')
    if lean and ns.lean_output:
        ns.lean_output.write_text(lean,encoding='utf-8')
    return 0 if report['status']!='REJECTED' else 2

if __name__=='__main__':
    raise SystemExit(main())
