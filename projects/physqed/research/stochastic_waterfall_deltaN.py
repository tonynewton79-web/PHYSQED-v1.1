"""Scoped Gaussian-seed separate-universe waterfall diagnostic.

No 3D quantum-vacuum covariance, pointwise ADM constraint propagation,
metric backreaction, microscopic reheating, or CMB-scale spectrum is claimed.
"""
from __future__ import annotations
import argparse
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import zeta
from scipy.stats import skew, kurtosis
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research import inflaton_waterfall_dynamics as m

def epsilon(y):
    e,h=m.energy_and_hubble(y)
    return 1.5*(y[1]**2+y[3]**2)/e+2*y[4]/e

def initial_at_pivot(x):
    w=m.potential(x,0)
    ux=m.gradient(x,0)[0]
    h=m.MU*math.sqrt(w/3)
    for _ in range(12):
        v=-ux/(3*h)
        h=m.MU*math.sqrt((w+v*v/2)/3)
    return np.array([x,v,0.,0.,0.,0.])

def event(f,direction=-1):
    def ev(t,y):return f(y)
    ev.terminal=True
    ev.direction=direction
    return ev

def compute(n=96,seed=2609):
    opts=dict(rtol=5e-8,atol=5e-10,max_step=.03)
    def rhs(t,y):return m.derivative(t,y,0.,0.)
    pre=solve_ivp(rhs,(0,20),initial_at_pivot(.6730287364275626),
                  method="DOP853",events=event(lambda y:y[0]-m.XC,+1),**opts)
    if not pre.success or len(pre.t_events[0])!=1:
        raise RuntimeError("Missing reference waterfall crossing")
    yw=pre.y_events[0][0].copy()
    yw[2]=1e-7
    post=solve_ivp(rhs,(0,14),yw,method="DOP853",
                   events=event(lambda y:epsilon(y)-1,+1),**opts)
    if not post.success or len(post.t_events[0])!=1:
        raise RuntimeError("Missing reference first epsilon_H=1 crossing")
    target=m.energy_and_hubble(post.y_events[0][0])[0]
    def stop_at_energy(z):
        y=yw.copy()
        y[2]=z
        y[-1]=0.
        sol=solve_ivp(rhs,(0,14),y,method="DOP853",
            events=event(lambda u:m.energy_and_hubble(u)[0]-target,-1),**opts)
        if not sol.success or len(sol.t_events[0])!=1:
            raise RuntimeError("Seed did not reach reference energy")
        return float(sol.y_events[0][0][-1])
    reference=stop_at_energy(1e-7)
    rng=np.random.default_rng(seed)
    seeds=rng.normal(0.,3.8e-7,n)
    shifts=np.array([stop_at_energy(float(z))-reference for z in seeds])
    corr=float(np.corrcoef(np.log(np.abs(seeds)),shifts)[0,1])
    sd=float(np.std(shifts))
    if not (.004<sd<.05 and corr<-.995 and skew(shifts)>0):
        raise AssertionError("Stochastic diagnostics outside conditional calibration window")
    return {
      "schema":"physqed.stochastic-separate-universe.research.v1",
      "status":"PASS_CONDITIONAL_STOCHASTIC_DELTA_N_ONLY",
      "n":int(n),"seed":int(seed),"input_sigma_z":3.8e-7,
      "uniform_energy_target":float(target),"reference_efolds":float(reference),
      "std_deltaN":sd,"skewness":float(skew(shifts)),
      "excess_kurtosis":float(kurtosis(shifts)),
      "correlation_with_log_abs_seed":corr,
      "ideal_log_normal_seed_skewness":float((7*zeta(3,1)/4)/(math.pi**2/8)**1.5),
      "ideal_log_normal_seed_excess_kurtosis":4.,
      "quantum_initial_conditions_derived":False,
      "local_3D_Einstein_constraints_solved":False,
      "spatial_gradients_evolved":False,
      "physical_CMB_spectrum_derived":False
    }

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="stochastic_waterfall_receipt.json")
    ap.add_argument("--n",type=int,default=96)
    args=ap.parse_args()
    if args.n<32 or args.n>4096:raise ValueError("Bounded diagnostic ensemble required")
    result=compute(args.n)
    Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
