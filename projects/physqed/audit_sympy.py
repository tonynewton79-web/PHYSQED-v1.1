"""Independent external symbolic audit for oscillator fixture.

Intentionally imports neither PHYSQED engine, compiler nor replay.
It reads the original contract and reconstructs exact equations from ASTs.
"""
import copy
import json
from pathlib import Path
from sympy import Rational, symbols, expand

CONTRACT=Path(__file__).with_name('fixtures')/'oscillator_contract.json'

def expr(node,env):
    if set(node)=={'const'}:
        return Rational(str(node['const']))
    if set(node)=={'var'}:
        return env[node['var']]
    if set(node)=={'op','arg','exp'} and node['op']=='pow':
        return expr(node['arg'],env)**node['exp']
    if set(node)=={'op','args'} and node['op']=='add':
        return sum(map(lambda a: expr(a,env),node['args']),Rational(0))
    if set(node)=={'op','args'} and node['op']=='mul':
        value=Rational(1)
        for a in node['args']: value*=expr(a,env)
        return value
    raise ValueError('unknown source expression')

def residue(claim):
    names=[s['name'] for s in claim['symbols']]
    vars=dict(zip(names,symbols(' '.join(names))))
    a=claim['assumptions'][0]
    c=claim['conclusions'][0]
    w=claim['proofs'][0]['multipliers'][a['id']]
    premise=expr(a['lhs'],vars)-expr(a['rhs'],vars)
    target=expr(c['lhs'],vars)-expr(c['rhs'],vars)
    return expand(target-expr(w,vars)*premise),premise,target

def main():
    claim=json.loads(CONTRACT.read_text())
    diff,premise,target=residue(claim)
    assert diff==0,(diff,'good fixture mismatched')
    assert premise!=0 and target!=0,'fixture became trivial or vacuous'
    hacked=copy.deepcopy(claim)
    hacked['proofs'][0]['multipliers'][hacked['assumptions'][0]['id']]={'op':'mul','args':[{'const':'2'},{'var':'v'}]}
    wrong,*_=residue(hacked)
    assert wrong!=0,'forged witness was not rejected by independent algebra'
    flipped=copy.deepcopy(claim)
    flipped['conclusions'][0]['lhs']['args'][0]['args'].insert(0,{'const':'-1'})
    wrong,*_=residue(flipped)
    assert wrong!=0,'wrong-sign control unexpectedly survived'
    print('SYMPY-INDEPENDENT AUDIT PASS: exact residue=0; forged multiplier/sign residues != 0')

if __name__ == '__main__': main()
