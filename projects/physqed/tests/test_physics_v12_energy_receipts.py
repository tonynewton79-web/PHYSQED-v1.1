"""Exact energy-receipt replay and tamper refusal."""
import sys
import unittest
from pathlib import Path
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.energy_receipts import issue_energy_receipt,replay_energy_receipt


class EnergyReceiptTests(unittest.TestCase):
    def test_roundtrip_and_tampered_claim(self):
        t,x=S.symbols("t x")
        A=[S.Matrix([[x]])]
        sym=[[1+x*x]]
        B=[[0]]
        r=issue_energy_receipt((t,x),sym,A,B)
        self.assertEqual(r["status"],"PASS_LOCAL_ENERGY_IDENTITY__DOMAIN_UNVERIFIED")
        self.assertTrue(replay_energy_receipt((t,x),sym,A,B,r))
        self.assertFalse(r["global_pde_uniqueness_proven"])
        altered=dict(r)
        altered["global_pde_uniqueness_proven"]=True
        self.assertFalse(replay_energy_receipt((t,x),sym,A,B,altered))

    def test_changed_physical_coefficients_cannot_replay(self):
        t,x=S.symbols("t x")
        r=issue_energy_receipt((t,x),[[1]],[S.Matrix([[x]])],[[0]])
        self.assertFalse(replay_energy_receipt(
            (t,x),[[1]],[S.Matrix([[x+1]])],[[0]],r))


if __name__=="__main__":
    unittest.main()
