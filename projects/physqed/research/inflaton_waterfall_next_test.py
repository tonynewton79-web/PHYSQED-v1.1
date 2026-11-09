#!/usr/bin/env python3
"""New conditional numerical test: pivot-to-actual-first-exit shooting.

This is not a primordial perturbation solver, an ABJM map, nor a proof
of reheating. Uses existing two-field flat-FLRW background equations.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import sys
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from research import inflaton_waterfall_dynamics as model


def configure(xc):
    m = model
    m.XC = float(xc)
    m.YC = float(xc * xc)
    m.BETA = m.V / ((m.A - m.YC) ** 2 + 2 * m.V)
    m.LAM = m.KAPPA ** 2 / (4 * m.BETA)
    m.YV = m.A + 2 * m.V / (m.A - m.YC)
    m.XV = math.sqrt(m.YV)
    m.ZV = math.sqrt(m.KAPPA / m.LAM * (m.YV - m.YC))


def initial(x):
    m = model
    w = m.potential(x, 0)
    ux, _ = m.gradient(x, 0)
    h = m.MU * math.sqrt(w / 3)
    for _ in range(12):
        vx = -ux / (3 * h)
        h = m.MU * math.sqrt((w + vx * vx / 2) / 3)
    return [x, vx, 0, 0, 0, 0]


def end_from_pivot(x, seed=1e-7):
    m = model
    if not 0 < x < m.XC:
        raise ValueError("pivot must precede waterfall")
    def threshold(t, y):
        return y[0] - m.XC
    threshold.terminal = True
    threshold.direction = 1
    sol = solve_ivp(lambda t, y: m.derivative(t, y, 0, 0),
                    (0, 160), initial(x), events=threshold, method="DOP853",
                    rtol=1e-8, atol=1e-11, max_step=.05)
    if not sol.success or len(sol.t_events[0]) != 1:
        raise AssertionError("waterfall threshold not reached")
    t0 = float(sol.t_events[0][0])
    y0 = sol.y_events[0][0].copy()
    nw = float(y0[5])
    y0[2] = seed

    def epsilon_cross(t, y):
        E, h = m.energy_and_hubble(y)
        kinetic = .5 * (y[1]**2 + y[3]**2)
        return (3 * kinetic + 2 * y[4]) / E - 1
    epsilon_cross.terminal = True
    epsilon_cross.direction = 1

    late = solve_ivp(lambda t, y: m.derivative(t, y, 0, 0),
                     (t0, t0 + 160), y0, events=epsilon_cross,
                     method="Radau", rtol=1e-8, atol=1e-11, max_step=.15)
    if not late.success or len(late.t_events[0]) != 1:
        raise AssertionError("first epsilon_H=1 crossing not reached")
    ne = float(late.y_events[0][0][5])
    return {"N_total": ne, "N_pre": nw, "N_post": ne - nw,
            "first_crossing_tau": float(late.t_events[0][0])}


def slow_roll_proxies(x):
    m = model
    w = m.potential(x, 0)
    eps = 2*x*x*(x*x-m.A)**2/(m.MU**2*w*w)
    eta = (-2*m.A + 6*x*x)/(m.MU**2*w)
    heavy = 3*m.KAPPA*(m.YC-x*x)/(m.MU**2*w)
    return {"n_s_adiabatic_proxy": 1 - 6*eps + 2*eta,
            "r_adiabatic_proxy": 16*eps, "mchi2_over_H2_pivot": heavy}


def shoot(xc):
    configure(xc)
    left, right = max(.05, .15*xc), xc-1e-6
    at_right = end_from_pivot(right)
    if at_right["N_total"] > 55:
        return {"xc": xc, "status": "NO_PRE_WATERFALL_PIVOT",
                "minimum_N_total": at_right["N_total"]}
    at_left = end_from_pivot(left)
    if at_left["N_total"] < 55:
        raise AssertionError("unbracketed 55-efold pivot")
    xstar = brentq(lambda x: end_from_pivot(x)["N_total"] - 55,
                   left, right, xtol=1e-8)
    outcome = end_from_pivot(xstar)
    if abs(outcome["N_total"] - 55) > .002:
        raise AssertionError("pivot shoot missed target")
    return {"xc": xc, "xstar": xstar, "status": "PIVOT_FOUND",
            **outcome, **slow_roll_proxies(xstar)}


def trough_post_efolds(xc, mu):
    a, v = model.A, model.V
    yc = xc * xc
    yv = a + 2*v/(a-yc)
    xe = (math.sqrt(4*yv+8/mu**2)-math.sqrt(8)/mu)/2
    if xe <= xc:
        return 0
    return mu**2/4*(yv*math.log(xe/xc)-(xe*xe-yc)/2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path("inflaton_next_test_receipt.json"))
    args = ap.parse_args()
    pivots = [shoot(xc) for xc in (.58, .7, .9, 1.1)]
    assert pivots[0]["status"] == "NO_PRE_WATERFALL_PIVOT"
    assert all(p["status"] == "PIVOT_FOUND" for p in pivots[1:])
    assert .065 < pivots[2]["r_adiabatic_proxy"] < .08
    assert all(p["r_adiabatic_proxy"] > .036 for p in pivots[1:])

    configure(.9)
    initial_pivot = model.start_at_pivot()[0]
    seeds = []
    for s in (1e-4, 1e-7, 1e-9):
        r = end_from_pivot(initial_pivot, seed=s)
        seeds.append({"seed": s, **r})
    assert max(s["N_total"] for s in seeds)-min(s["N_total"] for s in seeds)<.5
    opt = minimize_scalar(lambda x: trough_post_efolds(x, model.MU),
                          bounds=(.05, math.sqrt(model.A)-.002),
                          method="bounded", options={"xatol":1e-11})
    assert opt.success and 30.7 < opt.fun < 31.1

    output = {"schema": "physqed.inflaton-next-test.research.v1",
              "status": "PASS_CONDITIONAL_NUMERICAL_DIAGNOSTICS__PHYSICS_UNVERIFIED",
              "assumptions": [
                  "canonical homogeneous flat-FLRW two-field equations",
                  "model scale mu/MPl=10.05 and kappa=10000",
                  "first epsilon_H=1 crossing, not a permanently noninflating theorem",
                  "seed injected at the waterfall, no quantum mode evolution",
                  "n_s and r are leading single-field adiabatic proxies",
                  "no microscopic reheating or holographic bulk-field map"
              ],
              "pivots": pivots, "seeds": seeds,
              "adiabatic_trough_proxy_minimum": {"xc": opt.x, "N": opt.fun}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True)+"\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
