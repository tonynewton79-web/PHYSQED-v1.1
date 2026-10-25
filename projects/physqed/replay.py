"""Independent exact-grid identity verifier. Intentionally no imports from engine.py.

For a polynomial P over Q of separate degree <= d_i in each variable,
P vanishes identically iff it vanishes on the Cartesian grid {0,...,d_i}.
This supplies a separate reasoning path from coefficient normalization.
"""
from fractions import Fraction
from itertools import product
from math import prod

class ReplayError(ValueError):
    pass

def rational(x):
    if isinstance(x, bool) or not isinstance(x, (str, int)):
        raise ReplayError('rationals must be strings or integers; floats forbidden')
    if len(str(x)) > 100:
        raise ReplayError('rational too large')
    try:
        return Fraction(x)
    except (ValueError, ZeroDivisionError) as exc:
        raise ReplayError('invalid rational') from exc

def degree(node, names, depth=0):
    if depth > 30 or not isinstance(node, dict):
        raise ReplayError('invalid expression depth/type')
    if set(node) == {'const'}:
        rational(node['const'])
        return (0,) * len(names)
    if set(node) == {'var'}:
        if node['var'] not in names:
            raise ReplayError('unknown variable')
        return tuple(int(v == node['var']) for v in names)
    op = node.get('op')
    if op == 'pow' and set(node) == {'op', 'arg', 'exp'}:
        n = node['exp']
        if isinstance(n, bool) or not isinstance(n, int) or not 0 <= n <= 8:
            raise ReplayError('unsupported exponent')
        return tuple(n * d for d in degree(node['arg'], names, depth+1))
    if op in ('add', 'mul') and set(node) == {'op', 'args'} and isinstance(node['args'], list) and 2 <= len(node['args']) <= 12:
        ds = [degree(a, names, depth+1) for a in node['args']]
        return tuple((max(v) if op == 'add' else sum(v)) for v in zip(*ds))
    raise ReplayError('unknown or malformed expression')

def evaluate(node, env):
    if 'const' in node:
        return rational(node['const'])
    if 'var' in node:
        return env[node['var']]
    if node['op'] == 'pow':
        return evaluate(node['arg'], env) ** node['exp']
    vals = [evaluate(x, env) for x in node['args']]
    return sum(vals, Fraction(0)) if node['op'] == 'add' else prod(vals)

def verify_identity(left, right, names, max_grid=5000):
    dl, dr = degree(left, names), degree(right, names)
    bounds = tuple(max(x,y) for x,y in zip(dl,dr))
    size = prod(d+1 for d in bounds)
    if size > max_grid:
        raise ReplayError('grid budget exceeded; identity not certified')
    for values in product(*(range(d+1) for d in bounds)):
        env = dict(zip(names, map(Fraction, values)))
        if evaluate(left, env) != evaluate(right, env):
            return {'verified': False, 'grid_points': size, 'counterexample': {k: str(v) for k,v in env.items()}}
    return {'verified': True, 'grid_points': size, 'degree_bounds': list(bounds)}
