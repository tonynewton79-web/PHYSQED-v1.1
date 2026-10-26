"""Independent exact fixtures for the ideal beta-zero SU(2) null model."""

from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import statistics
import unittest

from research.yang_mills_su2.simulation import connected_timeslice
from research.yang_mills_su2.lattice import Lattice4D
from research.yang_mills_su2.beta_zero_correlators import (
    beta_zero_corrected_correlator,
    beta_zero_correlator_receipt,
    exact_beta_zero_covariance,
    expected_centered_covariance,
    replay_beta_zero_correlator_receipt,
)


class ExactBetaZeroCorrelatorTests(unittest.TestCase):
    def test_committed_example_receipt_matches_exact_recomputed_source(self):
        path = Path(__file__).resolve().parents[1] / "artifacts" / (
            "beta_zero_correlator_4x2x2x2_m2.json")
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")),
                         beta_zero_correlator_receipt((4,2,2,2), 2))

    def test_spatial_plaquette_loops_are_distinct_even_with_side_length_two(self):
        # Independent incidence check for the one-unshared-link step in
        # the Haar-orthogonality proof, including wrapped 2^3 tori.
        for extents in ((4,2,2,2), (4,3,3,3), (6,2,3,2)):
            lat = Lattice4D(extents)
            supports = []
            for site in lat.sites:
                for mu in (1, 2, 3):
                    for nu in range(mu+1, 4):
                        supports.append(frozenset((
                            (site, mu), (lat.shifted(site, mu), nu),
                            (lat.shifted(site, nu), mu), (site, nu))))
            self.assertEqual(len(set(supports)), 3 * math.prod(extents))
            self.assertTrue(all(len(support) == 4 for support in supports))

    def test_exact_time_covariance_at_spatial_volume_eight(self):
        self.assertEqual(
            exact_beta_zero_covariance((4, 2, 2, 2)),
            (Fraction(1, 96), Fraction(0), Fraction(0), Fraction(0)),
        )

    def test_centered_estimator_bias_uses_all_times_and_measurements(self):
        self.assertEqual(
            expected_centered_covariance((4, 2, 2, 2), 2),
            (Fraction(7, 768), Fraction(-1, 768), Fraction(-1, 768),
             Fraction(-1, 768)),
        )
        self.assertEqual(
            expected_centered_covariance((6, 2, 2, 3), 3),
            (Fraction(17, 18 * 144),) + (Fraction(-1, 18 * 144),) * 5,
        )

    def test_receipt_replays_exact_and_rejects_tampering(self):
        receipt = beta_zero_correlator_receipt((4, 2, 2, 2), 2)
        self.assertTrue(replay_beta_zero_correlator_receipt(receipt))
        self.assertEqual(receipt["centering_correction"],
                         {"numerator": "1", "denominator": "768"})
        self.assertEqual(receipt["expected_bias_corrected_covariance"],
                         receipt["exact_covariance"])
        for scope_flag in ("equilibrium_claim", "physical_law_proven",
                           "continuum_mass_gap_proven", "lean_kernel_verified"):
            self.assertIs(receipt[scope_flag], False)
            forged = deepcopy(receipt)
            forged[scope_flag] = True
            self.assertFalse(replay_beta_zero_correlator_receipt(forged))
        for bad in (None, [], {"parameters": {}}, {**receipt, "proof": True}):
            self.assertFalse(replay_beta_zero_correlator_receipt(bad))
        forged = deepcopy(receipt)
        forged["expected_empirical_centered_covariance"][1] = {
            "numerator": "0", "denominator": "1"}
        self.assertFalse(replay_beta_zero_correlator_receipt(forged))
        forged = deepcopy(receipt)
        forged["parameters"]["coupling_beta"] = False  # bool == 0 in Python
        self.assertFalse(replay_beta_zero_correlator_receipt(forged))
        forged = deepcopy(receipt)
        forged["physical_law_proven"] = 0  # int == False in Python
        self.assertFalse(replay_beta_zero_correlator_receipt(forged))

    def test_refuses_malformed_and_resource_exhaustive_arguments(self):
        invalid = [
            ((True, 2, 2, 2), 2), ((4, 1, 2, 2), 2),
            ((4, 2, 2, 2), True), ((4, 2, 2, 2), 1),
            ((4, 2, 2, 2), 1000000), ((1000000, 2, 2, 2), 2),
            ([4, 2, 2, 2], 2),
        ]
        for extents, measurements in invalid:
            with self.subTest(extents=extents, measurements=measurements):
                with self.assertRaises(ValueError):
                    beta_zero_correlator_receipt(extents, measurements)

    def test_known_bias_is_added_at_every_lag_without_mutating_raw_samples(self):
        samples = [(1.0, 0.5, -0.5, 0.0),
                   (-0.25, 0.75, 0.25, -0.75)]
        before = deepcopy(samples)
        raw = connected_timeslice(samples)
        corrected = beta_zero_corrected_correlator(samples, (4, 2, 2, 2))
        self.assertEqual(samples, before)
        for t in range(4):
            self.assertAlmostEqual(corrected[t] - raw[t], 1 / 768, 15)

    def test_complete_256_case_independent_rademacher_ensemble(self):
        # Every one of 2^(M*T)=256 equally weighted signs is enumerated.
        # Scaling each sign by 1/sqrt(96) gives exactly the beta-zero
        # time-slice variance, independently of the implementation.
        scale = 1 / math.sqrt(96)
        raw_ensemble = [[] for _ in range(4)]
        corrected_ensemble = [[] for _ in range(4)]
        for signs in product((-1, 1), repeat=8):
            samples = [tuple(signs[i] * scale for i in range(t, t + 4))
                       for t in (0, 4)]
            raw = connected_timeslice(samples)
            fixed = beta_zero_corrected_correlator(samples, (4, 2, 2, 2))
            for shift in range(4):
                raw_ensemble[shift].append(raw[shift])
                corrected_ensemble[shift].append(fixed[shift])
        for shift in range(4):
            self.assertAlmostEqual(
                statistics.fmean(raw_ensemble[shift]),
                7/768 if shift == 0 else -1/768, 15)
            self.assertAlmostEqual(
                statistics.fmean(corrected_ensemble[shift]),
                1/96 if shift == 0 else 0.0, 15)

    def test_corrector_refuses_bad_samples_and_extents(self):
        good = [(0.1, 0.2, 0.3, 0.4), (0.5, 0.6, 0.7, 0.8)]
        for samples, extents in [
            (good[:1], (4, 2, 2, 2)),
            (good, (5, 2, 2, 2)),
            ([(0.1, 0.2, math.nan, 0.4), good[1]], (4, 2, 2, 2)),
            ([(0.1, 0.2, 10**1000, 0.4), good[1]], (4, 2, 2, 2)),
            ([(True, 0.2, 0.3, 0.4), good[1]], (4, 2, 2, 2)),
            (good, (4, 1, 2, 2)),
            (good, (4, 2, 2, True)),
        ]:
            with self.subTest(samples=samples, extents=extents):
                with self.assertRaises(ValueError):
                    beta_zero_corrected_correlator(samples, extents)


if __name__ == "__main__":
    unittest.main()
