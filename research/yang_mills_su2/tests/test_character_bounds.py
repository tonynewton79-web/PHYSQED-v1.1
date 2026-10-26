"""Independent checks of exact Bessel-series interval enclosures."""
import unittest
from fractions import Fraction
import json
import tempfile
from pathlib import Path

import sympy as S

from research.yang_mills_su2.character_bounds import (
    bessel_i_bounds,
    character_ratio_bounds,
    character_gap_bounds,
    negative_log_bounds,
)
from research.yang_mills_su2.character_cli import (
    certify_character,
    main,
    replay_character_certificate,
)


class CharacterBoundsTests(unittest.TestCase):
    def test_replayable_exact_character_receipt_and_rejection(self):
        receipt = certify_character(2, 1, 12, 12)
        self.assertEqual(receipt, certify_character(2, 1, 12, 12))
        self.assertEqual(receipt["status"], "FINITE_CHARACTER_EXACT_INTERVAL")
        self.assertFalse(receipt["physical_law_proven"])
        self.assertFalse(receipt["continuum_mass_gap_proven"])
        self.assertFalse(receipt["lean_kernel_verified"])
        self.assertTrue(replay_character_certificate(receipt))
        altered = json.loads(json.dumps(receipt))
        altered["bounds"]["character_gap"]["lower"]["numerator"] += 1
        self.assertFalse(replay_character_certificate(altered))
        altered2 = json.loads(json.dumps(receipt))
        altered2["physical_law_proven"] = True
        self.assertFalse(replay_character_certificate(altered2))

    def test_receipt_cli_writes_and_verifies_or_refuses(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)/"receipt.json"
            args = ["--beta-num", "2", "--beta-den", "1", "--bessel-terms", "12",
                    "--log-terms", "12", "--output", str(out)]
            self.assertEqual(main(args), 0)
            first = out.read_bytes()
            self.assertEqual(main(args), 0)
            self.assertEqual(out.read_bytes(), first)
            self.assertEqual(main(["--verify", str(out)]), 0)
            wrong = json.loads(out.read_text())
            wrong["fingerprint"] = "0"*64
            out.write_text(json.dumps(wrong))
            self.assertEqual(main(["--verify", str(out)]), 2)

    def test_hostile_receipt_fails_closed_without_schema_trust(self):
        receipt = certify_character(2, 1, 12, 12)
        for extra in (float("nan"), {1, 2}):
            with self.subTest(extra=repr(extra)):
                self.assertFalse(replay_character_certificate({**receipt, "extra": extra}))
        self.assertFalse(replay_character_certificate({
            "input": {"beta": {"numerator": 2, "denominator": 1},
                      "bessel_terms": 40, "log_terms": 40},
        }))
        self.assertFalse(replay_character_certificate({**receipt, "fingerprint": True}))
        nested = 0
        for _ in range(10000):
            nested = [nested]
        self.assertFalse(replay_character_certificate({**receipt, "bounds": nested}))

    def test_deep_json_verification_refuses_without_exception(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/"deep.json"
            path.write_text("["*10000 + "0" + "]"*10000, encoding="utf-8")
            self.assertEqual(main(["--verify", str(path)]), 2)

    def test_receipt_resource_budget_is_explicit_and_early(self):
        with self.assertRaisesRegex(ValueError, "budget|unsupported"):
            certify_character(2, 1, 40, 40)

    def test_log_enclosures_near_endpoints_and_three_quarters(self):
        for q in (Fraction(1, 1000), Fraction(999, 1000), Fraction(3, 4)):
            lower, upper = negative_log_bounds(q, 16)
            # The interval for q near one can be narrower than 80 decimal
            # digits; oracle precision must exceed the enclosure precision.
            true_value = S.N(-S.log(S.Rational(q.numerator, q.denominator)), 200)
            self.assertLessEqual(S.Rational(lower.numerator, lower.denominator), true_value)
            self.assertGreaterEqual(S.Rational(upper.numerator, upper.denominator), true_value)

    def test_positive_rational_bessel_bounds_contain_independent_values(self):
        beta = Fraction(2)
        for order in (1, 2):
            low, high = bessel_i_bounds(order, beta, 12)
            oracle = S.N(S.besseli(order, 2), 60)
            self.assertLess(S.Rational(low.numerator, low.denominator), oracle)
            self.assertGreater(S.Rational(high.numerator, high.denominator), oracle)
            self.assertLess(high-low, bessel_i_bounds(order, beta, 7)[1] -
                            bessel_i_bounds(order, beta, 7)[0])

    def test_character_ratio_is_strictly_between_zero_and_one_at_test_points(self):
        for beta in (Fraction(2), Fraction(4), Fraction(8)):
            low, high = character_ratio_bounds(beta, 18)
            oracle = S.N(S.besseli(2, S.Rational(beta.numerator, beta.denominator)) /
                         S.besseli(1, S.Rational(beta.numerator, beta.denominator)), 60)
            self.assertLess(Fraction(0), low)
            self.assertLess(S.Rational(low.numerator, low.denominator), oracle)
            self.assertGreater(S.Rational(high.numerator, high.denominator), oracle)
            self.assertLess(high, Fraction(1))

    def test_log_series_bounds_and_character_gap(self):
        q = Fraction(1, 2)
        low, high = negative_log_bounds(q, 12)
        oracle = S.N(-S.log(S.Rational(1, 2)), 60)
        self.assertLess(S.Rational(low.numerator, low.denominator), oracle)
        self.assertGreater(S.Rational(high.numerator, high.denominator), oracle)
        self.assertLess(high-low, negative_log_bounds(q, 5)[1]-negative_log_bounds(q, 5)[0])
        lower_gap, upper_gap = character_gap_bounds(Fraction(2), 18, 18)
        c = S.besseli(2, 2)/S.besseli(1, 2)
        true_gap = S.N(-S.log(c), 60)
        self.assertLess(S.Rational(lower_gap.numerator, lower_gap.denominator), true_gap)
        self.assertGreater(S.Rational(upper_gap.numerator, upper_gap.denominator), true_gap)
        self.assertGreater(lower_gap, 0)

    def test_invalid_or_nonconvergent_bounds_fail_closed(self):
        for order, beta, terms in [
            (1, Fraction(0), 5), (2, Fraction(-1), 5), (1, 2.0, 5),
            (-1, Fraction(2), 5), (1, Fraction(2), 0),
            (1, Fraction(100), 2),
        ]:
            with self.subTest(order=order, beta=beta, terms=terms), self.assertRaises(ValueError):
                bessel_i_bounds(order, beta, terms)
        for q in (Fraction(0), Fraction(-1, 2), Fraction(3, 2)):
            with self.subTest(q=q), self.assertRaises(ValueError):
                negative_log_bounds(q, 5)
        self.assertEqual(negative_log_bounds(Fraction(1), 5), (Fraction(0), Fraction(0)))


if __name__ == "__main__":
    unittest.main()
