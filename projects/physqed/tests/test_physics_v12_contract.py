"""PHYSQED typed coupled physics: isolated textbook and adversarial controls.

Run each test method in a fresh interpreter in CI. Combined large SymPy
expressions can retain large global caches and distort performance.
"""
import dataclasses
import sys
import unittest
from pathlib import Path
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.contracts import EinsteinMaxwellSpec,evaluate_contract
from v12.geometry import ScopeError


def rn():
    t,r,th,ph=S.symbols('t r th ph',real=True)
    f=1-2/r+S.Rational(1,4)/r**2
    witness={t:S.Integer(0),r:S.Integer(4),th:S.pi/2,ph:S.Integer(0)}
    return EinsteinMaxwellSpec('RN',(t,r,th,ph),
      S.diag(-f,1/f,r**2,r**2*S.sin(th)**2),
      (S.Rational(1,2)/r,0,0,0),S.sqrt(f),(witness,),
      ('r beyond outer horizon','0<theta<pi'),source='textbook RN')


def check(name,receipt):
    return next(x for x in receipt['nodes'] if x['name']==name)['passed']


class CoupledContractTests(unittest.TestCase):
    def test_valid_einstein_maxwell_full_linked_contract(self):
        receipt=evaluate_contract(rn())
        self.assertEqual(receipt['status'],'PASS_LOCAL_TYPED_COUPLED_SYMBOLIC_CONTRACT')
        self.assertEqual(len(receipt['nodes']),16)
        self.assertTrue(all(x['passed'] for x in receipt['nodes']))
        self.assertTrue(receipt['independent_oracle'][0]['four_dimensional']['passed'])
        self.assertTrue(receipt['independent_oracle'][0]['three_dimensional']['passed'])
        self.assertEqual(len(receipt['receipt_sha256']),64)
        self.assertFalse(receipt['physical_truth_proven'])
        self.assertFalse(receipt['global_solution_proven'])

    def test_wrong_coupling_fails_dynamics_but_not_geometry_bridge(self):
        receipt=evaluate_contract(dataclasses.replace(rn(),gravitational_coupling=3))
        self.assertEqual(receipt['status'],'REJECTED_INCONSISTENT_COUPLED_PHYSICS')
        self.assertFalse(check('einstein_field_equation',receipt))
        self.assertFalse(check('hamiltonian_constraint',receipt))
        self.assertTrue(check('hamiltonian_gauss_bridge',receipt))
        self.assertTrue(check('momentum_codazzi_bridge',receipt))

    def test_wrong_cosmological_constant(self):
        receipt=evaluate_contract(dataclasses.replace(rn(),cosmological_constant=1))
        self.assertFalse(check('einstein_field_equation',receipt))
        self.assertTrue(check('hamiltonian_gauss_bridge',receipt))

    def test_declared_inconsistent_stress(self):
        receipt=evaluate_contract(dataclasses.replace(rn(),declared_stress=S.zeros(4)))
        self.assertFalse(check('maxwell_stress_constitutive',receipt))
        self.assertFalse(check('einstein_field_equation',receipt))

    def test_nonclosed_declared_field_is_detected(self):
        t,x,y,z=S.symbols('t x y z',real=True)
        case=EinsteinMaxwellSpec('NONCLOSED',(t,x,y,z),S.diag(-1,1,1,1),
            (0,0,0,0),1,({t:0,x:0,y:0,z:0},),('Cartesian metric',))
        F=S.zeros(4);F[1,2]=t;F[2,1]=-t
        receipt=evaluate_contract(dataclasses.replace(case,declared_field_strength=F))
        self.assertFalse(check('field_potential_consistency',receipt))
        self.assertFalse(check('electromagnetic_bianchi',receipt))
        self.assertEqual(receipt['status'],'REJECTED_INCONSISTENT_COUPLED_PHYSICS')

    def test_wrong_claimed_constraints_refused(self):
        receipt=evaluate_contract(dataclasses.replace(rn(),declared_hamiltonian=1,
            declared_momentum=(0,1,0)))
        self.assertFalse(check('claimed_hamiltonian_agreement',receipt))
        self.assertFalse(check('claimed_momentum_agreement',receipt))
        self.assertTrue(check('hamiltonian_constraint',receipt))
        self.assertTrue(check('momentum_constraints',receipt))

    def test_wrong_lapse_raises_not_green(self):
        with self.assertRaises(ScopeError):
            evaluate_contract(dataclasses.replace(rn(),lapse=1))

    def test_wrong_signature_witness_refused(self):
        case=rn();t,r,th,ph=case.coordinates
        with self.assertRaises(ScopeError):
            evaluate_contract(dataclasses.replace(case,
                witnesses=({t:0,r:1,th:S.pi/2,ph:0},)))

    def test_offshell_codazzi_bridge_nontrivial(self):
        t,x,y,z=S.symbols('t x y z',real=True)
        a=1+t*x;b=1+t*x*x
        case=EinsteinMaxwellSpec('OFFSHELL',(t,x,y,z),S.diag(-1,a*a,b*b,1),
            (0,0,0,0),1,
            ({t:S.Rational(1,3),x:S.Rational(1,2),y:0,z:0},),
            ('near witness spatial metric positive',))
        result=evaluate_contract(case)
        self.assertFalse(check('einstein_field_equation',result))
        self.assertFalse(check('momentum_constraints',result))
        self.assertTrue(check('hamiltonian_gauss_bridge',result))
        self.assertTrue(check('momentum_codazzi_bridge',result))
        self.assertTrue(result['independent_oracle'][0]['four_dimensional']['passed'])
        self.assertTrue(result['independent_oracle'][0]['three_dimensional']['passed'])

    def test_matter_noether_bridge_offshell_maxwell(self):
        t,x,y,z=S.symbols('t x y z',real=True)
        case=EinsteinMaxwellSpec('OFFSHELL_MAXWELL',(t,x,y,z),
            S.diag(-1,1,1,1),(0,t*t,0,0),1,
            ({t:S.Rational(1,2),x:0,y:0,z:0},),('Cartesian chart',))
        result=evaluate_contract(case)
        self.assertFalse(check('maxwell_euler_lagrange',result))
        self.assertFalse(check('stress_conservation',result))
        self.assertTrue(check('matter_noether_divergence',result))
        self.assertTrue(check('einstein_stress_divergence_bridge',result))
        self.assertTrue(check('hamiltonian_gauss_bridge',result))
        self.assertTrue(check('momentum_codazzi_bridge',result))


if __name__=='__main__':
    unittest.main()
