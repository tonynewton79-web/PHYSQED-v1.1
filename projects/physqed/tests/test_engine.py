import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import engine
from replay import ReplayError, verify_identity

class PhysQedTests(unittest.TestCase):
    def load(self, name):
        return json.loads((HERE/'fixtures'/name).read_text())

    def test_exact_algebra_pass(self):
        c = engine.certify(self.load('kinetic_identity.json'))
        self.assertEqual(c['status'], 'MATHEMATICAL_COMPONENTS_VERIFIED')
        self.assertTrue(c['checks'][0]['independent_replay']['verified'])
        self.assertFalse(c['physical_law_proven'])
        self.assertFalse(c['lean_kernel_verified'])

    def test_dimension_pass_but_no_physics_claim(self):
        c = engine.certify(self.load('newton_dimension.json'))
        self.assertEqual(c['status'], 'CONSISTENCY_CHECKS_PASSED')
        self.assertFalse(c['physical_law_proven'])

    def test_wrong_dimension_refused(self):
        self.assertEqual(engine.certify(self.load('wrong_dimension.json'))['status'], 'REJECTED')

    def test_wrong_identity_refused_with_witness(self):
        c=engine.certify(self.load('wrong_identity.json'))
        self.assertEqual(c['status'], 'REJECTED')
        self.assertIn('counterexample',c['checks'][0]['independent_replay'])

    def test_certificate_is_deterministic_and_self_hashing(self):
        x=engine.certify(self.load('kinetic_identity.json'))
        self.assertEqual(x, engine.certify(self.load('kinetic_identity.json')))
        copy=deepcopy(x)
        h=copy.pop('certificate_sha256')
        self.assertEqual(h,engine.digest(engine.canonical(copy)))

    def test_unknown_check_kind_refused(self):
        x=self.load('kinetic_identity.json');x['checks'][0]['kind']='AI_says_true'
        self.assertEqual(engine.certify(x)['status'],'REJECTED')

    def test_float_refused(self):
        x=self.load('kinetic_identity.json');x['checks'][0]['rhs']={'const':0.1}
        self.assertEqual(engine.certify(x)['status'],'REJECTED')

    def test_variable_without_dimension_refused(self):
        x=self.load('newton_dimension.json');del x['checks'][0]['variables']['m']
        self.assertEqual(engine.certify(x)['status'],'REJECTED')

    def test_incompatible_addition_refused(self):
        x=self.load('newton_dimension.json')
        x['checks'][0]['rhs']={'op':'add','args':[{'var':'m'},{'var':'a'}]}
        self.assertEqual(engine.certify(x)['status'],'REJECTED')

    def test_no_checks_refused(self):
        x=self.load('kinetic_identity.json');x['checks']=[]
        with self.assertRaises(engine.CertificationError): engine.certify(x)

    def test_unknown_schema_refused(self):
        x=self.load('kinetic_identity.json');x['schema_version']='future-1'
        with self.assertRaises(engine.CertificationError): engine.certify(x)

    def test_missing_provenance_refused(self):
        x=self.load('kinetic_identity.json');x['source']=''
        with self.assertRaises(engine.CertificationError): engine.certify(x)

    def test_independent_grid_handles_counterexample(self):
        x=self.load('wrong_identity.json')['checks'][0]
        self.assertFalse(verify_identity(x['lhs'],x['rhs'],x['variables'])['verified'])

    def test_unknown_operator_refused(self):
        x=self.load('kinetic_identity.json');x['checks'][0]['lhs']={'op':'eval','args':[]}
        self.assertEqual(engine.certify(x)['status'],'REJECTED')

    def test_exponent_budget_refused(self):
        x=self.load('kinetic_identity.json');x['checks'][0]['lhs']={'op':'pow','arg':{'var':'u'},'exp':1000}
        self.assertEqual(engine.certify(x)['status'],'REJECTED')

    def test_rational_normalization(self):
        x=self.load('kinetic_identity.json')
        s=x['checks'][0]
        s['lhs']={'const':'2/4'}; s['rhs']={'const':'1/2'}
        self.assertEqual(engine.certify(x)['status'],'MATHEMATICAL_COMPONENTS_VERIFIED')

    def test_independent_grid_budget_fails_closed(self):
        z={'op':'pow','arg':{'op':'add','args':[{'var':'x'},{'var':'y'}]},'exp':8}
        with self.assertRaises(ReplayError): verify_identity(z,z,['x','y'],max_grid=20)

    def test_lean_files_have_no_placeholders_or_custom_axioms(self):
        src=(HERE/'lean'/'PhysicsAlgebra.lean').read_text()
        self.assertNotIn('sorry',src)
        self.assertNotIn('admit',src)
        self.assertNotIn('axiom ',src)

if __name__ == '__main__':
    unittest.main()
