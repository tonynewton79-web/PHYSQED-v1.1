"""Command-line entry for the finite SU(2) Wilson pilot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .simulation import run_chains


def _int_tuple(raw: str, count: int | None = None) -> tuple[int, ...]:
    try:
        result = tuple(int(token) for token in raw.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("comma-separated integers required") from exc
    if count is not None and len(result) != count:
        raise argparse.ArgumentTypeError(f"exactly {count} integers required")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extents", type=lambda s: _int_tuple(s, 4), required=True)
    parser.add_argument("--beta", type=float, required=True)
    parser.add_argument("--seeds", type=_int_tuple, required=True)
    parser.add_argument("--warmup", type=int, default=8)
    parser.add_argument("--sweeps", type=int, default=16)
    parser.add_argument("--thin", type=int, default=2)
    parser.add_argument("--epsilon", type=float, default=0.2)
    parser.add_argument("--initialization", choices=("cold", "haar"), default="cold")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        result = run_chains(args.extents, args.beta, args.seeds, args.warmup,
                            args.sweeps, args.thin, args.epsilon, args.initialization)
    except ValueError as exc:
        parser.error(str(exc))
    body = json.dumps(result, sort_keys=True, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
    else:
        print(body, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
