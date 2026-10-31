"""Linearized harmonic reduced Einstein boundary counterexample gates."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.harmonic_boundary_obstruction import (
    verify_harmonic_boundary_obstruction as verify,
    replay_harmonic_boundary_obstruction as replay)


class HarmonicBoundaryObstructionTests(unittest.TestCase):
    def test_wave_equations_satisfied(self):
        self.assertTrue(verify()["reduced_wave_equations_zero"])

    def test_homogeneous_dirichlet_boundary_satisfied(self):
        self.assertTrue(verify()["homogeneous_Dirichlet_metric_at_x0"])

    def test_nonzero_harmonic_constraint_at_same_boundary(self):
        r=verify()
        self.assertEqual(r["harmonic_constraints_at_x0"],["0","t","0","0"])
        self.assertTrue(r["nonzero_boundary_constraint"])

    def test_wave_propagation_of_constraints(self):
        self.assertTrue(verify()["constraint_wave_equations_zero"])

    def test_initial_constraint_velocity_qualification(self):
        r=verify()
        self.assertTrue(r["initial_constraint_field_zero"])
        self.assertFalse(r["initial_constraint_time_derivative_zero"])

    def test_false_physical_solution_claim_never_issued(self):
        r=verify()
        self.assertEqual(r["status"],"PASS_EXACT_BOUNDARY_TO_CONSTRAINT_OBSTRUCTION")
        self.assertFalse(r["full_linearized_Einstein_equations_verified"])

    def test_replay_refuses_tampered_claim(self):
        r=verify()
        self.assertTrue(replay(r))
        bad=copy.deepcopy(r)
        bad["nonlinear_Einstein_boundary_well_posedness_proven"]=True
        self.assertFalse(replay(bad))


if __name__=="__main__":
    unittest.main()
