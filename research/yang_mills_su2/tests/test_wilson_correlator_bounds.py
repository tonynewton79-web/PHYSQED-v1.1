"""Exact but deliberately coarse finite-beta Wilson correlator bounds."""

import unittest
from fractions import Fraction


class WilsonCorrelatorBoundTests(unittest.TestCase):
    def test_beta_zero_and_positive_coupling_rational_bound(self):
        from research.yang_mills_su2.wilson_correlator_bounds import (
            finite_beta_spatial_correlator_bound,
        )

        extents = (4, 2, 2, 2)  # 32 sites and 6*32=192 plaquettes
        self.assertEqual(finite_beta_spatial_correlator_bound(
            extents, Fraction(0), 1), Fraction(0))
        self.assertEqual(finite_beta_spatial_correlator_bound(
            extents, Fraction(1,1000), 1), Fraction(3576,15625))
        self.assertEqual(finite_beta_spatial_correlator_bound(
            extents, Fraction(1,100), 2), Fraction(1))
        self.assertEqual(finite_beta_spatial_correlator_bound(
            extents, Fraction(2), 3), Fraction(1))

    def test_bound_grows_with_volume_and_is_not_uniform(self):
        from research.yang_mills_su2.wilson_correlator_bounds import (
            finite_beta_spatial_correlator_bound,
        )

        beta = Fraction(1, 10000)
        small = finite_beta_spatial_correlator_bound((4,2,2,2), beta, 1)
        large = finite_beta_spatial_correlator_bound((4,3,3,3), beta, 1)
        self.assertLess(small, large)
        self.assertGreater(small, 0)
        self.assertLess(large, 1)

    def test_ill_typed_parameters_or_equal_time_rejected(self):
        from research.yang_mills_su2.wilson_correlator_bounds import (
            finite_beta_spatial_correlator_bound,
        )

        for sizes, beta, lag in (
            ((4,2,2,2), Fraction(-1), 1),
            ((4,2,2,2), 0.5, 1),
            ((True,2,2,2), Fraction(1), 1),
            ((4,2,2), Fraction(1), 1),
            ((4,2,2,2), Fraction(1), 0),
            ((4,2,2,2), Fraction(1), True),
            ((4,2,2,2), Fraction(1), 4),
            ((64,32,32,32), Fraction(1), 1),
            ((4,2,2,2), Fraction(1,2**200), 1),
        ):
            with self.subTest(sizes=sizes,beta=beta,lag=lag), self.assertRaises(ValueError):
                finite_beta_spatial_correlator_bound(sizes,beta,lag)


if __name__ == "__main__":
    unittest.main()
