import copy
import unittest
import sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
from controlled_semantics import verify_controlled_claim,ControlledLanguageRefusal
from benchmarks.controlled_semantics_v07 import examples,run

class ControlledSemanticsTests(unittest.TestCase):
    def setUp(self):self.valid=examples()[0][1]
    def test_positive(self):
        z=verify_controlled_claim(self.valid)
        self.assertTrue(z['controlled_statement_alignment_verified'])
        self.assertFalse(z['unrestricted_semantic_correctness_verified'])
        self.assertFalse(z['physical_law_proven'])
    def test_wrong_math(self):
        with self.assertRaises(ControlledLanguageRefusal):verify_controlled_claim(examples()[1][1])
    def test_unrelated_true_identity(self):
        with self.assertRaises(ControlledLanguageRefusal):verify_controlled_claim(examples()[2][1])
    def test_physics_overclaim(self):
        with self.assertRaises(ControlledLanguageRefusal):verify_controlled_claim(examples()[3][1])
    def test_quantifier_change(self):
        with self.assertRaises(ControlledLanguageRefusal):verify_controlled_claim(examples()[4][1])
    def test_implicit_assumption(self):
        q=copy.deepcopy(self.valid);q['assumptions']=['extra assumption']
        with self.assertRaises(ControlledLanguageRefusal):verify_controlled_claim(q)
    def test_invalid_spec_kind(self):
        q=copy.deepcopy(self.valid);q['checks'][0]['kind']='dimension_equality'
        with self.assertRaises(ControlledLanguageRefusal):verify_controlled_claim(q)
    def test_python_call_injection(self):
        q=copy.deepcopy(self.valid);q['statement']=q['statement'].replace('x+y','__import__("os").system("true")')
        with self.assertRaises(ControlledLanguageRefusal):verify_controlled_claim(q)
    def test_extra_equality(self):
        q=copy.deepcopy(self.valid);q['statement']=q['statement'].replace(' == ',' == x == ')
        with self.assertRaises(ControlledLanguageRefusal):verify_controlled_claim(q)
    def test_swap_equality_sides(self):
        q=copy.deepcopy(self.valid)
        q['statement']=q['statement'].replace(' == ',' == x + ')
        with self.assertRaises(ControlledLanguageRefusal):verify_controlled_claim(q)
    def test_zero_division(self):
        q=copy.deepcopy(self.valid);q['statement']=q['statement'].replace('x+y','x/0+y')
        with self.assertRaises(ControlledLanguageRefusal):verify_controlled_claim(q)
    def test_unhashable_variable_declaration_fails_closed(self):
        for invalid in ([{'k':'x'}], [['x']], [None], [1]):
            q=copy.deepcopy(self.valid);q['checks'][0]['variables']=invalid
            with self.assertRaises(ControlledLanguageRefusal):verify_controlled_claim(q)

    def test_250_case_result(self):
        z=run();self.assertEqual(z['claims'],250)
        self.assertEqual(z['correct_classifications'],250)
        self.assertEqual(z['false_acceptances'],0)
        self.assertEqual(z['false_refusals'],0)

if __name__=='__main__':unittest.main()
