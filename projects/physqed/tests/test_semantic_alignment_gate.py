"""Test-only reviewer anchoring: never assert unrestricted NLP comprehension."""
import copy
import json
import sys
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from semantic_alignment_gate import issue_reference, verify_alignment, SemanticGateRefusal
TEST_KEY=bytes(range(32))

class SemanticAlignmentGateTests(unittest.TestCase):
    def setUp(self):
        self.claim=json.loads((HERE/'fixtures/kinetic_identity.json').read_text())
        self.reference=issue_reference(self.claim,TEST_KEY,'SYNTHETIC_TEST_KEY')

    def test_signed_exact_claim_matches_without_physics_credit(self):
        r=verify_alignment(self.claim,self.reference,TEST_KEY)
        self.assertTrue(r['binding_to_reviewed_statement'])
        for k in ('physical_law_proven','lean_kernel_verified',
                  'semantic_correctness_verified','reviewer_identity_authenticated'):
            self.assertIs(r[k],False)

    def test_false_english_remapping_refused(self):
        bad=copy.deepcopy(self.claim)
        bad['statement']='I have proved every quantum field equation.'
        with self.assertRaisesRegex(SemanticGateRefusal,'UNREVIEWED_NATURAL_LANGUAGE'):
            verify_alignment(bad,self.reference,TEST_KEY)

    def test_true_math_replaced_with_unreviewed_math_refused(self):
        bad=copy.deepcopy(self.claim)
        bad['checks'][0]['lhs']={'const':'0'}
        with self.assertRaisesRegex(SemanticGateRefusal,'UNREVIEWED_FORMAL'):
            verify_alignment(bad,self.reference,TEST_KEY)

    def test_changed_assumptions_refused(self):
        bad=copy.deepcopy(self.claim)
        bad['assumptions']=['all assumptions waived']
        with self.assertRaisesRegex(SemanticGateRefusal,'UNREVIEWED_FORMAL'):
            verify_alignment(bad,self.reference,TEST_KEY)

    def test_fake_key_refused(self):
        with self.assertRaises(SemanticGateRefusal):
            verify_alignment(self.claim,self.reference,b'x'*32)

    def test_edited_scope_refused(self):
        altered=copy.deepcopy(self.reference)
        altered['payload']['reviewed_scope']='PHYSICS_CERTIFIED'
        with self.assertRaises(SemanticGateRefusal):
            verify_alignment(self.claim,altered,TEST_KEY)

    def test_approval_for_physics_is_forbidden(self):
        with self.assertRaises(SemanticGateRefusal):
            issue_reference(self.claim,TEST_KEY,'TEST',reviewed_scope='PHYSICAL_LAW_PROVEN')

    def test_malicious_self_approval_is_not_semantic_truth(self):
        bad=copy.deepcopy(self.claim)
        bad['statement']='An algebraic identity proves that the Moon is made of antimatter.'
        self_review=issue_reference(bad,TEST_KEY,'UNTRUSTED_SELF_REVIEW')
        r=verify_alignment(bad,self_review,TEST_KEY)
        self.assertTrue(r['binding_to_reviewed_statement'])
        self.assertFalse(r['semantic_correctness_verified'])
        self.assertFalse(r['physical_law_proven'])

if __name__=='__main__':unittest.main()
