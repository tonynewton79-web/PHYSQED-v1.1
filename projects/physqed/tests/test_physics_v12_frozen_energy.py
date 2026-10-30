"""Independent exact Fraction energy audit controls on a spatial three-torus."""
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.frozen_energy import (audit_frozen_adm,frozen_matrices,
                                characteristic_check,flux_check)


class FrozenEnergyTests(unittest.TestCase):
    def setUp(self):
        self.h=[[2,F(1,3),0],[F(1,3),3,0],[0,0,F(5,4)]]
        self.n=F(3,2)
        self.b=[F(1,5),-F(2,7),F(1,9)]

    def test_diagonal_flat(self):
        r=audit_frozen_adm([[1,0,0],[0,1,0],[0,0,1]],1,[0,0,0])
        self.assertEqual(r["status"],"PASS_FROZEN_PERIODIC_CONSTRAINT_ENERGY_ALGEBRA")
        self.assertTrue(r["all_three_principal_symbols_symmetrized"])

    def test_nondiagonal_metric_nonzero_shift(self):
        r=audit_frozen_adm(self.h,self.n,self.b)
        self.assertEqual(r["status"],"PASS_FROZEN_PERIODIC_CONSTRAINT_ENERGY_ALGEBRA")
        self.assertEqual(len(r["characteristic_trials"]),4)
        self.assertEqual(len(r["energy_flux_trials"]),2)
        self.assertTrue(all(v["pointwise_exact_energy_flux_identity"] for v in r["energy_flux_trials"]))
        self.assertFalse(r["general_variable_coefficient_energy_estimate_proven"])
        self.assertFalse(r["global_einstein_solution_proven"])

    def test_exact_oblique_characteristic(self):
        h,hi,N,b,S,A=frozen_matrices(self.h,self.n,self.b)
        self.assertTrue(characteristic_check(hi,N,b,A,[2,-3,1])["charpoly_verified"])

    def test_bad_spatial_signature_refused(self):
        with self.assertRaises(ValueError):
            audit_frozen_adm([[1,0,0],[0,-1,0],[0,0,1]],1,[0,0,0])

    def test_nonsymmetric_metric_refused(self):
        with self.assertRaises(ValueError):
            audit_frozen_adm([[1,1,0],[0,1,0],[0,0,1]],1,[0,0,0])

    def test_nonpositive_lapse_refused(self):
        with self.assertRaises(ValueError):
            audit_frozen_adm(self.h,0,self.b)

    def test_floating_input_refused(self):
        with self.assertRaises(ValueError):
            audit_frozen_adm(self.h,1.5,self.b)

    def test_zero_covector_refused(self):
        h,hi,N,b,S,A=frozen_matrices(self.h,self.n,self.b)
        with self.assertRaises(ValueError):
            characteristic_check(hi,N,b,A,[0,0,0])

    def test_wrong_flux_sign_not_equal(self):
        h,hi,N,b,S,A=frozen_matrices(self.h,self.n,self.b)
        receipt=flux_check(hi,N,b,2,[1,2,3],[1,0,-2],
                           [[1,2,3],[2,3,1],[-1,2,0]])
        self.assertTrue(receipt["pointwise_exact_energy_flux_identity"])
        self.assertNotEqual(F(receipt["energy_time_derivative"]),
                            -F(receipt["transport_plus_flux_divergence"]))


if __name__=="__main__":
    unittest.main()
