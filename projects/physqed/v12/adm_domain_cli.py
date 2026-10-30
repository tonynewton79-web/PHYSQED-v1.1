"""Safe command line for typed rational ADM domain and boundary certificates.

Run:
 PYTHONPATH=projects/physqed python -m v12.adm_domain_cli --input model.json
 PYTHONPATH=projects/physqed python -m v12.adm_domain_cli --input model.json --output receipt.json

0 means exact *coefficient and conditional boundary-form* gates pass,
2 means an interior/flux sufficient bound is inconclusive,
3 means invalid/unsupported input. No result proves smooth solutions.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .typed_adm_domain import certify_typed_adm_domain,DomainScopeError

MAX_BYTES=65000


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,required=True)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args(argv)
    try:
        if args.input.stat().st_size>MAX_BYTES:
            raise DomainScopeError("input exceeds limit")
        def unique_keys(pairs):
            result={}
            for name,value in pairs:
                if name in result:
                    raise DomainScopeError("duplicate JSON key")
                result[name]=value
            return result
        model=json.loads(args.input.read_text(encoding="utf-8"),
             object_pairs_hook=unique_keys,
             parse_constant=lambda value: (_ for _ in ()).throw(
                 DomainScopeError("nonfinite JSON constant")))
        result=certify_typed_adm_domain(model)
        status=0 if result["status"].startswith("PASS_") else 2
        output=json.dumps(result,indent=2,sort_keys=True)+"\n"
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(output,encoding="utf-8")
        else:
            print(output,end="")
        return status
    except (OSError,UnicodeError,ValueError,TypeError,KeyError,
            ZeroDivisionError) as exc:
        print(json.dumps({"schema":"physqed.typed-adm-domain-error.v1",
             "status":"INVALID_OR_UNSUPPORTED_SCOPE",
             "reason":str(exc),"mathematical_claim_proven":False}))
        return 3


if __name__=="__main__":
    raise SystemExit(main())
