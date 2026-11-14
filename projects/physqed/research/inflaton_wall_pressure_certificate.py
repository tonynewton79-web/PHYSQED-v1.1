"""Analytical wall tension and weak-bias pressure/self-gravity scale gate.

Exact within the unbiased quartic and its stationary biased minima. Pressure
radii use unbiased tension in a small-bias thin-wall approximation. This does
NOT certify wall annihilation, quantum fluctuations or 3+1 Einstein evolution.
"""
from __future__ import annotations
import json
import math
from pathlib import Path

DELTA = 0.016202803686105016
MU = 10.05
ALPHA = (4 + DELTA)/2
YC = 0.81
KAPPA = 10000.0
V = 3 - ALPHA**2/2
BETA = V / ((ALPHA - YC)**2 + 2*V)
LAM = KAPPA**2 / (4*BETA)
B = LAM - KAPPA**2/2
A = KAPPA*(ALPHA-YC)
ZV = math.sqrt(A/B)
TLOW = (2/3)*math.sqrt(2*B)*ZV**3
THIGH = (2/3)*math.sqrt(2*LAM)*ZV**3
XSTAR = 0.6730287364275626
SIGMA_Z = 3.8e-7
HSCREEN = KAPPA*(YC-XSTAR**2)*SIGMA_Z + LAM*SIGMA_Z**3
HCRIT = math.sqrt(16*KAPPA*V*(ALPHA-YC)/27)

def reduced(z, h):
    return V - A*z*z/2 + B*z**4/4 - h*z

def root(h, left, right, steps=100):
    f=lambda z: B*z**3-A*z-h
    fl,fr=f(left),f(right)
    assert fl*fr<0
    for _ in range(steps):
        mid=(left+right)/2
        if f(mid)*fl>0:
            left,fl=mid,f(mid)
        else:
            right,fr=mid,f(mid)
    return (left+right)/2

def gap(h):
    zm=root(h, -2*ZV,-.5*ZV)
    zp=root(h, .5*ZV,2*ZV)
    assert zm<0<zp
    return reduced(zm,h)-reduced(zp,h)

def run():
    assert 0 < B < LAM
    assert math.isclose(B, KAPPA**2*(ALPHA-YC)**2/(4*V), rel_tol=2e-14)
    assert .0338944<TLOW<.0338945
    assert .0521871<THIGH<.0521873
    assert 83.57385672072<HCRIT<83.57385672073
    assert .0013567228<HSCREEN<.0013567230
    rows=[]
    for h in (1e-5,1e-4,5e-4,HSCREEN):
        dV=gap(h)
        rcrit=(2*TLOW/dV,2*THIGH/dV)
        rgrav=(1/(MU**2*THIGH),1/(MU**2*TLOW))
        minratio=2*MU**2*TLOW**2/dV
        assert rcrit[0]>rgrav[1]
        assert abs(dV-2*h*ZV)/dV<1e-3
        rows.append(dict(h=h,exact_vacuum_gap=dV,
                         pressure_balance_radii=rcrit,
                         gravity_length_range=rgrav,
                         min_ratio_Rcrit_to_Rgrav=minratio))
    assert rows[-1]["min_ratio_Rcrit_to_Rgrav"]>4700
    assert rows[1]["min_ratio_Rcrit_to_Rgrav"]>64000
    return dict(schema="physqed.wall-tension-pressure-gravity.v1",
        status="PASS_UNBIASED_VARIATIONAL_TENSION_AND_THIN_WALL_SCALE_TEST",
        dimensionless_tension_bounds=[TLOW,THIGH],
        positive_biased_vacuum_splittings=rows,
        h_screen=HSCREEN,h_spinodal=HCRIT,
        wall_self_gravity_ignored=False,
        wall_pressure_collapse_proven=False,
        curvature_network_evolved=False,
        stochastic_initial_state_derived=False,
        caveat="Rcrit is a spherical true-bubble pressure balance, not a necessary radius for collapse of a false bubble; Rgrav is an order-one self-gravity scale.")

if __name__=="__main__":
    ans=run()
    Path("inflaton_wall_pressure_receipt.json").write_text(
        json.dumps(ans,indent=2,sort_keys=True)+"\n")
    print(json.dumps(ans,indent=2,sort_keys=True))
