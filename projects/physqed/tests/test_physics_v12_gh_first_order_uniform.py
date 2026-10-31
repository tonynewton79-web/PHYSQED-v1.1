"""Flat first-order GH incoming characteristics, stable modes and exact bound."""
import copy
import sys
import unittest
from pathlib import Path
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12 import gh_first_order_uniform as gh


class FirstOrderGHUniformTests(unittest.TestCase):
    def test_symmetric_hyperbolic_normal_principal_block(self):
        c=gh.first_order_characteristics()
        self.assertTrue(c["symmetric"])
        self.assertEqual(c["normal_matrix"].shape,(5,5))

    def test_first_order_characteristic_multiplicities(self):
        c=gh.first_order_characteristics()
        self.assertEqual(c["eigenvalues"],{S.Integer(-1):1,S.Integer(0):3,S.Integer(1):1})
        self.assertTrue(c["incoming_eigenvector_verified"])
        self.assertTrue(c["outgoing_eigenvector_verified"])

    def test_stable_subspace_has_ten_metric_amplitudes(self):
        m=gh.stable_mode_reduction()
        self.assertEqual(m["first_order_state_dimension"],50)
        self.assertEqual(m["decaying_stable_subspace_dimension"],10)

    def test_first_order_reduced_wave_symbol_on_shell(self):
        self.assertTrue(gh.stable_mode_reduction()["stable_mode_wave_dispersion_verified"])

    def test_first_order_auxiliary_reduction_constraints_zero(self):
        self.assertTrue(gh.stable_mode_reduction()["reduction_constraints_verified"])

    def test_null_adapted_boundary_determinant_exact(self):
        b=gh.adapted_normal_symbol()
        self.assertTrue(b["determinant_verified"])
        self.assertEqual(str(b["determinant"] ),"(k + s)**10")

    def test_old_boundary_glancing_factor_not_confused_with_new(self):
        from v12.gh_boundary_map import normal_mode_symbol
        old=normal_mode_symbol()
        self.assertTrue(old["factorization_verified"])
        self.assertEqual(str(old["determinant"]),"k**4*(k + s)**6")
        self.assertNotEqual(old["determinant"],gh.adapted_normal_symbol()["determinant"])

    def test_null_gauge_subspace_annihilated_by_six_free_rows(self):
        self.assertTrue(gh.adapted_normal_symbol()["complement_P_F_zero"])

    def test_six_complementary_rows_independent(self):
        b=gh.adapted_normal_symbol()
        self.assertTrue(b["complement_P_E_identity"])
        self.assertTrue(b["complement_decomposition_invertible"])

    def test_exact_four_constraint_gauge_block(self):
        self.assertTrue(gh.adapted_normal_symbol()["gauge_block_verified"])

    def test_exact_four_constraint_gauge_inverse(self):
        self.assertTrue(gh.adapted_normal_symbol()["gauge_block_explicit_inverse_verified"])

    def test_norm_constants_from_exact_gram_matrices(self):
        b=gh.adapted_normal_symbol()
        self.assertEqual(b["gauge_gram_eigenvalues"],{
            S.Integer(6):1,S.Integer(4):1,S.Integer(2):2})
        self.assertTrue(b["E_gram_identity"])

    def test_uniform_analytic_bound_all_right_half_plane_modes(self):
        result=gh.analytic_uniform_bound()
        self.assertTrue(result["coefficient_A_lt_9"])
        self.assertTrue(result["coefficient_B_lt_28"])
        self.assertTrue(result["uniform_homogeneous_stable_mode_trace_estimate_proven"])
        self.assertIn("1/60",result["uniform_weighted_stable_state_bound"])

    def test_glancing_sequence_normalized_singular_value_8(self):
        r=gh.glancing_diagnostic(8)
        self.assertTrue(r["above_analytic_amplitude_threshold"])

    def test_glancing_sequence_normalized_singular_value_128(self):
        r=gh.glancing_diagnostic(128)
        self.assertTrue(r["above_analytic_amplitude_threshold"])

    def test_invalid_complexity_type_and_scale_refused(self):
        for n in (0,1,1.5,"16",1000001):
            with self.subTest(n=n),self.assertRaises(ValueError):
                gh.glancing_diagnostic(n)

    def test_no_false_full_resolvent_or_einstein_claim(self):
        r=gh.certify_first_order_gh()
        self.assertEqual(r["status"],"PASS_ADAPTED_GH_UNIFORM_WEIGHTED_STABLE_MODE")
        self.assertFalse(r["full_forced_resolvent_estimate_proven"])
        self.assertFalse(r["nonlinear_or_curved_Einstein_boundary_theorem_proven"])
        self.assertFalse(r["analytic_bound"]["nonzero_shift_extension_proven"])
        self.assertFalse(r["analytic_bound"]["variable_coefficient_boundary_estimate_proven"])

    def test_receipt_replay_refuses_tampering(self):
        r=gh.certify_first_order_gh()
        self.assertTrue(gh.replay_first_order_gh(r))
        modified=copy.deepcopy(r)
        modified["full_forced_resolvent_estimate_proven"]=True
        self.assertFalse(gh.replay_first_order_gh(modified))


if __name__=="__main__":
    unittest.main()
