"""Hand-derived exact checks for an abstract positive-transfer obstruction."""

import copy
import json
import unittest
from fractions import Fraction
from pathlib import Path


class TransferMomentObstructionTests(unittest.TestCase):
    def test_two_mode_moments_match_hand_derived_values(self):
        from research.yang_mills_su2.transfer_moment_obstructions import two_mode_moment

        self.assertEqual(two_mode_moment(10, 0), Fraction(1))
        self.assertEqual(two_mode_moment(10, 1), Fraction(27, 50))
        self.assertEqual(two_mode_moment(10, 2), Fraction(153, 500))
        self.assertEqual(two_mode_moment(100, 1), Fraction(5049, 10000))

    def test_log_convex_hankel_minor_has_correct_exponent_and_sign(self):
        from research.yang_mills_su2.transfer_moment_obstructions import (
            two_mode_hankel_minor, two_mode_moment,
        )

        self.assertEqual(two_mode_hankel_minor(10, 0), Fraction(9, 625))
        self.assertEqual(two_mode_hankel_minor(10, 1), Fraction(81, 12500))
        self.assertGreater(two_mode_hankel_minor(3, 20), 0)
        for n in (3, 10, 100):
            for t in range(11):
                self.assertEqual(two_mode_hankel_minor(n, t),
                                 two_mode_moment(n, t)*two_mode_moment(n, t+2)
                                 -two_mode_moment(n, t+1)**2)

    def test_uniform_absolute_error_bound_and_slow_eigenvalues(self):
        from research.yang_mills_su2.transfer_moment_obstructions import two_mode_moment

        for n in (3, 10, 100, 4096):
            for t in range(35):
                difference = two_mode_moment(n, t) - Fraction(1, 2)**t
                self.assertGreaterEqual(difference, 0)
                self.assertLessEqual(difference, Fraction(1, n))

    def test_periodic_trace_fixture_is_reflection_symmetric_and_log_convex(self):
        from research.yang_mills_su2.transfer_moment_obstructions import (
            finite_period_two_state_correlator,
        )

        values = finite_period_two_state_correlator(4, Fraction(1, 2))
        self.assertEqual(values, (Fraction(1), Fraction(10, 17),
                                  Fraction(8, 17), Fraction(10, 17)))
        self.assertEqual(values[1], values[3])
        self.assertEqual(values[0]*values[2] - values[1]**2, Fraction(36, 289))
        self.assertEqual((values[0]+values[2])/(2*values[1]), Fraction(5, 4))

    def test_receipt_exact_replay_and_tamper_rejection(self):
        from research.yang_mills_su2.transfer_moment_obstructions import (
            transfer_moment_receipt, replay_transfer_moment_receipt,
        )

        receipt = transfer_moment_receipt(10, 4)
        self.assertTrue(replay_transfer_moment_receipt(receipt))
        self.assertTrue(replay_transfer_moment_receipt(json.loads(json.dumps(receipt))))
        self.assertIs(receipt["physical_law_proven"], False)
        self.assertIs(receipt["continuum_mass_gap_proven"], False)
        for path, value in (
            (("moments", 1, "numerator"), "999"),
            (("hankel_minors", 0, "denominator"), "1"),
            (("parameters", "n"), True),
            (("parameters", "horizon"), False),
            (("physical_law_proven",), True),
            (("certificate_scope",), "WILSON_SU2_MASS_GAP"),
        ):
            altered = copy.deepcopy(receipt)
            node = altered
            for key in path[:-1]:
                node = node[key]
            node[path[-1]] = value
            self.assertFalse(replay_transfer_moment_receipt(altered), path)
        altered = copy.deepcopy(receipt)
        altered["invented_gap_proof"] = True
        self.assertFalse(replay_transfer_moment_receipt(altered))

    def test_checked_in_abstract_fixture_replays_without_hidden_solver(self):
        from research.yang_mills_su2.transfer_moment_obstructions import (
            replay_transfer_moment_receipt,
        )
        from research.yang_mills_su2.evidence_bridge import record_evidence

        source = (Path(__file__).resolve().parents[1] / "artifacts" /
                  "abstract_transfer_moments_n10.json")
        receipt = json.loads(source.read_text(encoding="utf-8"))
        self.assertEqual(receipt["parameters"], {"n": 10, "horizon": 4})
        self.assertTrue(replay_transfer_moment_receipt(receipt))
        self.assertEqual(record_evidence("EXACT_TRANSFER_MOMENT_OBSTRUCTION", source, {})[
            "status"], "ABSTRACT_SPECTRAL_MASKING_EXACT")

    def test_bad_types_and_excessive_parameters_rejected_before_computation(self):
        from research.yang_mills_su2.transfer_moment_obstructions import (
            two_mode_moment, two_mode_hankel_minor,
            transfer_moment_receipt, finite_period_two_state_correlator,
        )

        for n, t in ((True, 1), (3, False), (2, 1), (4097, 0), (10, -1),
                     (10, 65), ("10", 1)):
            with self.subTest(n=n, t=t), self.assertRaises(ValueError):
                two_mode_moment(n, t)
            with self.subTest(n=n, t=t), self.assertRaises(ValueError):
                two_mode_hankel_minor(n, t)
        for n, horizon in ((True, 1), (10, False), (2, 1), (4097, 1),
                           (10, -1), (10, 33), (10, 1.0)):
            with self.subTest(n=n, horizon=horizon), self.assertRaises(ValueError):
                transfer_moment_receipt(n, horizon)
        for period, q in ((1, Fraction(1, 2)), (33, Fraction(1, 2)),
                          (4, Fraction(0)), (4, Fraction(1)),
                          (True, Fraction(1, 2)), (4, 0.5),
                          (4, Fraction(2**300, 2**300 + 1))):
            with self.subTest(period=period, q=q), self.assertRaises(ValueError):
                finite_period_two_state_correlator(period, q)


if __name__ == "__main__":
    unittest.main()
