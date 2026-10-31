"""Scope-controlled finite triangle-finding benchmark.

No O(n) quantum query claim: this checks Boolean formulas and an elementary
phase-polynomial identity, not a quantum black-box algorithm. Uses SymPy only.
"""
import itertools
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import sympy as S
from v12.receipts import certify


def triangle_boolean(n,bits):
    ed={(i,j):bits[k] for k,(i,j) in enumerate(itertools.combinations(range(n),2))}
    expression=1
    for i,j,k in itertools.combinations(range(n),3):
        expression*=1-ed[i,j]*ed[i,k]*ed[j,k]
    return 1-expression


def direct_triangle(n,bits):
    ed={(i,j):bits[k] for k,(i,j) in enumerate(itertools.combinations(range(n),2))}
    return int(any(ed[i,j]*ed[i,k]*ed[j,k]==1
                   for i,j,k in itertools.combinations(range(n),3)))


class TriangleQueryScope(unittest.TestCase):
    def test_all_graphs_through_six_vertices(self):
        for n in (3,4,5,6):
            m=n*(n-1)//2
            for mask in range(1<<m):
                bits=tuple(mask>>k&1 for k in range(m))
                self.assertEqual(triangle_boolean(n,bits),direct_triangle(n,bits))

    def test_phase_parity_identity_and_negative_receipt(self):
        x,y,z=S.symbols("x y z")
        xor=lambda a,b:a+b-2*a*b
        parity=x+y+z-xor(x,y)-xor(x,z)-xor(y,z)+xor(xor(x,y),z)
        positive=certify("TRIANGLE-CCZ-PHASE-EXACT","quantum",
                 [(parity,4*x*y*z)],source="Boolean edge-bit phase identity",
                 assumptions=("x,y,z in {0,1} for Boolean XOR interpretation",))
        negative=certify("TRIANGLE-CCZ-PHASE-WRONG","quantum",
                 [(parity,4*x*y*z+1)],source="deliberately wrong phase identity")
        self.assertEqual(positive["status"],
                  "EXACT_SYMBOLIC_COMPONENTS_PASSED__PHYSICS_UNVERIFIED")
        self.assertEqual(negative["status"],"REJECTED")
        self.assertFalse(positive["physical_law_proven"])

    def test_naive_triangle_count_is_not_presence(self):
        bits=(1,)*6  # complete graph K4: 4 triangles but presence is 1
        self.assertEqual(triangle_boolean(4,bits),1)
        self.assertEqual(direct_triangle(4,bits),1)
        self.assertEqual(sum(1 for _ in itertools.combinations(range(4),3)),4)


if __name__=="__main__":
    unittest.main()
