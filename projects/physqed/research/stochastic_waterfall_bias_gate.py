"""Classical waterfall-vacuum topology and biased-basin negative controls.

This scoped research script checks a conditional two-field polynomial and a
hand-injected threshold kick. It does not solve a quantum stochastic state,
general-relativistic constraints, true wall evolution, or observational spectra.
"""
from __future__ import annotations
import json
import math
from fractions import Fraction as F
from pathlib import Path
import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research import inflaton_waterfall_dynamics as m

SIGMA=3.8e-7
XSTAR=0.6730287364275626
BIAS=1e-4


def positive_vacuum_and_offset(bias):
    def energy(q):
        x,z=q
        return m.potential(x,z)-bias*z
    def grad(q):
        ux,uz=m.gradient(*q)
        return [ux,uz-bias]
    fit=minimize(energy,[m.XV,m.ZV],jac=grad,method="BFGS",options={"gtol":1e-10})
    assert np.linalg.norm(grad(fit.x)) < 1e-6
    return fit.x,-float(energy(fit.x))


def field_ode(_,q,bias,offset):
    x,vx,z,vz,N=q
    u=m.potential(x,z)-bias*z+offset
    E=u+.5*(vx**2+vz**2)
    if E <= 0:
        raise ArithmeticError("nonpositive effective energy")
    hubble=m.MU*math.sqrt(E/3)
    ux,uz=m.gradient(x,z)
    return [vx,-3*hubble*vx-ux,vz,-3*hubble*vz-uz+bias,hubble]


def first_threshold(bias,offset):
    x=XSTAR
    z=bias/(m.KAPPA*(m.YC-x*x))
    u=m.potential(x,z)-bias*z+offset
    hubble=m.MU*math.sqrt(u/3)
    for _ in range(12):
        vx=-m.gradient(x,z)[0]/(3*hubble)
        hubble=m.MU*math.sqrt((u+.5*vx*vx)/3)
    y0=[x,vx,z,0,0]
    def event(_,q):
        return q[0]-m.XC
    event.terminal=True
    event.direction=1
    sol=solve_ivp(lambda t,q:field_ode(t,q,bias,offset),(0,15),y0,
                  events=event,method="DOP853",rtol=1e-9,atol=1e-12,max_step=.03)
    assert sol.success and len(sol.t_events[0])==1
    return sol.t_events[0][0],sol.y_events[0][0]


def first_exit(tw,yw,kick,bias,offset):
    y=yw.copy()
    y[2]+=kick
    n0=float(y[-1])
    def eps_event(_,q):
        x,vx,z,vz,N=q
        E=m.potential(x,z)-bias*z+offset+.5*(vx**2+vz**2)
        return 1.5*(vx*vx+vz*vz)/E-1
    eps_event.terminal=True
    eps_event.direction=1
    sol=solve_ivp(lambda t,q:field_ode(t,q,bias,offset),(tw,tw+12),y,
                  events=eps_event,method="Radau",rtol=3e-8,atol=3e-11,max_step=.08)
    assert sol.success and len(sol.t_events[0])==1
    end=sol.y_events[0][0]
    return {"kick":kick,"z_at_first_exit":float(end[2]),
            "post_threshold_efolds":float(end[-1]-n0)}


def run():
    delta=F("0.016202803686105016")
    a=(F(4)+delta)/2
    v=F(3)-a*a/2
    assert F(98,100)<v<F(99,100)
    assert abs(float(v)-m.V)<1e-13

    vac,off=positive_vacuum_and_offset(BIAS)
    tw,yw=first_threshold(BIAS,off)
    low=first_exit(tw,yw,-1.5e-6,BIAS,off)
    high=first_exit(tw,yw,-1e-6,BIAS,off)
    assert low["z_at_first_exit"]<0<high["z_at_first_exit"]
    assert all(34<r["post_threshold_efolds"]<35 for r in (low,high))

    def u(q):
        return m.potential(*q)-BIAS*q[1]+off
    def grad(q):
        ux,uz=m.gradient(*q)
        return [ux,uz-BIAS]
    local=minimize(u,[m.XV,-m.ZV],jac=grad,method="BFGS")
    x,z=local.x
    H=np.array([[-2*m.A+6*x*x-m.KAPPA*z*z,-2*m.KAPPA*x*z],
                [-2*m.KAPPA*x*z,m.KAPPA*(m.YC-x*x)+3*m.LAM*z*z]])
    e_min=float(np.min(np.linalg.eigvalsh(H)))
    assert z<0 and u(local.x)>0 and e_min>6
    mz=m.KAPPA*(m.YC-XSTAR**2)
    assert BIAS< SIGMA*mz
    return {"schema":"physqed.bias-gate.research.v1",
       "status":"PASS_SCOPED_POLYNOMIAL_AND_CLASSICAL_BASIN_TESTS__PHYSICS_UNVERIFIED",
       "unbiased_z0_potential_barrier":float(v),
       "four_original_vacua":True,
       "small_bias_value":BIAS,
       "pivot_quasistatic_displacement_over_sigma":BIAS/(mz*SIGMA),
       "threshold_field_over_sigma":float(yw[2]/SIGMA),
       "negative_test":low,"positive_test":high,
       "false_vacuum_energy":float(u(local.x)),
       "false_vacuum_smallest_Hessian_eigenvalue":e_min,
       "quantum_stochastic_state_derived":False,
       "domain_wall_abundance_derived":False,
       "Einstein_constraints_solved":False}


if __name__=="__main__":
    result=run()
    out=Path("inflaton_bias_gate_receipt.json")
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
