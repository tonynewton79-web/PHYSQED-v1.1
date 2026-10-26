"""Independent whole-action reference for local SU(2) link updates."""

import math
import random
import unittest

from research.yang_mills_su2.lattice import Lattice4D
from research.yang_mills_su2.simulation import haar_su2, metropolis_sweep
from research.yang_mills_su2.su2 import axis_angle
from research.yang_mills_su2.local_updates import (
    affected_plaquettes, link_delta_action, metropolis_sweep_local,
)


class LocalUpdateTests(unittest.TestCase):
    def test_each_link_touches_six_distinct_oriented_plaquettes(self):
        for lengths in ((2, 2, 2, 2), (3, 3, 3, 3)):
            lat = Lattice4D(lengths)
            for site in lat.sites:
                for mu in range(4):
                    keys = affected_plaquettes(lat, site, mu)
                    self.assertEqual(len(keys), 6)
                    self.assertEqual(len(set(keys)), 6)
                    self.assertTrue(all(a < b for _, a, b in keys))

    def test_exact_single_link_geometry_and_unmodified_input(self):
        lat = Lattice4D((2, 2, 2, 2))
        site = (0, 0, 0, 0)
        proposal = axis_angle((0, 0, 1), math.pi / 3)
        self.assertAlmostEqual(link_delta_action(lat, site, 0, proposal, 2.0), 6.0,
                               places=12)
        self.assertEqual(lat.link(site, 0), (1.0, 0.0, 0.0, 0.0))
        with self.assertRaises(ValueError):
            link_delta_action(lat, site, 0, (4.0, 0.0, 0.0, 0.0), 2.0)
        self.assertEqual(lat.link(site, 0), (1.0, 0.0, 0.0, 0.0))

    def test_local_change_agrees_with_independent_full_wilson_action(self):
        for lengths in ((2, 2, 2, 2), (3, 3, 3, 3)):
            rng = random.Random(2718)
            lat = Lattice4D(lengths)
            for site in lat.sites:
                for mu in range(4):
                    lat.set_link(site, mu, haar_su2(rng))
            for site, mu in [
                (lat.sites[0], 0), (lat.sites[len(lat.sites)//2], 1),
                (lat.sites[-1], 2), (lat.sites[3], 3),
            ]:
                proposal = haar_su2(rng)
                before = lat.wilson_action(0.75)
                delta = link_delta_action(lat, site, mu, proposal, 0.75)
                self.assertAlmostEqual(lat.wilson_action(0.75), before, places=10)
                original = lat.link(site, mu)
                lat.set_link(site, mu, proposal)
                full_delta = lat.wilson_action(0.75) - before
                self.assertAlmostEqual(delta, full_delta, places=9)
                lat.set_link(site, mu, original)

    def test_local_sweep_matches_original_metropolis_seeded_trajectory(self):
        old, new = Lattice4D((2, 2, 2, 2)), Lattice4D((2, 2, 2, 2))
        rng_old, rng_new = random.Random(19), random.Random(19)
        for _ in range(3):
            self.assertEqual(metropolis_sweep(old, 0.7, 0.3, rng_old),
                             metropolis_sweep_local(new, 0.7, 0.3, rng_new))
        for key in old.links:
            for left, right in zip(old.links[key], new.links[key]):
                self.assertAlmostEqual(left, right, places=12)


if __name__ == "__main__":
    unittest.main()
