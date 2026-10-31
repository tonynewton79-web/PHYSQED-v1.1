"""Run scoped GH glancing, higher-corner and curved Ricci-flat controls.

Outputs:
  * Exact counterexample to UNWEIGHTED uniform metric boundary estimate.
  * Exact finite higher-order GH corner hierarchy with late negative control.
  * Two independent curved pp-wave bulk checks.
This tool never claims a general weighted Kreiss or nonlinear IBVP proof.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .gh_glancing import certify_glancing_gate
from .gh_glancing_corners import certify_glancing_and_corners
from .gh_higher_corners import certify_metric_corners
from .gh_boundary_map import t,x,zero_metric
from .gh_curved_plane_wave import verify_curved_gh_control
from .gh_curved_ppwave import verify_curved_ppwave


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--corner-order",type=int,default=4)
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    if not 0<=args.corner_order<=8:
        p.error("corner order must be in 0..8")
    positive=zero_metric()
    positive["yz"]=(t+x)**6
    negative=zero_metric()
    negative["yz"]=(t-x)**4
    report={
        "schema":"physqed.gh-glancing-corners-curved-benchmark.v1",
        "glancing_exact":certify_glancing_gate(),
        "glancing_independent":certify_glancing_and_corners(),
        "higher_corner_positive":certify_metric_corners(positive,args.corner_order),
        "higher_corner_negative":certify_metric_corners(negative,args.corner_order),
        "curved_reduced_full_control":verify_curved_gh_control(),
        "curved_covariant_bulk_intertwiner":verify_curved_ppwave(),
        "uniform_unweighted_boundary_resolvent_proven":False,
        "uniform_weighted_Kreiss_estimate_proven":False,
        "curved_Einstein_IBVP_wellposedness_proven":False}
    good=(report["glancing_exact"]["status"]=="PASS_EXACT_UNIFORM_BOUND_OBSTRUCTION"
          and report["glancing_independent"]["status"]=="PASS_GH_GLANCING_OBSTRUCTION_AND_FINITE_CORNERS"
          and report["higher_corner_positive"]["all_temporal_orders_passed"]
          and report["curved_reduced_full_control"]["status"]=="PASS_EXACT_CURVED_GH_BACKGROUND_AND_REDUCED_CONTROL"
          and report["curved_covariant_bulk_intertwiner"]["status"]=="PASS_EXACT_CURVED_BULK_GH_INTERTWINER")
    report["status"]=("PASS_SCOPED_GH_FRONTIER_CONTROLS" if good else
                      "REJECTED_GH_FRONTIER_CONTROLS")
    output=json.dumps(report,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(output,encoding="utf-8")
    else:
        print(output,end="")
    return 0 if good else 2


if __name__=="__main__":
    raise SystemExit(main())
