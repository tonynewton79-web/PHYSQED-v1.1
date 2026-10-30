"""Linearized harmonic Einstein boundary map: exact positive/adversarial suite."""
import copy
import sys
import unittest
from pathlib import Path
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.gh_boundary_map import (
    t,x,y,z,zero_metric,tensor,wave,harmonic_constraint,
    linearized_einstein,general_differential_intertwiner,normal_mode_symbol,
    first_corner_gate,certify_explicit_linearized_metric,
    reference_positive_wave,reference_constraint_velocity_failure,
    reference_metric_corner_failure,naive_sommerfeld_counterexample,
    certify_symbol_and_controls,replay_gh_metric)


class GHBoundaryTests(unittest.TestCase):
    def test_exact_general_differential_intertwining(self):
        self.assertTrue(general_differential_intertwiner())

    def test_ten_by_ten_symbol_factorization(self):
        o=normal_mode_symbol()
        self.assertEqual(o["ten_by_ten_boundary_symbol"].shape,(10,10))
        self.assertTrue(o["factorization_verified"])

    def test_normal_mode_no_kernel_for_positive_laplace_frequency(self):
        o=normal_mode_symbol()
        s,k,eta,zeta=S.symbols("s k eta zeta")
        self.assertEqual(o["determinant"].subs({s:1,k:1,eta:0,zeta:0}),64)
        self.assertFalse(o["uniform_glancing_Kreiss_estimate_verified"])

    def test_nontrivial_transverse_wave_satisfies_full_linearized_Einstein(self):
        r=certify_explicit_linearized_metric(reference_positive_wave())
        self.assertEqual(r["status"],"PASS_LOCAL_LINEARIZED_GH_BOUNDARY_AND_CORNERS")
        self.assertTrue(r["full_linearized_vacuum_Einstein_passed"])

    def test_all_first_corner_conditions_checked(self):
        r=certify_explicit_linearized_metric(reference_positive_wave())
        c=r["initial_corner"]
        for name in ("C_initial_zero","dt_C_initial_zero",
                     "metric_corner_order0_zero","metric_corner_order1_zero",
                     "harmonic_corner_order0_zero","harmonic_corner_order1_zero"):
            self.assertTrue(c[name],name)
        self.assertFalse(c["higher_order_corner_compatibility_proven"])

    def test_linearized_constraint_velocity_missing_is_refused(self):
        r=certify_explicit_linearized_metric(reference_constraint_velocity_failure())
        self.assertTrue(r["initial_corner"]["C_initial_zero"])
        self.assertFalse(r["initial_corner"]["dt_C_initial_zero"])
        self.assertFalse(r["full_linearized_vacuum_Einstein_passed"])

    def test_wrong_harmonic_boundary_data_rejected(self):
        r=certify_explicit_linearized_metric(reference_constraint_velocity_failure())
        self.assertEqual(r["boundary_constraint_components"],["0","t","0","0"])
        self.assertFalse(r["four_boundary_harmonic_constraints_passed"])

    def test_metric_sommerfeld_corner_failure_even_if_C_zero(self):
        r=certify_explicit_linearized_metric(reference_metric_corner_failure())
        self.assertTrue(r["four_boundary_harmonic_constraints_passed"])
        self.assertFalse(r["six_tangent_sommerfeld_boundary_rows_passed"])
        self.assertFalse(r["initial_corner"]["metric_corner_order0_zero"])

    def test_all_component_metric_sommerfeld_false_inference(self):
        r=naive_sommerfeld_counterexample()
        self.assertTrue(r["all_reduced_wave_components_zero"])
        self.assertTrue(r["all_ten_metric_sommerfeld_rows_zero"])
        self.assertTrue(r["exact_obstruction_passed"])
        self.assertEqual(r["harmonic_Cx_on_boundary"],"2*t")

    def test_tangential_source_breaks_constraint_sommerfeld(self):
        r=naive_sommerfeld_counterexample()
        self.assertEqual(r["incoming_harmonic_Cx_boundary_residual"],"2")
        self.assertEqual(r["tangential_laplacian_source"],"2")

    def test_independently_derived_full_Einstein_not_assumed_from_reduced_wave(self):
        h=tensor(reference_constraint_velocity_failure())
        self.assertNotEqual(linearized_einstein(h),S.zeros(4))

    def test_untrusted_string_input_rejected(self):
        h=zero_metric();h["yz"]="__import__('os').system('id')"
        with self.assertRaises(ValueError):
            certify_explicit_linearized_metric(h)

    def test_untrusted_float_input_rejected(self):
        h=zero_metric();h["yz"]=0.5
        with self.assertRaises(ValueError):
            certify_explicit_linearized_metric(h)

    def test_undeclared_symbol_rejected(self):
        h=zero_metric();h["yz"]=S.Symbol("alpha")
        with self.assertRaises(ValueError):
            certify_explicit_linearized_metric(h)

    def test_missing_metric_component_rejected(self):
        h=zero_metric();del h["xx"]
        with self.assertRaises(ValueError):
            certify_explicit_linearized_metric(h)

    def test_invalid_cauchy_time_symbol_refused(self):
        h=zero_metric()
        h["yz"]=t
        with self.assertRaises(ValueError):
            first_corner_gate(h,zero_metric())

    def test_receipt_replay_tampering_refused(self):
        h=reference_positive_wave()
        r=certify_explicit_linearized_metric(h)
        self.assertTrue(replay_gh_metric(h,r))
        fake=copy.deepcopy(r)
        fake["nonlinear_GH_Einstein_IBVP_proven"]=True
        self.assertFalse(replay_gh_metric(h,fake))

    def test_cumulative_scoped_gate(self):
        r=certify_symbol_and_controls()
        self.assertEqual(r["status"],"PASS_SCOPED_LINEARIZED_GH_DIFFERENTIAL_BOUNDARY_MAP")
        self.assertTrue(r["operator_intertwiner_verified"])
        self.assertTrue(r["normal_mode_factorization_verified"])
        self.assertFalse(r["uniform_Kreiss_Lopatinski_proven"])
        self.assertFalse(r["nonlinear_Einstein_IBVP_proven"])


if __name__=="__main__":
    unittest.main()
