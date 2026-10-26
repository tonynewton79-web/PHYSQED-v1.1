"""Matched finite cold/Haar trace tests with no equilibrium claim."""

import math
import statistics
import unittest

from research.yang_mills_su2.equilibration import run_equilibration


class EquilibrationStudyTests(unittest.TestCase):
    def test_matching_protocol_traces_and_reproducible_descriptive_statistics(self):
        params = dict(extents=(2, 2, 2, 2), beta=0.0, seeds=(123, 456),
                      sweeps=8, epsilon=0.15)
        report = run_equilibration(**params)
        self.assertEqual(report, run_equilibration(**params))
        self.assertEqual(report["status"], "FINITE_COLD_HAAR_TRAJECTORY_DIAGNOSTIC")
        self.assertFalse(report["equilibrium_claim"])
        self.assertFalse(report["physical_law_proven"])
        self.assertFalse(report["continuum_mass_gap_proven"])
        self.assertEqual(set(report["groups"]), {"cold", "haar"})
        for name in ("cold", "haar"):
            group = report["groups"][name]
            self.assertEqual(len(group["chains"]), 2)
            self.assertEqual([c["seed"] for c in group["chains"]], [123, 456])
            for chain in group["chains"]:
                trace = chain["trace"]
                self.assertEqual([r["sweep"] for r in trace], list(range(1, 9)))
                values = [r["spatial_plaquette"] for r in trace]
                self.assertAlmostEqual(chain["early_mean"], statistics.fmean(values[:4]))
                self.assertAlmostEqual(chain["late_mean"], statistics.fmean(values[4:]))
                self.assertAlmostEqual(chain["late_minus_early"],
                                       chain["late_mean"] - chain["early_mean"])
                if chain["lag_one_correlation"] is not None:
                    self.assertLessEqual(abs(chain["lag_one_correlation"]), 1.0+1e-12)
        cold = report["groups"]["cold"]["late_mean"]
        hot = report["groups"]["haar"]["late_mean"]
        self.assertGreater(cold, 0.8)
        self.assertLess(abs(hot), 0.3)
        self.assertAlmostEqual(report["cold_minus_haar_late_mean"], cold-hot)

    def test_finite_resource_and_bad_parameter_guardrails(self):
        base = dict(extents=(2, 2, 2, 2), beta=0.5, seeds=(1, 2),
                    sweeps=8, epsilon=0.2)
        for field, invalid in [
            ("extents", (1, 2, 2, 2)), ("extents", (8, 8, 8, 8)),
            ("beta", -1), ("beta", math.inf), ("seeds", (1,)),
            ("seeds", (1, -1)), ("seeds", (True, 2)),
            ("sweeps", 3), ("sweeps", 5000),
            ("epsilon", -0.1), ("epsilon", math.nan),
        ]:
            with self.subTest(field=field, invalid=invalid):
                with self.assertRaises(ValueError):
                    run_equilibration(**{**base, field: invalid})


if __name__ == "__main__":
    unittest.main()
