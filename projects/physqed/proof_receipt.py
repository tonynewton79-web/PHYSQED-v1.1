"""PHYSQED v0.4 -- proof receipt with externally keyed review lock and live CI gate.

Security boundary:
 * A valid local HMAC attests only the exact reviewed FILE BYTES under its key.
 * Untrusted downloaded JSON or a pasted "CI passed" assertion NEVER suffices.
 * Lean success is reported only after independently fetching successful workflow,
   job/step metadata and comparing GitHub committed proof/workflow files with the
   reviewer-locked SHA256 hashes for that exact head SHA.
 * A CI compile result does not prove the natural-language physics description.

This is an experimental integrity verifier, NOT a formal proof of GitHub trust.
The operator must protect and authenticate the HMAC review key and GitHub token.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import hmac
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from engine import canonical, digest
from semantic_lock import ContractError, read_json, decode_key, freeze as semantic_freeze, verify as semantic_verify
from compiler import compile_contract

VERSION = 'physqed-receipt-v0.4'
REPO = 'tonynewton79-web/PHYSQED-v1.1'
WORKFLOW = '.github/workflows/physqed-v03.yml'
RUN_NAME = 'PHYSQED 0.3 Physics Conservation and Locked Statement'
LEAN_JOB = 'lean-calculus'
LEAN_STEPS = (
    'Compile calculus-level oscillator theorem (zero admits)',
    'Compile pre-existing v0.2 polynomial source',
    'Reject proof placeholders or added axioms (strip comment lines)',
)
REVIEW_WARNING = 'Integrity/authentication of approved bytes only; physics semantic and empirical validation NOT established.'
BINDINGS = (
    '.github/workflows/physqed-v03.yml',
    'projects/physqed/engine.py',
    'projects/physqed/compiler.py',
    'projects/physqed/replay.py',
    'projects/physqed/semantic_lock.py',
    'projects/physqed/lean-toolchain',
    'projects/physqed/lakefile.toml',
    'projects/physqed/lean/CompiledOscillator.lean',
    'projects/physqed/lean/Conservation.lean',
    'projects/physqed/fixtures/oscillator_contract.json',
)
MAX_FILE = 1 << 20
SHA = re.compile(r'^[a-f0-9]{40}$')

class ReceiptError(ValueError):
    pass

def file_bytes(root, path):
    if path not in BINDINGS:
        raise ReceiptError('unapproved file path')
    p = Path(root) / path
    if p.is_symlink() or not p.is_file():
        raise ReceiptError('file absent or symlink: ' + path)
    if p.stat().st_size > MAX_FILE:
        raise ReceiptError('file too large: ' + path)
    return p.read_bytes()

def snapshot(root):
    return {path: digest(file_bytes(root,path)) for path in BINDINGS}

def assert_compiler_alignment(root,contract):
    report,generated=compile_contract(contract)
    if report['status']!='DERIVATION_CHECKED__SEMANTIC_REVIEW_REQUIRED' or generated is None:
        raise ReceiptError('compiler did not verify supplied contract')
    if generated.encode('utf-8')!=file_bytes(root,'projects/physqed/lean/CompiledOscillator.lean'):
        raise ReceiptError('compiled Lean source differs from reviewed contract output')
    return generated

def issue_review(root, contract, key, reviewer_label):
    """Only explicit human key custody makes this a reviewer approval.

    No key, signature or test reviewer lock is distributed with production files.
    """
    if not isinstance(reviewer_label,str) or not reviewer_label.strip() or len(reviewer_label)>100:
        raise ReceiptError('explicit reviewer label required')
    assert_compiler_alignment(root,contract)
    slock = semantic_freeze(contract,key,reviewer_label)
    manifest = {
        'receipt_version': VERSION,
        'reviewer_label_unverified': reviewer_label,
        'repository': REPO,
        'required_workflow_path': WORKFLOW,
        'required_workflow_name': RUN_NAME,
        'required_job': LEAN_JOB,
        'required_steps': list(LEAN_STEPS),
        'files_sha256': snapshot(root),
        'semantic_lock': slock,
        'warning': REVIEW_WARNING,
    }
    return {'manifest':manifest, 'hmac_algorithm':'HMAC-SHA256',
            'hmac_hex':hmac.new(key,canonical(manifest),hashlib.sha256).hexdigest()}

def validate_review(root, contract, review, key):
    if not isinstance(review,dict) or set(review) != {'manifest','hmac_algorithm','hmac_hex'}:
        raise ReceiptError('review format mismatch')
    if review['hmac_algorithm'] != 'HMAC-SHA256':
        raise ReceiptError('review algorithm invalid')
    payload=review['manifest']
    if not isinstance(payload,dict) or not isinstance(review['hmac_hex'],str):
        raise ReceiptError('invalid review payload')
    expected=hmac.new(key,canonical(payload),hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected,review['hmac_hex']):
        raise ReceiptError('review HMAC mismatch')
    permitted={'receipt_version','reviewer_label_unverified','repository',
               'required_workflow_path','required_workflow_name','required_job',
               'required_steps','files_sha256','semantic_lock','warning'}
    if set(payload)!=permitted or payload.get('receipt_version')!=VERSION:
        raise ReceiptError('unrecognized review schema')
    if payload['repository']!=REPO or payload['required_workflow_path']!=WORKFLOW or payload['required_workflow_name']!=RUN_NAME or payload['required_job']!=LEAN_JOB or payload['required_steps']!=list(LEAN_STEPS):
        raise ReceiptError('reviewed policy was downgraded')
    if payload['warning']!=REVIEW_WARNING or set(payload['files_sha256'])!=set(BINDINGS):
        raise ReceiptError('required warnings or files altered')
    actual=snapshot(root)
    assert_compiler_alignment(root,contract)
    if actual != payload['files_sha256']:
        raise ReceiptError('source bytes changed after review')
    match=semantic_verify(contract,payload['semantic_lock'],key)
    if match['status'] != 'EXACT_FROZEN_CONTRACT_MATCH':
        raise ReceiptError('semantic-lock mismatch')
    return {'local_review_lock_verified':True, 'files_sha256':actual,
            'claim_id':contract['id'], 'source_lock_sha256':digest(canonical(payload)),
            'semantic_alignment_verified':False, 'physical_law_proven':False}

class GithubClient:
    """Fixed-host, TLS-protected GitHub API client, with no caller-provided URLs."""
    def __init__(self, token):
        if not isinstance(token,str) or not token.strip():
            raise ReceiptError('GitHub token required for live evidence')
        self.token=token

    def fetch(self, path):
        if not isinstance(path,str) or not path.startswith('/repos/'+REPO+'/') or '..' in path or '://' in path:
            raise ReceiptError('API route blocked')
        url='https://api.github.com'+path
        req=Request(url,headers={'Authorization':'Bearer '+self.token,
                                 'Accept':'application/vnd.github+json',
                                 'X-GitHub-Api-Version':'2022-11-28',
                                 'User-Agent':'PHYSQED-receipt-v04'})
        try:
            with urlopen(req,timeout=20) as rsp:
                if rsp.geturl().split('/')[2] != 'api.github.com':
                    raise ReceiptError('unexpected API redirect host')
                raw=rsp.read(4*MAX_FILE+1)
                if len(raw)>4*MAX_FILE:
                    raise ReceiptError('GitHub response too large')
                return json.loads(raw)
        except (HTTPError,URLError,TimeoutError,OSError,json.JSONDecodeError) as exc:
            raise ReceiptError('GitHub API request did not provide validated evidence') from exc

def live_check(root, review, run_id, expected_sha, client):
    """Live check tied to exact GitHub SHA. No offline evidence imports accepted."""
    if not isinstance(run_id,int) or isinstance(run_id,bool) or run_id<=0:
        raise ReceiptError('invalid workflow run id')
    if not isinstance(expected_sha,str) or not SHA.fullmatch(expected_sha):
        raise ReceiptError('full 40-character git SHA required')
    prefix='/repos/'+REPO
    run=client.fetch(f'{prefix}/actions/runs/{run_id}')
    if not isinstance(run,dict):
        raise ReceiptError('invalid run evidence')
    if run.get('head_sha')!=expected_sha or run.get('name')!=RUN_NAME:
        raise ReceiptError('wrong source commit/workflow name')
    if run.get('repository',{}).get('full_name')!=REPO:
        raise ReceiptError('workflow belongs to wrong repository')
    # v0.3 uses default actions/checkout. Pull-request runs usually check out
    # a synthetic merge commit, which need not equal run.head_sha. Without an
    # independently attested checked-out SHA, never promote such a run.
    if run.get('event')!='push':
        raise ReceiptError('only exact-head push runs are admissible; PR merge checkout not certified')
    workflow_path=run.get('path','').split('@',1)[0]
    if workflow_path != WORKFLOW:
        raise ReceiptError('workflow path mismatch')
    if run.get('status')!='completed' or run.get('conclusion')!='success':
        return {'gate':'CI_NOT_VERIFIED','reason':'workflow has not completed successfully',
                'run_status':run.get('status'),'run_conclusion':run.get('conclusion')}
    jobs=client.fetch(f'{prefix}/actions/runs/{run_id}/jobs?per_page=100')
    if not isinstance(jobs,dict) or not isinstance(jobs.get('jobs'),list) or jobs.get('total_count',0)>100:
        raise ReceiptError('job data incomplete or malformed')
    lean=[j for j in jobs['jobs'] if j.get('name')==LEAN_JOB]
    if len(lean)!=1 or lean[0].get('status')!='completed' or lean[0].get('conclusion')!='success':
        raise ReceiptError('required Lean job not successful')
    job=lean[0]
    step_list=job.get('steps',[])
    for req_name in LEAN_STEPS:
        matches=[s for s in step_list if s.get('name')==req_name]
        if len(matches)!=1 or matches[0].get('status')!='completed' or matches[0].get('conclusion')!='success':
            raise ReceiptError('Lean proof step failed or missing: '+req_name)
    # Review hash locks important source, mathlib pin and *workflow code* as
    # actually recorded by GitHub at the run's HEAD. Not just a job name.
    for path in BINDINGS:
        reply=client.fetch(f'{prefix}/contents/{quote(path,safe="/")}?ref={expected_sha}')
        if not isinstance(reply,dict) or reply.get('type')!='file' or reply.get('encoding')!='base64':
            raise ReceiptError('GitHub file content unavailable: '+path)
        try:
            content=base64.b64decode(reply['content'],validate=False)
        except (KeyError,ValueError) as exc:
            raise ReceiptError('invalid GitHub content encoding') from exc
        if digest(content)!=review['manifest']['files_sha256'][path]:
            raise ReceiptError('GitHub commit did not run the exact reviewed file: '+path)
    return {'gate':'CI_LEAN_SOURCE_AND_STEPS_CONFIRMED',
            'run_id':run_id,'head_sha':expected_sha,'job_id':job['id'],
            'source_files_checked':len(BINDINGS),
            'scope':'Verified success of specified Lean CI commands for reviewed files',
            'semantic_alignment_verified':False, 'physical_law_proven':False}

def make_receipt(root,contract,review,key,run_id=None,expected_sha=None,token=None):
    local=validate_review(root,contract,review,key)
    result={'version':VERSION,**local,
            'status':'REVIEW_LOCK_VERIFIED__LEAN_CI_NOT_CONFIRMED',
            'lean_kernel_verified':False,
            'empirical_validation_verified':False,
            'warning':'No unconditional physics certification from proof receipts'}
    if run_id is not None or expected_sha is not None or token is not None:
        if run_id is None or expected_sha is None or token is None:
            raise ReceiptError('live check requires token, complete SHA and run id')
        remote=live_check(root,review,run_id,expected_sha,GithubClient(token))
        result['github_evidence']=remote
        if remote['gate']=='CI_LEAN_SOURCE_AND_STEPS_CONFIRMED':
            result['status']='LEAN_CI_CONFIRMED__SEMANTICS_UNREVIEWED'
            result['lean_kernel_verified']=True
    result['receipt_sha256']=digest(canonical(result))
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--contract',type=Path,required=True)
    parser.add_argument('--review',type=Path,required=True)
    parser.add_argument('--key-file',type=Path,required=True)
    parser.add_argument('--freeze',action='store_true')
    parser.add_argument('--reviewer-label',default='unverified-reviewer')
    parser.add_argument('--run-id',type=int)
    parser.add_argument('--sha')
    parser.add_argument('--github-token-env',default='GITHUB_TOKEN')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    try:
        key=decode_key(args.key_file.read_text().strip())
        contract=read_json(args.contract)
        if args.freeze:
            if args.run_id is not None or args.sha is not None:
                raise ReceiptError('freeze does not accept CI attestation')
            result=issue_review(args.root,contract,key,args.reviewer_label)
            args.review.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        else:
            use_remote=args.run_id is not None or args.sha is not None
            token=os.environ.get(args.github_token_env) if use_remote else None
            result=make_receipt(args.root,contract,read_json(args.review),key,
                                args.run_id,args.sha,token)
        out=json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+'\n'
        if args.output:
            args.output.write_text(out)
        else:
            print(out,end='')
    except (ReceiptError,ContractError,ValueError,OSError,KeyError,TypeError) as exc:
        parser.exit(2,'PHYSQED v0.4 REFUSED: '+str(exc)+'\n')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
