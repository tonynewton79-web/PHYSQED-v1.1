"""PHYSQED 0.1: fail-closed proof-component checks, NOT physics-law certification.

All computations use exact rational arithmetic; no eval or code execution.
Inputs are declarative JSON, not uploaded Python programs.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from replay import ReplayError, verify_identity

BASES = ('M', 'L', 'T', 'I', 'Theta', 'N', 'J')
VERSION = 'physqed-0.1'

class CertificationError(ValueError):
    pass

def digest(data):
    return hashlib.sha256(data).hexdigest()

def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('utf-8')

def rational(x):
    if isinstance(x, bool) or not isinstance(x, (str, int)) or len(str(x)) > 100:
        raise CertificationError('use bounded string/int exact rationals, never floats')
    try:
        return Fraction(x)
    except (ValueError, ZeroDivisionError) as exc:
        raise CertificationError('invalid rational literal') from exc

def dimension(x):
    if not isinstance(x, dict) or any(k not in BASES for k in x):
        raise CertificationError('invalid SI base-dimension vector')
    if any(isinstance(v, bool) or not isinstance(v, int) or abs(v) > 32 for v in x.values()):
        raise CertificationError('dimension exponents must be small integers')
    return tuple(x.get(k, 0) for k in BASES)

def unit_of(expr, variable_units, depth=0):
    if depth > 30 or not isinstance(expr, dict):
        raise CertificationError('invalid expression')
    if set(expr) == {'const'}:
        rational(expr['const'])
        return (0,)*len(BASES)
    if set(expr) == {'var'}:
        if expr['var'] not in variable_units:
            raise CertificationError('variable without declared dimension')
        return dimension(variable_units[expr['var']])
    if set(expr) == {'op','arg','exp'} and expr['op'] == 'pow':
        n = expr['exp']
        if type(n) is not int or not 0 <= n <= 8:
            raise CertificationError('unsupported exponent')
        return tuple(n*v for v in unit_of(expr['arg'], variable_units, depth+1))
    if set(expr) == {'op','args'} and expr['op'] in ('add', 'mul') and isinstance(expr['args'], list) and 2 <= len(expr['args']) <= 12:
        ds = [unit_of(a, variable_units, depth+1) for a in expr['args']]
        if expr['op'] == 'add':
            if len(set(ds)) != 1:
                raise CertificationError('addition of incompatible physical dimensions')
            return ds[0]
        return tuple(sum(v) for v in zip(*ds))
    raise CertificationError('unknown expression operator or unexpected keys')

def combine(p, q, multiply=False):
    out = dict(p)
    if multiply:
        out = {}
        for a, av in p.items():
            for b, bv in q.items():
                key = tuple(x+y for x,y in zip(a,b))
                out[key] = out.get(key, Fraction(0)) + av*bv
                if len(out) > 512:
                    raise CertificationError('polynomial term budget exceeded')
    else:
        for b, v in q.items():
            out[b] = out.get(b, Fraction(0)) + v
    return {k:v for k,v in out.items() if v != 0}

def polynomial(node, names, depth=0):
    if depth > 30 or not isinstance(node, dict):
        raise CertificationError('invalid expression')
    zero = (0,)*len(names)
    if set(node) == {'const'}:
        c = rational(node['const'])
        return {zero: c} if c else {}
    if set(node) == {'var'}:
        if node['var'] not in names:
            raise CertificationError('undeclared variable')
        return {tuple(int(k == node['var']) for k in names): Fraction(1)}
    if set(node) == {'op','arg','exp'} and node['op'] == 'pow':
        n = node['exp']
        if type(n) is not int or not 0 <= n <= 8:
            raise CertificationError('invalid exponent')
        p = polynomial(node['arg'], names, depth+1)
        acc = {zero: Fraction(1)}
        for _ in range(n):
            acc = combine(acc, p, True)
        return acc
    if set(node) == {'op','args'} and node['op'] in ('add','mul') and isinstance(node['args'], list) and 2 <= len(node['args']) <= 12:
        op = node['op']
        acc = {} if op == 'add' else {zero:Fraction(1)}
        for a in node['args']:
            acc = combine(acc, polynomial(a, names, depth+1), op == 'mul')
        return acc
    raise CertificationError('unknown expression operator or unexpected keys')

def check(spec):
    kind = spec.get('kind')
    left, right = spec.get('lhs'), spec.get('rhs')
    if kind == 'dimension_equality':
        variables = spec.get('variables')
        if not isinstance(variables, dict) or len(variables) > 6:
            raise CertificationError('invalid variable dimensions')
        lhs, rhs = unit_of(left, variables), unit_of(right, variables)
        return {'kind': kind, 'passed':lhs == rhs,
                'note':'Dimensional consistency ONLY; not a proof of the physical equation',
                'lhs_dimension':list(lhs), 'rhs_dimension':list(rhs)}
    if kind == 'algebra_identity':
        variables = spec.get('variables')
        if not isinstance(variables, list) or not 1 <= len(variables) <= 6 or len(set(variables)) != len(variables) or any(not isinstance(v,str) or not v.isidentifier() for v in variables):
            raise CertificationError('invalid polynomial variable list')
        l, r = polynomial(left, variables), polynomial(right, variables)
        replay = verify_identity(left, right, variables)
        return {'kind':kind, 'passed':l == r and replay['verified'],
                'independent_replay':replay,
                'note':'Exact polynomial identity only; physical assumptions are not discharged'}
    raise CertificationError('unknown check kind; refusing to certify')

def certify(claim):
    if not isinstance(claim, dict) or claim.get('schema_version') != VERSION:
        raise CertificationError('unrecognised schema version')
    if not isinstance(claim.get('id'),str) or not claim['id'] or len(claim['id']) > 100:
        raise CertificationError('missing/invalid claim identifier')
    if not isinstance(claim.get('statement'),str) or not claim['statement'].strip():
        raise CertificationError('missing natural-language statement')
    if not isinstance(claim.get('assumptions'),list) or any(not isinstance(x,str) for x in claim['assumptions']):
        raise CertificationError('assumptions must be declared in an array')
    if not isinstance(claim.get('source'),str) or not claim['source']:
        raise CertificationError('source/provenance is required')
    items = claim.get('checks')
    if not isinstance(items,list) or not 1 <= len(items) <= 30:
        raise CertificationError('need 1-30 checks')
    results = []
    for i, spec in enumerate(items):
        try:
            if not isinstance(spec,dict):
                raise CertificationError('check must be object')
            result = check(spec)
        except (CertificationError, ReplayError, KeyError, TypeError, OverflowError) as exc:
            result = {'kind':spec.get('kind','unknown') if isinstance(spec,dict) else 'unknown',
                      'passed':False, 'error':str(exc)}
        results.append({'index':i, **result})
    passed = all(r['passed'] for r in results)
    only_dims = all(r['kind'] == 'dimension_equality' for r in results)
    status = ('REJECTED' if not passed else 'CONSISTENCY_CHECKS_PASSED' if only_dims else 'MATHEMATICAL_COMPONENTS_VERIFIED')
    src = Path(__file__).read_bytes()
    other = Path(__file__).with_name('replay.py').read_bytes()
    cert = {'schema_version':VERSION, 'claim_id':claim['id'], 'statement':claim['statement'],
            'assumptions':claim['assumptions'], 'source':claim['source'], 'status':status,
            'physical_law_proven':False, 'lean_kernel_verified':False,
            'verification_scope':'finite exact checks, with independent polynomial grid replay',
            'input_sha256':digest(canonical(claim)), 'engine_sha256':digest(src),
            'replay_sha256':digest(other), 'checks':results,
            'hash_note':'SHA256 confirms integrity, NOT reviewer identity or authenticity'}
    cert['certificate_sha256'] = digest(canonical(cert))
    return cert

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        claim = json.loads(args.input.read_text(encoding='utf-8'), parse_float=lambda x: (_ for _ in ()).throw(CertificationError('floating point input forbidden')))
        result = certify(claim)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'PHYSQED REFUSED: {exc}\n')
    body = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(body,encoding='utf-8')
    else:
        print(body,end='')
    return 0 if result['status'] != 'REJECTED' else 2

if __name__ == '__main__':
    raise SystemExit(main())
