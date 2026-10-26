"""Adversarial and hand-derived SU(2) strong-coupling influence tests."""

import copy
import unittest
from fractions import Fraction

from research.yang_mills_su2.wilson_dobrushin import (
    max_wilson_link_incidences,
    strong_coupling_receipt,
    strong_coupling_timeslice_bound,
    replay_strong_coupling_receipt,
)


class WilsonDobrushinTests(unittest.TestCase):
    def test_every_link_has_eighteen_other_edge_plaquette_incidences(self):
        self.assertEqual(max_wilson_link_incidences((2, 2, 2, 2)), 18)
        self.assertEqual(max_wilson_link_incidences((4, 3, 2, 2)), 18)

    def test_time_four_beta_one_hundred_exact(self):
        self.assertEqual(
            strong_coupling_timeslice_bound((8, 2, 2, 2), Fraction(1, 100), 4),
            Fraction(13122, 640625),
        )

    def test_bound_is_spatial_volume_independent(self):
        beta = Fraction(1, 100)
        reference = strong_coupling_timeslice_bound((8, 2, 2, 2), beta, 3)
        self.assertEqual(reference, strong_coupling_timeslice_bound(
            (8, 3, 3, 2), beta, 3))
        self.assertEqual(reference, strong_coupling_timeslice_bound(
            (8, 2, 2, 2), beta, 5))

    def test_outside_uniqueness_window_is_rejected(self):
        for beta in (Fraction(1, 18), Fraction(1, 10), Fraction(-1, 200),
                     0.01, True, Fraction(1, 2**20)):
            with self.subTest(beta=beta), self.assertRaises(ValueError):
                strong_coupling_timeslice_bound((8, 2, 2, 2), beta, 4)

    def test_geometry_and_time_guard(self):
        for geometry, lag in (((1, 2, 2, 2), 1), ((8, 2, 2, 2), 0),
                              ((8, 2, 2, 2), 8), ((100, 3, 3, 3), 4)):
            with self.subTest(geometry=geometry, lag=lag), self.assertRaises(ValueError):
                strong_coupling_timeslice_bound(geometry, Fraction(1, 100), lag)

    def test_exact_receipt_replays_and_refuses_tampering(self):
        original = strong_coupling_receipt((8, 2, 2, 2), 1, 100, 4)
        self.assertTrue(replay_strong_coupling_receipt(original))
        self.assertFalse(original["physical_law_proven"])
        self.assertFalse(original["continuum_mass_gap_proven"])
        altered = copy.deepcopy(original)
        altered["covariance_upper"]["numerator"] = "1"
        self.assertFalse(replay_strong_coupling_receipt(altered))
        for key in ("physical_law_proven", "continuum_mass_gap_proven"):
            forged = copy.deepcopy(original)
            forged[key] = True
            self.assertFalse(replay_strong_coupling_receipt(forged))


if __name__ == "__main__":
    unittest.main()
