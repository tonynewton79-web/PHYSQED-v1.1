"""Independent rational expectations for the beta-zero SU(2) proposal law."""

from fractions import Fraction
import unittest

from research.yang_mills_su2.mixing_certificates import (
    beta_zero_rep_eigenvalue, cold_l2_squared_bounds, mixing_receipt,
    replay_mixing_receipt,
)


class ExactBetaZeroMixingTests(unittest.TestCase):
    def test_integer_and_half_integer_spin_eigenvalues(self):
        expected = [
            Fraction(1), Fraction(0), Fraction(1, 3),
            Fraction(0), Fraction(1, 5), Fraction(0),
        ]
        self.assertEqual([beta_zero_rep_eigenvalue(k) for k in range(6)], expected)

    def test_two_sweep_l2_bound_contains_first_nontrivial_term(self):
        low, high = cold_l2_squared_bounds(2, 1, 1)
        self.assertEqual(low, Fraction(1, 9))
        self.assertEqual(high, Fraction(5, 18))

    def test_rational_enclosure_tightens_with_terms(self):
        lo2, hi2 = cold_l2_squared_bounds(3, 4, 2)
        lo4, hi4 = cold_l2_squared_bounds(3, 4, 4)
        self.assertLess(lo2, lo4)
        self.assertLess(hi4, hi2)
        self.assertLess(lo4, hi4)

    def test_exact_beta_zero_adjoint_plaquette_and_proof_scope(self):
        receipt = mixing_receipt(2, 64, 4)
        self.assertEqual(receipt["cold_adjoint_plaquette_at_first_sweep"],
                         {"numerator": "1", "denominator": "81"})
        self.assertEqual(receipt["cold_fundamental_plaquette_at_first_sweep"],
                         {"numerator": "0", "denominator": "1"})
        self.assertFalse(receipt["continuum_mass_gap_proven"])
        self.assertFalse(receipt["physical_law_proven"])
        self.assertFalse(receipt["lean_kernel_verified"])
        self.assertEqual(receipt["certificate_scope"], "EXACT_FINITE_BETA_ZERO_PROPOSAL")

    def test_receipt_replay_recomputes_and_refuses_tampering(self):
        receipt = mixing_receipt(3, 64, 4)
        self.assertTrue(replay_mixing_receipt(receipt))
        altered = {**receipt, "l2_distance_squared_interval": {
            **receipt["l2_distance_squared_interval"],
            "lower": {"numerator": "0", "denominator": "1"},
        }}
        self.assertFalse(replay_mixing_receipt(altered))
        self.assertFalse(replay_mixing_receipt({
            **receipt, "continuum_mass_gap_proven": True}))
        self.assertFalse(replay_mixing_receipt({
            **receipt, "parameters": {**receipt["parameters"], "proposal_angle": "0"}}))
        self.assertFalse(replay_mixing_receipt({"parameters": {}}))
        self.assertFalse(replay_mixing_receipt("fake"))

    def test_large_rational_receipt_fails_with_explicit_serialization_budget(self):
        # Analytic Fraction bounds remain legal, but these inputs previously
        # produced >4300 decimal digits in the public JSON serializer.
        with self.assertRaisesRegex(ValueError, "serialization"):
            mixing_receipt(12, 166, 2)

    def test_rejects_invalid_or_unbounded_input_before_large_products(self):
        for spin in (-1, 1.5, True):
            with self.subTest(spin=spin), self.assertRaises(ValueError):
                beta_zero_rep_eigenvalue(spin)
        for args in [(1, 64, 4), (2, 0, 3), (2, 64, 0),
                     (2, 513, 1), (4, 512, 32), (True, 64, 4)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                cold_l2_squared_bounds(*args)


if __name__ == "__main__":
    unittest.main()
