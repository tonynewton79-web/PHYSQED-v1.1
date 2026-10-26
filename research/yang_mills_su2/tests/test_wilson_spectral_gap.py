"""Exact arithmetic consequences of the restricted lattice transfer theorem."""

import copy
import unittest
from fractions import Fraction

import mpmath as mp

from research.yang_mills_su2.wilson_spectral_gap import (
    lattice_gap_log_lower,
    lattice_spectral_gap_receipt,
    lattice_spectral_ratio_upper,
    replay_lattice_spectral_gap_receipt,
)


class WilsonLatticeSpectralGapTests(unittest.TestCase):
    def test_beta_one_hundredth_has_exact_volume_free_ratio(self):
        self.assertEqual(lattice_spectral_ratio_upper(Fraction(1, 100)),
                         Fraction(9, 50))

    def test_logarithm_lower_series_is_rational_and_monotone(self):
        beta = Fraction(1, 100)
        self.assertEqual(lattice_gap_log_lower(beta, 1), Fraction(82, 59))
        lower = lattice_gap_log_lower(beta, 4)
        upper = lattice_gap_log_lower(beta, 12)
        self.assertLess(Fraction(82, 59), lower)
        self.assertLess(lower, upper)
        with mp.workdps(70):
            true = -mp.log(mp.mpf(9)/50)
            self.assertLess(mp.mpf(upper.numerator)/upper.denominator, true)

    def test_replay_rejects_mutated_bounds_and_false_continuum_scope(self):
        receipt = lattice_spectral_gap_receipt(1, 100, 8)
        self.assertTrue(replay_lattice_spectral_gap_receipt(receipt))
        self.assertEqual(receipt["spectral_ratio_upper"],
                         {"numerator": "9", "denominator": "50"})
        self.assertFalse(receipt["continuum_mass_gap_proven"])
        self.assertFalse(receipt["analytic_theorem_kernel_verified"])
        for field, value in (("continuum_mass_gap_proven", True),
                             ("continuum_mass_gap_proven", 0),
                             ("analytic_theorem_kernel_verified", True),
                             ("spectral_ratio_upper", {"numerator": "1", "denominator": "2"})):
            forged = copy.deepcopy(receipt)
            forged[field] = value
            with self.subTest(field=field):
                self.assertFalse(replay_lattice_spectral_gap_receipt(forged))

    def test_rejects_invalid_or_unbounded_inputs(self):
        for args in ((0, 1, 8), (1, 18, 8), (1, 10, 8),
                     (True, 100, 8), (1, True, 8), (1, 100, True),
                     (1, 100, 0), (1, 100, 33), (1, 2**20, 8)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                lattice_spectral_gap_receipt(*args)
        with self.assertRaises(ValueError):
            lattice_spectral_ratio_upper(0.01)
        with self.assertRaises(ValueError):
            lattice_gap_log_lower(Fraction(1, 100), 0)


if __name__ == "__main__":
    unittest.main()
