"""Rational ADM energy sign, matrix, refinement, original-pole regression tests."""
import sys
import unittest
from pathlib import Path
import sympy as sp
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.rational_energy import (certify_rational_domain_energy,
                                 replay_rational_domain_energy,DomainScopeError)
from v12.variable_energy import adm_constraint_matrices


def controls():
    t,x=sp.symbols('t x')
    return (t,x),{t:(0,1),x:(0,1)},sp.diag(1+1/(1+t),2),[sp.diag(1,2)],sp.zeros(2)


class RationalDomainTests(unittest.TestCase):
    def test_rational_positive(self):
        z=certify_rational_domain_energy(*controls(),coercivity=1,growth=2)
        self.assertEqual(z['status'],'PASS_RATIONAL_INTERIOR_BOUNDS__PDE_HYPOTHESES_PENDING')
        self.assertEqual(z['verified_cells'],1)
        self.assertFalse(z['global_Einstein_Cauchy_theorem_proven'])

    def test_strict_negative_denominator(self):
        t,x=sp.symbols('t x')
        z=certify_rational_domain_energy((t,x),{t:(0,1),x:(0,1)},
            sp.diag(1+1/(-2-t),2),[sp.diag(1,2)],sp.zeros(2),
            coercivity=F(1,3),growth=2)
        self.assertTrue(z['interior_coercivity_proven'])

    def test_true_pole_no_certificate(self):
        t,x=sp.symbols('t x')
        z=certify_rational_domain_energy((t,x),{t:(0,1),x:(0,1)},
            sp.diag(1/(t-sp.Rational(1,2)),2),[sp.diag(1,2)],sp.zeros(2),
            coercivity=1,growth=2)
        self.assertEqual(z['status'],'INCONCLUSIVE_RATIONAL_DOMAIN_BOUNDS')

    def test_subdivision_recovers_positive_denominator(self):
        t,x=sp.symbols('t x')
        q=t*t-t+sp.Rational(3,10)
        args=((t,x),{t:(0,1),x:(0,1)},sp.diag(1+1/q,2),
              [sp.zeros(2)],sp.zeros(2))
        no=certify_rational_domain_energy(*args,coercivity=1,growth=100,max_depth=0)
        yes=certify_rational_domain_energy(*args,coercivity=1,growth=100,max_depth=1)
        self.assertEqual(no['status'],'INCONCLUSIVE_RATIONAL_DOMAIN_BOUNDS')
        self.assertTrue(yes['interior_coercivity_proven'])
        self.assertEqual(yes['verified_cells'],2)

    def test_guard_for_cancelled_pole(self):
        t,x=sp.symbols('t x')
        args=((t,x),{t:(0,1),x:(0,1)},sp.eye(2),
              [sp.eye(2)],sp.zeros(2))
        z=certify_rational_domain_energy(*args,coercivity=1,growth=0,
                  denominator_guards=[t-sp.Rational(1,2)])
        self.assertFalse(z['interior_growth_proven'])

    def test_positive_source_guard(self):
        t,x=sp.symbols('t x')
        args=((t,x),{t:(0,1),x:(0,1)},sp.eye(2),[sp.eye(2)],sp.zeros(2))
        z=certify_rational_domain_energy(*args,coercivity=1,growth=0,
                  denominator_guards=[t+2])
        self.assertTrue(z['interior_growth_proven'])

    def test_bad_float(self):
        t,x=sp.symbols('t x')
        with self.assertRaises(DomainScopeError):
            certify_rational_domain_energy((t,x),{t:(0,1),x:(0,1)},
                sp.diag(sp.Float(1.5),1),[sp.eye(2)],sp.zeros(2),
                coercivity=1,growth=1)

    def test_wrong_symmetry(self):
        t,x=sp.symbols('t x')
        with self.assertRaises(DomainScopeError):
            certify_rational_domain_energy((t,x),{t:(0,1),x:(0,1)},
                sp.eye(2),[sp.Matrix([[0,1],[2,0]])],sp.zeros(2),
                coercivity=1,growth=1)

    def test_tampered_receipt(self):
        args=controls()
        z=certify_rational_domain_energy(*args,coercivity=1,growth=2)
        self.assertTrue(replay_rational_domain_energy(*args,z,coercivity=1,growth=2))
        z['cells'][0]['coercivity']['rows'][0]['passed']=False
        self.assertFalse(replay_rational_domain_energy(*args,z,coercivity=1,growth=2))

    def test_bad_nonlinear_expression(self):
        t,x=sp.symbols('t x')
        with self.assertRaises(DomainScopeError):
            certify_rational_domain_energy((t,x),{t:(0,1),x:(0,1)},
                sp.diag(sp.sin(t)+1,1),[sp.eye(2)],sp.zeros(2),
                coercivity=1,growth=1)

    def test_insufficient_growth_is_inconclusive(self):
        t,x=sp.symbols('t x')
        z=certify_rational_domain_energy((t,x),{t:(0,1),x:(0,1)},
            sp.eye(2),[sp.eye(2)],-sp.eye(2),coercivity=1,growth=0)
        self.assertEqual(z['status'],'INCONCLUSIVE_RATIONAL_DOMAIN_BOUNDS')

    def test_parameter_in_denominator_refused(self):
        t,x,a=sp.symbols('t x a')
        with self.assertRaises(DomainScopeError):
            certify_rational_domain_energy((t,x),{t:(0,1),x:(0,1)},
                sp.diag(1/(t+a),1),[sp.eye(2)],sp.zeros(2),
                coercivity=1,growth=1)

    def test_input_coefficient_pole_not_hidden_by_energy_cancellation(self):
        t,x=sp.symbols('t x')
        args=((t,x),{t:(0,1),x:(0,1)},sp.eye(2),
              [sp.diag(1/(t-sp.Rational(1,2)),1)],sp.zeros(2))
        # Since A depends on time, not x, div(S A) hides the pole
        # unless the received coefficient domains are audited directly.
        z=certify_rational_domain_energy(*args,coercivity=1,growth=0)
        self.assertFalse(z['all_received_coefficient_denominators_certified'])
        self.assertEqual(z['status'],'INCONCLUSIVE_RATIONAL_DOMAIN_BOUNDS')

    def test_true_shifted_adm_inverse_metric_and_lapse(self):
        t,x,y,z=sp.symbols('t x y z')
        h=sp.diag(1+t,1,1)
        lapse=1+t
        beta=[sp.Rational(1,5),0,0]
        Sm,A,B=adm_constraint_matrices((t,x,y,z),h,lapse,beta)
        result=certify_rational_domain_energy((t,x,y,z),
             {t:(0,1),x:(0,1),y:(0,1),z:(0,1)},Sm,A,B,
             coercivity=1,growth=12,denominator_guards=[1+t],
             original_expression_denominators_complete=True,
             boundary='periodic_solution_assumed')
        self.assertTrue(result['interior_coercivity_proven'])
        self.assertTrue(result['interior_growth_proven'])
        self.assertTrue(result['all_received_coefficient_denominators_certified'])
        self.assertTrue(result['all_required_original_denominator_guards_certified'])
        self.assertFalse(result['smooth_solution_exists_proven'])


if __name__=='__main__':
    unittest.main()
