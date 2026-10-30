"""Glancing obstruction, higher GH corner hierarchy and curved pp-wave gates."""
from __future__ import annotations
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12 import gh_glancing_corners as flat
from v12 import gh_curved_ppwave as curved


class ExactGHExtendedTests(unittest.TestCase):
    def test_glancing_exact_frequency_formula(self):
        r=flat.glancing_obstruction(8)
        self.assertTrue(r["strict_upper_bound_verified"])
        self.assertEqual(r["normalized_minimum_singular_value_upper_bound"],"sqrt(3)/n")

    def test_glancing_sequence_rules_out_unweighted_bound(self):
        r=flat.glancing_summary()
        self.assertTrue(r["glancing_obstruction_proven"])
        self.assertFalse(r["uniform_weighted_Kreiss_estimate_proven"])
        self.assertEqual(len(r["sequence"]),6)

    def test_invalid_glancing_scales_refused(self):
        for n in (0,1,2.0,"100"):
            with self.subTest(n=n),self.assertRaises(ValueError):
                flat.glancing_obstruction(n)

    def test_positive_sommerfeld_corners_through_six(self):
        r=flat.higher_corner_hierarchy(
            *flat.reference_data("tangent_outgoing_poly"),max_order=6)
        self.assertTrue(r["passed"])
        self.assertEqual(len(r["levels"]),7)

    def test_first_corner_gate_misses_second_order_obstruction(self):
        r=flat.higher_corner_hierarchy(
            *flat.reference_data("order2_failure"),max_order=4)
        self.assertTrue(r["initial_C_zero"])
        self.assertTrue(r["initial_dt_C_zero"])
        self.assertTrue(all(row["metric_sommerfeld_zero"] for row in r["levels"][:2]))
        self.assertFalse(r["levels"][2]["metric_sommerfeld_zero"])
        self.assertEqual(r["levels"][2]["metric_residuals"][4],"-6")

    def test_zero_initial_data_at_corner_order_zero(self):
        r=flat.higher_corner_hierarchy(*flat.reference_data("zero"),max_order=0)
        self.assertTrue(r["passed"])

    def test_corner_order_bounded(self):
        with self.assertRaises(ValueError):
            flat.higher_corner_hierarchy(*flat.reference_data("zero"),max_order=20)

    def test_spacetime_dependent_initial_data_refused(self):
        f,g=flat.reference_data("zero")
        f["yz"]=flat.t
        with self.assertRaises(ValueError):
            flat.higher_corner_hierarchy(f,g)

    def test_ppwave_genuinely_curved_and_Ricci_flat(self):
        r=curved.verify_curved_ppwave()
        self.assertTrue(r["Ricci_tensor_zero"])
        self.assertTrue(r["nonflat_background"])
        self.assertEqual(r["curvature_R_x_u_x_u"],"-1")
        self.assertEqual(r["curvature_R_y_u_y_u"],"1")

    def test_ppwave_exact_covariant_constraint_operator(self):
        r=curved.verify_curved_ppwave()
        self.assertTrue(r["harmonic_coordinates"])
        self.assertTrue(r["curved_gauge_divergence_identity"])
        self.assertTrue(r["reduced_divergence_equals_minus_half_constraint_wave"])

    def test_ppwave_linearized_Bianchi(self):
        self.assertTrue(curved.verify_curved_ppwave()[
            "linearized_Bianchi_div_dG_zero"])

    def test_curved_bulk_does_not_claim_boundary_stability(self):
        r=curved.verify_curved_ppwave()
        self.assertFalse(r["curved_boundary_spectrum_proven"])
        self.assertFalse(r["curved_background_uniform_energy_proven"])
        self.assertFalse(r["curved_Einstein_IBVP_wellposedness_proven"])

    def test_curved_receipt_replay_refuses_tamper(self):
        r=curved.verify_curved_ppwave()
        self.assertTrue(curved.replay_curved_ppwave(r))
        forged=copy.deepcopy(r)
        forged["Ricci_tensor_zero"]=False
        self.assertFalse(curved.replay_curved_ppwave(forged))

    def test_joint_exact_glancing_corner_gate(self):
        self.assertEqual(flat.certify_glancing_and_corners()["status"],
            "PASS_GH_GLANCING_OBSTRUCTION_AND_FINITE_CORNERS")


if __name__=="__main__":
    unittest.main()
