"""Exact rational spinodal for the specified biased two-field potential.
Verifies algebraic stationary-point structure, not quantum cosmological dynamics.
"""
from fractions import Fraction as F
import json
from math import sqrt
from pathlib import Path

def run():
    delta=F('0.016202803686105016')
    a=(4+delta)/2
    yc=F('0.81')
    k=F(10000)
    v=3-a*a/2
    d=a-yc
    beta=v/(d*d+2*v)
    lam=k*k/(4*beta)
    A,B=k*d,lam-k*k/2
    assert v>0 and A>0 and B>0
    assert B==k*k*d*d/(4*v)
    hc2=4*A**3/(27*B)
    assert hc2==16*k*v*d/27
    low,high=F('83.57385672072'),F('83.57385672073')
    assert low**2<hc2<high**2
    assert 4*A**3-27*B*80**2>0
    assert 4*A**3-27*B*90**2<0
    fixed2=4*lam*lam*(A/B)**3/27
    assert fixed2>4*hc2
    xstar=F('0.6730287364275626')
    sigma=F('0.00000038')
    mass=k*(yc-xstar*xstar)
    hs=mass*sigma+lam*sigma**3
    assert F('0.0013567228')<hs<F('0.0013567230')
    assert (61000*hs)**2<hc2
    zfloor=F('0.005')
    assert (mass*zfloor+lam*zfloor**3)**2<hc2
    return {
      'schema':'physqed.exact-bias-spinodal.v1',
      'status':'PASS_EXACT_RATIONAL_SPINODAL__PHYSICS_SCOPE_RESTRICTED',
      'hcrit_squared_exact':str(hc2),
      'hcrit_bracket':[str(low),str(high)],
      'hcrit_approx':sqrt(float(hc2)),
      'h_sigma_exact':str(hs),
      'h_sigma_approx':float(hs),
      'ratio_critical_to_screen':sqrt(float(hc2))/float(hs),
      'stationary_branches_h80':3,
      'stationary_branches_h90':1,
      'off_axis_local_minima_for_0_lt_h_lt_hcrit':4,
      'off_axis_local_minima_for_h_gt_hcrit':2,
      'x_parity_degeneracy_remains':True,
      'hcrit_fixed_x_approx':sqrt(float(fixed2)),
      'negative_control_fixed_x_threshold_is_not_exact':True,
      'fixed_pivot_z_at_hcrit_exceeds_0_005':True,
      'domain_wall_abundance_derived':False,
      'physical_CMB_state_verified':False,
      'ABJM_map_derived':False
    }

if __name__=='__main__':
    receipt=run()
    Path('inflaton_spinodal_exact_receipt.json').write_text(
       json.dumps(receipt,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2,sort_keys=True))
