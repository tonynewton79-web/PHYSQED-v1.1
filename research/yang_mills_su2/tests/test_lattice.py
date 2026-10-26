"""Finite 4D Wilson-action invariance and orientation checks."""
import math
import unittest

from research.yang_mills_su2.lattice import Lattice4D
from research.yang_mills_su2.su2 import axis_angle, dagger


class LatticeTests(unittest.TestCase):
    def test_periodic_identity_geometry(self):
        lat = Lattice4D((2, 2, 2, 2))
        self.assertEqual(lat.shifted((1, 0, 0, 0), 0), (0, 0, 0, 0))
        self.assertEqual(lat.shifted((0, 0, 0, 0), 3, -1), (0, 0, 0, 1))
        self.assertEqual(len(lat.sites), 16)
        self.assertEqual(lat.plaquette_count, 96)
        self.assertEqual(lat.wilson_action(2.0), 0.0)

    def test_plaquette_reverse_orientation(self):
        lat = Lattice4D((2, 2, 2, 2))
        lat.set_link((0, 0, 0, 0), 0, axis_angle((0, 0, 1), math.pi/3))
        p = lat.plaquette((0, 0, 0, 0), 0, 1)
        rev = lat.plaquette((0, 0, 0, 0), 1, 0)
        for x, y in zip(rev, dagger(p)):
            self.assertAlmostEqual(x, y, places=12)
        self.assertGreater(lat.wilson_action(2.0), 0.0)
        self.assertAlmostEqual(lat.wilson_action(2.0), 6*2*(1-math.cos(math.pi/3)), places=11)

    def test_nonconstant_local_gauge_transform_preserves_action(self):
        lat = Lattice4D((2, 2, 2, 2))
        lat.set_link((0, 0, 0, 0), 0, axis_angle((1, 2, 3), 0.63))
        lat.set_link((1, 0, 0, 1), 2, axis_angle((3, 2, 1), 0.47))
        before = lat.wilson_action(3.5)
        site_gauge = {
            x: axis_angle((1+x[0], 1+x[1], 1+x[2]), 0.1+0.12*sum(x))
            for x in lat.sites
        }
        transformed = lat.gauge_transformed(site_gauge)
        self.assertAlmostEqual(transformed.wilson_action(3.5), before, places=9)
        self.assertAlmostEqual(lat.wilson_action(3.5), before, places=12)

    def test_invalid_lattice_links_and_couplings_rejected(self):
        for extents in [(1, 2, 2, 2), (2, 2, 2), (2, 2, 2, -1)]:
            with self.subTest(extents=extents), self.assertRaises(ValueError):
                Lattice4D(extents)
        lat = Lattice4D((2, 2, 2, 2))
        with self.assertRaises(ValueError):
            lat.set_link((0, 0, 0, 0), 0, (2, 0, 0, 0))
        with self.assertRaises(ValueError):
            lat.wilson_action(-1)
        with self.assertRaises(ValueError):
            lat.wilson_action(math.nan)
        with self.assertRaises(ValueError):
            lat.gauge_transformed({})


if __name__ == "__main__":
    unittest.main()
