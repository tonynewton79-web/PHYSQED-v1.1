"""Run predefined exact linearized harmonic Einstein boundary benchmarks.

Example:
 PYTHONPATH=projects/physqed python -m v12.gh_boundary_cli --case positive
 --case positive, initial_velocity, metric_corner, or naive_sommerfeld
Only built-in cases are accepted; arbitrary external SymPy code is not parsed.
Exit 0 for positive and correctly detected negative-control benchmarks,
3 for bad CLI/file inputs. Result is never a nonlinear Einstein theorem.
"""
import argparse
import json
from pathlib import Path
from .gh_boundary_map import (
    certify_symbol_and_controls,certify_explicit_linearized_metric,
    reference_positive_wave,reference_constraint_velocity_failure,
    reference_metric_corner_failure,naive_sommerfeld_counterexample)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--case",choices=("positive","initial_velocity","metric_corner",
                                      "naive_sommerfeld","all"),default="all")
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    try:
        results={}
        if args.case in ("all","positive"):
            results["positive"]=certify_explicit_linearized_metric(reference_positive_wave())
        if args.case in ("all","initial_velocity"):
            results["initial_velocity"]=certify_explicit_linearized_metric(
                reference_constraint_velocity_failure())
        if args.case in ("all","metric_corner"):
            results["metric_corner"]=certify_explicit_linearized_metric(
                reference_metric_corner_failure())
        if args.case in ("all","naive_sommerfeld"):
            results["naive_sommerfeld"]=naive_sommerfeld_counterexample()
        results["symbol_and_control_summary"]=certify_symbol_and_controls()
        payload=json.dumps(results,sort_keys=True,indent=2)+"\n"
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(payload,encoding="utf-8")
        else:
            print(payload,end="")
        return (0 if results["symbol_and_control_summary"]["status"].startswith("PASS_")
                  else 2)
    except (ValueError,TypeError,OSError,UnicodeError) as e:
        print(json.dumps({"status":"INVALID_OR_UNSUPPORTED_SCOPE","reason":str(e)}))
        return 3


if __name__=="__main__":
    raise SystemExit(main())
