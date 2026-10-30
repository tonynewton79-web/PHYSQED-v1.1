"""Run exact GH glancing/corner and curved pp-wave built-in controls.

Only predefined sources, not arbitrary Python or free-text SymPy, accepted.
A PASS means a correct obstruction and curved bulk identities; it does
NOT mean the uniform boundary estimate was proved.
"""
import argparse
import json
from pathlib import Path
from .gh_glancing_corners import certify_glancing_and_corners
from .gh_curved_ppwave import verify_curved_ppwave


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--case",choices=("glancing_corners","curved_ppwave","all"),
                   default="all")
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    try:
        result={}
        if args.case in ("glancing_corners","all"):
            result["glancing_corners"]=certify_glancing_and_corners()
        if args.case in ("curved_ppwave","all"):
            result["curved_ppwave"]=verify_curved_ppwave()
        good=(("glancing_corners" not in result or result["glancing_corners"][
              "status"]=="PASS_GH_GLANCING_OBSTRUCTION_AND_FINITE_CORNERS")
              and ("curved_ppwave" not in result or result["curved_ppwave"][
              "status"]=="PASS_EXACT_CURVED_BULK_GH_INTERTWINER"))
        result["scope"]={
            "unweighted_metric_boundary_inverse_uniform":False,
            "first_order_Kreiss_estimate_proven":False,
            "curved_boundary_wellposedness_proven":False,
            "full_Einstein_IBVP_proven":False}
        result["status"]="PASS_SCOPED_OBSTRUCTION_AND_CURVED_BULK_CHECKS" if good else "FAILED"
        payload=json.dumps(result,sort_keys=True,indent=2)+"\n"
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(payload,encoding="utf-8")
        else:
            print(payload,end="")
        return 0 if good else 2
    except (ValueError,TypeError,OSError,UnicodeError) as exc:
        print(json.dumps({"status":"INVALID_SCOPE","reason":str(exc)}))
        return 3


if __name__=="__main__":
    raise SystemExit(main())
