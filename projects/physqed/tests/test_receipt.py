"""v0.4: adversarial and positive-control CI evidence tests.

Synthetic GitHub responses in this file are MOCKS and are never cited as a
real GitHub Actions run or as evidence of actual Lean compilation.
"""
import base64
import copy
import hashlib
import hmac
import json
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from engine import canonical, digest
from proof_receipt import (BINDINGS, VERSION, RUN_NAME, WORKFLOW, LEAN_JOB,
                            LEAN_STEPS, REPO, GithubClient, ReceiptError, live_check,
                            issue_review, validate_review, make_receipt, snapshot, assert_compiler_alignment)

class FakeGithubClient:
    def __init__(self, review, root, sha='a'*40, status='completed', conclusion='success'):
        self.sha=sha
        self.calls=[]
        self.files={p:(root/p).read_bytes() for p in BINDINGS}
        self.run={
            'name':RUN_NAME,'head_sha':sha, 'event':'push', 'path':WORKFLOW+'@refs/heads/feature/physqed-v0.3',
            'repository':{'full_name':REPO},'status':status,'conclusion':conclusion,
        }
        self.jobs={'total_count':1,'jobs':[{'name':LEAN_JOB,'id':123,'status':'completed','conclusion':'success','steps':[
            {'name':n,'status':'completed','conclusion':'success'} for n in LEAN_STEPS
        ]}]}
    def fetch(self,path):
        self.calls.append(path)
        if '/actions/runs/' in path and '/jobs?' in path:
            return copy.deepcopy(self.jobs)
        if '/actions/runs/' in path:
            return copy.deepcopy(self.run)
        if '/contents/' in path:
            p=path.split('/contents/',1)[1].split('?ref=',1)[0]
            return {'type':'file','encoding':'base64','content':base64.b64encode(self.files[p]).decode()}
        raise AssertionError('unexpected route '+path)

class ReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract=json.loads((HERE/'fixtures'/'oscillator_contract.json').read_text())
        cls.key=bytes(range(32))   # TEST-ONLY FAKE KEY. NEVER production authority.
        cls.review=issue_review(ROOT,cls.contract,cls.key,'synthetic-test-only')
    def test_cli_freeze_writes_review_and_offline_verify(self):
        with tempfile.TemporaryDirectory() as d:
            directory=Path(d)
            key=directory/'key.base64'
            key.write_text(base64.b64encode(self.key).decode()+'\n')
            lock=directory/'review.lock.json'
            out=directory/'receipt.json'
            command=[sys.executable,str(HERE/'proof_receipt.py'),'--root',str(ROOT),
                '--contract',str(HERE/'fixtures'/'oscillator_contract.json'),
                '--key-file',str(key),'--review',str(lock)]
            a=subprocess.run(command+['--freeze','--reviewer-label','synthetic-ci-test'],
                capture_output=True,text=True,check=True)
            self.assertTrue(lock.is_file())
            self.assertEqual(json.loads(lock.read_text())['manifest']['receipt_version'],VERSION)
            b=subprocess.run(command+['--output',str(out)],capture_output=True,text=True,check=True)
            result=json.loads(out.read_text())
            self.assertFalse(result['lean_kernel_verified'])
    def test_review_lock_valid(self):
        x=validate_review(ROOT,self.contract,self.review,self.key)
        self.assertTrue(x['local_review_lock_verified'])
        self.assertFalse(x['physical_law_proven'])
    def test_offline_output_has_no_lean_credit(self):
        result=make_receipt(ROOT,self.contract,self.review,self.key)
        self.assertEqual(result['status'],'REVIEW_LOCK_VERIFIED__LEAN_CI_NOT_CONFIRMED')
        self.assertFalse(result['lean_kernel_verified'])
        self.assertNotIn('github_evidence',result)
    def test_offline_output_deterministic(self):
        r=make_receipt(ROOT,self.contract,self.review,self.key)
        self.assertEqual(r,make_receipt(ROOT,self.contract,self.review,self.key))
        check=copy.deepcopy(r);h=check.pop('receipt_sha256')
        self.assertEqual(h,digest(canonical(check)))
    def test_missing_online_parameters_refused(self):
        with self.assertRaises(ReceiptError):
            make_receipt(ROOT,self.contract,self.review,self.key,run_id=123,expected_sha='a'*40)
    def test_invalid_reviewer_key_refused(self):
        with self.assertRaises(ReceiptError):
            validate_review(ROOT,self.contract,self.review,b'wrong')
    def test_modified_review_body_refused(self):
        r=copy.deepcopy(self.review)
        r['manifest']['warning']='proof of physics!'
        with self.assertRaises(ReceiptError): validate_review(ROOT,self.contract,r,self.key)
    def test_review_warning_forced_even_with_resign(self):
        r=copy.deepcopy(self.review)
        r['manifest']['warning']='physical law proved'
        r['hmac_hex']=hmac.new(self.key,canonical(r['manifest']),hashlib.sha256).hexdigest()
        with self.assertRaises(ReceiptError):validate_review(ROOT,self.contract,r,self.key)
    def test_unrecognised_review_fields_refused(self):
        r=copy.deepcopy(self.review)
        r['manifest']['semantic_override']=True
        r['hmac_hex']=hmac.new(self.key,canonical(r['manifest']),hashlib.sha256).hexdigest()
        with self.assertRaises(ReceiptError):validate_review(ROOT,self.contract,r,self.key)
    def test_missing_bound_file_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for path in BINDINGS:
                target=root/path;target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes((ROOT/path).read_bytes())
            (root/BINDINGS[0]).unlink()
            with self.assertRaises(ReceiptError):snapshot(root)
    def test_compiled_source_matches_compiler(self):
        actual=(ROOT/'projects/physqed/lean/CompiledOscillator.lean').read_text()
        self.assertEqual(assert_compiler_alignment(ROOT,self.contract),actual)
    def test_forged_compiled_theorem_refused_even_at_issue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for path in BINDINGS:
                target=root/path;target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes((ROOT/path).read_bytes())
            target=root/'projects/physqed/lean/CompiledOscillator.lean'
            target.write_text('import Mathlib\ntheorem irrelevant : True := by trivial\n')
            with self.assertRaises(ReceiptError): issue_review(root,self.contract,self.key,'test')
    def test_tampered_proof_file_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for path in BINDINGS:
                target=root/path;target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes((ROOT/path).read_bytes())
            target=root/'projects/physqed/lean/Conservation.lean'
            target.write_bytes(target.read_bytes()+b'\n-- altered after review\n')
            with self.assertRaises(ReceiptError):validate_review(root,self.contract,self.review,self.key)
    def test_tampered_workflow_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for path in BINDINGS:
                target=root/path;target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes((ROOT/path).read_bytes())
            target=root/WORKFLOW
            target.write_bytes(target.read_bytes()+b'\n# edited workflow\n')
            with self.assertRaises(ReceiptError):validate_review(root,self.contract,self.review,self.key)
    def test_wrong_physics_frame_refused(self):
        c=copy.deepcopy(self.contract);c['context']['frame']='rotating frame'
        with self.assertRaises(ValueError):validate_review(ROOT,c,self.review,self.key)
    def test_wrong_english_statement_refused(self):
        c=copy.deepcopy(self.contract);c['statement']='perpetual motion proven'
        with self.assertRaises(ValueError):validate_review(ROOT,c,self.review,self.key)
    def test_review_source_manifest_exact(self):
        self.assertEqual(set(self.review['manifest']['files_sha256']),set(BINDINGS))
        self.assertEqual(self.review['manifest']['files_sha256'],snapshot(ROOT))
    def test_locked_lean_step_names(self):
        self.assertEqual(self.review['manifest']['required_steps'],list(LEAN_STEPS))
    def test_queued_ci_is_not_verified(self):
        fake=FakeGithubClient(self.review,ROOT,status='queued',conclusion=None)
        x=live_check(ROOT,self.review,123,'a'*40,fake)
        self.assertEqual(x['gate'],'CI_NOT_VERIFIED')
        self.assertEqual(len(fake.calls),1)
    def test_failed_ci_is_not_verified(self):
        fake=FakeGithubClient(self.review,ROOT,status='completed',conclusion='failure')
        self.assertEqual(live_check(ROOT,self.review,123,'a'*40,fake)['gate'],'CI_NOT_VERIFIED')
    def test_wrong_sha_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'b'*40,fake)
    def test_invalid_sha_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'abc',fake)
    def test_pull_request_merge_event_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        fake.run['event']='pull_request'
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'a'*40,fake)
    def test_missing_event_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        del fake.run['event']
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'a'*40,fake)
    def test_mismatched_repository_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        fake.run['repository']['full_name']='attacker/fake'
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'a'*40,fake)
    def test_mismatched_workflow_name_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        fake.run['name']='Fake Lean CI'
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'a'*40,fake)
    def test_mismatched_workflow_path_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        fake.run['path']='.github/workflows/fake.yml'
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'a'*40,fake)
    def test_missing_lean_job_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        fake.jobs['jobs'][0]['name']='python-only'
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'a'*40,fake)
    def test_failed_lean_job_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        fake.jobs['jobs'][0]['conclusion']='failure'
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'a'*40,fake)
    def test_missing_lean_step_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        fake.jobs['jobs'][0]['steps'].pop()
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'a'*40,fake)
    def test_failed_lean_step_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        fake.jobs['jobs'][0]['steps'][0]['conclusion']='failure'
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'a'*40,fake)
    def test_duplicate_lean_steps_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        fake.jobs['jobs'][0]['steps'].append(copy.deepcopy(fake.jobs['jobs'][0]['steps'][0]))
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'a'*40,fake)
    def test_forced_wrong_github_blob_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        fake.files['projects/physqed/lean/Conservation.lean']+=b'\n-- forged\n'
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'a'*40,fake)
    def test_forced_wrong_dependency_refused(self):
        fake=FakeGithubClient(self.review,ROOT)
        fake.files['projects/physqed/lakefile.toml']+=b'\n# edited mathlib pin\n'
        with self.assertRaises(ReceiptError):live_check(ROOT,self.review,123,'a'*40,fake)
    def test_synthetic_complete_evidence_only(self):
        fake=FakeGithubClient(self.review,ROOT)
        x=live_check(ROOT,self.review,123,'a'*40,fake)
        self.assertEqual(x['gate'],'CI_LEAN_SOURCE_AND_STEPS_CONFIRMED')
        self.assertEqual(x['source_files_checked'],len(BINDINGS))
        self.assertFalse(x['physical_law_proven'])
    def test_network_token_required(self):
        with self.assertRaises(ReceiptError):GithubClient(None)
    def test_github_unsafe_path_refused(self):
        with self.assertRaises(ReceiptError):GithubClient('not-a-real-token').fetch('https://evil.invalid/fake')
    def test_no_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            target=root/BINDINGS[0]
            target.parent.mkdir(parents=True,exist_ok=True)
            target.symlink_to(ROOT/BINDINGS[0])
            with self.assertRaises(ReceiptError):snapshot(root)

if __name__ == '__main__': unittest.main()
