"""Geometric lower obstruction for single-link Wilson SU2 Dobrushin maps."""

import copy
from fractions import Fraction
import json
import math
from pathlib import Path
import unittest

from research.yang_mills_su2.lattice import IDENTITY, Lattice4D
from research.yang_mills_su2.wilson_dobrushin_ceiling import (
    ceiling_receipt,
    ceiling_row_lower,
    local_ceiling_witness,
    replay_ceiling_receipt,
)


_BASIS = ((1., 0., 0., 0.), (0., 1., 0., 0.),
          (0., 0., 1., 0.), (0., 0., 0., 1.))


def _local_parameter(lattice: Lattice4D, witness: dict) -> tuple[float, ...]:
    """Independent Wilson plaquette evaluations recover the linear e-field."""
    center, direction = witness["center_link"]
    old = lattice.link(center, direction)
    try:
        values = []
        for basis in _BASIS:
            lattice.set_link(center, direction, basis)
            values.append(sum(lattice.plaquette(root, 0, nu)[0]
                              for root, nu in witness["incident_plaquettes"]))
        return tuple(values)
    finally:
        lattice.set_link(center, direction, old)


class WilsonDobrushinCeilingTests(unittest.TestCase):
    def test_committed_method_ceiling_example_replays(self):
        path = (Path(__file__).resolve().parents[1] / "artifacts" /
                "wilson_single_link_ceiling_beta2_over_9.json")
        obj = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(obj, ceiling_receipt(2, 9))
        self.assertTrue(replay_ceiling_receipt(obj))

    def test_all_six_sign_staples_cancel_and_eighteen_neighbors_are_distinct(self):
        for sizes in ((3, 3, 3, 3), (4, 3, 3, 4)):
            with self.subTest(sizes=sizes):
                w = local_ceiling_witness(sizes)
                self.assertEqual(w["center_link"], ((0, 0, 0, 0), 0))
                self.assertEqual(len(w["incident_plaquettes"]), 6)
                self.assertEqual(len(w["neighbor_links"]), 18)
                self.assertEqual(len(set(w["neighbor_links"])), 18)
                self.assertEqual(len(w["negative_opposite_links"]), 3)
                links = {(site, direction): IDENTITY for site in Lattice4D(sizes).sites
                         for direction in range(4)}
                for key in w["negative_opposite_links"]:
                    links[key] = (-1., 0., 0., 0.)
                lattice = Lattice4D(sizes, links)
                self.assertEqual(_local_parameter(lattice, w), (0., 0., 0., 0.))

    def test_each_of_eighteen_links_reaches_haar_point_derivative(self):
        w = local_ceiling_witness((3, 3, 3, 3))
        lattice = Lattice4D((3, 3, 3, 3))
        for key in w["negative_opposite_links"]:
            lattice.set_link(*key, (-1., 0., 0., 0.))
        self.assertEqual(_local_parameter(lattice, w), (0., 0., 0., 0.))
        theta = 0.0001
        for key in w["neighbor_links"]:
            old = lattice.link(*key)
            sign = old[0]
            lattice.set_link(*key, (sign*math.cos(theta),
                                    sign*math.sin(theta), 0., 0.))
            varied = _local_parameter(lattice, w)
            lattice.set_link(*key, old)
            self.assertAlmostEqual(math.sqrt(sum(x*x for x in varied))/theta,
                                   1., delta=0.00001, msg=str(key))

    def test_method_ceiling_is_nine_beta_over_two_not_continuum_gap(self):
        self.assertEqual(ceiling_row_lower(Fraction(2, 9)), Fraction(1))
        self.assertEqual(ceiling_row_lower(Fraction(1, 4)), Fraction(9, 8))
        self.assertEqual(ceiling_row_lower(Fraction(1, 10)), Fraction(9, 20))

    def test_strict_replay_and_adversarial_status(self):
        receipt = ceiling_receipt(2, 9)
        self.assertTrue(replay_ceiling_receipt(receipt))
        self.assertFalse(receipt["continuum_mass_gap_proven"])
        self.assertFalse(receipt["global_sharp_wasserstein_upper_proven"])
        self.assertEqual(receipt["row_lower"],
                         {"numerator": "1", "denominator": "1"})
        for field, bad in (("continuum_mass_gap_proven", True),
                           ("global_sharp_wasserstein_upper_proven", True),
                           ("row_lower", {"numerator": "0", "denominator": "1"}),
                           ("fingerprint", "0"*64)):
            changed = copy.deepcopy(receipt)
            changed[field] = bad
            self.assertFalse(replay_ceiling_receipt(changed))

    def test_reject_torus_aliasing_and_nonrational_parameters(self):
        for sizes in ((2, 3, 3, 3), (3, 2, 3, 3),
                      (3, 3, 3, 2), (3, 3, 3, True)):
            with self.subTest(sizes=sizes), self.assertRaises(ValueError):
                local_ceiling_witness(sizes)
        for beta in (0.25, True, Fraction(-1, 2)):
            with self.subTest(beta=beta), self.assertRaises(ValueError):
                ceiling_row_lower(beta)
        for args in ((0, 9), (2, 0), (True, 9),
                     (2, True), (2, 2**200)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                ceiling_receipt(*args)


if __name__ == "__main__":
    unittest.main()
