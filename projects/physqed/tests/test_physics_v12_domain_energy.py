"""PHYSQED exact domain-wide polynomial energy-bound regressions."""
import sys
import unittest
from pathlib import Path
from fractions import Fraction as F
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.domain_energy import (bernstein_bounds,certify_domain_energy,
                              replay_domain_energy,DomainScopeError)


def specimen():
    t,x=S.symbols("t x")
    return (t,x),{t:(0,1),x:(0,1)},S.diag(1+t,2+t),[S.diag(1,2)],S.zeros(2)


class DomainEnergyTests(unittest.TestCase):
    def test_exact_multivariate_Bernstein_inclusion(self):
        t,x=S.symbols("t x")
        polynomial=S.expand((t-S.Rational(1,3))**2+(x-S.Rational(1,2))**2)
        bounds=bernstein_bounds(polynomial,{t:(0,1),x:(0,1)})
        for i in range(11):
            for j in range(11):
                actual=F(polynomial.subs({t:S.Rational(i,10),x:S.Rational(j,10)}))
                self.assertLessEqual(bounds["lower"],actual)
                self.assertGreaterEqual(bounds["upper"],actual)

    def test_zero_polynomial(self):
        t,x=S.symbols("t x")
        r=bernstein_bounds(0,{t:(0,1),x:(0,1)})
        self.assertEqual((r["lower"],r["upper"]),(0,0))

    def test_time_dependent_periodic_conditional(self):
        r=certify_domain_energy(*specimen(),coercivity=F(1,2),growth=2,
                                boundary="periodic_solution_assumed")
        self.assertEqual(r["status"],"PASS_INTERIOR_DOMAIN_BOUNDS__PDE_HYPOTHESES_PENDING")
        self.assertTrue(r["conditional_periodic_flux_applies"])
        self.assertTrue(r["growth_bound_proved"])
        self.assertTrue(r["coercivity_bound_proved"])
        self.assertFalse(r["underlying_smooth_solution_existence_proven"])
        self.assertFalse(r["boundary_flux_proven_from_input"])

    def test_spatial_variable_interior_bounds(self):
        t,x=S.symbols("t x")
        r=certify_domain_energy((t,x),{t:(0,1),x:("-1/2","1/2")},
                                S.diag(2+x,2-x),[S.zeros(2)],S.zeros(2),
                                coercivity=1,growth=0)
        self.assertTrue(r["coercivity_bound_proved"])
        self.assertTrue(r["growth_bound_proved"])
        self.assertFalse(r["conditional_periodic_flux_applies"])

    def test_offdiagonal_symmetric_matrix(self):
        t,x=S.symbols("t x")
        Sm=S.Matrix([[2+t,S.Rational(1,8)],[S.Rational(1,8),2+x]])
        r=certify_domain_energy((t,x),{t:(0,1),x:(0,1)},
                                Sm,[S.eye(2)],S.zeros(2),
                                coercivity=1,growth=2)
        self.assertTrue(r["growth_bound_proved"] and r["coercivity_bound_proved"])

    def test_insufficient_growth_is_inconclusive_not_refuted(self):
        r=certify_domain_energy(*specimen(),coercivity=F(1,2),growth=0)
        self.assertEqual(r["status"],"INCONCLUSIVE_SUFFICIENT_BOUND_NOT_ESTABLISHED")
        self.assertTrue(r["coercivity_bound_proved"])
        self.assertFalse(r["growth_bound_proved"])

    def test_insufficient_coercivity_is_inconclusive(self):
        r=certify_domain_energy(*specimen(),coercivity=3,growth=2)
        self.assertEqual(r["status"],"INCONCLUSIVE_SUFFICIENT_BOUND_NOT_ESTABLISHED")
        self.assertFalse(r["coercivity_bound_proved"])

    def test_nonsymmetrizable_matrix_refused(self):
        t,x=S.symbols("t x")
        with self.assertRaises(DomainScopeError):
            certify_domain_energy((t,x),{t:(0,1),x:(0,1)},S.eye(2),
                                  [S.Matrix([[0,1],[2,0]])],S.zeros(2),
                                  coercivity=1,growth=1)

    def test_nonpolynomial_input_refused(self):
        t,x=S.symbols("t x")
        with self.assertRaises(DomainScopeError):
            certify_domain_energy((t,x),{t:(0,1),x:(0,1)},
                                  S.diag(1+S.sin(t),1),[S.eye(2)],S.zeros(2),
                                  coercivity=1,growth=2)

    def test_float_input_refused(self):
        t,x=S.symbols("t x")
        with self.assertRaises(DomainScopeError):
            certify_domain_energy((t,x),{t:(0,1),x:(0,1)},
                                  S.diag(S.Float(1.0),1),[S.eye(2)],S.zeros(2),
                                  coercivity=1,growth=2)

    def test_inverted_box_refused(self):
        t,x=S.symbols("t x")
        with self.assertRaises(DomainScopeError):
            certify_domain_energy((t,x),{t:(1,0),x:(0,1)},
                                  S.eye(2),[S.eye(2)],S.zeros(2),
                                  coercivity=1,growth=2)

    def test_full_replay_detects_tampering(self):
        args=specimen()
        r=certify_domain_energy(*args,coercivity=1,growth=2)
        self.assertTrue(replay_domain_energy(*args,r,coercivity=1,growth=2))
        r["growth_bound_proved"]=False
        self.assertFalse(replay_domain_energy(*args,r,coercivity=1,growth=2))


if __name__=="__main__":
    unittest.main()
