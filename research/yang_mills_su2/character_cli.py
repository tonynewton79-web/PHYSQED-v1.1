"""Tamper-detecting exact character-series receipts, independently replayed.

Only a finite special-function diagnostic is checked. The receipts do not
certify the four-dimensional physical mass gap, quantum field existence,
experimental data, or a Lean-kernel theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from .character_bounds import character_ratio_bounds, negative_log_bounds

MAX_BESSEL_TERMS = 32
MAX_LOG_TERMS = 24
MAX_BETA_BITS = 24
MAX_CERTIFICATE_INTEGER_BITS = 11000
MAX_RECEIPT_BYTES = 2 * 1024 * 1024


def _fraction_record(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def _canonical(data: dict) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")


def _validate_request(beta_numer: int, beta_denom: int,
                      bessel_terms: int, log_terms: int) -> None:
    if (type(beta_numer) is not int or type(beta_denom) is not int or
        type(bessel_terms) is not int or type(log_terms) is not int or
        beta_denom == 0 or beta_numer <= 0 or beta_denom <= 0):
        raise ValueError("positive exact rational beta and integer term counts required")
    if (beta_numer.bit_length() > MAX_BETA_BITS or
        beta_denom.bit_length() > MAX_BETA_BITS or
        not 1 <= bessel_terms <= MAX_BESSEL_TERMS or
        not 1 <= log_terms <= MAX_LOG_TERMS):
        raise ValueError("unsupported receipt resource budget")


def _validate_bounds_budget(*values: Fraction) -> None:
    for number in values:
        if (number.numerator.bit_length() > MAX_CERTIFICATE_INTEGER_BITS or
            number.denominator.bit_length() > MAX_CERTIFICATE_INTEGER_BITS):
            raise ValueError("unsupported certificate serialization budget")


def _valid_fraction_record(record: object) -> bool:
    if type(record) is not dict or set(record) != {"numerator", "denominator"}:
        return False
    n, d = record["numerator"], record["denominator"]
    return (type(n) is int and type(d) is int and d > 0 and
            n.bit_length() <= MAX_CERTIFICATE_INTEGER_BITS and
            d.bit_length() <= MAX_CERTIFICATE_INTEGER_BITS)


def _valid_nested_bounds(bounds: object) -> bool:
    if type(bounds) is not dict or set(bounds) != {"character_ratio", "character_gap"}:
        return False
    for key in ("character_ratio", "character_gap"):
        interval = bounds[key]
        if type(interval) is not dict or set(interval) != {"lower", "upper"}:
            return False
        if not _valid_fraction_record(interval["lower"]) or not _valid_fraction_record(interval["upper"]):
            return False
    return True


def certify_character(
    beta_numer: int,
    beta_denom: int,
    bessel_terms: int,
    log_terms: int,
) -> dict:
    _validate_request(beta_numer, beta_denom, bessel_terms, log_terms)
    beta = Fraction(beta_numer, beta_denom)
    rlo, rhi = character_ratio_bounds(beta, bessel_terms)
    glo = negative_log_bounds(rhi, log_terms)[0]
    ghi = negative_log_bounds(rlo, log_terms)[1]
    _validate_bounds_budget(rlo, rhi, glo, ghi)
    record = {
        "schema_version": "ym-su2-character-certificate-0.1",
        "status": "FINITE_CHARACTER_EXACT_INTERVAL",
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
        "input": {
            "beta": _fraction_record(beta),
            "bessel_terms": bessel_terms,
            "log_terms": log_terms,
        },
        "bounds": {
            "character_ratio": {"lower": _fraction_record(rlo), "upper": _fraction_record(rhi)},
            "character_gap": {"lower": _fraction_record(glo), "upper": _fraction_record(ghi)},
        },
        "source_sha256": hashlib.sha256(Path(__file__).with_name("character_bounds.py").read_bytes()).hexdigest(),
        "scope": "exact pointwise SU2 Bessel-character bounds, not the physical 4D spectrum",
        "integrity_note": "SHA256 is reproducibility/integrity evidence, not authenticity",
    }
    record["fingerprint"] = hashlib.sha256(_canonical(record)).hexdigest()
    return record


def replay_character_certificate(receipt: dict) -> bool:
    """Recompute exact bounds from untrusted inputs; ignore asserted success."""
    if not isinstance(receipt, dict):
        return False
    try:
        required = {"schema_version", "status", "physical_law_proven",
                    "continuum_mass_gap_proven", "lean_kernel_verified", "input",
                    "bounds", "source_sha256", "scope", "integrity_note", "fingerprint"}
        if set(receipt) != required:
            return False
        if (receipt["schema_version"] != "ym-su2-character-certificate-0.1" or
            receipt["status"] != "FINITE_CHARACTER_EXACT_INTERVAL" or
            receipt["physical_law_proven"] is not False or
            receipt["continuum_mass_gap_proven"] is not False or
            receipt["lean_kernel_verified"] is not False or
            type(receipt["fingerprint"]) is not str or
            len(receipt["fingerprint"]) != 64):
            return False
        if (not _valid_nested_bounds(receipt["bounds"]) or
            type(receipt["source_sha256"]) is not str or
            type(receipt["scope"]) is not str or
            type(receipt["integrity_note"]) is not str or
            len(receipt["source_sha256"]) != 64 or
            len(receipt["scope"]) > 256 or
            len(receipt["integrity_note"]) > 256):
            return False
        inputs = receipt["input"]
        if type(inputs) is not dict or set(inputs) != {"beta", "bessel_terms", "log_terms"}:
            return False
        beta = inputs["beta"]
        if type(beta) is not dict or set(beta) != {"numerator", "denominator"}:
            return False
        _validate_request(beta["numerator"], beta["denominator"],
                          inputs["bessel_terms"], inputs["log_terms"])
        expected = certify_character(beta["numerator"], beta["denominator"],
                                     inputs["bessel_terms"], inputs["log_terms"])
        return _canonical(expected) == _canonical(receipt)
    except (ValueError, TypeError, KeyError, OverflowError, ZeroDivisionError, OSError,
            RecursionError):
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--beta-num", type=int)
    parser.add_argument("--beta-den", type=int)
    parser.add_argument("--bessel-terms", type=int)
    parser.add_argument("--log-terms", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args(argv)
    if args.verify is not None:
        try:
            if args.verify.stat().st_size > MAX_RECEIPT_BYTES:
                raise ValueError("receipt exceeds maximum supported size")
            data = json.loads(args.verify.read_text(encoding="utf-8"))
            valid = replay_character_certificate(data)
        except (OSError, ValueError, UnicodeError, RecursionError):
            valid = False
        print("VERIFIED: finite exact character interval" if valid else "REJECTED")
        return 0 if valid else 2
    try:
        if None in (args.beta_num, args.beta_den, args.bessel_terms, args.log_terms):
            raise ValueError("beta numerator/denominator and term counts required")
        result = certify_character(args.beta_num, args.beta_den,
                                   args.bessel_terms, args.log_terms)
    except ValueError as exc:
        parser.error(str(exc))
    body = json.dumps(result, sort_keys=True, indent=2, allow_nan=False) + "\n"
    if args.output is not None:
        args.output.write_text(body, encoding="utf-8")
    else:
        print(body, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
