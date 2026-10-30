"""CLI for a single source-compatible shifted Einstein--Maxwell/domain model.

The pass status means: the supplied exact spacetime meets the 18 linked
Einstein/Maxwell checks, interior energy inequalities and maximal
nonnegative boundary trace *algebra*. Not a nonlinear Einstein IBVP
existence or strong Lopatinski proof.

PYTHONPATH=projects/physqed python -m v12.linked_adm_cli --input model.json
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .linked_adm_boundary import certify_linked_adm_boundary

MAX_BYTES=95000


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input",type=Path,required=True)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args(argv)
    try:
        if args.input.stat().st_size>MAX_BYTES:
            raise ValueError("JSON input exceeds allowed byte limit")
        def unique_keys(pairs):
            d={}
            for key,value in pairs:
                if key in d:raise ValueError("duplicate object key")
                d[key]=value
            return d
        model=json.loads(args.input.read_text("utf-8"),
             object_pairs_hook=unique_keys,
             parse_constant=lambda x: (_ for _ in ()).throw(
                 ValueError("nonfinite JSON literal")))
        result=certify_linked_adm_boundary(model)
        exit_code=0 if result["status"].startswith("PASS_") else 2
        s=json.dumps(result,sort_keys=True,indent=2)+"\n"
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(s,encoding="utf-8")
        else:
            print(s,end="")
        return exit_code
    except (ValueError,TypeError,KeyError,OSError,UnicodeError,
            ZeroDivisionError) as exc:
        print(json.dumps({"schema":"physqed.linked-adm-boundary-error.v1",
             "status":"INVALID_OR_UNSUPPORTED_SCOPE","reason":str(exc),
             "Einstein_boundary_theorem_proven":False},sort_keys=True))
        return 3


if __name__=="__main__":
    raise SystemExit(main())
