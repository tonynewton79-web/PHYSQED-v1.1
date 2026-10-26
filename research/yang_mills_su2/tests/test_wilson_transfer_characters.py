"""Exact bounded character tails for the true Wilson temporal-link kernel."""

import copy
import json
import unittest
from fractions import Fraction

import sympy as S


class WilsonTransferCharacterTests(unittest.TestCase):
    def test_uniform_tail_at_beta_two_is_small_and_decreases(self):
        from research.yang_mills_su2.wilson_transfer_characters import character_tail_upper

        tail6 = character_tail_upper(Fraction(2), 6, 12)
        tail8 = character_tail_upper(Fraction(2), 8, 12)
        self.assertGreater(tail6, tail8)
        self.assertGreater(tail8, 0)
        self.assertLess(tail8, Fraction(1, 1000))

    def test_character_kernel_enclosures_contain_independent_exponentials(self):
        from research.yang_mills_su2.wilson_transfer_characters import (
            wilson_character_kernel_interval,
        )

        for x in (Fraction(-1), Fraction(0), Fraction(1, 2), Fraction(1)):
            with self.subTest(x=x):
                lo, hi = wilson_character_kernel_interval(Fraction(2), 8, 12, 12, x)
                oracle = S.N(S.exp(2*S.Rational(x.numerator, x.denominator)), 100)
                self.assertLess(S.Rational(lo.numerator, lo.denominator), oracle)
                self.assertGreater(S.Rational(hi.numerator, hi.denominator), oracle)
                self.assertLess(hi-lo, Fraction(1, 100))
        lo, hi = wilson_character_kernel_interval(Fraction(2), 8, 12, 12, Fraction(0))
        self.assertLess(lo, Fraction(1))
        self.assertGreater(hi, Fraction(1))

    def test_receipt_replays_exact_fundamental_convolution_ratio(self):
        from research.yang_mills_su2.wilson_transfer_characters import (
            wilson_transfer_receipt, replay_wilson_transfer_receipt,
        )

        receipt = wilson_transfer_receipt(2, 1, 8, 12, 12)
        self.assertEqual(receipt["status"], "FINITE_WILSON_TRANSFER_CHARACTER_EXACT")
        self.assertTrue(replay_wilson_transfer_receipt(json.loads(json.dumps(receipt))))
        self.assertIs(receipt["physical_law_proven"], False)
        self.assertIs(receipt["continuum_mass_gap_proven"], False)
        ratio = receipt["fundamental_to_trivial_ratio"]
        low = Fraction(int(ratio["lower"]["numerator"]), int(ratio["lower"]["denominator"]))
        high = Fraction(int(ratio["upper"]["numerator"]), int(ratio["upper"]["denominator"]))
        oracle = S.N(S.besseli(2,2)/S.besseli(1,2), 100)
        self.assertLess(S.Rational(low.numerator, low.denominator), oracle)
        self.assertGreater(S.Rational(high.numerator, high.denominator), oracle)
        forged = copy.deepcopy(receipt)
        forged["kernel_samples"][0]["upper"]["numerator"] = "1"
        self.assertFalse(replay_wilson_transfer_receipt(forged))
        forged = copy.deepcopy(receipt)
        forged["physical_law_proven"] = True
        self.assertFalse(replay_wilson_transfer_receipt(forged))
        forged = copy.deepcopy(receipt)
        forged["input"]["D"] = True
        self.assertFalse(replay_wilson_transfer_receipt(forged))

    def test_bounds_reject_resource_bombs_and_improper_parameters(self):
        from research.yang_mills_su2.wilson_transfer_characters import (
            character_tail_upper, wilson_character_kernel_interval,
            wilson_transfer_receipt,
        )

        for beta, D, terms in ((Fraction(0),8,12), (Fraction(-1),8,12),
                               (Fraction(5),8,12), (Fraction(2),True,12),
                               (Fraction(2),17,12), (Fraction(4),2,2),
                               (Fraction(2),8,33),
                               (Fraction(1,2**200),8,12)):
            with self.subTest(beta=beta,D=D,terms=terms), self.assertRaises(ValueError):
                character_tail_upper(beta,D,terms)
        for x in (Fraction(2), float("nan"), Fraction(1,2**200)):
            with self.subTest(x=x), self.assertRaises(ValueError):
                wilson_character_kernel_interval(Fraction(2),8,12,12,x)
        for inputs in ((True,1,8,12,12),(2,False,8,12,12),
                       (2,1,8,True,12),(2,1,8,12,0)):
            with self.subTest(inputs=inputs), self.assertRaises(ValueError):
                wilson_transfer_receipt(*inputs)


if __name__ == "__main__":
    unittest.main()
