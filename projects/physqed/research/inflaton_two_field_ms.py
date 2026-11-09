"""Research-only gauge-invariant two-field Mukhanov--Sasaki mode solver.

Uses the prior exact polynomial / homogeneous Friedmann benchmark. This solves
linear canonical scalar and tensor modes with the GR constraint mass. At the
waterfall threshold it imposes the same homogeneous chi seed as the previous
background test and matches modes continuously. This is NOT the quantum seed
matching law, stochastic waterfall, microscopic reheating, or ABJM map.
"""
from __future__ import annotations
import argparse
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from research import inflaton_waterfall_dynamics as m

XSTAR=0.6730287364275626
AS=2.1e-9

def grad(x,z):
    return np.array(m.gradient(x,z), dtype=float)

def hubble(y):
    x,vx,z,vz=y
    return m.energy_and_hubble([x,vx,z,vz,0,0])

def eps_h(y):
    E,h=hubble(y)
    return 1.5*(y[1]*y[1]+y[3]*y[3])/E

def bg_rhs(N,y):
    x,vx,z,vz=y
    E,h=hubble(y)
    acc=-3*h*np.array([vx,vz])-grad(x,z)
    return np.array([vx/h,acc[0]/h,vz/h,acc[1]/h])

def mass_matrix(y,include_gravity=True):
    x,vx,z,vz=y
    E,h=hubble(y)
    v=np.array([vx,vz]); u=grad(x,z)
    ep=1.5*np.dot(v,v)/E
    Hess=np.array([[-2*m.A+6*x*x-m.KAPPA*z*z,-2*m.KAPPA*x*z],
                   [-2*m.KAPPA*x*z,m.KAPPA*(m.YC-x*x)+3*m.LAM*z*z]])
    if include_gravity:
        Hess=Hess + m.MU**2*((3-ep)*np.outer(v,v)
                   +(np.outer(u,v)+np.outer(v,u))/h)
    return Hess/h**2,ep,h

def slowroll_pre(x0,x1):
    a=m.A
    return m.MU**2/4*((3/a)*math.log((x1/x0)**2)
       +(3/a-a/2)*math.log((a-x0*x0)/(a-x1*x1))
       -(x1*x1-x0*x0)/2)

def early_state(before):
    x0=brentq(lambda x:slowroll_pre(x,XSTAR)-before,.1,XSTAR-1e-8)
    u=m.potential(x0,0); ux=m.gradient(x0,0)[0]
    h=m.MU*math.sqrt(u/3)
    for _ in range(12):
        vx=-ux/(3*h)
        h=m.MU*math.sqrt((u+vx*vx/2)/3)
    return np.array([x0,vx,0,0])

def event_x(value,terminal=False):
    def ev(N,y):return y[0]-value
    ev.terminal=terminal
    ev.direction=1
    return ev

def background(before=5,seed=1e-7):
    pre=solve_ivp(bg_rhs,[0,80],early_state(before),
           events=[event_x(XSTAR),event_x(m.XC,True)],
           method="DOP853",rtol=2e-10,atol=3e-12,
           max_step=.025,dense_output=True)
    if not pre.success or len(pre.t_events[0])!=1 or len(pre.t_events[1])!=1:
        raise RuntimeError("pivot/waterfall event missing")
    npiv=float(pre.t_events[0][0])
    nw=float(pre.t_events[1][0])
    y0=pre.y_events[1][0].copy()
    y0[2]=seed
    def end(N,y):return eps_h(y)-1
    end.terminal=True
    end.direction=1
    post=solve_ivp(bg_rhs,[nw,nw+80],y0,events=end,
            method="Radau",rtol=2e-10,atol=3e-12,
            max_step=.04,dense_output=True)
    if not post.success or len(post.t_events[0])!=1:
        raise RuntimeError("first epsilon=1 event missing")
    return pre,post,npiv,nw,float(post.t_events[0][0]),pre.y_events[0][0],y0

def scalar_rhs(N,Y,interp,k,correct=True):
    C,ep,h=mass_matrix(interp(N),include_gravity=correct)
    rho=k*math.exp(-N)/h
    q=Y[:4].reshape(2,2);p=Y[4:].reshape(2,2)
    return np.r_[p.reshape(-1),(-(3-ep)*p-(C+np.eye(2)*rho*rho)@q).reshape(-1)]

def tensor_rhs(N,Y,interp,k):
    C,ep,h=mass_matrix(interp(N))
    rho=k*math.exp(-N)/h
    return np.array([Y[1],-(3-ep)*Y[1]-rho*rho*Y[0]],dtype=complex)

def finite_k(background_data,kfactor):
    pre,post,npiv,nw,ne,yp,yw=background_data
    hstar=mass_matrix(yp)[2]
    k=kfactor*math.exp(npiv)*hstar
    C0,ep0,h0=mass_matrix(pre.sol(0))
    rho0=k/h0
    om=np.sqrt(rho0**2+np.diag(C0)-2+ep0)
    if np.min(om)<=0:raise RuntimeError("not subhorizon")
    amp=np.sqrt(rho0/om)
    q0=np.diag(amp).astype(complex)
    p0=np.diag((-1-1j*om)*amp)
    sc0=np.r_[q0.reshape(-1),p0.reshape(-1)]
    ten0=np.array([1,-1-1j*rho0],dtype=complex)
    opts=dict(method="DOP853",rtol=4e-8,atol=5e-10,max_step=.05)
    sp=solve_ivp(lambda N,y:scalar_rhs(N,y,pre.sol,k),[0,nw],sc0,**opts)
    tp=solve_ivp(lambda N,y:tensor_rhs(N,y,pre.sol,k),[0,nw],ten0,**opts)
    ss=solve_ivp(lambda N,y:scalar_rhs(N,y,post.sol,k),[nw,ne],sp.y[:,-1],**opts)
    ts=solve_ivp(lambda N,y:tensor_rhs(N,y,post.sol,k),[nw,ne],tp.y[:,-1],**opts)
    if not all(q.success for q in (sp,tp,ss,ts)):
        raise RuntimeError("mode integration did not complete")
    final=post.y[:,-1]
    v=np.array([final[1],final[3]])
    h=mass_matrix(final)[2]
    Q=ss.y[:4,-1].reshape(2,2)
    R=h*(v@Q)/(v@v)
    power=float(np.sum(np.abs(R)**2))
    tensor=float(np.abs(ts.y[0,-1])**2)
    return {"kfactor":kfactor,"initial_k_over_aH":rho0,
            "scalar_mode_power":power,"tensor_mode_power":tensor,
            "r_linear":8*m.MU**2*tensor/power,
            "initial_waterfall_vacuum_mode_fraction":float(abs(R[1])**2/power),
            "q_z_chi_at_waterfall":float(abs(sp.y[:4,-1].reshape(2,2)[1,1]))}

def result(before=5,seed=1e-7,scales=(.85,1.,1.15)):
    b=background(before,seed)
    pre,post,npiv,nw,ne,yp,yw=b
    modes=[finite_k(b,kf) for kf in scales]
    pivot=next(x for x in modes if x["kfactor"]==1)
    ns=nt=None
    if len(modes)>=3:
        l,r=modes[0],modes[-1]
        dx=math.log(r["kfactor"]/l["kfactor"])
        ns=3+math.log(r["scalar_mode_power"]/l["scalar_mode_power"])/dx
        nt=2+math.log(r["tensor_mode_power"]/l["tensor_mode_power"])/dx
    ep=eps_h(yp)
    U=m.potential(yp[0],0)
    Lam4=24*math.pi**2*AS*ep/U
    hw=mass_matrix(yw)[2]
    local_noise=math.sqrt(Lam4)*hw/(2*math.pi*m.MU**2)
    cmb_noise=math.sqrt(AS*2*ep/m.MU**2)*math.exp(npiv)*pivot["q_z_chi_at_waterfall"]
    return {"status":"CONDITIONAL_LINEAR_MODE_RESULT__NOT_STOCHASTIC_WATERFALL",
            "initial_efolds_before_pivot":before,"imposed_seed":seed,
            "N_waterfall_relative_to_pivot":nw-npiv,
            "N_first_epsilonH1_relative_to_pivot":ne-npiv,
            "r_linear":pivot["r_linear"],"n_s_linear":ns,"n_t_linear":nt,
            "pivot_waterfall_mode_power_fraction":pivot["initial_waterfall_vacuum_mode_fraction"],
            "mass_chi2_over_H2_at_pivot":m.KAPPA*(m.YC-yp[0]**2)/mass_matrix(yp)[2]**2,
            "waterfall_quantum_seed_ratio_estimate":local_noise/seed,
            "cmb_waterfall_mode_over_seed":cmb_noise/seed,
            "scales":modes,"physical_truth_proven":False,
            "ABJM_map_derived":False,"stochastic_waterfall_solved":False}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,default=Path("inflaton_ms_receipt.json"))
    p.add_argument("--before",type=float,default=5.)
    args=p.parse_args()
    r=result(before=args.before)
    assert 54.7<r["N_first_epsilonH1_relative_to_pivot"]<55.3
    assert .069<r["r_linear"]<.071
    assert r["pivot_waterfall_mode_power_fraction"]<1e-15
    assert r["waterfall_quantum_seed_ratio_estimate"]>1
    assert not r["physical_truth_proven"]
    args.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print(json.dumps(r,indent=2,sort_keys=True))
