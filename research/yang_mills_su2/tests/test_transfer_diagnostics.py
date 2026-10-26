"""Finite heatbath timeslices must not become spectral-proof assertions."""

import math
import unittest

from research.yang_mills_su2.transfer_diagnostics import (
    cosh_effective_mass, run_heatbath_timeslices,
)


class HeatbathTimesliceTests(unittest.TestCase):
    def test_cosh_mass_recovers_periodic_exact_two_state_fixture(self):
        # C(t)=cosh((2-t)ln2), T=4.  Independently: (17/8,5/4,1,5/4).
        values = (17/8, 5/4, 1.0, 5/4)
        self.assertAlmostEqual(cosh_effective_mass(values, 1), math.log(2), 12)

    def test_invalid_or_negative_correlations_refuse_mass_extraction(self):
        self.assertIsNone(cosh_effective_mass((1.0,-0.5,0.3,-0.5), 1))
        self.assertIsNone(cosh_effective_mass((1.0,2.0,1.0,2.0), 1))
        self.assertIsNone(cosh_effective_mass((math.nan,1.0,1.0,1.0), 1))
        for args in [((1.0,0.5,1.0), 1), ((1.0,0.5,0.3,0.5),0),
                     ((1.0,0.5,0.3,0.5),2)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                cosh_effective_mass(*args)

    def test_short_seeded_heatbath_run_has_raw_gauge_invariant_timeslices(self):
        receipt = run_heatbath_timeslices((4,2,2,2),0.0,(17,29),2,4,1)
        self.assertEqual(receipt["status"], "FINITE_HEATBATH_TIMESLICE_DIAGNOSTIC")
        for forbidden in ("continuum_mass_gap_proven", "equilibrium_claim",
                          "physical_law_proven", "lean_kernel_verified"):
            self.assertFalse(receipt[forbidden])
        for label in ("cold", "haar"):
            group = receipt["groups"][label]
            self.assertEqual(len(group["chains"]), 2)
            self.assertEqual(len(group["folded_connected_correlator"]), 4)
            for chain in group["chains"]:
                self.assertEqual([p["sweep"] for p in chain["trace"]], [1,2,3,4])
                for point in chain["trace"]:
                    self.assertEqual(len(point["timeslice"]), 4)
                    self.assertTrue(all(-1 <= x <= 1 for x in point["timeslice"]))

    def test_heatbath_receipt_replays_with_same_parameters(self):
        args=((4,2,2,2),0.5,(2,3),1,2,1)
        self.assertEqual(run_heatbath_timeslices(*args),run_heatbath_timeslices(*args))

    def test_beta_zero_emits_only_explicitly_scoped_bias_control(self):
        receipt = run_heatbath_timeslices((4,2,2,2),0.0,(17,29),1,2,1)
        for group in receipt["groups"].values():
            certificate = group["beta_zero_exact_receipt"]
            self.assertEqual(certificate["centering_correction"],
                             {"numerator": "1", "denominator": "768"})
            for raw, adjusted in zip(group["connected_correlator"],
                                     group["beta_zero_bias_corrected_correlator"]):
                self.assertAlmostEqual(adjusted - raw, 1/768, 15)
            self.assertFalse(group["beta_zero_exact_receipt"]["continuum_mass_gap_proven"])

    def test_positive_beta_must_not_inherit_beta_zero_certificate(self):
        receipt = run_heatbath_timeslices((4,2,2,2),0.5,(17,29),0,2,1)
        for group in receipt["groups"].values():
            self.assertNotIn("beta_zero_exact_receipt", group)
            self.assertNotIn("beta_zero_bias_corrected_correlator", group)

    def test_rejects_temporal_size_and_expensive_inputs(self):
        for args in [
            ((3,2,2,2),0.5,(1,2),1,4,1),
            ((4,2,2,2),-1.0,(1,2),1,4,1),
            ((4,2,2,2),0.5,(1,1),1,4,1),
            ((6,3,3,3),0.5,(1,2,3,4),500,500,1),
            ((4,2,2,2),0.5,(1,2),1,2,3),
        ]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                run_heatbath_timeslices(*args)


if __name__ == "__main__":
    unittest.main()
