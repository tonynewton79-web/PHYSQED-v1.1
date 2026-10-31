"""Textbook coupled Einstein–Maxwell and adversarial standard physics tests."""
import sys
import unittest
from pathlib import Path
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12 import Geometry, ScopeError, certify
from v12.coupled import (maxwell_from_potential,maxwell_stress,
                         maxwell_bianchi,maxwell_equations,
                         covariant_divergence_stress,
                         einstein_maxwell_residual,check_einstein_maxwell)


def rn_fixture():
    t,r,th,ph = S.symbols("t r theta phi",real=True)
    M=S.Integer(1)
    Q=S.Rational(1,2)
    f=1-2*M/r+Q*Q/r**2
    chart=(t,r,th,ph)
    geometry=Geometry(chart,S.diag(-f,1/f,r*r,r*r*S.sin(th)**2))
    # A_t=Q/r yields F_tr=Q/r^2; stress does not depend on electric sign.
    field=maxwell_from_potential(chart,(Q/r,0,0,0))
    return geometry,field


class EinsteinMaxwellBenchmarks(unittest.TestCase):
    def test_reissner_nordstrom_full_coupled_system(self):
        geom,F=rn_fixture()
        self.assertEqual(S.simplify(F[0,1]-S.Rational(1,2)/geom.x[1]**2),0)
        result=check_einstein_maxwell(geom,F)
        self.assertTrue(all(result.values()),result)
        receipt=certify("STD-GR-EM-001","einstein",
                 [(einstein_maxwell_residual(geom,F),S.zeros(4)),
                  (maxwell_equations(geom,F),(0,0,0,0)),
                  (covariant_divergence_stress(geom,maxwell_stress(geom,F)),
                   (0,0,0,0))],
                 source="textbook Reissner-Nordstrom electrovacuum",
                 assumptions=("r outside the outer horizon",
                              "Levi-Civita chart",
                              "geometrized R-F^2 action normalization"))
        self.assertIn("PASSED",receipt["status"])
        self.assertFalse(receipt["physical_law_proven"])
        self.assertFalse(receipt["lean_kernel_verified"])

    def test_scaled_electric_field_breaks_einstein_equation(self):
        geom,F=rn_fixture()
        # Maxwell's equation remains satisfied by rescaling F; Einstein's
        # equation does not. This tests *cross*-domain coupling, not only YM.
        outcome=check_einstein_maxwell(geom,2*F)
        self.assertTrue(outcome["maxwell_equation"])
        self.assertTrue(outcome["maxwell_bianchi"])
        self.assertFalse(outcome["einstein_equation"])

    def test_corrupted_potential_does_not_meet_maxwell_equations(self):
        geom,F=rn_fixture()
        altered=maxwell_from_potential(geom.x,(geom.x[1]**2,0,0,0))
        self.assertTrue(all(v==0 for v in maxwell_bianchi(altered,geom.x)))
        self.assertFalse(all(S.simplify(v)==0 for v in maxwell_equations(geom,altered)))

    def test_algebraic_invalid_two_form_refused(self):
        geom,F=rn_fixture()
        F[0,0]=1
        with self.assertRaises(ScopeError):
            maxwell_stress(geom,F)

    def test_tracelessness_is_4d_specific(self):
        geom,F=rn_fixture()
        T=maxwell_stress(geom,F)
        self.assertEqual(S.simplify(S.trace(geom.g_inv*T)),0)
        self.assertEqual(S.simplify(geom.scalar),0)


if __name__=="__main__":
    unittest.main()
