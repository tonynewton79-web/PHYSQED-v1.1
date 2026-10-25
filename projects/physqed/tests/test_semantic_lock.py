import base64
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from semantic_lock import (ContractError, decode_key, freeze, pairs_without_duplicates,
                           read_json, verify, locked_payload)


class SemanticLockTests(unittest.TestCase):
    def setUp(self):
        self.good = json.loads((HERE/'fixtures'/'oscillator_contract.json').read_text())
        self.key = bytes(range(32))  # SYNTHETIC test key, never used for approval.
        self.lock = freeze(self.good,self.key,'synthetic-test-reviewer')

    def assert_reject(self, changed, lock=None, key=None):
        with self.assertRaises(ContractError):
            verify(changed, self.lock if lock is None else lock,
                   self.key if key is None else key)

    def test_roundtrip(self):
        r=verify(self.good,self.lock,self.key)
        self.assertEqual(r['status'],'EXACT_FROZEN_CONTRACT_MATCH')
        self.assertFalse(r['semantic_alignment_verified'])
        self.assertFalse(r['physical_law_proven'])
        self.assertFalse(r['lean_kernel_verified'])

    def test_lock_stable_and_deterministic(self):
        self.assertEqual(self.lock,freeze(self.good,self.key,'synthetic-test-reviewer'))

    def test_statement_change(self):
        q=copy.deepcopy(self.good);q['statement']='Mass-energy experimentally proven.'
        self.assert_reject(q)

    def test_frame_change(self):
        q=copy.deepcopy(self.good);q['context']['frame']='rotating frame'
        self.assert_reject(q)

    def test_regime_change(self):
        q=copy.deepcopy(self.good);q['context']['regime']='quantum oscillator'
        self.assert_reject(q)

    def test_gauge_change(self):
        q=copy.deepcopy(self.good);q['context']['gauge']='Coulomb gauge'
        self.assert_reject(q)

    def test_boundary_change(self):
        q=copy.deepcopy(self.good);q['context']['boundary_conditions']='Dirichlet'
        self.assert_reject(q)

    def test_symbol_meaning_change(self):
        q=copy.deepcopy(self.good);q['symbols'][3]['meaning']='momentum rather than velocity'
        self.assert_reject(q)

    def test_change_assumption_source(self):
        q=copy.deepcopy(self.good);q['assumptions'][0]['source']='fabricated-paper'
        self.assert_reject(q)

    def test_sign_change(self):
        q=copy.deepcopy(self.good);q['assumptions'][0]['rhs']['args'][0]['const']='1'
        self.assert_reject(q)

    def test_proof_witness_change(self):
        q=copy.deepcopy(self.good);q['proofs'][0]['multipliers']['force_balance']={'const':'1'}
        self.assert_reject(q)

    def test_mapping_change(self):
        q=copy.deepcopy(self.good);q['mapping']['explanation']='unrelated claim'
        self.assert_reject(q)

    def test_bad_authentication_key(self):
        self.assert_reject(self.good,key=bytes(range(1,33)))

    def test_modified_signature(self):
        lock=copy.deepcopy(self.lock);lock['mac_hex']='0'*64
        self.assert_reject(self.good,lock=lock)

    def test_warning_forgery_refused(self):
        lock=copy.deepcopy(self.lock);lock['warning']='EVERYTHING PROVEN'
        self.assert_reject(self.good,lock=lock)

    def test_payload_spoof(self):
        lock=copy.deepcopy(self.lock);lock['payload']['statement_sha256']='0'*64
        self.assert_reject(self.good,lock=lock)

    def test_cross_contract_replay(self):
        q=copy.deepcopy(self.good);q['id']='different_claim'
        self.assert_reject(q)

    def test_invalid_review_key(self):
        with self.assertRaises(ContractError): decode_key('AAAA')
        with self.assertRaises(ContractError): decode_key('%GARBAGE%')
        self.assertEqual(decode_key(base64.b64encode(self.key).decode()),self.key)

    def test_duplicate_json_root_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'bad.json';p.write_text('{"statement":"true","statement":"fake"}')
            with self.assertRaises(ContractError): read_json(p)

    def test_duplicate_nested_key_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'bad.json';p.write_text('{"context":{"frame":"inertial","frame":"rotating"}}')
            with self.assertRaises(ContractError): read_json(p)

    def test_lock_cannot_approve_failed_math(self):
        q=copy.deepcopy(self.good)
        q['proofs'][0]['multipliers']['force_balance']={'op':'mul','args':[{'const':'2'},{'var':'v'}]}
        with self.assertRaises(ContractError): freeze(q,self.key,'synthetic-test-reviewer')

    def test_lock_requires_reviewer_label(self):
        with self.assertRaises(ContractError): freeze(self.good,self.key,'')

    def test_warning_cannot_be_dropped(self):
        lock=copy.deepcopy(self.lock);del lock['warning']
        self.assert_reject(self.good,lock=lock)

    def test_semantic_correctness_not_auto_asserted(self):
        q=copy.deepcopy(self.good)
        q['statement']='These calculations show gravity is quantised by experiments.'
        malicious=freeze(q,self.key,'synthetic-test-reviewer')
        r=verify(q,malicious,self.key)
        self.assertFalse(r['semantic_alignment_verified'])
        self.assertFalse(r['empirical_validation_verified'])

if __name__=='__main__': unittest.main()
