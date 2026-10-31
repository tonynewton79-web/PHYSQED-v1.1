"""Independent refined glancing inverse, higher-order GH corner and curved control tests."""
from __future__ import annotations
import copy
import sys
import unittest
from pathlib import Path
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.gh_boundary_map import t,x,zero_metric
from v12.gh_glancing import (symbolic_glancing_obstruction,
    off_glancing_constant,glancing_trials,certify_glancing_gate,replay_glancing_gate)
from v12.gh_higher_corners import (
    certify_metric_corners,initial_jet_hierarchy,replay_metric_corners)
from v12.gh_curved_plane_wave import (
    verify_curved_gh_control,replay_curved_gh)


class GHUniformSectorTests(unittest.TestCase):
    def test_exact_obstructing_metric_amplitude(self):
        a=symbolic_glancing_obstruction()
        self.assertTrue(a["explicit_glancing_amplitude_verified"])
        self.assertTrue(a["uniform_unweighted_normalized_lopatinski_bound_refuted"])

    def test_glancing_sequence_converges_to_zero(self):
        a=glancing_trials()
        self.assertEqual(len(a),4)
        self.assertTrue(all(v["bound_satisfied"] and v["strictly_decaying"] for v in a))
        self.assertLess(a[-1]["normalized_residual_ratio"],a[0]["normalized_residual_ratio"])

    def test_offglancing_inverse_constant_is_finite(self):
        self.assertGreater(off_glancing_constant(0.25),0)
        self.assertLess(off_glancing_constant(0.5),off_glancing_constant(0.25))
        with self.assertRaises(ValueError):
            off_glancing_constant(0)

    def test_glancing_receipt_recomputed(self):
        r=certify_glancing_gate()
        self.assertEqual(r["status"],"PASS_EXACT_UNIFORM_BOUND_OBSTRUCTION")
        self.assertTrue(replay_glancing_gate(r))
        fake=copy.deepcopy(r)
        fake["algebra"]["uniform_unweighted_normalized_lopatinski_bound_proven"]=True
        self.assertFalse(replay_glancing_gate(fake))

    def test_high_order_positive_outgoing_wave(self):
        h=zero_metric()
        h["yz"]=S.exp(t+x)
        r=certify_metric_corners(h,max_order=6)
        self.assertTrue(r["all_temporal_orders_passed"])
        self.assertFalse(r["all_orders_infinite_hierarchy_proven"])

    def test_late_corner_failure_missed_by_lower_order(self):
        h=zero_metric()
        h["yz"]=(t-x)**4
        self.assertTrue(certify_metric_corners(h,2)["all_temporal_orders_passed"])
        r=certify_metric_corners(h,4)
        self.assertEqual(r["first_failure"]["sommerfeld"],3)
        self.assertEqual(r["six_Sommerfeld_corner_rows"][3]["residuals"][4],"48")
        self.assertFalse(r["all_temporal_orders_passed"])

    def test_initial_constraint_time_derivative_required(self):
        f=zero_metric()
        g=zero_metric()
        g["xx"]=x
        r=initial_jet_hierarchy(f,g,3)
        self.assertTrue(r["initial_C_zero"])
        self.assertFalse(r["initial_dt_C_zero"])

    def test_explicit_non_wave_source_refused(self):
        h=zero_metric()
        h["yz"]=t*t
        with self.assertRaises(ValueError):
            certify_metric_corners(h,4)

    def test_curved_background_Ricci_flat_but_nonzero_Riemann(self):
        r=verify_curved_gh_control()
        self.assertEqual(r["status"],"PASS_EXACT_CURVED_GH_BACKGROUND_AND_REDUCED_CONTROL")
        self.assertTrue(r["vacuum_Ricci_zero"])
        self.assertTrue(r["coordinates_harmonic_Gamma_contracted_zero"])
        self.assertEqual(r["nonzero_R_uxux"],"-1")
        self.assertEqual(r["nonzero_R_uyuy"],"1")

    def test_curved_reduced_wave_does_not_imply_full_einstein(self):
        r=verify_curved_gh_control()
        self.assertTrue(r["reduced_Ricci_flat_Lichnerowicz_wave_zero"])
        self.assertTrue(r["covariant_constraint_wave_zero"])
        self.assertEqual(r["harmonic_constraint_covector"],["2*u","0","0","0"])
        self.assertEqual(r["full_linearized_Einstein_nonzero_uu"],"2")
        self.assertFalse(r["full_linearized_Einstein_satisfied"])

    def test_curved_timelike_box_and_no_boundary_stability_claim(self):
        r=verify_curved_gh_control()
        self.assertTrue(r["timelike_box_margin_nonnegative_decomposition_verified"])
        self.assertTrue(r["boundary_x_constant_timelike"])
        self.assertFalse(r["curved_boundary_symbol_uniform_resolvent_proven"])
        self.assertFalse(r["nonlinear_Einstein_IBVP_proven"])

    def test_curved_receipt_replay_refuses_tampered_claim(self):
        r=verify_curved_gh_control()
        self.assertTrue(replay_curved_gh(r))
        forged=copy.deepcopy(r)
        forged["general_curved_GH_operator_intertwiner_verified"]=True
        self.assertFalse(replay_curved_gh(forged))


if __name__=="__main__":
    unittest.main()
