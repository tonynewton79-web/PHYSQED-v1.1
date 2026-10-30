"""PHYSQED safe CLI for bounded typed JSON physics-input contracts.

Usage:
    PYTHONPATH=projects/physqed python -m v12.typed_cli --input model.json
    PYTHONPATH=projects/physqed python -m v12.typed_cli --input model.json --plan
    PYTHONPATH=projects/physqed python -m v12.typed_cli --input model.json --output receipt.json

Exit codes: 0 supported obligations passed, 2 mathematical refusal,
3 unsupported/invalid input. --plan only prints obligations (not a pass).
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .geometry import ScopeError
from .typed_input import (load_physics_input, plan_physics_obligations,
                          execute_physics_input, MAX_BYTES)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,required=True)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--plan",action="store_true")
    args=parser.parse_args(argv)
    try:
        if args.input.stat().st_size>MAX_BYTES:
            raise ScopeError("typed input exceeds byte limit")
        body=args.input.read_text(encoding="utf-8")
        if args.plan:
            spec=load_physics_input(body)
            result={"schema":"physqed.typed-plan.v1","claim_id":spec.claim_id,
                    "kind":spec.kind,"obligations":plan_physics_obligations(spec),
                    "physics_verified":False,
                    "execution_status":"NOT_EXECUTED"}
            code=0
        else:
            result=execute_physics_input(body)
            code=0 if result["status"].startswith("PASS_") else 2
        serialized=json.dumps(result,indent=2,sort_keys=True)+"\n"
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(serialized,encoding="utf-8")
        else:
            print(serialized,end="")
        return code
    except (ScopeError, UnicodeError, OSError, KeyError, IndexError, TypeError) as exc:
        print(json.dumps({"schema":"physqed.typed-error.v1",
            "status":"UNSUPPORTED_SCOPE", "reason":str(exc),
            "physics_verified":False},sort_keys=True))
        return 3


if __name__=="__main__":
    raise SystemExit(main())
