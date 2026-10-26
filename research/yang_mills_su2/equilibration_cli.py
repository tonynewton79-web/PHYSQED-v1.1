"""Bounded replay of finite cold/Haar SU(2) trajectory diagnostics.

The certificate attests to deterministic computation and source identity,
not equilibrium, the physical spectrum, continuum existence or a mass gap.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import sys
from fractions import Fraction
from pathlib import Path

from .equilibration import run_equilibration

MAX_RECEIPT_BYTES = 2 * 1024 * 1024
SOURCE_NAMES = ("equilibration_cli.py", "equilibration.py", "local_updates.py", "lattice.py",
                "simulation.py", "su2.py")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(data: object) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def _source_digest() -> str:
    root = Path(__file__).resolve().parent
    return _digest(_canonical({name: _digest((root/name).read_bytes())
                               for name in SOURCE_NAMES}))


def _valid_inputs(extents: object, beta_numer: object, beta_denom: object,
                  seeds: object, sweeps: object, eps_numer: object,
                  eps_denom: object) -> None:
    if (type(extents) is not tuple or len(extents) != 4 or
        any(type(v) is not int or not 2 <= v <= 3 for v in extents) or
        type(seeds) is not tuple or not 2 <= len(seeds) <= 3 or
        any(type(s) is not int or abs(s) > 2**20 for s in seeds) or
        len({abs(s) for s in seeds}) != len(seeds) or
        type(sweeps) is not int or not 8 <= sweeps <= 32 or
        any(type(v) is not int for v in (beta_numer, beta_denom, eps_numer, eps_denom)) or
        not 0 <= beta_numer <= 2**16 or not 1 <= beta_denom <= 2**16 or
        not 1 <= eps_numer <= 2**16 or not 1 <= eps_denom <= 2**16 or
        not 0 <= Fraction(beta_numer, beta_denom) <= 8 or
        not 0 < Fraction(eps_numer, eps_denom) <= Fraction(22, 7)):
        raise ValueError("unsupported exact rational finite trajectory request")
    if float(Fraction(eps_numer, eps_denom)) > math.pi:
        raise ValueError("proposal angle must not exceed pi")


def _fraction_data(v: Fraction) -> dict:
    return {"numerator": v.numerator, "denominator": v.denominator}


def certify_equilibration(extents: tuple[int, int, int, int],
                          beta_numer: int, beta_denom: int,
                          seeds: tuple[int, ...], sweeps: int,
                          eps_numer: int, eps_denom: int) -> dict:
    _valid_inputs(extents, beta_numer, beta_denom, seeds, sweeps,
                  eps_numer, eps_denom)
    beta, epsilon = Fraction(beta_numer, beta_denom), Fraction(eps_numer, eps_denom)
    report = run_equilibration(extents, float(beta), seeds, sweeps, float(epsilon))
    receipt = {
        "schema_version": "ym-su2-equilibration-certificate-0.1",
        "status": "FINITE_DIAGNOSTIC_REPLAY",
        "input": {"extents": list(extents), "beta": _fraction_data(beta),
                  "seeds": list(seeds), "sweeps": sweeps,
                  "epsilon": _fraction_data(epsilon)},
        "report": report,
        "implementation_sha256": _source_digest(),
        "python_runtime": sys.version.split()[0],
        "equilibrium_claim": False,
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
        "scope": "recomputed bounded finite cold/Haar trajectories only",
    }
    receipt["fingerprint"] = _digest(_canonical(receipt))
    return receipt


def replay_equilibration_receipt(receipt: object) -> bool:
    if type(receipt) is not dict:
        return False
    try:
        if set(receipt) != {"schema_version", "status", "input", "report",
                            "implementation_sha256", "python_runtime", "equilibrium_claim",
                            "physical_law_proven", "continuum_mass_gap_proven",
                            "lean_kernel_verified", "scope", "fingerprint"}:
            return False
        if (receipt["schema_version"] != "ym-su2-equilibration-certificate-0.1" or
            receipt["status"] != "FINITE_DIAGNOSTIC_REPLAY" or
            any(receipt[key] is not False for key in (
                "equilibrium_claim", "physical_law_proven", "continuum_mass_gap_proven",
                "lean_kernel_verified")) or
            receipt["python_runtime"] != sys.version.split()[0] or
            type(receipt["fingerprint"]) is not str or len(receipt["fingerprint"]) != 64):
            return False
        info = receipt["input"]
        if type(info) is not dict or set(info) != {
            "extents", "beta", "seeds", "sweeps", "epsilon",
        }:
            return False
        if type(info["extents"]) is not list or type(info["seeds"]) is not list:
            return False
        beta, epsilon = info["beta"], info["epsilon"]
        if (type(beta) is not dict or type(epsilon) is not dict or
            set(beta) != {"numerator", "denominator"} or
            set(epsilon) != {"numerator", "denominator"}):
            return False
        _valid_inputs(tuple(info["extents"]), beta["numerator"], beta["denominator"],
                      tuple(info["seeds"]), info["sweeps"],
                      epsilon["numerator"], epsilon["denominator"])
        expected = certify_equilibration(tuple(info["extents"]),
                                         beta["numerator"], beta["denominator"],
                                         tuple(info["seeds"]), info["sweeps"],
                                         epsilon["numerator"], epsilon["denominator"])
        return _canonical(receipt) == _canonical(expected)
    except (ValueError, TypeError, KeyError, OverflowError, OSError, RecursionError):
        return False


def _read_bounded_json(path: Path) -> object:
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
        with os.fdopen(fd, "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise ValueError("receipt must be a regular file")
            data = stream.read(MAX_RECEIPT_BYTES + 1)
    except OSError as exc:
        raise ValueError("receipt not readable") from exc
    if len(data) > MAX_RECEIPT_BYTES:
        raise ValueError("oversized receipt")
    try:
        return json.loads(data.decode("utf-8"))
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ValueError("invalid receipt JSON") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extents", type=str)
    parser.add_argument("--beta-num", type=int)
    parser.add_argument("--beta-den", type=int)
    parser.add_argument("--seeds", type=str)
    parser.add_argument("--sweeps", type=int)
    parser.add_argument("--epsilon-num", type=int)
    parser.add_argument("--epsilon-den", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args(argv)
    if args.verify is not None:
        try:
            valid = replay_equilibration_receipt(_read_bounded_json(args.verify))
        except ValueError:
            valid = False
        print("VERIFIED: finite equilibration diagnostic only" if valid else "REJECTED")
        return 0 if valid else 2
    try:
        if None in (args.extents, args.beta_num, args.beta_den, args.seeds,
                    args.sweeps, args.epsilon_num, args.epsilon_den):
            raise ValueError("all extent, coupling, seed, sweep and epsilon parameters required")
        extents = tuple(int(v) for v in args.extents.split(","))
        seeds = tuple(int(v) for v in args.seeds.split(","))
        receipt = certify_equilibration(extents, args.beta_num, args.beta_den,
                                        seeds, args.sweeps,
                                        args.epsilon_num, args.epsilon_den)
        body = json.dumps(receipt, indent=2, sort_keys=True, allow_nan=False) + "\n"
        if args.output is None:
            print(body, end="")
        else:
            args.output.write_text(body, encoding="utf-8")
    except (OSError, ValueError) as exc:
        parser.exit(2, f"FINITE DIAGNOSTIC REFUSED: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
