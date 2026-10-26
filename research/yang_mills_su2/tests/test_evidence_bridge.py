"""Real PHYSQED subprocess and fail-closed cross-evidence contract tests."""

import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from research.yang_mills_su2.character_cli import certify_character
from research.yang_mills_su2.simulation import run_chains


ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "research/yang_mills_su2/fixtures/quaternion_scalar_norm_identity.json"


class EvidenceBridgeTests(unittest.TestCase):
    def setUp(self):
        from research.yang_mills_su2.evidence_bridge import (
            assemble_pilot_report, build_ledger, record_evidence,
            validate_ledger, verify_physqed_fixture,
        )
        self.assemble = assemble_pilot_report
        self.ledger = build_ledger
        self.record = record_evidence
        self.validate = validate_ledger
        self.physqed = verify_physqed_fixture

    def test_unmodified_physqed_engine_certifies_fixture_only(self):
        self.assertTrue(FIXTURE.is_file())
        result = self.physqed(FIXTURE)
        self.assertEqual(result["status"], "MATHEMATICAL_COMPONENTS_VERIFIED")
        self.assertEqual(len(result["checks"]), 1)
        self.assertTrue(result["checks"][0]["passed"])
        self.assertFalse(result["physical_law_proven"])
        self.assertFalse(result["lean_kernel_verified"])

    def test_sign_error_is_not_forgiven_by_claim_prose(self):
        altered = json.loads(FIXTURE.read_text())
        altered["checks"][0]["lhs"]["args"][1]["args"][0]["const"] = "1"
        with tempfile.TemporaryDirectory() as temp:
            altered_file = Path(temp) / "bad_identity.json"
            altered_file.write_text(json.dumps(altered))
            with self.assertRaises(ValueError):
                self.physqed(altered_file)
            with self.assertRaises(ValueError):
                self.record("PHYSQED_EXACT_POLYNOMIAL", altered_file, {})

    def test_lookalike_tautology_cannot_masquerade_as_quaternion_fixture(self):
        altered = json.loads(FIXTURE.read_text())
        altered["checks"][0]["lhs"] = copy.deepcopy(altered["checks"][0]["rhs"])
        with tempfile.TemporaryDirectory() as temp:
            pretend = Path(temp) / "tautology.json"
            pretend.write_text(json.dumps(altered))
            with self.assertRaises(ValueError):
                self.physqed(pretend)

    def test_reject_compact_arithmetic_bomb_before_unmodified_engine(self):
        altered = json.loads(FIXTURE.read_text())
        expression = {"const": "2"}
        for _ in range(10):
            expression = {"op": "pow", "arg": expression, "exp": 8}
        altered["checks"][0]["lhs"] = expression
        with tempfile.TemporaryDirectory() as temp:
            attack = Path(temp) / "exponential_nested.json"
            attack.write_text(json.dumps(altered))
            with self.assertRaisesRegex(ValueError, "unsupported PHYSQED arithmetic|wrong quaternion"):
                self.physqed(attack)

    def test_provenance_race_refused_if_initial_record_differs_from_verified_fixture(self):
        import research.yang_mills_su2.evidence_bridge as bridge

        good_bytes = FIXTURE.read_bytes()
        good = json.loads(good_bytes)
        bad = copy.deepcopy(good)
        bad["checks"] = []
        bad_bytes = json.dumps(bad).encode("utf-8")
        original = bridge._load_json
        calls = [0]

        def changed_source(path):
            calls[0] += 1
            if calls[0] == 1:
                return bad, bad_bytes
            return original(path)

        with patch.object(bridge, "_load_json", side_effect=changed_source):
            with self.assertRaises(ValueError):
                self.record("PHYSQED_EXACT_POLYNOMIAL", FIXTURE, {})

    def test_three_scoped_evidence_classes_and_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            cert, sim = self._make_files(Path(temp))
            records = [
                self.record("PHYSQED_EXACT_POLYNOMIAL", FIXTURE, {}),
                self.record("EXACT_RATIONAL_INTERVAL", cert, {}),
                self.record("FINITE_LATTICE_NUMERICAL", sim, {}),
            ]
            self.assertEqual(len({r["source_sha256"] for r in records}), 3)
            self.assertEqual({r["kind"] for r in records}, {
                "PHYSQED_EXACT_POLYNOMIAL", "EXACT_RATIONAL_INTERVAL",
                "FINITE_LATTICE_NUMERICAL",
            })
            self.assertTrue(all(r["physical_law_proven"] is False for r in records))
            ledger = self.ledger(records)
            self.validate(ledger)
            forged = copy.deepcopy(ledger)
            forged["records"][1]["source_sha256"] = "0" * 64
            with self.assertRaises(ValueError):
                self.validate(forged)
            forged = copy.deepcopy(ledger)
            forged["records"][0]["physical_law_proven"] = True
            with self.assertRaises(ValueError):
                self.validate(forged)
            certificate = json.loads(cert.read_text())
            certificate["physical_law_proven"] = True
            cert.write_text(json.dumps(certificate))
            with self.assertRaises(ValueError):
                self.validate(ledger)
            # A plausible looking but edited measurement cannot reuse seeds
            # as a claim of independent numerical replay.
            sim_data = json.loads(sim.read_text())
            sim_data["per_chain"][0]["measurements"][0]["timeslice"][0] += 0.01
            sim.write_text(json.dumps(sim_data))
            with self.assertRaises(ValueError):
                self.record("FINITE_LATTICE_NUMERICAL", sim, {})

    def test_unknown_kinds_and_missing_sources_refused(self):
        with self.assertRaises(ValueError):
            self.record("CONTINUUM_MASS_GAP_PROOF", FIXTURE, {})
        with self.assertRaises(ValueError):
            self.record(["PHYSQED_EXACT_POLYNOMIAL"], FIXTURE, {})
        with self.assertRaises(ValueError):
            self.record("PHYSQED_EXACT_POLYNOMIAL", None, {})
        with self.assertRaises(ValueError):
            self.record("PHYSQED_EXACT_POLYNOMIAL", Path("not-real-physqed.json"), {})
        if hasattr(os, "mkfifo"):
            with tempfile.TemporaryDirectory() as temp:
                pipe = Path(temp) / "non_regular_source"
                os.mkfifo(pipe)
                with self.assertRaises(ValueError):
                    self.record("PHYSQED_EXACT_POLYNOMIAL", pipe, {})

    def test_external_engines_remain_unexecuted_even_when_source_present(self):
        empty = self.ledger([])
        self.assertEqual(empty["external_solver_integrations"]["newton_solver"]["status"],
                         "SOURCE_UNAVAILABLE_NOT_EXECUTED")
        self.assertEqual(empty["external_solver_integrations"]["einstein_x_omega"]["status"],
                         "SOURCE_UNAVAILABLE_NOT_EXECUTED")
        found = self.ledger([], newton_source=FIXTURE)
        self.assertEqual(found["external_solver_integrations"]["newton_solver"]["status"],
                         "SOURCE_LOCATED_UNTESTED")
        self.validate(found)
        forged = copy.deepcopy(found)
        forged["external_solver_integrations"]["newton_solver"]["status"] = "EXECUTED"
        with self.assertRaises(ValueError):
            self.validate(forged)

    def test_report_assembles_actual_sources_no_fake_spectral_gap(self):
        with tempfile.TemporaryDirectory() as temp:
            cert, sim = self._make_files(Path(temp))
            report = self.assemble(cert, sim, FIXTURE)
            self.assertEqual(report["status"], "FINITE_CROSS_EVIDENCE_PILOT")
            self.assertFalse(report["continuum_mass_gap_proven"])
            self.assertFalse(report["physical_law_proven"])
            self.assertFalse(report["lean_kernel_verified"])
            self.assertEqual(len(report["evidence_ledger"]["records"]), 3)
            self.assertIn("reflection positivity", " ".join(report["open_obligations"]).lower())
            self.validate(report["evidence_ledger"])
            sim.unlink()
            with self.assertRaises(ValueError):
                self.assemble(cert, sim, FIXTURE)

    def test_report_cli_roundtrip_and_tampered_report_rejection(self):
        from research.yang_mills_su2.evidence_bridge import main

        with tempfile.TemporaryDirectory() as temp:
            cert, sim = self._make_files(Path(temp))
            report = Path(temp) / "integrated.json"
            args = ["--character", str(cert), "--simulation", str(sim),
                    "--algebra", str(FIXTURE), "--output", str(report)]
            self.assertEqual(main(args), 0)
            self.assertEqual(main(["--verify", str(report)]), 0)
            altered = json.loads(report.read_text())
            altered["physical_law_proven"] = True
            report.write_text(json.dumps(altered))
            self.assertEqual(main(["--verify", str(report)]), 2)

    def test_committed_research_artifacts_can_be_independently_replayed(self):
        from research.yang_mills_su2.evidence_bridge import validate_report

        artifact = ROOT / "research/yang_mills_su2/artifacts/integrated_evidence_report.json"
        report = json.loads(artifact.read_text(encoding="utf-8"))
        validate_report(report)
        self.assertEqual({r["source_path"] for r in report["evidence_ledger"]["records"]}, {
            "research/yang_mills_su2/artifacts/character_beta2_exact.json",
            "research/yang_mills_su2/artifacts/finite_su2_2x2x2x2_pilot.json",
            "research/yang_mills_su2/fixtures/quaternion_scalar_norm_identity.json",
            "research/yang_mills_su2/artifacts/cold_beta0_negative_control.json",
            "research/yang_mills_su2/artifacts/haar_beta0_negative_control.json",
        })

    def test_beta_zero_negative_controls_expose_cold_start_bias(self):
        folder = ROOT / "research/yang_mills_su2/artifacts"
        cold = folder / "cold_beta0_negative_control.json"
        hot = folder / "haar_beta0_negative_control.json"
        for path in (cold, hot):
            self.record("FINITE_LATTICE_NUMERICAL", path, {})
        cold_data, hot_data = (json.loads(path.read_text()) for path in (cold, hot))
        self.assertEqual(cold_data["parameters"]["beta"], 0.0)
        self.assertEqual(hot_data["parameters"]["beta"], 0.0)
        self.assertEqual(cold_data["parameters"]["initialization"], "cold")
        self.assertEqual(hot_data["parameters"]["initialization"], "haar")
        self.assertGreater(cold_data["spatial_plaquette"]["mean"], 0.8)
        self.assertLess(abs(hot_data["spatial_plaquette"]["mean"]), 0.3)
        self.assertFalse(cold_data["equilibrium_claim"])
        self.assertFalse(hot_data["equilibrium_claim"])

    def test_integrated_report_cites_both_control_sources(self):
        folder = ROOT / "research/yang_mills_su2/artifacts"
        with tempfile.TemporaryDirectory() as temp:
            cert, sim = self._make_files(Path(temp))
            with self.assertRaises(ValueError):
                self.assemble(cert, sim, FIXTURE,
                              cold_control=folder / "cold_beta0_negative_control.json")
            report = self.assemble(
                cert, sim, FIXTURE,
                cold_control=folder / "cold_beta0_negative_control.json",
                haar_control=folder / "haar_beta0_negative_control.json",
            )
            self.assertEqual(len(report["negative_controls"]), 2)
            self.assertEqual(len(report["evidence_ledger"]["records"]), 5)
            self.validate(report["evidence_ledger"])

    @staticmethod
    def _make_files(temp: Path) -> tuple[Path, Path]:
        cert = temp / "certificate.json"
        sim = temp / "simulation.json"
        cert.write_text(json.dumps(certify_character(2, 1, 8, 8)), encoding="utf-8")
        sim.write_text(json.dumps(run_chains((2, 2, 2, 2), 0.5, (3, 11), 0, 2, 1, 0.1)),
                       encoding="utf-8")
        return cert, sim


if __name__ == "__main__":
    unittest.main()
