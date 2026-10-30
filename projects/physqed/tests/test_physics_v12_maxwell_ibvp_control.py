"""Shifted Maxwell differential-constraint and moving-wall boundary gates."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.maxwell_ibvp_control import (
    verify_maxwell_shifted_boundary as verify,
    replay_maxwell_shifted_boundary as replay)


class MaxwellShiftedIBVPTests(unittest.TestCase):
    def test_six_maximal_nonnegative_perfect_conductor_faces(self):
        r=verify("1/5")
        self.assertEqual(r["status"],"PASS_EXACT_SHIFTED_MAXWELL_BOUNDARY_ALGEBRA")
        self.assertEqual(len(r["boundary_faces"]),6)
        self.assertTrue(all(f["passed"] for f in r["boundary_faces"]))
        self.assertFalse(r["nonlinear_Einstein_boundary_to_constraint_map_proven"])

    def test_two_positive_two_negative_two_zero(self):
        r=verify("1/5")
        self.assertTrue(all(f["two_positive_two_negative_two_zero"]
            for f in r["boundary_faces"]))

    def test_perfect_conductor_exact_zero_outward_flux(self):
        r=verify("1/5")
        self.assertTrue(all(f["flux_zero"] for f in r["boundary_faces"]))

    def test_fixed_coordinate_walls_not_equal_moving_physical_walls(self):
        r=verify("1/5",boundary_velocity=0)
        self.assertFalse(r["all_six_maximal_nonnegative"])
        self.assertEqual(r["status"],"REJECTED_OR_INCONCLUSIVE_MAXWELL_BOUNDARY")

    def test_undercomplete_positive_flux_rejected(self):
        r=verify("1/5",undercomplete=True)
        self.assertFalse(r["all_six_maximal_nonnegative"])

    def test_zero_shift_limit(self):
        self.assertTrue(verify(0)["all_six_maximal_nonnegative"])

    def test_electric_and_magnetic_gauss_transport_identities(self):
        r=verify("1/5")
        self.assertTrue(r["electric_gauss_propagation_verified"])
        self.assertTrue(r["magnetic_gauss_propagation_verified"])

    def test_float_rejected(self):
        with self.assertRaises(ValueError):
            verify(0.2)

    def test_superluminal_control_shift_refused(self):
        with self.assertRaises(ValueError):
            verify("6/5")

    def test_replay_recomputes_and_rejects_tampering(self):
        r=verify("1/5")
        self.assertTrue(replay("1/5",r))
        altered=copy.deepcopy(r)
        altered["nonlinear_Einstein_boundary_to_constraint_map_proven"]=True
        self.assertFalse(replay("1/5",altered))


if __name__=="__main__":
    unittest.main()
