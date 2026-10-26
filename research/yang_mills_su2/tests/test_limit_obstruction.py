"""Exact separation of finite positive gaps from a continuum lower bound."""
from fractions import Fraction
import unittest

from research.yang_mills_su2.limit_obstruction import collapsing_gap


class LimitObstructionTests(unittest.TestCase):
    def test_every_finite_gap_positive_but_physical_gap_collapses(self):
        for n in (1, 2, 5, 100):
            record = collapsing_gap(n)
            self.assertEqual(record["lattice_spacing"], Fraction(1, n))
            self.assertEqual(record["dimensionless_gap"], Fraction(1, n*n))
            self.assertEqual(record["physical_gap"], Fraction(1, n))
            self.assertGreater(record["dimensionless_gap"], 0)
            self.assertEqual(record["status"], "COUNTEREXAMPLE_TO_FINITE_GAP_INFERENCE")
        self.assertLess(collapsing_gap(100)["physical_gap"], collapsing_gap(5)["physical_gap"])

    def test_nonpositive_or_noninteger_index_rejected(self):
        for n in (0, -1, 1.0, True):
            with self.subTest(n=n), self.assertRaises(ValueError):
                collapsing_gap(n)


if __name__ == "__main__":
    unittest.main()
