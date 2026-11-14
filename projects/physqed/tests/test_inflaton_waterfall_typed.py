"""Inflaton/waterfall minisuperspace exact scoped PHYSQED gates.

The conservative homogeneous lapse-fixed Lagrangian is checked against its
displayed Euler-Lagrange equations. This deliberately does NOT check a
radiation-bath law, an FLRW solution, an ABJM field map or observational fit.
"""
import copy
import json
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from v12.typed_input import execute_physics_input, replay_physics_input


FIXTURE = ROOT / "examples" / "typed" / "inflaton_waterfall_minisuperspace.json"


class InflatonWaterfallExactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_physics_lagrangian_equations(self):
        result = execute_physics_input(self.spec)
        self.assertTrue(result["status"].startswith("PASS_SCOPED_"), result["status"])
        self.assertEqual([c["obligation"] for c in result["checks"]],
                         ["euler_lagrange", "translation_noether"])
        self.assertTrue(all(c["passed"] for c in result["checks"]))
        self.assertFalse(result["physical_truth_proven"])
        self.assertFalse(result["global_theorem_proven"])
        self.assertFalse(result["lean_kernel_verified"])

    def test_full_receipt_replay_and_tampering(self):
        receipt = execute_physics_input(self.spec)
        self.assertTrue(replay_physics_input(self.spec, receipt))
        altered = copy.deepcopy(receipt)
        altered["checks"][0]["passed"] = False
        self.assertFalse(replay_physics_input(self.spec, altered))

    def test_wrong_waterfall_eom_is_refused(self):
        incorrect = copy.deepcopy(self.spec)
        # The negative of the true z equation must not be accepted.
        incorrect["expected_eom"][2] = {"neg": incorrect["expected_eom"][2]}
        result = execute_physics_input(incorrect)
        self.assertFalse(result["checks"][0]["passed"])
        self.assertEqual(result["status"], "REJECTED_UNSATISFIED_PHYSICS_OBLIGATION")

    def test_rational_sum_of_squares(self):
        delta = F(16202803686105016, 10**18)
        a = (4 + delta) / 2
        yc = F(81, 100)
        v = 3 - a*a/2
        beta = v / ((a - yc)**2 + 2*v)
        kappa = F(10000)
        lam = kappa*kappa / (4*beta)
        c = F(1, 2) - beta
        yv = (a - 2*beta*yc) / (1 - 2*beta)
        self.assertTrue(0 < beta < F(1, 2))
        self.assertTrue(yv > a > yc)
        left = {
            (0, 0): F(3), (1, 0): -a, (2, 0): F(1, 2),
            (0, 1): kappa*yc/2, (1, 1): -kappa/2, (0, 2): lam/4
        }
        right = {
            (0, 0): beta*yc**2 + c*yv**2,
            (1, 0): -2*beta*yc - 2*c*yv, (2, 0): beta+c,
            (0, 1): kappa*yc/2, (1, 1): -kappa/2, (0, 2): lam/4
        }
        self.assertEqual(left, right)

    def test_no_radiation_claim_is_sneaked_into_typed_contract(self):
        self.assertEqual(self.spec["kind"], "lagrangian")
        self.assertEqual(self.spec["fields"], ["b", "x", "z"])
        self.assertEqual(self.spec["claims"],
                         ["euler_lagrange", "translation_noether"])
        self.assertNotIn("radiation_domination", self.spec["claims"])


if __name__ == "__main__":
    unittest.main()
