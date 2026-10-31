"""Exact timelike-foliated genuinely curved GH frozen principal control."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.gh_curved_timelike_frozen import (
    verify_ppwave_timelike_frozen, replay_ppwave_timelike_frozen)


class CurvedTimelikeFrozenTests(unittest.TestCase):
    def test_timelike_3plus1_metric_reconstruction(self):
        r=verify_ppwave_timelike_frozen()
        self.assertTrue(r["exact_tensor_algebra_tests"]["time_spatial_signature_reconstructs"])
        self.assertTrue(r["exact_tensor_algebra_tests"]["shift_cross_term_reconstructs"])

    def test_inverse_metric_and_lapse_exact(self):
        r=verify_ppwave_timelike_frozen()
        self.assertTrue(r["exact_tensor_algebra_tests"]["inverse_lapse_relation"])
        self.assertTrue(r["exact_tensor_algebra_tests"]["inverse_shift_relation"])

    def test_strict_positive_box_geometry(self):
        r=verify_ppwave_timelike_frozen()
        self.assertEqual(r["spatial_min_eigenvalue_at_least"],"7/8")
        self.assertEqual(r["lapse_squared_bounds"],["8/9","8/7"])

    def test_normal_wave_pair_speeds(self):
        r=verify_ppwave_timelike_frozen()
        self.assertTrue(r["normal_wave_pair_strict_signs_proved"])
        self.assertTrue(r["exact_tensor_algebra_tests"]["normal_speed_plus_exact_one"])
        self.assertTrue(r["exact_tensor_algebra_tests"]["normal_speed_minus_exact"])

    def test_advective_zero_crossing_blocks_global_boundary_claim(self):
        r=verify_ppwave_timelike_frozen()
        self.assertTrue(r["advective_normal_speed_changes_sign_at_H_zero"])
        self.assertFalse(r["globally_uniform_boundary_inertia_proven"])
        self.assertFalse(r["curved_boundary_resolvent_estimate_proven"])

    def test_replay_rejects_tampered_boundary_claim(self):
        r=verify_ppwave_timelike_frozen()
        self.assertTrue(replay_ppwave_timelike_frozen(r))
        fake=copy.deepcopy(r)
        fake["curved_Einstein_IBVP_theorem_proven"]=True
        self.assertFalse(replay_ppwave_timelike_frozen(fake))


if __name__=="__main__":
    unittest.main()
