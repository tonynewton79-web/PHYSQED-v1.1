"""Fail-closed replay of deliberately finite cold/Haar diagnostic receipts."""

import copy
import json
import tempfile
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from research.yang_mills_su2.equilibration_cli import (
    certify_equilibration, replay_equilibration_receipt, main,
)
import research.yang_mills_su2.equilibration_cli as cli


class EquilibrationReceiptTests(unittest.TestCase):
    def test_source_identity_includes_the_replay_verifier_and_python_runtime(self):
        receipt = certify_equilibration((2, 2, 2, 2), 0, 1, (12, 34), 8, 3, 20)
        self.assertEqual(receipt["python_runtime"], sys.version.split()[0])
        original_digest = cli._source_digest()
        normal_read = Path.read_bytes

        def modified_verifier_source(path):
            contents = normal_read(path)
            if path.name == "equilibration_cli.py":
                return contents + b"\n# changed verifier"
            return contents

        with patch.object(Path, "read_bytes", modified_verifier_source):
            self.assertNotEqual(cli._source_digest(), original_digest)
            self.assertFalse(replay_equilibration_receipt(receipt))

    def test_replay_committed_finite_example_receipts(self):
        root = Path(__file__).resolve().parents[1] / "artifacts/equilibration"
        names = (
            "beta0_volume2.json", "beta_half_volume2.json", "beta_half_volume3.json",
        )
        for name in names:
            with self.subTest(name=name):
                receipt = json.loads((root/name).read_text(encoding="utf-8"))
                self.assertTrue(replay_equilibration_receipt(receipt))
                self.assertFalse(receipt["equilibrium_claim"])
                self.assertFalse(receipt["continuum_mass_gap_proven"])

    def test_exact_inputs_and_recomputed_raw_traces(self):
        receipt = certify_equilibration((2, 2, 2, 2), 0, 1, (123, 456), 8, 3, 20)
        self.assertEqual(receipt, certify_equilibration((2, 2, 2, 2), 0, 1,
                                                         (123, 456), 8, 3, 20))
        self.assertTrue(replay_equilibration_receipt(receipt))
        self.assertFalse(receipt["physical_law_proven"])
        self.assertFalse(receipt["continuum_mass_gap_proven"])
        self.assertFalse(receipt["equilibrium_claim"])
        modified = copy.deepcopy(receipt)
        modified["report"]["groups"]["haar"]["chains"][0]["trace"][2]["spatial_plaquette"] += 0.1
        self.assertFalse(replay_equilibration_receipt(modified))
        modified = copy.deepcopy(receipt)
        modified["equilibrium_claim"] = True
        self.assertFalse(replay_equilibration_receipt(modified))
        modified = copy.deepcopy(receipt)
        modified["fingerprint"] = "0" * 64
        self.assertFalse(replay_equilibration_receipt(modified))

    def test_budget_and_wrong_schema_fail_closed(self):
        for args in [
            ((2, 2, 2, 2), 1, 0, (1, 2), 8, 3, 20),
            ((2, 2, 2, 2), 1, 2, (1, 2), 200, 3, 20),
            ((4, 4, 4, 4), 1, 2, (1, 2), 8, 3, 20),
            ((2, 2, 2, 2), 1, 2, (1, -1), 8, 3, 20),
            ((2, 2, 2, 2), 1, 2, (1, 2), 8, 0, 1),
        ]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                certify_equilibration(*args)
        self.assertFalse(replay_equilibration_receipt({"status": "CERTIFIED_MASS_GAP"}))
        self.assertFalse(replay_equilibration_receipt([1, 2, 3]))

    def test_cli_recomputes_and_rejects_tampered_and_deep_json(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "study.json"
            args = ["--extents", "2,2,2,2", "--beta-num", "0", "--beta-den", "1",
                    "--seeds", "123,456", "--sweeps", "8", "--epsilon-num", "3",
                    "--epsilon-den", "20", "--output", str(file)]
            self.assertEqual(main(args), 0)
            self.assertEqual(main(["--verify", str(file)]), 0)
            corrupted = json.loads(file.read_text())
            corrupted["report"]["cold_minus_haar_late_mean"] += 0.1
            file.write_text(json.dumps(corrupted))
            self.assertEqual(main(["--verify", str(file)]), 2)
            file.write_text("[" * 4000 + "0" + "]" * 4000)
            self.assertEqual(main(["--verify", str(file)]), 2)


if __name__ == "__main__":
    unittest.main()
