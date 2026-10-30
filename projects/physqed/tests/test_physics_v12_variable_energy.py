"""Variable-coefficient ADM energy identity and type/refusal tests."""
import sys
import unittest
from pathlib import Path
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.variable_energy import audit_matrix_energy,adm_constraint_matrices,ScopeError


class VariableEnergyTests(unittest.TestCase):
    def test_variable_transport(self):
        t,x=S.symbols("t x")
        r=audit_matrix_energy((t,x),[[2+x*x]],
                              [S.Matrix([[1+t+x]])],S.Matrix([[t]]))
        self.assertTrue(r["exact_local_balance_identity"])
        self.assertFalse(r["boundary_flux_control_proven"])

    def test_two_component_wave(self):
        t,x=S.symbols("t x")
        N=1+x*x
        Sm=S.diag(1,4)
        A=S.Matrix([[t,-2*N],[-N/2,t]])
        r=audit_matrix_energy((t,x),Sm,[A],S.diag(x,t))
        self.assertTrue(r["exact_local_balance_identity"])

    def test_wrong_symmetrizer_refused(self):
        t,x=S.symbols("t x")
        with self.assertRaises(ScopeError):
            audit_matrix_energy((t,x),S.eye(2),
                  [S.Matrix([[0,1],[2,0]])],S.zeros(2))

    def test_frozen_adm_reduces_to_constant_coefficients(self):
        t,x,y,z=S.symbols("t x y z")
        Sm,A,B=adm_constraint_matrices((t,x,y,z),
                                       S.eye(3),1,[S.Rational(1,3),0,0])
        self.assertEqual(B,S.zeros(4))
        r=audit_matrix_energy((t,x,y,z),Sm,A,B)
        self.assertTrue(r["exact_local_balance_identity"])

    def test_nonconstant_spatial_metric_and_shift(self):
        t,x,y,z=S.symbols("t x y z")
        a=1+t
        h=S.diag(a*a,1,1)
        beta=[x/a,0,0]
        Sm,A,B=adm_constraint_matrices((t,x,y,z),h,1,beta)
        self.assertEqual(S.simplify(B[1,1]+1/a),0)
        r=audit_matrix_energy((t,x,y,z),Sm,A,B)
        self.assertTrue(r["exact_local_balance_identity"])
        self.assertFalse(r["bounded_defect_proven"])
        self.assertFalse(r["global_coercivity_proven"])
        self.assertFalse(r["global_pde_uniqueness_proven"])


if __name__=="__main__":
    unittest.main()
