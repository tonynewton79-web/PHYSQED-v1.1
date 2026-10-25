"""Second-route analytic and numerical oscillator audit, independent of Lean.
Not a replacement for Lean compilation and not experimental evidence.
"""
from math import cos, exp, isclose, sin, sqrt
from sympy import Function, Symbol, diff, expand, simplify


def independent_symbolic_replay():
    t = Symbol('t', real=True)
    m = Symbol('m', positive=True)
    k = Symbol('k', positive=True)
    c = Symbol('c', nonnegative=True)
    x = Function('x')(t)
    v = Function('v')(t)
    energy = (m*v**2+k*x**2)/2
    rate = diff(energy,t)
    actual_rate = expand(rate.subs({diff(x,t):v, diff(v,t):(-c*v-k*x)/m}))
    assert simplify(actual_rate + c*v**2) == 0
    assert simplify(actual_rate.subs(c,0)) == 0
    assert simplify(actual_rate.subs({c:1,v:1}) + 1) == 0
    # A false version with damping but zero energy derivative leaves a residual.
    assert simplify(actual_rate.subs({c:1,v:1})) == -1
    return {'identity': 'dE/dt=-c*v^2', 'passed':True, 'method':'SymPy differentiation and separate ODE substitution'}


def trajectory(t,m,k,c,x0=1.,v0=0.3):
    gamma = c/(2*m)
    w0sq = k/m
    wdsq = w0sq-gamma**2
    if wdsq <= 0:
        raise ValueError('analytic formula restricted to underdamped oscillator')
    wd = sqrt(wdsq)
    beta = (v0+gamma*x0)/wd
    osc = x0*cos(wd*t)+beta*sin(wd*t)
    oscprime = -x0*wd*sin(wd*t)+beta*wd*cos(wd*t)
    factor=exp(-gamma*t)
    return factor*osc, factor*(oscprime-gamma*osc)


def energy(m,k,x,v):
    return (m*v*v+k*x*x)/2


def numerical_replay():
    m,k=2.,8.
    for c in [0.,1.]:
        grid=[j/100. for j in range(301)]
        vals=[]
        for t in grid:
            x,v=trajectory(t,m,k,c)
            vals.append(energy(m,k,x,v))
        if c == 0:
            assert max(vals)-min(vals) < 1e-12
        else:
            assert vals[-1] < vals[0]-0.1
            assert all(vals[i+1] <= vals[i]+1e-12 for i in range(len(vals)-1))
            # Exact integral balance independently approximated by trapezoids
            samples=[trajectory(t,m,k,c)[1]**2 for t in grid]
            integral=sum(0.01*(samples[i]+samples[i+1])/2 for i in range(len(samples)-1))
            assert abs((vals[-1]-vals[0])+c*integral)<0.0003
    return {'undamped_constant':True, 'damped_decreases':True,
            'balance_integral_tolerance':0.0003, 'method':'closed-form trajectory and independent trapezoid quadrature'}


def main():
    assert independent_symbolic_replay()['passed']
    assert numerical_replay()['damped_decreases']
    print('PASS: SymPy analytic proof check; undamped and damped trajectory replay; false conservation control refused')

if __name__=='__main__':
    main()
