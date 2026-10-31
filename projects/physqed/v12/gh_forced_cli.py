"""Built-in exact regular-source first-order GH forced resolvent benchmarks.

This CLI does not execute arbitrary source code or accept arbitrary
untrusted SymPy expressions. A positive status proves only the scoped
regular-source Laplace-Fourier theorem and finite sourced corner gates.
"""
import argparse
import json
from pathlib import Path
from .gh_forced_resolvent import (
    prove_regular_source_resolvent,
    exact_exponential_volume_and_boundary_solution,
    nonzero_reduction_defect_solution)
from .gh_forced_corners import sourced_wave_positive_control


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    result={
       "theorem":prove_regular_source_resolvent(),
       "exponential_forced_solution":exact_exponential_volume_and_boundary_solution(),
       "nonzero_reduction_defect":nonzero_reduction_defect_solution(),
       "sourced_corners_positive":sourced_wave_positive_control(),
       "sourced_corners_bad_order2":
           sourced_wave_positive_control(bad_second_order=True),
       "sourced_corners_nonconserved":
           sourced_wave_positive_control(nonconserved=True)}
    pass_gate=(result["theorem"]["status"]==
          "PASS_REGULAR_SOURCE_INHOMOGENEOUS_GH_HALFSPACE_ESTIMATE" and
          result["exponential_forced_solution"][
              "direct_boundary_equals_corrected_B_amplitude"] and
          result["sourced_corners_positive"]["requested_corner_orders_passed"] and
          result["nonzero_reduction_defect"]["reduction_defect_nonzero"] and
          not result["sourced_corners_bad_order2"]["requested_corner_orders_passed"] and
          not result["sourced_corners_nonconserved"][
               "conditional_harmonic_constraint_preservation"])
    result["status"]=("PASS_REGULAR_FORCED_GH_CHECKS_ONLY"
                      if pass_gate else "REJECTED_FORCED_GH_CHECKS")
    result["arbitrary_L2_strong_wellposedness_proven"]=False
    result["nonlinear_Einstein_boundary_theorem_proven"]=False
    payload=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf-8")
    else:
        print(payload,end="")
    return 0 if pass_gate else 2


if __name__=="__main__":
    raise SystemExit(main())
