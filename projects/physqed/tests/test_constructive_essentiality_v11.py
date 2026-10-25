"""PHYSQED v1.1 rational missing-premise witnesses, independently re-evaluated."""
import sys
import unittest
from fractions import Fraction as Q
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/"projects"/"physqed"))
sys.path.insert(0,str(ROOT/"research"/"physqed-multi-premise-v10"))
from constructive_essentiality_v11 import (
    verify_and_construct,constructive_witnesses,WitnessRefusal)
from benchmarks.multi_premise_v10 import specimen
from independent_oracle import formal

class ConstructiveEssentialityV11Tests(unittest.TestCase):
    def test_all_80_v10_positive_specimens_have_independently_validated_points(self):
        counts={3:0,4:0}
        for index in range(80):
            contract=specimen(index)
            result=verify_and_construct(contract)
            k=len(contract["premises"])
            self.assertEqual(result["premise_count"],k)
            self.assertEqual(len(result["counterexamples"]),k)
            counts[k]+=1
            self.assertFalse(result["physical_law_proven"])
            self.assertFalse(result["lean_kernel_verified"])
            symbols={v:S.Symbol(v) for v in contract["variables"]}
            equations=[S.expand(formal(p["lhs"],symbols)-formal(p["rhs"],symbols))
                       for p in contract["premises"]]
            target=S.expand(formal(contract["conclusion"]["lhs"],symbols)-
                            formal(contract["conclusion"]["rhs"],symbols))
            for witness in result["counterexamples"]:
                missing=witness["dropped_premise"]-1
                at={S.Symbol(name):S.Rational(v)
                    for name,v in witness["assignment"].items()}
                self.assertNotEqual(S.expand(target.subs(at)),0)
                self.assertNotEqual(S.expand(equations[missing].subs(at)),0)
                for j,p in enumerate(equations):
                    if j!=missing:
                        self.assertEqual(S.expand(p.subs(at)),0)
        self.assertEqual(counts,{3:40,4:40})

    def test_two_premise_energy_flow_model(self):
        # Normalized two-stage ideal energy-flow model (math conditional).
        names=["input","middle","output"]
        premises=[{(1,0,0):Q(1),(0,1,0):Q(-1)},
                  {(0,1,0):Q(1),(0,0,1):Q(-1)}]
        conclusion={(1,0,0):Q(1),(0,0,1):Q(-1)}
        result=constructive_witnesses(names,premises,conclusion)
        self.assertEqual(len(result),2)
        self.assertTrue(all(Q(x["conclusion_residual"])!=0 for x in result))

    def test_nonessential_assumption_refused(self):
        p=[{(1,0,0):Q(1)},{(0,1,0):Q(1)},{(0,0,1):Q(1)}]
        with self.assertRaisesRegex(WitnessRefusal,"not essential"):
            constructive_witnesses(["x","y","z"],p,p[0])

    def test_dependent_subsystem_refused(self):
        p=[{(1,0,0):Q(1)},{(1,0,0):Q(1)},{(0,0,1):Q(1)}]
        with self.assertRaises(WitnessRefusal):
            constructive_witnesses(["x","y","z"],p,
                {(1,0,0):Q(2),(0,0,1):Q(1)})

    def test_nonlinear_premise_refused(self):
        p=[{(2,0,0):Q(1)},{(0,1,0):Q(1)}]
        with self.assertRaises(WitnessRefusal):
            constructive_witnesses(["x","y","z"],p,
                {(2,0,0):Q(1),(0,1,0):Q(1)})

if __name__=="__main__":
    unittest.main()
