"""Adversarial exact conditional proof/units/controlled-text regression."""
import copy,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from conditional_claims import verify,ConditionalRefusal
from benchmarks.conditional_v08 import specimen,run,expr

class ConditionalClaimTests(unittest.TestCase):
    def setUp(self):self.a=specimen(0);self.b=specimen(1)
    def refused(self,x):
        with self.assertRaises(ConditionalRefusal):verify(x)
    def test_exact_damped_balance_and_scope(self):
        for x in (self.a,self.b):
            r=verify(x)
            self.assertTrue(r['exact_single_premise_witness_verified'])
            for field in ('physical_law_proven','lean_kernel_verified','experimental_evidence_verified'):
                self.assertFalse(r[field])
    def test_hidden_physical_interpretation_refused(self):
        x=copy.deepcopy(self.a);x['statement']+=' Hence Einstein equations hold.';self.refused(x)
    def test_text_truth_not_enough_if_formal_perturbed(self):
        x=copy.deepcopy(self.b);x['conclusion']['rhs']=expr('x**2');self.refused(x)
    def test_true_consequent_no_valid_witness_refused(self):
        x=copy.deepcopy(self.b);x['witness']={'const':'0'};self.refused(x)
    def test_overloaded_new_variable_refused(self):
        x=copy.deepcopy(self.b);x['variables']=['x','x','z'];self.refused(x)
    def test_false_numeric_premise_refused(self):
        x=copy.deepcopy(self.b);x['premise']={'lhs':{'const':'1'},'rhs':{'const':'0'}}
        # To ensure we're testing false-premise detection and not a text mismatch,
        # also alter the controlled text to the corresponding constant premise.
        x['statement']=x['statement'].replace('if x+y == z,','if 1 == 0,')
        self.refused(x)
    def test_bad_primitive_types_refused(self):
        for bad in (None,2,[],[{}],['x','x'],['x',[]]):
            x=copy.deepcopy(self.b);x['variables']=bad;self.refused(x)
    def test_false_units_refused(self):
        x=copy.deepcopy(self.a);x['dimensions']['c']={'T':1};self.refused(x)
    def test_untrusted_provenance_refused(self):
        x=copy.deepcopy(self.a);x['provenance']='experimental_certified';self.refused(x)
    def test_code_injection_refused(self):
        x=copy.deepcopy(self.a);x['statement']=x['statement'].replace('m*a','__import__("os").system("true")');self.refused(x)
    def test_quantifier_refused(self):
        x=copy.deepcopy(self.b);x['statement']=x['statement'].replace('For all','There exist',1);self.refused(x)
    def test_huge_polynomial_witness_budget_refused_consistently(self):
        x=copy.deepcopy(self.b)
        huge={'const':'9'*95}
        x['witness']={'op':'mul','args':[huge]*12}
        self.refused(x)
    def test_benchmark_score(self):
        r=run();self.assertEqual((r['cases'],r['correct']),(560,560))

if __name__=='__main__':unittest.main()
