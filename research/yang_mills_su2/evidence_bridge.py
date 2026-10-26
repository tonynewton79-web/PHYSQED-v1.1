"""Fail-closed evidence ledger for a finite Yang--Mills SU(2) research pilot.

Each source is re-read and its appropriate *limited* check re-executed. No
category in this module establishes a physical law or a continuum mass gap.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

from .beta_zero_correlators import replay_beta_zero_correlator_receipt
from .transfer_moment_obstructions import replay_transfer_moment_receipt
from .wilson_transfer_characters import replay_wilson_transfer_receipt
from .wilson_dobrushin import replay_strong_coupling_receipt
from .wilson_spectral_gap import replay_lattice_spectral_gap_receipt
from .wilson_chordal_mixing import replay_chordal_mixing_receipt
from .character_cli import replay_character_certificate
from .simulation import run_chains

ROOT = Path(__file__).resolve().parents[2]
SOURCE_BYTE_LIMIT = 2 * 1024 * 1024
KINDS = {
    "PHYSQED_EXACT_POLYNOMIAL": "Exact scalar polynomial identity; no physical assumptions discharged",
    "EXACT_RATIONAL_INTERVAL": "Finite SU(2) character-series interval; no four-dimensional spectrum",
    "EXACT_HAAR_CORRELATOR": "Exact ideal beta-zero Haar expectation; no physical spectral bound",
    "EXACT_TRANSFER_MOMENT_OBSTRUCTION": (
        "Exact abstract positive-transfer counterexample; not a Wilson SU2 spectral bound"),
    "EXACT_WILSON_TRANSFER_CHARACTER": (
        "Exact Wilson temporal-link character kernel; not the interacting 4D transfer spectrum"),
    "EXACT_WILSON_DOBRUSHIN_BOUND": (
        "Finite Wilson strong-coupling covariance bound; not a continuum or full-spectrum gap"),
    "EXACT_WILSON_LATTICE_SPECTRAL_RATIO": (
        "Exact gauge-invariant strong-coupling lattice spectral ratio arithmetic; "
        "analytic inputs not kernel-formalized, no continuum mass gap"),
    "EXACT_WILSON_CHORDAL_LATTICE_RATIO": (
        "Exact SU2 chordal finite-lattice spectral ratio arithmetic; "
        "analytic Poincare/mixing premises not kernel-formalized, no continuum gap"),
    "FINITE_LATTICE_NUMERICAL": "Seeded finite Wilson-lattice sampling; no continuum limit",
}
ALLOWED_METADATA = {
    "PHYSQED_EXACT_POLYNOMIAL": ({},),
    "EXACT_RATIONAL_INTERVAL": ({},),
    "EXACT_HAAR_CORRELATOR": ({}, {"scope": "beta0"}),
    "EXACT_TRANSFER_MOMENT_OBSTRUCTION": (
        {}, {"model": "positive-transfer-abstract"}),
    "EXACT_WILSON_TRANSFER_CHARACTER": (
        {}, {"model": "wilson-temporal-link"}),
    "EXACT_WILSON_DOBRUSHIN_BOUND": (
        {}, {"scope": "finite-strong-coupling"}),
    "EXACT_WILSON_LATTICE_SPECTRAL_RATIO": (
        {}, {"scope": "finite-strong-coupling-spectral-ratio"}),
    "EXACT_WILSON_CHORDAL_LATTICE_RATIO": (
        {}, {"scope": "finite-chordal-beta-lt-one-sixth"}),
    "FINITE_LATTICE_NUMERICAL": (
        {}, {"negative_control": "beta0-cold"},
        {"negative_control": "beta0-haar"}),
}
SOLVER_IDS = ("newton_solver", "einstein_x_omega")
# Pin the exact declarative quaternion polynomial. This both prevents a
# substituted tautology acquiring the quaternion label and bounds expensive
# expression execution in the unchanged, general-purpose PHYSQED engine.
QUATERNION_CHECK_SHA256 = "cb6f2479bf6bb1374bafebc128f5271d09cc05b13cac2f19dd1e5a64256be083"
OPEN_OBLIGATIONS = [
    "Construct the nontrivial continuum Yang-Mills quantum field theory in four dimensions",
    "Establish reflection positivity and the Osterwalder-Schrader axioms for the limiting measure",
    "Control ultraviolet lattice-spacing and infinite-volume limits jointly",
    "Prove a uniform positive lower bound for the full physical excitation spectrum",
    "Supply a general argument covering every compact simple gauge group G",
    "Obtain real Newton Solver and EINSTEIN-X Omega versioned source and verified integration runs",
]


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _source_path(source: Path) -> Path:
    """Interpret portable ledger paths relative to the repository root."""
    requested = Path(source)
    return (requested if requested.is_absolute() else ROOT / requested).resolve()


def _path_label(source: Path) -> str:
    try:
        return source.relative_to(ROOT).as_posix()
    except ValueError:
        return str(source)


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      allow_nan=False, ensure_ascii=True).encode("ascii")


def _bounded_bytes(path: Path) -> bytes:
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
        with os.fdopen(fd, "rb") as handle:
            if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
                raise ValueError("evidence source must be a regular file")
            data = handle.read(SOURCE_BYTE_LIMIT + 1)
    except OSError as exc:
        raise ValueError(f"source not readable: {path}") from exc
    if len(data) > SOURCE_BYTE_LIMIT:
        raise ValueError("source exceeds finite-pilot evidence byte budget")
    return data


def _load_json(path: Path) -> tuple[object, bytes]:
    data = _bounded_bytes(path)
    def unique_keys(pairs: list[tuple[str, object]]) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("ambiguous duplicate JSON key")
            result[key] = value
        return result

    try:
        return json.loads(data.decode("utf-8"), parse_constant=lambda _s: (_ for _ in ()).throw(
            ValueError("non-finite JSON value")), object_pairs_hook=unique_keys), data
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise ValueError("source must be bounded valid JSON") from exc


def verify_physqed_fixture(path: Path) -> dict:
    """Execute the repository's unchanged PHYSQED engine in a child process."""
    source_path = _source_path(path)
    claim, source_bytes = _load_json(source_path)
    if len(source_bytes) > 16 * 1024:
        raise ValueError("quaternion fixture exceeds the restricted input budget")
    if (type(claim) is not dict or
        set(claim) != {"schema_version", "id", "statement", "source", "assumptions", "checks"} or
        claim.get("schema_version") != "physqed-0.1"):
        raise ValueError("not a PHYSQED v0.1 source fixture")
    if (type(claim["statement"]) is not str or len(claim["statement"]) > 1024 or
        type(claim["source"]) is not str or len(claim["source"]) > 1024 or
        type(claim["assumptions"]) is not list or len(claim["assumptions"]) > 8 or
        any(type(a) is not str or len(a) > 256 for a in claim["assumptions"])):
        raise ValueError("unsupported quaternion fixture metadata")
    try:
        check_hash = _digest(_canonical(claim.get("checks")))
    except (TypeError, ValueError, RecursionError) as exc:
        raise ValueError("malformed quaternion expression") from exc
    if (claim.get("id") != "YM-SU2-ALG-001" or
        type(claim.get("checks")) is not list or
        check_hash != QUATERNION_CHECK_SHA256):
        raise ValueError("wrong quaternion identity or unsupported PHYSQED arithmetic")
    try:
        # Verify the immutable bytes we just parsed, not a racing path that
        # might be replaced between hash measurement and subprocess parsing.
        with tempfile.TemporaryDirectory(prefix="ym-physqed-") as folder:
            snapshot = Path(folder) / "claim.json"
            snapshot.write_bytes(source_bytes)
            command = [sys.executable, str(ROOT / "projects/physqed/engine.py"),
                       str(snapshot)]
            proc = subprocess.run(command, cwd=ROOT, check=False, capture_output=True,
                                  text=True, timeout=15)
        cert = json.loads(proc.stdout)
    except (subprocess.TimeoutExpired, OSError, ValueError, RecursionError) as exc:
        raise ValueError("PHYSQED did not produce a readable verification receipt") from exc
    if (proc.returncode != 0 or type(cert) is not dict or
        cert.get("status") != "MATHEMATICAL_COMPONENTS_VERIFIED" or
        cert.get("physical_law_proven") is not False or
        cert.get("lean_kernel_verified") is not False or
        not isinstance(cert.get("checks"), list) or
        len(cert["checks"]) != len(claim.get("checks", [])) or
        any(c.get("kind") != "algebra_identity" or c.get("passed") is not True
            for c in cert["checks"] if isinstance(c, dict)) or
        any(not isinstance(c, dict) for c in cert["checks"])):
        raise ValueError("PHYSQED rejected the finite exact polynomial fixture")
    expected_input_hash = _digest(_canonical(claim))
    if (cert.get("input_sha256") != expected_input_hash or
        cert.get("engine_sha256") != _digest((ROOT / "projects/physqed/engine.py").read_bytes()) or
        cert.get("replay_sha256") != _digest((ROOT / "projects/physqed/replay.py").read_bytes())):
        raise ValueError("PHYSQED receipt/source hash mismatch")
    claimed_hash = cert.get("certificate_sha256")
    if type(claimed_hash) is not str or claimed_hash != _digest(_canonical({
        k: v for k, v in cert.items() if k != "certificate_sha256"
    })):
        raise ValueError("PHYSQED receipt was altered")
    return cert


def _replay_numerical(obj: object) -> None:
    if type(obj) is not dict or obj.get("schema_version") != "ym-su2-finite-pilot-0.1":
        raise ValueError("not a finite SU(2) pilot result")
    if (obj.get("status") != "FINITE_LATTICE_NUMERICAL" or
        obj.get("physical_law_proven") is not False or
        obj.get("continuum_mass_gap_proven") is not False or
        obj.get("equilibrium_claim") is not False):
        raise ValueError("false or unknown numerical evidence status")
    if obj.get("thermalization_status") not in (
        "UNTHERMALIZED_COLD_START_TRANSIENT", "UNTHERMALIZED_HAAR_START_TRANSIENT",
    ):
        raise ValueError("unsubstantiated thermalization claim")
    p = obj.get("parameters")
    if type(p) is not dict or set(p) != {
        "extents", "beta", "seeds", "warmup", "sweeps", "thin",
        "epsilon", "initialization", "boundary_conditions", "action",
    }:
        raise ValueError("invalid finite pilot parameters")
    sizes, seeds = p["extents"], p["seeds"]
    if (type(sizes) is not list or len(sizes) != 4 or
        any(type(s) is not int or not 2 <= s <= 4 for s in sizes) or
        math.prod(sizes) > 32 or
        type(seeds) is not list or not 2 <= len(seeds) <= 3 or
        any(type(s) is not int or abs(s) > 2**32 for s in seeds) or
        type(p["warmup"]) is not int or not 0 <= p["warmup"] <= 32 or
        type(p["sweeps"]) is not int or not 2 <= p["sweeps"] <= 64 or
        type(p["thin"]) is not int or not 1 <= p["thin"] <= 16 or
        type(p["beta"]) not in (int, float) or
        not 0 <= p["beta"] <= 16 or not math.isfinite(p["beta"]) or
        type(p["epsilon"]) not in (int, float) or
        p["initialization"] not in ("cold", "haar") or
        not math.isfinite(p["epsilon"])):
        raise ValueError("unsafe or invalid finite numerical replay budget")
    try:
        expected = run_chains(tuple(sizes), p["beta"], tuple(seeds),
                              p["warmup"], p["sweeps"], p["thin"], p["epsilon"],
                              p["initialization"])
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        raise ValueError("finite numerical replay failed") from exc
    if _canonical(obj) != _canonical(expected):
        raise ValueError("finite numerical result does not reproduce from recorded seeds")


def record_evidence(kind: str, source_path: Path | None, metadata: dict) -> dict:
    """Produce a source-backed scoped record, never trusting reported success."""
    if type(kind) is not str or kind not in KINDS or source_path is None:
        raise ValueError("unknown evidence kind or missing source")
    if (type(metadata) is not dict or len(metadata) > 8 or
        any(type(k) is not str or len(k) > 40 or type(v) not in (str, int, bool)
            or len(str(v)) > 160 for k, v in metadata.items())):
        raise ValueError("metadata must contain at most eight short scalar fields")
    if metadata not in ALLOWED_METADATA[kind]:
        raise ValueError("unrecognized evidence provenance or physical classification")
    path = _source_path(source_path)
    obj, data = _load_json(path)
    if kind == "PHYSQED_EXACT_POLYNOMIAL":
        receipt = verify_physqed_fixture(path)
        assert receipt["physical_law_proven"] is False
        if receipt["input_sha256"] != _digest(_canonical(obj)):
            raise ValueError("PHYSQED receipt is not bound to its source data")
        if _bounded_bytes(path) != data:
            raise ValueError("PHYSQED source changed during certificate generation")
        status = "MATHEMATICAL_COMPONENTS_VERIFIED"
        verification_hash = receipt["certificate_sha256"]
    elif kind == "EXACT_RATIONAL_INTERVAL":
        if not replay_character_certificate(obj):
            raise ValueError("character interval certificate failed exact replay")
        status = "FINITE_CHARACTER_EXACT_INTERVAL"
        verification_hash = obj["fingerprint"]
    elif kind == "EXACT_HAAR_CORRELATOR":
        if not replay_beta_zero_correlator_receipt(obj):
            raise ValueError("beta-zero Haar correlation expectation failed exact replay")
        status = "FINITE_HAAR_CORRELATOR_EXPECTATIONS"
        verification_hash = _digest(_canonical(obj))
    elif kind == "EXACT_TRANSFER_MOMENT_OBSTRUCTION":
        if not replay_transfer_moment_receipt(obj):
            raise ValueError("abstract positive-transfer moment certificate failed exact replay")
        status = "ABSTRACT_SPECTRAL_MASKING_EXACT"
        verification_hash = _digest(_canonical(obj))
    elif kind == "EXACT_WILSON_TRANSFER_CHARACTER":
        if not replay_wilson_transfer_receipt(obj):
            raise ValueError("Wilson temporal-link character certificate failed exact replay")
        status = "FINITE_WILSON_TRANSFER_CHARACTER_EXACT"
        verification_hash = _digest(_canonical(obj))
    elif kind == "EXACT_WILSON_DOBRUSHIN_BOUND":
        if not replay_strong_coupling_receipt(obj):
            raise ValueError("Wilson Dobrushin rational bound failed exact replay")
        status = "FINITE_STRONG_COUPLING_COVARIANCE_BOUND"
        verification_hash = _digest(_canonical(obj))
    elif kind == "EXACT_WILSON_LATTICE_SPECTRAL_RATIO":
        if not replay_lattice_spectral_gap_receipt(obj):
            raise ValueError("Wilson lattice spectral ratio arithmetic failed exact replay")
        status = "FINITE_WILSON_LATTICE_SPECTRAL_RATIO_ARITHMETIC"
        verification_hash = _digest(_canonical(obj))
    elif kind == "EXACT_WILSON_CHORDAL_LATTICE_RATIO":
        if not replay_chordal_mixing_receipt(obj):
            raise ValueError("Wilson chordal lattice ratio arithmetic failed exact replay")
        status = "FINITE_SU2_CHORDAL_MIXING_RATIO_ARITHMETIC"
        verification_hash = _digest(_canonical(obj))
    else:
        _replay_numerical(obj)
        status = "FINITE_LATTICE_NUMERICAL"
        verification_hash = _digest(data)
    implementation = {
        "PHYSQED_EXACT_POLYNOMIAL": ("projects/physqed/engine.py", "projects/physqed/replay.py"),
        "EXACT_RATIONAL_INTERVAL": ("research/yang_mills_su2/character_bounds.py",
                                    "research/yang_mills_su2/character_cli.py"),
        "EXACT_HAAR_CORRELATOR": ("research/yang_mills_su2/beta_zero_correlators.py",),
        "EXACT_TRANSFER_MOMENT_OBSTRUCTION": (
            "research/yang_mills_su2/transfer_moment_obstructions.py",),
        "EXACT_WILSON_TRANSFER_CHARACTER": (
            "research/yang_mills_su2/wilson_transfer_characters.py",
            "research/yang_mills_su2/character_bounds.py"),
        "EXACT_WILSON_DOBRUSHIN_BOUND": (
            "research/yang_mills_su2/wilson_dobrushin.py",),
        "EXACT_WILSON_LATTICE_SPECTRAL_RATIO": (
            "research/yang_mills_su2/wilson_spectral_gap.py",
            "research/yang_mills_su2/wilson_dobrushin.py"),
        "EXACT_WILSON_CHORDAL_LATTICE_RATIO": (
            "research/yang_mills_su2/wilson_chordal_mixing.py",
            "research/yang_mills_su2/wilson_spectral_gap.py"),
        "FINITE_LATTICE_NUMERICAL": ("research/yang_mills_su2/su2.py",
                                     "research/yang_mills_su2/lattice.py",
                                     "research/yang_mills_su2/simulation.py"),
    }[kind]
    implementation_digest = _digest(b"".join(
        len(blob).to_bytes(8, "big") + blob
        for blob in (_bounded_bytes(ROOT / filename) for filename in implementation)
    ))
    return {
        "kind": kind, "status": status, "scope": KINDS[kind],
        "source_path": _path_label(path), "source_sha256": _digest(data),
        "verification_sha256": verification_hash,
        "verification_implementation_sha256": implementation_digest,
        "python_runtime": sys.version.split()[0], "metadata": metadata,
        "physical_law_proven": False, "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
    }


def _source_state(path: Path | None) -> dict:
    if path is None:
        return {"status": "SOURCE_UNAVAILABLE_NOT_EXECUTED",
                "source_path": None, "source_sha256": None}
    source = _source_path(path)
    return {"status": "SOURCE_LOCATED_UNTESTED", "source_path": _path_label(source),
            "source_sha256": _digest(_bounded_bytes(source))}


def _ledger_hash(ledger: dict) -> str:
    return _digest(_canonical({key: value for key, value in ledger.items()
                               if key != "ledger_sha256"}))


def build_ledger(records: list[dict], newton_source: Path | None = None,
                 einstein_source: Path | None = None) -> dict:
    if type(records) is not list or len(records) > 16:
        raise ValueError("finite-pilot ledger must have at most sixteen records")
    for record in records:
        _validate_record(record)
    ledger = {
        "schema_version": "ym-su2-evidence-ledger-0.1",
        "status": "FINITE_RESEARCH_EVIDENCE_ONLY",
        "records": records,
        "external_solver_integrations": {
            "newton_solver": _source_state(newton_source),
            "einstein_x_omega": _source_state(einstein_source),
        },
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
    }
    ledger["ledger_sha256"] = _ledger_hash(ledger)
    return ledger


def _validate_record(record: object) -> None:
    if type(record) is not dict or set(record) != {
        "kind", "status", "scope", "source_path", "source_sha256",
        "verification_sha256", "verification_implementation_sha256", "python_runtime",
        "metadata", "physical_law_proven",
        "continuum_mass_gap_proven", "lean_kernel_verified",
    }:
        raise ValueError("malformed evidence record")
    if type(record["source_path"]) is not str or len(record["source_path"]) > 1024:
        raise ValueError("invalid source path")
    expected = record_evidence(record["kind"], Path(record["source_path"]),
                               record["metadata"])
    if expected != record:
        raise ValueError("evidence record no longer agrees with its independent replay")


def validate_ledger(ledger: dict) -> None:
    if type(ledger) is not dict or set(ledger) != {
        "schema_version", "status", "records", "external_solver_integrations",
        "physical_law_proven", "continuum_mass_gap_proven", "lean_kernel_verified",
        "ledger_sha256",
    }:
        raise ValueError("malformed evidence ledger")
    if (ledger["schema_version"] != "ym-su2-evidence-ledger-0.1" or
        ledger["status"] != "FINITE_RESEARCH_EVIDENCE_ONLY" or
        any(ledger[key] is not False for key in (
            "physical_law_proven", "continuum_mass_gap_proven", "lean_kernel_verified")) or
        type(ledger["records"]) is not list or len(ledger["records"]) > 16):
        raise ValueError("false or unsupported evidence ledger claims")
    for record in ledger["records"]:
        _validate_record(record)
    states = ledger["external_solver_integrations"]
    if type(states) is not dict or set(states) != set(SOLVER_IDS):
        raise ValueError("missing external solver integration status")
    for key in SOLVER_IDS:
        state = states[key]
        if type(state) is not dict or set(state) != {
            "status", "source_path", "source_sha256",
        }:
            raise ValueError("invalid external engine evidence")
        source = state["source_path"]
        if source is not None and type(source) is not str:
            raise ValueError("invalid external engine source")
        if state != _source_state(Path(source) if source is not None else None):
            raise ValueError("external engine execution cannot be inferred from mere source presence")
    if type(ledger["ledger_sha256"]) is not str or _ledger_hash(ledger) != ledger["ledger_sha256"]:
        raise ValueError("evidence ledger integrity hash mismatch")


def assemble_pilot_report(character_certificate: Path, simulation_result: Path,
                          algebra_fixture: Path, cold_control: Path | None = None,
                          haar_control: Path | None = None) -> dict:
    if (cold_control is None) != (haar_control is None):
        raise ValueError("cold and Haar beta-zero controls must be supplied together")
    records = [
        record_evidence("EXACT_RATIONAL_INTERVAL", character_certificate, {}),
        record_evidence("FINITE_LATTICE_NUMERICAL", simulation_result, {}),
        record_evidence("PHYSQED_EXACT_POLYNOMIAL", algebra_fixture, {}),
    ]
    controls = []
    if cold_control is not None:
        for path, label in ((cold_control, "cold"), (haar_control, "haar")):
            record = record_evidence("FINITE_LATTICE_NUMERICAL", path,
                                     {"negative_control": f"beta0-{label}"})
            obj, raw = _load_json(_source_path(path))
            if _digest(raw) != record["source_sha256"]:
                raise ValueError("beta-zero control source changed during assembly")
            p = obj["parameters"]
            if p["beta"] != 0.0 or p["initialization"] != label:
                raise ValueError("invalid beta-zero negative control initialization")
            controls.append((record, p))
        cold_parameters, hot_parameters = (p for _, p in controls)
        if {k: v for k, v in cold_parameters.items() if k != "initialization"} != {
            k: v for k, v in hot_parameters.items() if k != "initialization"
        }:
            raise ValueError("negative control protocols are not matched")
    ledger = build_ledger(records + [record for record, _ in controls])
    return {
        "schema_version": "ym-su2-combined-pilot-report-0.1",
        "status": "FINITE_CROSS_EVIDENCE_PILOT",
        "math": records[0], "physical_numerical": records[1],
        "physqed": records[2],
        "negative_controls": [record for record, _ in controls],
        "external_solver_integrations": ledger["external_solver_integrations"],
        "evidence_ledger": ledger,
        "open_obligations": list(OPEN_OBLIGATIONS),
        "physical_law_proven": False,
        "continuum_mass_gap_proven": False,
        "lean_kernel_verified": False,
    }


def validate_report(report: dict) -> None:
    """Rebuild all evidence before accepting an allegedly verified report."""
    if (type(report) is not dict or
        report.get("schema_version") != "ym-su2-combined-pilot-report-0.1" or
        type(report.get("evidence_ledger")) is not dict):
        raise ValueError("malformed combined pilot report")
    ledger = report["evidence_ledger"]
    validate_ledger(ledger)
    records = ledger["records"]
    if len(records) not in (3, 5) or [r["kind"] for r in records] != [
        "EXACT_RATIONAL_INTERVAL", "FINITE_LATTICE_NUMERICAL",
        "PHYSQED_EXACT_POLYNOMIAL",
    ] + (["FINITE_LATTICE_NUMERICAL"] * (len(records)-3)):
        raise ValueError("combined report has missing or reclassified evidence")
    expected = assemble_pilot_report(*(Path(r["source_path"]) for r in records))
    if _canonical(report) != _canonical(expected):
        raise ValueError("combined report does not match independently regenerated evidence")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--character", type=Path)
    parser.add_argument("--simulation", type=Path)
    parser.add_argument("--algebra", type=Path)
    parser.add_argument("--cold-control", type=Path)
    parser.add_argument("--haar-control", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args(argv)
    if args.verify is not None:
        try:
            obj, _ = _load_json(args.verify)
            validate_report(obj)
        except (ValueError, TypeError, KeyError, RecursionError):
            print("REJECTED: combined finite pilot")
            return 2
        print("VERIFIED: combined finite pilot only")
        return 0
    if None in (args.character, args.simulation, args.algebra):
        parser.error("--character, --simulation and --algebra required")
    try:
        report = assemble_pilot_report(args.character, args.simulation, args.algebra,
                                       args.cold_control, args.haar_control)
        body = json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n"
        if args.output is not None:
            args.output.write_text(body, encoding="utf-8")
        else:
            print(body, end="")
    except (ValueError, OSError, RecursionError) as exc:
        parser.exit(2, f"EVIDENCE REFUSED: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
