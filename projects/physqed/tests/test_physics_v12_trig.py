"""Regression: textbook spherical trigonometric conservation identity.

In spherical-coordinate Christoffel calculations SymPy's first simplify
can leave an exact identity unevaluated. A conservative two-route zero
gate must pass exact identity and refuse nearby wrong signs.
"""
import sys
import unittest
from pathlib import Path
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.geometry import zero
from v12.receipts import certify


class TrigConservationRegression(unittest.TestCase):
    def test_exact_conservation_expression(self):
        theta,r=S.symbols("theta r",real=True)
        q=(S.sin(2*theta)*S.tan(theta)+S.cos(2*theta)-1) / (
           16*r**4*S.sin(theta)**2*S.tan(theta))
        self.assertTrue(zero(q))
        receipt=certify("STD-SPHERE-TRIG-001","tensor",[(q,0)],
                        source="exact spherical-coordinate conservation identity",
                        assumptions=("r>0","0<theta<pi","theta!=pi/2"))
        self.assertIn("PASSED",receipt["status"])
        self.assertTrue(receipt["checks"][0]["exact_secondary_zero"])

    def test_wrong_sign_or_missing_term_refused(self):
        theta=S.symbols("theta")
        good=S.sin(2*theta)*S.tan(theta)+S.cos(2*theta)-1
        bad=S.sin(2*theta)*S.tan(theta)-S.cos(2*theta)-1
        self.assertTrue(zero(good))
        self.assertFalse(zero(bad))
        receipt=certify("STD-SPHERE-TRIG-NEG","tensor",[(bad,0)],
                        source="adversarial wrong-sign spherical identity")
        self.assertEqual(receipt["status"],"REJECTED")


if __name__=="__main__":
    unittest.main()
