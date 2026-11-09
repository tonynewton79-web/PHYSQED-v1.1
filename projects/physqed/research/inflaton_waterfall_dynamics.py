#!/usr/bin/env python3
"""Research-only flat-FLRW inflaton/waterfall/radiation evolution.

This is distinct from the PHYSQED exact conservative Lagrangian receipt:
Gamma is an externally imposed nonnegative energy-transfer law, not derived
from ABJM, QFT, or the conservative minisuperspace action.
Units: tau = Lambda^2 * physical_time / mu; x=phi/mu; z=chi/mu;
R=rho_r/Lambda^4; h=H*mu/Lambda^2; N=log(scale_factor).
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

DELTA=0.016202803686105016
A=(4+DELTA)/2
MU=10.05
YC=0.81
XC=math.sqrt(YC)
V=3-A*A/2
BETA=V/((A-YC)**2+2*V)
KAPPA=10000.0
LAM=KAPPA**2/(4*BETA)
YV=(A-2*BETA*YC)/(1-2*BETA)
XV=math.sqrt(YV)
ZV=math.sqrt(KAPPA/LAM*(YV-YC))


def potential(x,z):
    return 3-A*x*x+0.5*x**4+0.5*KAPPA*(YC-x*x)*z*z+0.25*LAM*z**4


def gradient(x,z):
    return (2*x*(x*x-A)-KAPPA*x*z*z,
            (KAPPA*(YC-x*x)+LAM*z*z)*z)


def energy_and_hubble(y):
    x,vx,z,vz,R,N=y
    E=potential(x,z)+0.5*(vx*vx+vz*vz)+R
    if not math.isfinite(E) or E<=0:
        raise ArithmeticError("Nonpositive/invalid FRW energy")
    return E, MU*math.sqrt(E/3)


def derivative(tau,y,gphi,gchi,width=0.005):
    x,vx,z,vz,R,N=y
    E,h=energy_and_hubble(y)
    ux,uz=gradient(x,z)
    switch=0.5*(1+math.tanh((x-XC)/width))
    gp,gc=gphi*switch,gchi*switch
    return (vx,-(3*h+gp)*vx-ux,
            vz,-(3*h+gc)*vz-uz,
            -4*h*R+gp*vx*vx+gc*vz*vz,h)


def start_at_pivot():
    from scipy.optimize import brentq
    def r_target(x):
        w=potential(x,0)
        wx=gradient(x,0)[0]
        return 8*(wx/(MU*w))**2-0.02629
    x=brentq(r_target,.1,.8)
    w=potential(x,0)
    wx=gradient(x,0)[0]
    h=MU*math.sqrt(w/3)
    for _ in range(12):
        vx=-wx/(3*h)
        h=MU*math.sqrt((w+vx*vx/2)/3)
    return (x,vx,0,0,0,0)


def run_case(gamma,seed=1e-7,post_duration=55.0,rtol=2e-8,atol=5e-11):
    from scipy.integrate import solve_ivp
    def hit_waterfall(t,y):
        return y[0]-XC
    hit_waterfall.terminal=True
    hit_waterfall.direction=1
    early=solve_ivp(lambda t,y:derivative(t,y,0,0),
                    (0,20),start_at_pivot(),events=hit_waterfall,
                    method="DOP853",rtol=rtol,atol=atol,max_step=.025)
    if not early.success or not len(early.t_events[0]):
        raise AssertionError("Pivot trajectory failed to hit waterfall")
    t0=float(early.t_events[0][0])
    y0=early.y_events[0][0].copy()
    n_water=float(y0[5])
    # A stated stochastic fluctuation proxy injected at the threshold;
    # injected potential energy is lambda*seed**4/4, not exactly zero.
    y0[2]=seed
    late=solve_ivp(lambda t,y:derivative(t,y,gamma,gamma),
                   (t0,t0+post_duration),y0,method="Radau",
                   rtol=rtol,atol=atol,max_step=.2)
    if not late.success:
        raise AssertionError(late.message)
    end_cross=None
    rad_cross=None
    rad_max=0.0
    final_frac=0.0
    prev_eps=None
    for i in range(len(late.t)):
        y=late.y[:,i]
        E,h=energy_and_hubble(y)
        x,vx,z,vz,R,N=y
        if R < -1e-7*E:
            raise AssertionError("Negative radiation energy")
        frac=R/E
        kinetic=(vx*vx+vz*vz)/2
        eps=(3*kinetic+2*R)/E
        if end_cross is None and eps>1:
            end_cross=float(N)
        if rad_cross is None and frac>.9:
            rad_cross=float(N)
        rad_max=max(rad_max,frac)
        final_frac=frac
    return dict(gamma_phi=gamma,gamma_chi=gamma,seed=seed,
                waterfall_efolds=n_water,first_epsilonH_above_one=end_cross,
                first_radiation_fraction_above_90pct=rad_cross,
                final_radiation_fraction=final_frac,
                max_radiation_fraction=rad_max,
                final_efolds=float(late.y[5,-1]),
                final_x=float(late.y[0,-1]),final_z=float(late.y[2,-1]),
                inserted_seed_energy_over_Lambda4=LAM*seed**4/4,
                duration_after_threshold=post_duration,
                numerical_steps=len(late.t))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,default=Path("inflaton_waterfall_receipt.json"))
    p.add_argument("--post-duration",type=float,default=55)
    args=p.parse_args()
    if args.post_duration<1 or args.post_duration>200:
        raise ValueError("post-duration outside bounded research window")
    cases=[run_case(g,post_duration=args.post_duration) for g in (0,15,30)]
    assert all(54<c["waterfall_efolds"]<57 for c in cases)
    assert all(c["first_epsilonH_above_one"] is not None for c in cases)
    assert cases[0]["max_radiation_fraction"]==0
    assert cases[1]["max_radiation_fraction"]>.9
    assert cases[2]["max_radiation_fraction"]>.5
    result={
      "schema":"physqed.inflaton-dynamics.research.v1",
      "status":"NUMERICAL_BENCHMARK_ONLY__NO_HOLOGRAPHIC_OR_REHEATING_THEOREM",
      "assumptions":["canonical flat FLRW fields","imposed smooth dissipation after threshold",
                     "seeded chi fluctuation at x=xc","no metric/field quantum fluctuations",
                     "radiation is a phenomenological perfect-fluid bath"],
      "parameters":{"mu_over_Mpl":MU,"delta":DELTA,"yc":YC,
                    "kappa":KAPPA,"lambda":LAM,"vacuum_x":XV,"vacuum_abs_z":ZV},
      "cases":cases}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
