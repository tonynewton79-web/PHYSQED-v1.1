"""PHYSQED v0.3 offline claim-freeze integrity gate (stdlib only).

IMPORTANT: matching a reviewer-held cryptographic lock is not proof that a
natural-language statement is correctly translated or physically true.
No reviewer key belongs in Git or in an AI generated certificate.
"""
import argparse
import base64
import hashlib
import hmac
import json
from pathlib import Path

from compiler import ContractError, compile_contract
from engine import canonical, digest

VERSION = 'physqed-lock-v0.3'
WARNING = ('Authenticated key possession only; semantic correctness and '
           'physical truth NOT certified.')
MAX_INPUT_BYTES = 1024 * 1024


def pairs_without_duplicates(pairs):
    obj = {}
    for k, v in pairs:
        if k in obj:
            raise ContractError('duplicate JSON key: ' + k)
        obj[k] = v
    return obj


def read_json(path):
    p = Path(path)
    raw = p.read_bytes()
    if len(raw) > MAX_INPUT_BYTES:
        raise ContractError('contract or lock exceeds size budget')
    return json.loads(raw, object_pairs_hook=pairs_without_duplicates,
                      parse_float=lambda _: (_ for _ in ()).throw(ContractError('float forbidden')),
                      parse_constant=lambda _: (_ for _ in ()).throw(ContractError('nonfinite forbidden')))


def decode_key(text):
    if not isinstance(text, str):
        raise ContractError('reviewer HMAC key is required')
    try:
        key = base64.b64decode(text, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise ContractError('invalid base64 reviewer key') from exc
    if len(key) < 32:
        raise ContractError('reviewer key must contain >= 256 bits')
    return key


def locked_payload(contract, report, lean):
    if report['status'] != 'DERIVATION_CHECKED__SEMANTIC_REVIEW_REQUIRED' or lean is None:
        raise ContractError('cannot lock a failed derivation')
    return {'lock_version': VERSION,
            'claim_id': contract['id'],
            'exact_contract_sha256': digest(canonical(contract)),
            'generated_lean_sha256': digest(lean.encode('utf-8')),
            'compiler_sha256': report['compiler_sha256'],
            'engine_sha256': report['engine_sha256'],
            'replay_sha256': report['replay_sha256'],
            'formal_conclusions': report['structured_conclusions'],
            'formal_assumptions': report['declared_assumptions'],
            'context_sha256': digest(canonical(contract['context'])),
            'statement_sha256': digest(contract['statement'].encode('utf-8')),
            'mapping_sha256': digest(canonical(contract['mapping']))}


def freeze(contract, key, reviewer_label):
    if not isinstance(reviewer_label, str) or not 1 <= len(reviewer_label) <= 100:
        raise ContractError('reviewer label required')
    report, lean = compile_contract(contract)
    payload = locked_payload(contract, report, lean)
    payload['reviewer_label_unverified'] = reviewer_label
    sig = hmac.new(key, canonical(payload), hashlib.sha256).hexdigest()
    return {'payload': payload, 'mac_algorithm':'HMAC-SHA256', 'mac_hex': sig,
            'warning':WARNING}


def verify(contract, lock, key):
    if not isinstance(lock, dict) or set(lock) != {'payload','mac_algorithm','mac_hex','warning'}:
        raise ContractError('invalid or incomplete lock format')
    if lock['warning'] != WARNING:
        raise ContractError('lock warning altered')
    if lock['mac_algorithm'] != 'HMAC-SHA256':
        raise ContractError('unsupported lock algorithm')
    payload = lock['payload']
    expected = hmac.new(key, canonical(payload), hashlib.sha256).hexdigest()
    if not isinstance(lock['mac_hex'], str) or not hmac.compare_digest(lock['mac_hex'], expected):
        raise ContractError('reviewer lock signature mismatch')
    if not isinstance(payload, dict) or payload.get('lock_version') != VERSION:
        raise ContractError('lock schema mismatch')
    report, lean = compile_contract(contract)
    current = locked_payload(contract, report, lean)
    current['reviewer_label_unverified'] = payload.get('reviewer_label_unverified')
    if not hmac.compare_digest(canonical(payload), canonical(current)):
        raise ContractError('contract, context, statement, Lean source or code has changed')
    return {'status':'EXACT_FROZEN_CONTRACT_MATCH', 'review_label': payload['reviewer_label_unverified'],
            'exact_contract_sha256': payload['exact_contract_sha256'],
            'generated_lean_sha256': payload['generated_lean_sha256'],
            'review_key_proof':'HMAC verified using key supplied at runtime; owner identity not authenticated',
            'lean_kernel_verified':False, 'semantic_alignment_verified':False,
            'physical_law_proven':False, 'empirical_validation_verified':False,
            'interpretation':'Unchanged formal claim relative to a held review lock; NOT automated approval of its meaning.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('contract')
    ap.add_argument('--lock', required=True)
    ap.add_argument('--key-file', required=True,
                    help='local base64 key file outside Git. Never commit this key.')
    ap.add_argument('--freeze', action='store_true', help='create review lock; otherwise verify')
    ap.add_argument('--reviewer-label', default='unverified-reviewer')
    args = ap.parse_args()
    try:
        key = decode_key(Path(args.key_file).read_text().strip())
        contract = read_json(args.contract)
        if args.freeze:
            result = freeze(contract,key,args.reviewer_label)
            Path(args.lock).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
        else:
            result = verify(contract,read_json(args.lock),key)
    except (ValueError,OSError,TypeError,KeyError,OverflowError,RecursionError) as exc:
        ap.exit(2,'PHYSQED LOCK REFUSED: '+str(exc)+'\n')
    print(json.dumps(result,sort_keys=True,indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
