"""Independent adversarial regression tests for standalone generic method gate."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
from method_gate import MethodGateError, evaluate, _read_json_strict
FIXTURE=BASE/'fixtures'/'generic_method_fixture.json'


class GenericGateTests(unittest.TestCase):
    def setUp(self):
        self.base=json.loads(FIXTURE.read_text())

    def check_refused(self,edit):
        x=copy.deepcopy(self.base);edit(x)
        with self.assertRaises((MethodGateError,TypeError,ValueError)):
            evaluate(x)

    def test_success_scope(self):
        r=evaluate(self.base)
        self.assertEqual(r['status'],'LOCAL_METHOD_CONSISTENCY_PASSED__SOURCE_UNVERIFIED__PROOF_UNVERIFIED')
        self.assertFalse(r['lean_kernel_verified'])
        self.assertFalse(r['empirical_validation_verified'])
        self.assertFalse(r['independent_method_provenance_authenticated'])
        self.assertEqual(r['negative_controls_passed'],2)

    def test_source_file_verification(self):
        r=evaluate(self.base,source_root=BASE)
        self.assertTrue(r['method_source_hashes_verified'])
        self.assertFalse(r['lean_kernel_verified'])
        self.assertEqual(r['status'],'LOCAL_METHOD_AND_SOURCE_INTEGRITY_PASSED__PROOF_UNVERIFIED')

    def test_verified_input_hash_mismatch(self):
        x=copy.deepcopy(self.base);x['input_sha256']='e'*64
        for m in x['methods']:m['input_sha256']='e'*64
        with self.assertRaises(MethodGateError):evaluate(x,source_root=BASE)

    def test_verified_context_hash_mismatch(self):
        x=copy.deepcopy(self.base);x['context_sha256']='e'*64
        for m in x['methods']:m['context_sha256']='e'*64
        with self.assertRaises(MethodGateError):evaluate(x,source_root=BASE)

    def test_verified_input_path_traversal(self):
        x=copy.deepcopy(self.base);x['input_path']='../../file.json'
        with self.assertRaises(MethodGateError):evaluate(x,source_root=BASE)

    def test_verified_source_hash_mismatch(self):
        x=copy.deepcopy(self.base)
        x['methods'][0]['source_sha256']='e'*64
        with self.assertRaises(MethodGateError):evaluate(x,source_root=BASE)

    def test_verified_source_traversal_refused(self):
        x=copy.deepcopy(self.base)
        x['methods'][0]['source_path']='../../proof_receipt.py'
        with self.assertRaises(MethodGateError):evaluate(x,source_root=BASE)

    def test_verified_source_symlink_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'fixtures').mkdir()
            src=BASE/'fixtures'/'toy_method_a.py'
            (root/'fixtures'/'toy_method_a.py').symlink_to(src)
            with self.assertRaises(MethodGateError):evaluate(self.base,source_root=root)

    def test_verified_fixture_methods_execute_as_expected(self):
        out=[]
        for script in ('toy_method_a.py','toy_method_b.py'):
            r=subprocess.run([sys.executable,str(BASE/'fixtures'/script)],capture_output=True,text=True,check=True)
            out.append(r.stdout.strip())
        self.assertEqual(out,['2','2.0001'])

    def test_manifest_digest_sensitive_to_input(self):
        r=evaluate(self.base)
        x=copy.deepcopy(self.base);x['claim_text']='Modified synthetic physical statement'
        self.assertNotEqual(r['manifest_sha256'],evaluate(x)['manifest_sha256'])

    def test_missing_schema_field(self):self.check_refused(lambda x:x.pop('negative_controls'))
    def test_unknown_schema_field(self):self.check_refused(lambda x:x.update({'certified':True}))
    def test_wrong_schema(self):self.check_refused(lambda x:x.update(schema='other'))
    def test_empty_statement(self):self.check_refused(lambda x:x.update(claim_text=''))
    def test_null_input_hash(self):self.check_refused(lambda x:x.update(input_sha256=None))
    def test_zero_context_hash(self):self.check_refused(lambda x:x.update(context_sha256='0'*64))
    def test_nan(self):self.check_refused(lambda x:x['methods'][0]['result'].update(re='NaN'))
    def test_infinity(self):self.check_refused(lambda x:x['methods'][0]['result'].update(im='Infinity'))
    def test_float_for_decimal(self):self.check_refused(lambda x:x['methods'][0]['result'].update(re=0.0))
    def test_extreme_exponent(self):self.check_refused(lambda x:x['methods'][0]['result'].update(re='1e99999'))
    def test_missing_method(self):self.check_refused(lambda x:x['methods'].pop())
    def test_method_not_done(self):self.check_refused(lambda x:x['methods'][0].update(status='queued'))
    def test_tampered_input(self):self.check_refused(lambda x:x['methods'][1].update(input_sha256='b'*64))
    def test_tampered_context(self):self.check_refused(lambda x:x['methods'][1].update(context_sha256='b'*64))
    def test_duplicate_method_id(self):self.check_refused(lambda x:x['methods'][1].update(method_id=x['methods'][0]['method_id']))
    def test_same_family(self):self.check_refused(lambda x:x['methods'][1].update(method_family=x['methods'][0]['method_family']))
    def test_same_source(self):self.check_refused(lambda x:x['methods'][1].update(source_sha256=x['methods'][0]['source_sha256']))
    def test_same_implementation(self):self.check_refused(lambda x:x['methods'][1].update(implementation_id=x['methods'][0]['implementation_id']))
    def test_same_equation_family(self):self.check_refused(lambda x:x['methods'][1].update(equation_family=x['methods'][0]['equation_family']))
    def test_wrong_result_sign(self):self.check_refused(lambda x:x['methods'][1]['result'].update(re='-2'))
    def test_large_error_budget_negative(self):self.check_refused(lambda x:x['methods'][1].update(absolute_error_budget='-1'))
    def test_malicious_unchecked_budget(self):self.check_refused(lambda x:x['methods'][1].update(error_budget_class='provably_real'))
    def test_missing_negative(self):self.check_refused(lambda x:x.update(negative_controls=[]))
    def test_dup_negative(self):self.check_refused(lambda x:x['negative_controls'][1].update(name=x['negative_controls'][0]['name']))
    def test_false_negative_rejected(self):self.check_refused(lambda x:x['negative_controls'][0].update(corrupted_residual='0.00000000001'))
    def test_positive_false_rejected(self):self.check_refused(lambda x:x['negative_controls'][1].update(baseline_residual='0.002'))
    def test_threshold_ordering(self):self.check_refused(lambda x:x['negative_controls'][0].update(corruption_minimum='0'))
    def test_instability_refused(self):self.check_refused(lambda x:x['stability_samples'][0]['result'].update(re='3000'))
    def test_too_few_stability(self):self.check_refused(lambda x:x['stability_samples'].pop())
    def test_duplicate_stability(self):self.check_refused(lambda x:x['stability_samples'][1].update(setting=x['stability_samples'][0]['setting']))
    def test_unknown_reference(self):self.check_refused(lambda x:x['stability_samples'][0].update(reference_method_id='Other'))
    def test_no_error_tolerance(self):self.check_refused(lambda x:x['comparison'].update(absolute_tolerance='0'))
    def test_missing_provenance(self):self.check_refused(lambda x:x['methods'][0].update(provenance=''))
    def test_wrong_boolean_type(self):self.check_refused(lambda x:x['comparison'].update(require_distinct_equation_families='false'))

    def test_same_equation_allowed_only_when_declared(self):
        x=copy.deepcopy(self.base)
        x['methods'][1]['equation_family']=x['methods'][0]['equation_family']
        x['comparison']['require_distinct_equation_families']=False
        r=evaluate(x)
        self.assertFalse(r['different_equation_families_declared'])
        self.assertFalse(r['independent_method_provenance_authenticated'])

    def test_bad_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'x.json';p.write_text('{"a":1,"a":2}')
            with self.assertRaises(MethodGateError):_read_json_strict(p)

    def test_bad_nonfinite_json_literal(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'x.json';p.write_text('{"a":NaN}')
            with self.assertRaises(MethodGateError):_read_json_strict(p)

    def test_invalid_symlink_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=Path(tmp)/'a.json'; b=Path(tmp)/'b.json';a.write_text('{}');b.symlink_to(a)
            with self.assertRaises(MethodGateError):_read_json_strict(b)

    def test_cli_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'report.json'
            p=subprocess.run([sys.executable,str(BASE/'method_gate.py'),'--manifest',str(FIXTURE),'--source-root',str(BASE),'--output',str(path)],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(json.loads(path.read_text())['lean_kernel_verified'],False)

    def test_cli_refusal(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp=Path(tmp)/'wrong.json';inp.write_text('{"a":1,"a":2}')
            p=subprocess.run([sys.executable,str(BASE/'method_gate.py'),'--manifest',str(inp)],capture_output=True,text=True)
            self.assertEqual(p.returncode,2)
            self.assertIn('REFUSED',p.stderr)

    def test_paper_independence(self):
        for component in ('method_gate.py','fixtures/generic_method_fixture.json','fixtures/toy_method_a.py','fixtures/toy_method_b.py','fixtures/toy_input.json','fixtures/toy_context.json'):
            data=(BASE/component).read_text(encoding='utf-8').lower()
            for secret in ('event_specific_','paper_specific_','case_dataset_'):
                self.assertNotIn(secret,data)


if __name__=='__main__':unittest.main()
