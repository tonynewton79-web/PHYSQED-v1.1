"""PHYSQED v0.9 two-premise witness adversarial tests."""
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from two_premise_claims import verify, MultiPremiseRefusal
from benchmarks.two_premise_v09 import expr,specimen,run

class TwoPremiseClaims(unittest.TestCase):
    def setUp(self):
        self.a=specimen(0)
        self.p=specimen(1)

    def denied(self, c, reason=None):
        if reason:
            with self.assertRaisesRegex(MultiPremiseRefusal,reason):verify(c)
        else:
            with self.assertRaises(MultiPremiseRefusal):verify(c)

    def test_genuine_two_premise_certificate(self):
        r=verify(self.a)
        self.assertEqual(r['affine_gradient_rank'],2)
        self.assertTrue(r['exact_ideal_membership_identity'])
        self.assertFalse(r['physical_law_proven'])
        self.assertFalse(r['lean_kernel_verified'])

    def test_dimensionful_kinematic_identity(self):
        r=verify(self.p)
        self.assertTrue(r['declared_dimensions_consistent'])
        self.assertFalse(r['unrestricted_semantic_correctness'])

    def test_witness_one_wrong(self):
        c=copy.deepcopy(self.a);c['witnesses'][0]=expr('0');self.denied(c,'invalid two-premise')

    def test_witness_two_wrong(self):
        c=copy.deepcopy(self.a);c['witnesses'][1]=expr('0');self.denied(c,'invalid two-premise')

    def test_tautological_and_duplicate_second_premise_refused(self):
        c=copy.deepcopy(self.a);c['premises'][1]=c['premises'][0]
        self.denied(c,'dependent affine normals|SIDE MISMATCH')

    def test_affine_dependent_even_if_exact_membership_identity(self):
        c=copy.deepcopy(self.a)
        c['premises'][1]={'lhs':expr('2*(x+y)'), 'rhs':expr('2*z')}
        c['conclusion']={'lhs':expr('x+y'), 'rhs':expr('z')}
        c['witnesses']=[expr('1'),expr('0')]
        c['statement']=('For all real scalars x, y, z, w, if x+y == z and '
                        '2*(x+y) == 2*z, then x+y == z holds.'
                        ' This checks only a conditional polynomial consequence; no physical law is established.')
        self.denied(c,'dependent affine normals')

    def test_disallowed_nonlinear_premise_even_if_certificate(self):
        c=copy.deepcopy(self.a)
        c['premises'][0]={'lhs':expr('x**2'), 'rhs':expr('y')}
        c['statement']=c['statement'].replace('if x+y == z and','if x**2 == y and')
        self.denied(c,'independence not established')

    def test_wrong_english_formal_alignment(self):
        c=copy.deepcopy(self.a)
        c['statement']=c['statement'].replace('x+y == z','x+z == z')
        self.denied(c,'SIDE MISMATCH')

    def test_units_refused(self):
        c=copy.deepcopy(self.p);c['dimensions']['v']={'T':1}
        self.denied(c)

    def test_quantifier_refused(self):
        c=copy.deepcopy(self.a);c['statement']=c['statement'].replace('For all','There exist',1)
        self.denied(c,'uncontrolled')

    def test_physics_overclaim_refused(self):
        c=copy.deepcopy(self.a);c['statement']+=' Therefore all black holes are singular.'
        self.denied(c,'uncontrolled')

    def test_code_payload_refused(self):
        c=copy.deepcopy(self.a)
        c['statement']=c['statement'].replace('x+y','__import__("os").system("echo x")',1)
        self.denied(c)

    def test_false_provenance_refused(self):
        c=copy.deepcopy(self.a);c['provenance']='EXPERIMENT_CONFIRMED';self.denied(c)

    def test_missing_assumption_refused(self):
        c=copy.deepcopy(self.a);c['premises']=c['premises'][:1];self.denied(c)

    def test_extra_assumption_refused(self):
        c=copy.deepcopy(self.a);c['premises'].append(copy.deepcopy(c['premises'][1]));self.denied(c)

    def test_wrong_witness_dimension_refused(self):
        c=copy.deepcopy(self.p);c['witnesses'][0]=expr('1')
        self.denied(c)

    def test_synthetic_540(self):
        r=run();self.assertEqual((r['correct'],r['total']), (540,540))

if __name__=='__main__':unittest.main()
