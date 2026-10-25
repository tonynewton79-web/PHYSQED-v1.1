"""Guard the public standalone repository's verification boundary."""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from proof_receipt import REPO, issue_review


class StandaloneReleaseTests(unittest.TestCase):
    def test_proof_receipt_targets_public_physqed_repository(self):
        self.assertEqual(REPO, "tonynewton79-web/PHYSQED-v1.1")
        contract = json.loads(
            (HERE / "fixtures" / "oscillator_contract.json").read_text()
        )
        review = issue_review(ROOT, contract, bytes(range(32)), "test-only")
        self.assertEqual(
            review["manifest"]["repository"],
            "tonynewton79-web/PHYSQED-v1.1",
        )

    def test_root_readme_explains_scope_and_has_entrypoint(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("PHYSQED v1.1", text)
        self.assertIn("projects/physqed", text)
        self.assertIn("physics", text.lower())


if __name__ == "__main__":
    unittest.main()
