"""Exact SU2 chordal strong-coupling consequences and strict replay."""

import copy
import unittest
from fractions import Fraction

import mpmath as mp
import sympy as sp

from research.yang_mills_su2.wilson_chordal_mixing import (
    chordal_spectral_ratio_upper,
    chordal_gap_log_lower,
    chordal_mixing_receipt,
    replay_chordal_mixing_receipt,
)
from research.yang_mills_su2.wilson_spectral_gap import lattice_spectral_ratio_upper


class WilsonChordalMixingTests(unittest.TestCase):
    def test_barta_operator_identities_independently_symbolic(self):
        """Differentiate both analytic supersolutions, not just coefficients.

        SymPy is a test dependency; the PHYSQED arithmetic receipt does not
        claim these functional identities have a kernel proof.
        """
        theta, kappa = sp.symbols("theta kappa", real=True)
        drift = 2 * sp.cot(theta) - kappa * sp.sin(theta)

        def normalized_neg_generator(a, extra_potential):
            trial = sp.sin(theta) * sp.exp(a*kappa*sp.cos(theta))
            operator = (sp.diff(trial, theta, 2)
                        + drift*sp.diff(trial, theta)
                        - extra_potential*trial)
            return sp.trigsimp(sp.simplify(-operator/trial))

        degree_one = normalized_neg_generator(
            -sp.Rational(1, 5), 2/sp.sin(theta)**2)
        zonal_derivative = normalized_neg_generator(
            -sp.Rational(2, 5), -sp.diff(drift, theta))
        self.assertEqual(sp.simplify(
            degree_one - 3 - sp.Rational(4, 25)*kappa**2*sp.sin(theta)**2), 0)
        self.assertEqual(sp.simplify(
            zonal_derivative - 3 - sp.Rational(6, 25)*kappa**2*sp.sin(theta)**2), 0)

    def test_beta_one_tenth_beyond_old_window_has_exact_ratio_three_fifths(self):
        self.assertEqual(chordal_spectral_ratio_upper(Fraction(1, 10)),
                         Fraction(3, 5))

    def test_overlap_with_old_beta_window_is_threefold_improvement(self):
        beta = Fraction(1, 100)
        self.assertEqual(chordal_spectral_ratio_upper(beta), Fraction(3, 50))
        self.assertEqual(3 * chordal_spectral_ratio_upper(beta),
                         lattice_spectral_ratio_upper(beta))

    def test_atanh_log_lower_is_exact_in_new_coupling_window(self):
        beta = Fraction(1, 10)
        self.assertEqual(chordal_gap_log_lower(beta, 1), Fraction(1, 2))
        self.assertEqual(chordal_gap_log_lower(beta, 2), Fraction(49, 96))
        later = chordal_gap_log_lower(beta, 8)
        self.assertGreater(later, Fraction(49, 96))
        with mp.workdps(75):
            self.assertLess(mp.mpf(later.numerator)/later.denominator,
                            -mp.log(mp.mpf(3)/5))

    def test_receipt_replays_barta_quadratic_coefficients_and_rejects_forgery(self):
        receipt = chordal_mixing_receipt(1, 10, 8)
        self.assertTrue(replay_chordal_mixing_receipt(receipt))
        self.assertEqual(receipt["barta_degree_one_quadratic"],
                         {"numerator": "4", "denominator": "25"})
        self.assertEqual(receipt["barta_zonal_derivative_quadratic"],
                         {"numerator": "6", "denominator": "25"})
        self.assertEqual(receipt["chordal_wasserstein_parameter_upper"],
                         {"numerator": "1", "denominator": "3"})
        self.assertFalse(receipt["analytic_theorem_kernel_verified"])
        self.assertFalse(receipt["continuum_mass_gap_proven"])
        for field, altered in (("chordal_wasserstein_parameter_upper",
                                {"numerator": "1", "denominator": "4"}),
                               ("barta_zonal_derivative_quadratic",
                                {"numerator": "7", "denominator": "25"}),
                               ("continuum_mass_gap_proven", True),
                               ("analytic_theorem_kernel_verified", 0)):
            with self.subTest(field=field):
                tampered = copy.deepcopy(receipt)
                tampered[field] = altered
                self.assertFalse(replay_chordal_mixing_receipt(tampered))

    def test_strict_rejection_at_and_beyond_new_endpoint(self):
        for args in ((0, 1, 8), (1, 6, 8), (1, 5, 8),
                     (True, 10, 8), (1, True, 8), (1, 10, True),
                     (1, 10, 0), (1, 10, 33), (1, 2**20, 8)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                chordal_mixing_receipt(*args)
        with self.assertRaises(ValueError):
            chordal_spectral_ratio_upper(0.1)


if __name__ == "__main__":
    unittest.main()
