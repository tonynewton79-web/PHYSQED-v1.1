"""Heatbath conditional law is checked against independent Wilson-action oracles."""

import math
import random
import statistics
import unittest
from fractions import Fraction
from unittest.mock import patch

from research.yang_mills_su2.character_bounds import character_ratio_bounds
from research.yang_mills_su2.heatbath import (
    heatbath_sweep, sample_heatbath_link, staple_linear_coefficients,
)
from research.yang_mills_su2.lattice import Lattice4D
from research.yang_mills_su2.local_updates import affected_plaquettes
from research.yang_mills_su2.simulation import haar_su2
from research.yang_mills_su2.su2 import axis_angle, norm2


def random_lattice(extents, seed):
    lat = Lattice4D(extents)
    rng = random.Random(seed)
    for site in lat.sites:
        for mu in range(4):
            lat.set_link(site, mu, haar_su2(rng))
    return lat


class WilsonHeatbathTests(unittest.TestCase):
    def test_staple_coefficients_match_six_plaquettes_and_full_action(self):
        for extents in ((2, 2, 2, 2), (4, 2, 2, 2)):
            lat = random_lattice(extents, 91)
            site = (0, 0, 0, 0)
            for mu in range(4):
                with self.subTest(extents=extents, mu=mu):
                    old = lat.link(site, mu)
                    coeff = staple_linear_coefficients(lat, site, mu)
                    self.assertEqual(old, lat.link(site, mu))
                    proposal = axis_angle((1.0, -2.0, 3.0), 0.713)
                    actual_before = lat.wilson_action(0.7)
                    before_local = sum(lat.plaquette(s, i, j)[0]
                                       for s, i, j in affected_plaquettes(lat, site, mu))
                    try:
                        lat.set_link(site, mu, proposal)
                        actual_after = lat.wilson_action(0.7)
                        after_local = sum(lat.plaquette(s, i, j)[0]
                                          for s, i, j in affected_plaquettes(lat, site, mu))
                    finally:
                        lat.set_link(site, mu, old)
                    predicted_after_local = sum(x*y for x, y in zip(coeff, proposal))
                    predicted_before_local = sum(x*y for x, y in zip(coeff, old))
                    self.assertAlmostEqual(predicted_before_local, before_local, places=11)
                    self.assertAlmostEqual(predicted_after_local, after_local, places=11)
                    self.assertAlmostEqual(actual_after-actual_before,
                                           0.7*(predicted_before_local-predicted_after_local),
                                           places=10)

    def test_failed_basis_evaluation_restores_original_link(self):
        lat = random_lattice((2, 2, 2, 2), 12)
        site, mu = (0, 0, 0, 0), 3
        old = lat.link(site, mu)
        with patch.object(lat, "plaquette", side_effect=RuntimeError("failure")):
            with self.assertRaisesRegex(RuntimeError, "failure"):
                staple_linear_coefficients(lat, site, mu)
        self.assertEqual(lat.link(site, mu), old)

    def test_beta_zero_sampler_is_seeded_and_haar_consistent(self):
        rng = random.Random(123)
        q = [sample_heatbath_link((6.0, 1.0, 0.0, 0.0), 0.0, rng)
             for _ in range(1500)]
        self.assertTrue(all(abs(norm2(x)-1) < 1e-12 for x in q))
        self.assertLess(abs(statistics.fmean(x[0] for x in q)), 0.05)
        first = sample_heatbath_link((0.0, 0.0, 0.0, 0.0), 0.0, random.Random(19))
        second = sample_heatbath_link((0.0, 0.0, 0.0, 0.0), 0.0, random.Random(19))
        self.assertEqual(first, second)

    def test_kappa_two_conditional_mean_matches_independent_bessel_interval(self):
        rng = random.Random(42)
        values = [sample_heatbath_link((1., 0., 0., 0.), 2., rng)[0]
                  for _ in range(4000)]
        bound_lo, bound_hi = character_ratio_bounds(Fraction(2), 12)
        midpoint = float((bound_lo + bound_hi) / 2)
        self.assertLess(abs(statistics.fmean(values)-midpoint), 0.04)
        self.assertGreater(midpoint, 0.4331)
        self.assertLess(midpoint, 0.4332)

    def test_stable_high_concentration_and_zero_staple(self):
        q = sample_heatbath_link((6.0, 0.0, 0.0, 0.0), 8.0, random.Random(13))
        self.assertTrue(math.isfinite(q[0]))
        self.assertAlmostEqual(norm2(q), 1.0, places=12)
        flat = sample_heatbath_link((0.0,)*4, 0.7, random.Random(19))
        self.assertAlmostEqual(norm2(flat), 1.0, places=12)

    def test_subnormal_positive_concentration_keeps_haar_second_moment(self):
        rng = random.Random(42)
        values = [sample_heatbath_link((1.,0.,0.,0.),5e-324,rng)[0]**2
                  for _ in range(1000)]
        # Any almost-Haar distribution on S3 has E[q0^2] close to 1/4.
        self.assertGreater(statistics.fmean(values), 0.18)
        self.assertLess(statistics.fmean(values), 0.32)

    def test_standalone_conditional_handles_small_and_large_finite_staples(self):
        # Both have physically moderate kappa=1 despite extreme scaling.
        for coeff, beta in [((1e-200,0.,0.,0.),1e200),
                            ((1e200,0.,0.,0.),1e-200)]:
            with self.subTest(coeff=coeff):
                rng = random.Random(4)
                samples = [sample_heatbath_link(coeff,beta,rng)[0]
                           for _ in range(500)]
                self.assertGreater(statistics.fmean(samples), 0.15)
        zero = sample_heatbath_link((1e200,0.,0.,0.),0.0,random.Random(4))
        self.assertAlmostEqual(norm2(zero),1.0,places=12)
        # The mathematical coefficient norm exceeds max finite float, but
        # beta*h and the unit direction are both representable.
        diag = sample_heatbath_link((1e308,1e308,0.,0.),1e-308,random.Random(4))
        self.assertAlmostEqual(norm2(diag),1.0,places=12)

    def test_sweep_reproducibility_and_invalid_input(self):
        a = Lattice4D((2,2,2,2))
        b = Lattice4D((2,2,2,2))
        self.assertEqual(heatbath_sweep(a, 0.5, random.Random(44)), 64)
        self.assertEqual(heatbath_sweep(b, 0.5, random.Random(44)), 64)
        self.assertEqual(a.links, b.links)
        for beta in (-1, float("nan"), float("inf"), True):
            with self.subTest(beta=beta), self.assertRaises(ValueError):
                sample_heatbath_link((1.0,0.0,0.0,0.0), beta, random.Random(1))
        with self.assertRaises(ValueError):
            sample_heatbath_link((float("nan"),0,0,0), 1, random.Random(1))


if __name__ == "__main__":
    unittest.main()
