"""Finite-rank projected Wilson transfer error: mathematical regression."""

import unittest
from fractions import Fraction

import mpmath as mp

from research.yang_mills_su2.wilson_projected_cutoff import (
    normalized_link_spectral_tail,
    projected_transfer_operator_error,
    uncoupled_fourier_cutoff_dimension,
)


class WilsonProjectedCutoffTests(unittest.TestCase):
    def test_true_bessel_sector_is_below_outward_exact_tail(self):
        beta = Fraction(1, 100)
        bound = normalized_link_spectral_tail(beta, 4, 12, 12)
        with mp.workdps(80):
            true_ratio = mp.besseli(5, mp.mpf(1) / 100) / mp.besseli(1, mp.mpf(1) / 100)
            exact_bound = mp.mpf(bound.numerator) / bound.denominator
            self.assertGreater(exact_bound, true_ratio)
        self.assertLess(bound, 1)

    def test_dimension_cutoff_improves_normalized_operator_error(self):
        beta = Fraction(1, 100)
        low = normalized_link_spectral_tail(beta, 3, 12, 12)
        high = normalized_link_spectral_tail(beta, 8, 12, 12)
        self.assertGreater(low, high)
        self.assertGreater(high, 0)

    def test_interacting_projected_bound_tracks_spatial_volume(self):
        beta = Fraction(1, 100)
        eight_sites = projected_transfer_operator_error((2, 2, 2), beta, 5, 12, 12)
        twelve_sites = projected_transfer_operator_error((3, 2, 2), beta, 5, 12, 12)
        self.assertGreater(twelve_sites, eight_sites)
        self.assertGreater(eight_sites, 0)

    def test_spectral_cutoff_remains_defined_at_finite_beta_two(self):
        # This spectral approximation is valid outside Dobrushin's narrow
        # beta window, although the huge spatial multiplier can be vacuous.
        self.assertGreater(projected_transfer_operator_error(
            (2, 2, 2), Fraction(2), 8, 12, 12), 0)

    def test_finite_fourier_basis_is_a_rank_upper_bound_not_matrix_eigenvalues(self):
        self.assertEqual(uncoupled_fourier_cutoff_dimension((2, 2, 2), 2), 5**24)

    def test_reject_bad_coupling_dimension_budget_and_geometry(self):
        cases = ((Fraction(0), 4, 12, 12),
                 (Fraction(5), 4, 12, 12),
                 (Fraction(1, 100), 17, 12, 12),
                 (Fraction(1, 100), 4, 0, 12),
                 (Fraction(1, 100), 4, 12, 0))
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                normalized_link_spectral_tail(*args)
        with self.assertRaises(ValueError):
            projected_transfer_operator_error((1, 2, 2), Fraction(1, 100), 4, 12, 12)


if __name__ == "__main__":
    unittest.main()
