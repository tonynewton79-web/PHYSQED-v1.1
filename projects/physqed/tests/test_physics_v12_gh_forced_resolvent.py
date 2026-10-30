"""Adversarial first-order inhomogeneous GH resolvent and source corner gates."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.gh_forced_resolvent import (
    first_order_forcing_normal_form,boundary_source_lift,
    exact_exponential_volume_and_boundary_solution,
    prove_regular_source_resolvent,replay_regular_source_resolvent,
    nonzero_reduction_defect_solution)
from v12.gh_forced_corners import (
    check_sourced_harmonic_corners,sourced_wave_positive_control)
from v12.gh_first_order_uniform import analytic_uniform_bound


class ForcedGHTests(unittest.TestCase):
    def test_first_order_source_kinematic_rows(self):
        self.assertTrue(first_order_forcing_normal_form()[
            "first_order_kinematic_rows_zero"])

    def test_wave_source_elimination(self):
        self.assertTrue(first_order_forcing_normal_form()[
            "momentum_row_equals_forced_wave_residual"])

    def test_reduction_source_not_silently_zero(self):
        self.assertTrue(first_order_forcing_normal_form()[
            "reduction_source_equations_zero"])
        self.assertFalse(first_order_forcing_normal_form()[
            "arbitrary_first_order_L2_source_estimate_proven"])

    def test_exact_boundary_six_plus_four_lift(self):
        v=boundary_source_lift()
        self.assertTrue(v["P_gram_exact"])
        self.assertTrue(v["N_gram_identity"])
        self.assertEqual(v["T_operator_norm_squared_upper_bound"],7)

    def test_uniform_homogeneous_bound_used_explicitly(self):
        self.assertTrue(analytic_uniform_bound()[
            "uniform_homogeneous_stable_mode_trace_estimate_proven"])
        self.assertTrue(prove_regular_source_resolvent()[
            "boundary_source_lift"]["original_matched_boundary_matrix"])

    def test_forced_source_and_bound(self):
        r=prove_regular_source_resolvent()
        self.assertEqual(r["status"],
            "PASS_REGULAR_SOURCE_INHOMOGENEOUS_GH_HALFSPACE_ESTIMATE")
        self.assertTrue(r["constants_exactly_verified"])
        self.assertTrue(r["uniform_over_glancing_for_gamma_positive"])

    def test_nonzero_forced_wave_exact(self):
        self.assertTrue(exact_exponential_volume_and_boundary_solution()[
            "effective_wave_equation_exact"])

    def test_green_boundary_trace_sign(self):
        self.assertTrue(exact_exponential_volume_and_boundary_solution()[
            "Green_boundary_source_J_exact"])

    def test_exact_nonzero_boundary_reconstruction(self):
        r=exact_exponential_volume_and_boundary_solution()
        self.assertTrue(r["direct_boundary_equals_corrected_B_amplitude"])
        self.assertEqual(r["nonzero_boundary_data_yz"],"2")

    def test_exact_L2_energy_sample(self):
        r=exact_exponential_volume_and_boundary_solution()
        self.assertEqual(r["weighted_first_order_state_norm_squared"],"13/24")
        self.assertEqual(r["effective_source_L2_squared"],"9/4")
        self.assertTrue(r["estimate_holds_for_exact_specimen"])

    def test_sourced_corners_through_four(self):
        r=sourced_wave_positive_control()
        self.assertTrue(r["requested_corner_orders_passed"])
        self.assertEqual(len(r["levels"]),5)

    def test_source_conservation_for_constraint_preservation(self):
        r=sourced_wave_positive_control()
        self.assertTrue(r["source_divergence_free"])
        self.assertTrue(r["initial_C_zero"] and r["initial_dt_C_zero"])
        self.assertTrue(r["conditional_harmonic_constraint_preservation"])

    def test_bad_second_order_boundary_data_rejected(self):
        r=sourced_wave_positive_control(bad_second_order=True)
        self.assertTrue(r["levels"][0]["all_ten_corner_equations_passed"])
        self.assertTrue(r["levels"][1]["all_ten_corner_equations_passed"])
        self.assertFalse(r["levels"][2]["all_ten_corner_equations_passed"])
        self.assertIn("2",r["levels"][2]["six_metric_residuals"])

    def test_nonconserved_source_is_not_constraint_preserving(self):
        r=sourced_wave_positive_control(nonconserved=True)
        self.assertFalse(r["source_divergence_free"])
        self.assertFalse(r["conditional_harmonic_constraint_preservation"])

    def test_invalid_corner_order_fails_closed(self):
        with self.assertRaises(ValueError):
            check_sourced_harmonic_corners({},{},{},[],[],max_order=9)

    def test_nonzero_auxiliary_reduction_defect_sample(self):
        sample=nonzero_reduction_defect_solution()
        self.assertTrue(sample["first_order_equations_zero"])
        self.assertTrue(sample["reduction_defect_nonzero"])
        self.assertTrue(sample["effective_wave_source_zero"])
        self.assertTrue(sample["regular_source_bound_passes"])

    def test_replay_refuses_tampered_theorem(self):
        r=prove_regular_source_resolvent()
        self.assertTrue(replay_regular_source_resolvent(r))
        forged=copy.deepcopy(r)
        forged["strong_time_domain_wellposedness_proven"]=True
        self.assertFalse(replay_regular_source_resolvent(forged))

    def test_no_arbitrary_L2_strong_wellposedness_claim(self):
        r=prove_regular_source_resolvent()
        self.assertFalse(r[
            "arbitrary_L2_first_order_source_no_loss_theorem_proven"])
        self.assertFalse(r["strong_time_domain_wellposedness_proven"])
        self.assertFalse(r["nonlinear_Einstein_IBVP_proven"])


if __name__=="__main__":
    unittest.main()
