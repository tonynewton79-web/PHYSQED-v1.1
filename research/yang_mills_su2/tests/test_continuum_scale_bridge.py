"""Exact conditional block-window and deliberately abstract transfer tests."""

import copy
from fractions import Fraction
import json
from pathlib import Path
import unittest

from research.yang_mills_su2.continuum_scale_bridge import (
    diagonal_transfer_family,
    physical_block_window,
    replay_scale_bridge_receipt,
    residual_stable_block_upper,
    scale_bridge_receipt,
)


class ContinuumScaleBridgeTests(unittest.TestCase):
    def test_committed_abstract_example_replays_exactly(self):
        path = (Path(__file__).resolve().parents[1] / "artifacts" /
                "abstract_physical_scale_bridge_n2.json")
        obj = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(replay_scale_bridge_receipt(obj))
        self.assertEqual(obj, scale_bridge_receipt("finite_mass", 2, 2))

    def test_physical_block_window_distinguishes_two_spectral_directions(self):
        window = physical_block_window(
            Fraction(1, 4), 4, Fraction(1, 2),
            Fraction(1, 4), Fraction(1), 1)
        self.assertEqual(window["physical_scale"], Fraction(1))
        self.assertEqual(window["block_lower"], Fraction(1, 4))
        self.assertEqual(window["block_upper"], Fraction(1, 2))
        self.assertEqual(window["mass_lower"], Fraction(2, 3))
        self.assertEqual(window["mass_upper"], Fraction(57, 40))
        self.assertLess(window["mass_lower"], window["mass_upper"])

    def test_diagonal_families_are_exact_and_physically_distinct(self):
        for n in (2, 4, 8, 16):
            with self.subTest(n=n):
                finite = diagonal_transfer_family("finite_mass", n, 4)
                collapse = diagonal_transfer_family("gap_collapse", n, 4)
                ultra = diagonal_transfer_family("ultralocal", n, 4)
                self.assertEqual(finite["single_step_ratio"], Fraction(n-1, n))
                self.assertEqual(collapse["single_step_ratio"],
                                 Fraction(n*n-1, n*n))
                self.assertEqual(ultra["single_step_ratio"], Fraction(1, 2))
                self.assertEqual(finite["block_ratio"], Fraction(n-1, n)**n)
                self.assertEqual(finite["window"]["physical_scale"], 1)
                self.assertEqual(finite["window"]["block_lower"],
                                 finite["window"]["block_upper"])
                self.assertGreaterEqual(finite["block_ratio"], Fraction(1, 4))
                self.assertLess(finite["block_ratio"], Fraction(1, 2))
        self.assertGreater(diagonal_transfer_family("gap_collapse", 32, 2)[
            "block_ratio"], Fraction(9, 10))
        self.assertLess(diagonal_transfer_family("ultralocal", 32, 2)[
            "block_ratio"], Fraction(1, 1000000))

    def test_conditional_window_rejects_bad_spectral_witnesses_and_inputs(self):
        base = (Fraction(1, 4), 4, Fraction(1, 2),
                Fraction(1, 4), Fraction(1), 4)
        failures = [
            (0.25,) + base[1:],
            (True,) + base[1:],
            (Fraction(0),) + base[1:],
            (base[0], False) + base[2:],
            (base[0], 4097) + base[2:],
            base[:2] + (Fraction(1),) + base[3:],
            base[:2] + (Fraction(-1, 2),) + base[3:],
            base[:3] + (Fraction(0),) + base[4:],
            base[:3] + (Fraction(2), Fraction(1), 4),
            base[:4] + (Fraction(0), 4),
            base[:-1] + (0,),
            base[:-1] + (33,),
            (Fraction(1, 2**500),) + base[1:],
        ]
        for args in failures:
            with self.subTest(args=args), self.assertRaises(ValueError):
                physical_block_window(*args)

    def test_receipts_replay_but_refuse_continuum_or_wilson_promotion(self):
        obj = scale_bridge_receipt("finite_mass", 8, 6)
        self.assertTrue(replay_scale_bridge_receipt(obj))
        self.assertEqual(obj["status"], "EXACT_ABSTRACT_DIAGONAL_TRANSFER_ARITHMETIC")
        self.assertFalse(obj["physical_law_proven"])
        self.assertFalse(obj["continuum_mass_gap_proven"])
        self.assertFalse(obj["analytic_theorem_kernel_verified"])
        self.assertEqual(obj["input"]["n"], 8)
        for key, forged_value in (
            ("physical_law_proven", True),
            ("continuum_mass_gap_proven", True),
            ("analytic_theorem_kernel_verified", True),
            ("status", "WILSON_4D_CONTINUUM_GAP_PROVED"),
            ("fingerprint", "0"*64),
        ):
            with self.subTest(key=key):
                fake = copy.deepcopy(obj)
                fake[key] = forged_value
                self.assertFalse(replay_scale_bridge_receipt(fake))
        fake = copy.deepcopy(obj)
        fake["derived"]["physical_gap_lower"]["numerator"] = "100"
        self.assertFalse(replay_scale_bridge_receipt(fake))

    def test_family_budget_and_unknown_family_reject(self):
        for args in (("massless", 8, 4), ("finite_mass", 1, 4),
                     ("finite_mass", True, 4), ("finite_mass", 257, 4),
                     ("finite_mass", 8, 100)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                scale_bridge_receipt(*args)

    def test_operator_error_accumulates_across_physical_block(self):
        # The telescope bound is ||Q^k-Q_D^k|| <= k||Q-Q_D||
        # when both excited-sector operators are contractions.
        self.assertEqual(residual_stable_block_upper(
            Fraction(1, 3), Fraction(1, 96), 8), Fraction(5, 12))
        self.assertEqual(residual_stable_block_upper(
            Fraction(1, 3), Fraction(0), 8), Fraction(1, 3))
        for args in ((Fraction(1, 3), Fraction(1, 12), 8),
                     (Fraction(1), Fraction(0), 8),
                     (Fraction(1, 3), Fraction(-1, 16), 8),
                     (Fraction(1, 3), 0.1, 8),
                     (Fraction(1, 3), Fraction(0), True)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                residual_stable_block_upper(*args)


if __name__ == "__main__":
    unittest.main()
