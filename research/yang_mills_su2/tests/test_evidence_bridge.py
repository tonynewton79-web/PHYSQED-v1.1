"""Real PHYSQED subprocess and fail-closed cross-evidence contract tests."""

import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from research.yang_mills_su2.character_cli import certify_character
from research.yang_mills_su2.beta_zero_correlators import beta_zero_correlator_receipt
from research.yang_mills_su2.transfer_moment_obstructions import transfer_moment_receipt
from research.yang_mills_su2.wilson_transfer_characters import wilson_transfer_receipt
from research.yang_mills_su2.wilson_dobrushin import strong_coupling_receipt
from research.yang_mills_su2.wilson_spectral_gap import lattice_spectral_gap_receipt
from research.yang_mills_su2.wilson_chordal_mixing import chordal_mixing_receipt
from research.yang_mills_su2.continuum_scale_bridge import scale_bridge_receipt
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

    def test_exact_beta_zero_receipt_can_enter_fail_closed_evidence_ledger(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "beta0-correlator.json"
            original = beta_zero_correlator_receipt((4,2,2,2), 2)
            path.write_text(json.dumps(original), encoding="utf-8")
            record = self.record("EXACT_HAAR_CORRELATOR", path, {"scope": "beta0"})
            self.assertEqual(record["status"], "FINITE_HAAR_CORRELATOR_EXPECTATIONS")
            self.assertFalse(record["continuum_mass_gap_proven"])
            ledger = self.ledger([record])
            self.validate(ledger)
            forged = copy.deepcopy(original)
            forged["equilibrium_claim"] = True
            path.write_text(json.dumps(forged), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.validate(ledger)
            path.write_text(json.dumps(original), encoding="utf-8")
            changed_ledger = copy.deepcopy(ledger)
            changed_ledger["records"][0]["verification_sha256"] = "0" * 64
            with self.assertRaises(ValueError):
                self.validate(changed_ledger)

    def test_exact_abstract_transfer_obstruction_has_distinct_evidence_status(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "abstract-transfer.json"
            original = transfer_moment_receipt(10, 3)
            path.write_text(json.dumps(original), encoding="utf-8")
            record = self.record("EXACT_TRANSFER_MOMENT_OBSTRUCTION", path,
                                 {"model": "positive-transfer-abstract"})
            self.assertEqual(record["status"], "ABSTRACT_SPECTRAL_MASKING_EXACT")
            self.assertIn("abstract", record["scope"].lower())
            self.assertFalse(record["physical_law_proven"])
            self.assertFalse(record["continuum_mass_gap_proven"])
            self.assertFalse(record["lean_kernel_verified"])
            ledger = self.ledger([record])
            self.validate(ledger)
            altered = copy.deepcopy(original)
            altered["hankel_minors"][1]["numerator"] = "1"
            path.write_text(json.dumps(altered), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.record("EXACT_TRANSFER_MOMENT_OBSTRUCTION", path, {})
            with self.assertRaises(ValueError):
                self.validate(ledger)
            path.write_text(json.dumps(original), encoding="utf-8")
            forged = copy.deepcopy(ledger)
            forged["records"][0]["scope"] = "Proven SU2 continuum mass gap"
            with self.assertRaises(ValueError):
                self.validate(forged)

    def test_abstract_transfer_evidence_rejects_physically_misleading_metadata(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "exact-abstract.json"
            path.write_text(json.dumps(transfer_moment_receipt(10, 2)), encoding="utf-8")
            for metadata in (
                {"continuum_mass_gap_proven": True},
                {"model": "Wilson SU2 Yang Mills"},
                {"model": "positive-transfer-abstract", "physical_law_proven": True},
                {"model": "positive-transfer-abstract", "status": "PROVED"},
            ):
                with self.subTest(metadata=metadata), self.assertRaises(ValueError):
                    self.record("EXACT_TRANSFER_MOMENT_OBSTRUCTION", path, metadata)

    def test_duplicate_physical_claim_key_cannot_hide_in_json_receipt(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "ambiguous.json"
            source = json.dumps(transfer_moment_receipt(10, 2))
            self.assertIn('"physical_law_proven": false', source)
            ambiguous = source.replace('"physical_law_proven": false',
                                       '"physical_law_proven": true, "physical_law_proven": false')
            path.write_text(ambiguous, encoding="utf-8")
            with self.assertRaises(ValueError):
                self.record("EXACT_TRANSFER_MOMENT_OBSTRUCTION", path, {})

    def test_exact_positive_beta_wilson_temporal_kernel_has_separate_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "wilson-temporal.json"
            original = wilson_transfer_receipt(2, 1, 8, 12, 12)
            path.write_text(json.dumps(original), encoding="utf-8")
            record = self.record("EXACT_WILSON_TRANSFER_CHARACTER", path,
                                 {"model": "wilson-temporal-link"})
            self.assertEqual(record["status"], "FINITE_WILSON_TRANSFER_CHARACTER_EXACT")
            self.assertIn("Wilson temporal-link", record["scope"])
            self.assertFalse(record["continuum_mass_gap_proven"])
            ledger = self.ledger([record])
            self.validate(ledger)
            forged = copy.deepcopy(original)
            forged["fundamental_to_trivial_ratio"]["upper"]["numerator"] = "1"
            path.write_text(json.dumps(forged), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.validate(ledger)
            path.write_text(json.dumps(original), encoding="utf-8")
            for metadata in ({"continuum_mass_gap_proven": True},
                             {"model": "continuum Wilson spectrum"}):
                with self.subTest(metadata=metadata), self.assertRaises(ValueError):
                    self.record("EXACT_WILSON_TRANSFER_CHARACTER", path, metadata)

    def test_committed_wilson_character_artifact_exactly_replays(self):
        path = ROOT / "research/yang_mills_su2/artifacts/wilson_transfer_beta2_exact.json"
        record = self.record("EXACT_WILSON_TRANSFER_CHARACTER", path, {})
        self.assertEqual(record["status"], "FINITE_WILSON_TRANSFER_CHARACTER_EXACT")

    def test_exact_strong_coupling_receipt_has_distinct_fail_closed_scope(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "strong-coupling.json"
            original = strong_coupling_receipt((8, 2, 2, 2), 1, 100, 4)
            path.write_text(json.dumps(original), encoding="utf-8")
            record = self.record("EXACT_WILSON_DOBRUSHIN_BOUND", path,
                                 {"scope": "finite-strong-coupling"})
            self.assertEqual(record["status"], "FINITE_STRONG_COUPLING_COVARIANCE_BOUND")
            self.assertIn("strong-coupling", record["scope"])
            self.assertFalse(record["continuum_mass_gap_proven"])
            ledger = self.ledger([record])
            self.validate(ledger)
            for bad_metadata in ({"continuum_mass_gap_proven": True},
                                 {"scope": "full-spectrum-gap"},
                                 {"scope": "finite-strong-coupling", "lean_proven": True}):
                with self.subTest(metadata=bad_metadata), self.assertRaises(ValueError):
                    self.record("EXACT_WILSON_DOBRUSHIN_BOUND", path, bad_metadata)
            forged = copy.deepcopy(original)
            forged["covariance_upper"]["denominator"] = "1"
            path.write_text(json.dumps(forged), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.validate(ledger)

    def test_lattice_transfer_ratio_has_distinct_noncontinuum_evidence_kind(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "lattice-spectral-gap.json"
            original = lattice_spectral_gap_receipt(1, 100, 8)
            path.write_text(json.dumps(original), encoding="utf-8")
            record = self.record("EXACT_WILSON_LATTICE_SPECTRAL_RATIO", path,
                                 {"scope": "finite-strong-coupling-spectral-ratio"})
            self.assertEqual(record["status"],
                             "FINITE_WILSON_LATTICE_SPECTRAL_RATIO_ARITHMETIC")
            self.assertIn("gauge-invariant", record["scope"])
            self.assertFalse(record["continuum_mass_gap_proven"])
            ledger = self.ledger([record])
            self.validate(ledger)
            for metadata in ({"continuum_mass_gap_proven": True},
                             {"scope": "continuum-mass-gap"},
                             {"scope": "finite-strong-coupling-spectral-ratio",
                              "lean_kernel_verified": True}):
                with self.subTest(metadata=metadata), self.assertRaises(ValueError):
                    self.record("EXACT_WILSON_LATTICE_SPECTRAL_RATIO", path, metadata)
            forged = copy.deepcopy(original)
            forged["lattice_gap_lower"]["numerator"] = "0"
            path.write_text(json.dumps(forged), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.validate(ledger)

    def test_committed_lattice_transfer_ratio_artifact_replays(self):
        path = ROOT / "research/yang_mills_su2/artifacts/wilson_lattice_spectral_gap_beta1_over_100.json"
        record = self.record("EXACT_WILSON_LATTICE_SPECTRAL_RATIO", path, {})
        self.assertEqual(record["status"],
                         "FINITE_WILSON_LATTICE_SPECTRAL_RATIO_ARITHMETIC")

    def test_chordal_wilson_lattice_bound_has_distinct_fail_closed_kind(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "chordal-spectral-ratio.json"
            original = chordal_mixing_receipt(1, 10, 8)
            path.write_text(json.dumps(original), encoding="utf-8")
            record = self.record("EXACT_WILSON_CHORDAL_LATTICE_RATIO", path,
                                 {"scope": "finite-chordal-beta-lt-one-sixth"})
            self.assertEqual(record["status"],
                             "FINITE_SU2_CHORDAL_MIXING_RATIO_ARITHMETIC")
            self.assertIn("chordal", record["scope"])
            self.assertFalse(record["continuum_mass_gap_proven"])
            ledger = self.ledger([record])
            self.validate(ledger)
            for bad_metadata in ({"scope": "continuum"},
                                 {"physical_law_proven": True},
                                 {"scope": "finite-chordal-beta-lt-one-sixth",
                                  "lean_kernel_verified": True}):
                with self.subTest(metadata=bad_metadata), self.assertRaises(ValueError):
                    self.record("EXACT_WILSON_CHORDAL_LATTICE_RATIO", path,
                                bad_metadata)
            forged = copy.deepcopy(original)
            forged["sharp_quarter_wasserstein_bound_verified"] = True
            path.write_text(json.dumps(forged), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.validate(ledger)

    def test_committed_chordal_wilson_beta_tenth_artifact_replays(self):
        path = ROOT / "research/yang_mills_su2/artifacts/wilson_chordal_beta1_over_10.json"
        record = self.record("EXACT_WILSON_CHORDAL_LATTICE_RATIO", path, {})
        self.assertEqual(record["status"],
                         "FINITE_SU2_CHORDAL_MIXING_RATIO_ARITHMETIC")

    def test_abstract_scale_window_has_separate_nonphysical_ledger_scope(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "scale-bridge.json"
            original = scale_bridge_receipt("finite_mass", 8, 6)
            path.write_text(json.dumps(original), encoding="utf-8")
            record = self.record("EXACT_ABSTRACT_PHYSICAL_SCALE_BRIDGE", path,
                                 {"model": "diagonal-transfer-abstract"})
            self.assertEqual(record["status"],
                             "ABSTRACT_SCALE_BRIDGE_ARITHMETIC_ONLY")
            self.assertIn("abstract", record["scope"].lower())
            self.assertFalse(record["continuum_mass_gap_proven"])
            ledger = self.ledger([record])
            self.validate(ledger)
            for bad in ({"continuum_mass_gap_proven": True},
                        {"model": "Wilson continuum SU2"},
                        {"model": "diagonal-transfer-abstract",
                         "lean_kernel_verified": True}):
                with self.subTest(bad=bad), self.assertRaises(ValueError):
                    self.record("EXACT_ABSTRACT_PHYSICAL_SCALE_BRIDGE", path, bad)
            forged = copy.deepcopy(original)
            forged["derived"]["physical_gap_lower"]["numerator"] = "999"
            path.write_text(json.dumps(forged), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.validate(ledger)

    def test_legacy_evidence_categories_also_refuse_false_physical_metadata(self):
        character = ROOT / "research/yang_mills_su2/artifacts/character_beta2_exact.json"
        for kind, source in (("PHYSQED_EXACT_POLYNOMIAL", FIXTURE),
                             ("EXACT_RATIONAL_INTERVAL", character)):
            for metadata in ({"continuum_mass_gap_proven": True},
                             {"model": "4D Wilson SU2 spectrum proven"},
                             {"physical_law_proven": True}):
                with self.subTest(kind=kind, metadata=metadata), self.assertRaises(ValueError):
                    self.record(kind, source, metadata)

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
