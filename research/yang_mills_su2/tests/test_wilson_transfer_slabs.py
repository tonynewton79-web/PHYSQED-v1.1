"""Gauge-invariant positive-beta Wilson transfer-slab action identities."""

import math
import random
import unittest

from research.yang_mills_su2.lattice import Lattice4D
from research.yang_mills_su2.simulation import (
    connected_timeslice, haar_su2, timeslice_plaquette,
)


class WilsonTransferSlabTests(unittest.TestCase):
    def _haar_configuration(self, seed: int) -> tuple[Lattice4D, dict]:
        rng = random.Random(seed)
        lattice = Lattice4D((4, 2, 2, 2))
        for site in lattice.sites:
            for direction in range(4):
                lattice.set_link(site, direction, haar_su2(rng))
        gauges = {site: haar_su2(rng) for site in lattice.sites}
        return lattice, gauges

    def test_identity_four_dimensional_wilson_slabs_have_exact_counts(self):
        from research.yang_mills_su2.wilson_transfer_slabs import wilson_slab_log_weights

        lattice = Lattice4D((4, 2, 2, 2))
        self.assertEqual(wilson_slab_log_weights(lattice, 2.0), (96.0,)*4)
        self.assertEqual(wilson_slab_log_weights(lattice, 0.0), (0.0,)*4)
        self.assertEqual(sum(wilson_slab_log_weights(lattice, 2.0)),
                         2.0*lattice.plaquette_count)

    def test_nontrivial_wilson_action_factorizes_and_preserves_gauge(self):
        from research.yang_mills_su2.wilson_transfer_slabs import wilson_slab_log_weights

        lattice, gauges = self._haar_configuration(619)
        beta = 0.625
        slabs = wilson_slab_log_weights(lattice, beta)
        self.assertEqual(len(slabs), 4)
        expected = beta*lattice.plaquette_count - lattice.wilson_action(beta)
        self.assertAlmostEqual(math.fsum(slabs), expected, places=11)
        transformed = lattice.gauge_transformed(gauges)
        for actual, other in zip(slabs, wilson_slab_log_weights(transformed, beta)):
            self.assertAlmostEqual(actual, other, places=11)

    def test_temporal_transfer_link_product_matches_wilson_plaquette(self):
        from research.yang_mills_su2.wilson_transfer_slabs import (
            wilson_temporal_kernel_log,
        )

        lattice, gauges = self._haar_configuration(1049)
        beta = 0.75
        self.assertEqual(wilson_temporal_kernel_log(Lattice4D((4,2,2,2)),2.0,0),48.0)
        for time in range(4):
            expected = beta * math.fsum(
                lattice.plaquette(site,0,direction)[0]
                for site in lattice.sites if site[0] == time
                for direction in (1,2,3))
            self.assertAlmostEqual(wilson_temporal_kernel_log(lattice,beta,time),
                                   expected, places=11)
            self.assertAlmostEqual(
                wilson_temporal_kernel_log(lattice.gauge_transformed(gauges),beta,time),
                expected, places=11)
        with self.assertRaises(ValueError):
            wilson_temporal_kernel_log(lattice,beta,True)

    def test_temporal_plaquette_correlator_is_gauge_invariant(self):
        from research.yang_mills_su2.wilson_transfer_slabs import wilson_slab_log_weights

        lattice0, gauges0 = self._haar_configuration(619)
        lattice1, gauges1 = self._haar_configuration(803)
        samples = [timeslice_plaquette(lattice0), timeslice_plaquette(lattice1)]
        rotated = [timeslice_plaquette(lattice0.gauge_transformed(gauges0)),
                   timeslice_plaquette(lattice1.gauge_transformed(gauges1))]
        for raw, rotated_value in zip(connected_timeslice(samples),
                                       connected_timeslice(rotated)):
            self.assertAlmostEqual(raw, rotated_value, places=11)
        # The physical Wilson density at nonzero beta is also unchanged.
        self.assertAlmostEqual(
            sum(wilson_slab_log_weights(lattice0, 0.5)),
            sum(wilson_slab_log_weights(lattice0.gauge_transformed(gauges0), 0.5)),
            places=11)

    def test_bad_physical_configuration_or_coupling_is_rejected(self):
        from research.yang_mills_su2.wilson_transfer_slabs import wilson_slab_log_weights

        lattice = Lattice4D((4, 2, 2, 2))
        for obj, beta in ((lattice, -0.1), (lattice, True),
                          (lattice, float("nan")), (lattice, 9.0),
                          (object(), 0.5)):
            with self.subTest(beta=beta, obj=type(obj)), self.assertRaises(ValueError):
                wilson_slab_log_weights(obj, beta)


if __name__ == "__main__":
    unittest.main()
