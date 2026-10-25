"""Bounded multi-premise verifier regression and nonlinear/essentiality controls."""
import copy
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from multi_premise_v10 import verify,MultiPremiseRefusal
from benchmarks.multi_premise_v10 import specimen,run

class MultiPremiseVersion10Tests(unittest.TestCase):
    def test_three_premise_dimensionless(self):
        r=verify(specimen(0))
        self.assertEqual((r['premise_count'],r['affine_gradient_rank']),(3,3))
        self.assertTrue(r['all_premises_essential_to_conclusion'])
    def test_four_premise_dimensionless(self):
        r=verify(specimen(1));self.assertEqual(r['affine_gradient_rank'],4)
    def test_three_premise_physical_dimensions(self):
        r=verify(specimen(2));self.assertTrue(r['declared_dimensions_consistent'])
    def test_four_premise_physical_dimensions(self):
        r=verify(specimen(3))
        self.assertEqual(r['premise_count'],4)
        self.assertFalse(r['physical_law_proven'])
        self.assertFalse(r['lean_kernel_verified'])
    def test_modified_witness_fails(self):
        c=specimen(3);c['witnesses'][1]={'const':'0'}
        with self.assertRaises(MultiPremiseRefusal):verify(c)
    def test_false_physical_wording_fails(self):
        c=specimen(0);c['statement']+=' Therefore gravity is false.'
        with self.assertRaises(MultiPremiseRefusal):verify(c)
    def test_dimensional_corruption_fails(self):
        c=specimen(3);c['dimensions']['m']={'T':1}
        with self.assertRaises(MultiPremiseRefusal):verify(c)
    def test_full_rank_is_not_conclusion_essentiality(self):
        c=specimen(0)
        c['conclusion']={'lhs':{'var':'x0'},'rhs':{'var':'y0'}}
        c['witnesses']=[{'const':'1'},{'const':'0'},{'const':'0'}]
        c['statement']=c['statement'].split(', then ')[0]+', then x0 == y0 holds.'+__import__('two_premise_claims').TAIL
        with self.assertRaisesRegex(MultiPremiseRefusal,'not essential'):verify(c)
        self.assertEqual(verify(c,require_essential=False)['affine_gradient_rank'],3)
    def test_dependent_affine_gradients_refused(self):
        c=specimen(0)
        c['premises'][1]=copy.deepcopy(c['premises'][0])
        c['statement']=c['statement'].replace('x1 == y1','x0 == y0',1)
        with self.assertRaisesRegex(MultiPremiseRefusal,'dependent'):verify(c)
    def test_nonlinear_premise_refused(self):
        c=specimen(0)
        c['premises'][0]={'lhs':{'op':'pow','arg':{'var':'x0'},'exp':2},'rhs':{'var':'y0'}}
        c['statement']=c['statement'].replace('x0 == y0','x0**2 == y0',1)
        with self.assertRaisesRegex(MultiPremiseRefusal,'nonlinear'):verify(c)
    def test_incorrect_number_of_assumptions(self):
        c=specimen(1)
        c['premises'].append(copy.deepcopy(c['premises'][-1]))
        with self.assertRaises(MultiPremiseRefusal):verify(c)
    def test_synthetic_challenge_classifications(self):
        r=run()
        self.assertEqual((r['total'],r['correct'],r['positives']), (880,880,80))
        self.assertEqual((r['false_accepts'],r['false_refusals']), (0,0))

if __name__=='__main__':unittest.main()
