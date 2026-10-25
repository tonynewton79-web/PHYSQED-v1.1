"""PHYSQED v0.2 model-mismatch/adversarial regression tests."""
import copy
import json
import sys
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from compiler import SCHEMA, ContractError, compile_contract, SI_UNITS, ROLE_UNITS
from engine import canonical, digest

class StatementCompilerTests(unittest.TestCase):
    def setUp(self):
        self.x=json.loads((HERE/'fixtures'/'oscillator_contract.json').read_text())

    def compile(self):
        return compile_contract(self.x)

    def refuses(self):
        with self.assertRaises((ContractError,KeyError,TypeError,ValueError)):
            self.compile()

    def test_oscillator_witness(self):
        r,lean=self.compile()
        self.assertEqual(r['status'],'DERIVATION_CHECKED__SEMANTIC_REVIEW_REQUIRED')
        self.assertTrue(r['proof_checks'][0]['passed'])
        self.assertFalse(r['physical_law_proven'])
        self.assertFalse(r['semantic_alignment_verified'])
        self.assertFalse(r['lean_kernel_verified'])
        self.assertTrue(r['lean_source_sha256'])
        self.assertIn('linear_combination',lean)

    def test_lean_source_repeatability(self):
        a,lean_a=self.compile()
        b,lean_b=self.compile()
        self.assertEqual(a,b)
        self.assertEqual(lean_a,lean_b)
        self.assertEqual(digest(lean_a.encode()),a['lean_source_sha256'])
        h=a.pop('report_sha256')
        self.assertEqual(digest(canonical(a)),h)

    def test_vetted_role_dimensions(self):
        self.assertEqual(ROLE_UNITS['velocity'],'m/s')
        self.assertEqual(SI_UNITS['N'],{'M':1,'L':1,'T':-2})
        self.x['symbols'][3]['unit']='m'
        self.refuses()

    def test_undeclared_role_refused(self):
        self.x['symbols'][3]['role']='magic_physics'
        self.refuses()

    def test_false_conclusion_requires_witness(self):
        self.x['proofs'][0]['multipliers']['force_balance']={'op':'mul','args':[{'const':'2'},{'var':'v'}]}
        r,lean=self.compile()
        self.assertEqual(r['status'],'REJECTED')
        self.assertFalse(r['proof_checks'][0]['passed'])
        self.assertIsNone(lean)

    def test_wrong_sign_rejected(self):
        t=self.x['conclusions'][0]['lhs']['args'][0]['args'][0]
        self.x['conclusions'][0]['lhs']['args'][0]['args'][0]={'op':'mul','args':[{'const':'-1'},t]}
        r,lean=self.compile()
        self.assertEqual(r['status'],'REJECTED')
        self.assertIsNone(lean)

    def test_missing_law_refused(self):
        self.x['assumptions']=[]
        self.refuses()

    def test_circular_derivation_refused(self):
        self.x['proofs'][0]['multipliers']={'work_rate_balance':{'const':'1'}}
        self.refuses()

    def test_assumption_repeated_as_conclusion_refused(self):
        self.x['conclusions'][0]['lhs']=self.x['assumptions'][0]['lhs']
        self.x['conclusions'][0]['rhs']=self.x['assumptions'][0]['rhs']
        self.refuses()

    def test_numeric_inconsistent_assumption_refused(self):
        self.x['assumptions'][0]['lhs']={'const':'0'}
        self.x['assumptions'][0]['rhs']={'const':'1'}
        self.refuses()

    def test_mismatched_formula_dimensions_refused(self):
        self.x['conclusions'][0]['lhs']={'var':'v'}
        self.refuses()

    def test_dimensionally_wrong_witness_refused(self):
        self.x['proofs'][0]['multipliers']['force_balance']={'var':'x'}
        self.refuses()

    def test_mapping_must_include_all_conclusions(self):
        self.x['mapping']['statement_conclusion_ids']=[]
        self.refuses()

    def test_mapping_unknown_target_refused(self):
        self.x['mapping']['statement_conclusion_ids']=['energy_hacked']
        self.refuses()

    def test_deleted_assumption_provenance_refused(self):
        self.x['assumptions'][0]['source']=''
        self.refuses()

    def test_blank_frame_refused(self):
        self.x['context']['frame']=''
        self.refuses()

    def test_missing_gauge_field_refused(self):
        del self.x['context']['gauge']
        self.refuses()

    def test_bad_extra_keys_refused(self):
        self.x['symbols'][0]['trusted']=True
        self.refuses()

    def test_unsupported_numeric_dsl_refused(self):
        self.x['conclusions'][0]['rhs']={'op':'sqrt','arg':{'var':'v'}}
        self.refuses()

    def test_witness_with_float_refused(self):
        self.x['proofs'][0]['multipliers']['force_balance']={'const':0.5}
        self.refuses()

    def test_invalid_contract_version_refused(self):
        self.x['contract_version']='future'
        self.refuses()

    def test_identifier_injection_refused(self):
        self.x['symbols'][0]['name']='x) : False := by sorry'
        self.refuses()

    def test_custom_axiom_injection_refused(self):
        self.x['assumptions'][0]['id']='axiom'
        self.refuses()

    def test_assumption_id_collision_refused(self):
        self.x['conclusions'][0]['id']='force_balance'
        self.refuses()

    def test_unconditional_polynomial_identity(self):
        a=self.x['symbols'][0]['name']
        self.x['assumptions']=[]
        self.x['conclusions']=[{
            'id':'difference_of_squares', 'meaning':'exact algebraic relation',
            'lhs':{'op':'add','args':[{'op':'pow','arg':{'var':a},'exp':2}, {'const':'0'}]},
            'rhs':{'op':'pow','arg':{'var':a},'exp':2}
        }]
        # The v0.2 checker deliberately does not coerce dimensionful zero inside
        # an addition; rewrite with a direct equality that matches units.
        self.x['conclusions'][0]['lhs']={'op':'mul','args':[{'const':'1'},{'var':a}]}
        self.x['conclusions'][0]['rhs']={'var':a}
        self.x['proofs']=[{'conclusion_id':'difference_of_squares', 'method':'polynomial_identity','multipliers':{}}]
        self.x['mapping']['statement_conclusion_ids']=['difference_of_squares']
        r,lean=self.compile()
        self.assertEqual(r['status'],'DERIVATION_CHECKED__SEMANTIC_REVIEW_REQUIRED')
        self.assertIn('ring',lean)

    def test_assumption_method_without_assumptions_refused(self):
        self.x['proofs'][0]['multipliers']={}
        self.refuses()

    def test_provenance_not_authentication(self):
        self.x['provenance']['origin_kind']='published'
        self.x['provenance']['source_uri']='https://example.org/unknown-paper'
        r,_=self.compile()
        self.assertFalse(r['physics_assumptions_established'])
        self.assertFalse(r['semantic_alignment_verified'])

    def test_empty_english_statement_refused(self):
        self.x['statement']='  '
        self.refuses()

    def test_true_formula_but_wrong_human_statement_never_certified(self):
        self.x['statement']='We have proved faster-than-light signalling experimentally.'
        r,_=self.compile()
        self.assertTrue(r['status'].endswith('SEMANTIC_REVIEW_REQUIRED'))
        self.assertFalse(r['physical_law_proven'])
        self.assertFalse(r['semantic_alignment_verified'])

if __name__=='__main__': unittest.main()
