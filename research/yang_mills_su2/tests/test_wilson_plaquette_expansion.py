"""Finite Wilson plaquette subset and character-product error checks."""

import unittest
from fractions import Fraction

from research.yang_mills_su2.wilson_plaquette_expansion import (
    wilson_subset_tail,
    wilson_plaquette_character_product_tail,
)


class WilsonPlaquetteExpansionTests(unittest.TestCase):
    def test_one_missing_plaquette_subset_order_has_exact_rational_tail(self):
        # 2x2x2x2 has exactly 6*16=96 plaquettes. The one-term enclosure
        # e^(1/100) <= 1 + 2/199 yields the sole missing k=96 term.
        self.assertEqual(
            wilson_subset_tail((2, 2, 2, 2), Fraction(1, 100), 95, 1),
            Fraction(2, 199)**96,
        )

    def test_retaining_every_subset_has_no_omitted_terms(self):
        self.assertEqual(wilson_subset_tail(
            (2, 2, 2, 2), Fraction(1, 100), 96, 1), Fraction(0))
        self.assertEqual(wilson_subset_tail(
            (2, 2, 2, 2), Fraction(0), 0, 1), Fraction(0))

    def test_full_character_product_bound_shrinks_with_dimension(self):
        beta = Fraction(1, 100)
        coarse = wilson_plaquette_character_product_tail(
            (2, 2, 2, 2), beta, 4, 8)
        refined = wilson_plaquette_character_product_tail(
            (2, 2, 2, 2), beta, 8, 8)
        self.assertGreater(coarse, refined)
        self.assertGreater(refined, 0)

    def test_reject_unsupported_tail_requests(self):
        for geometry, beta, K, terms in (
            ((2, 2, 2, 2), Fraction(1, 100), 97, 1),
            ((2, 2, 2, 2), Fraction(-1, 100), 95, 1),
            ((2, 2, 2, 2), 0.01, 95, 1),
            ((2, 2, 2, 2), Fraction(1, 100), 95, 0),
            ((8, 3, 3, 3), Fraction(1, 100), 95, 1),
        ):
            with self.subTest(geometry=geometry, beta=beta, K=K):
                with self.assertRaises(ValueError):
                    wilson_subset_tail(geometry, beta, K, terms)

    def test_character_product_rejects_zero_beta_and_oversized_D(self):
        for beta, D in ((Fraction(0), 4), (Fraction(1, 100), 100),
                        (Fraction(1, 3), 4)):
            with self.subTest(beta=beta, D=D), self.assertRaises(ValueError):
                wilson_plaquette_character_product_tail(
                    (2, 2, 2, 2), beta, D, 8)


if __name__ == "__main__":
    unittest.main()
