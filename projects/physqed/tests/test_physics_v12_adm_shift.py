"""Nonzero ADM shift and constraint-propagation contract regressions.

Tests distinguish Gauss/Codazzi geometry, full field equations,
spatial Einstein evolution and off-shell Bianchi propagation.
Run methods in fresh interpreters for expensive symbolic curved tests.
"""
import sys
import unittest
from dataclasses import replace
from pathlib import Path
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.geometry import ScopeError,zero
from v12.adm_shift import ShiftedEinsteinMaxwellSpec,evaluate_shifted_einstein_maxwell,replay_shifted_adm


def flat_shift():
    t,x,y,z=S.symbols("t x y z",real=True)
    return ShiftedEinsteinMaxwellSpec(
        claim_id="SHIFTED_FLAT", coordinates=(t,x,y,z),
        spatial_metric=S.eye(3),lapse=1,
        shift=(t,0,0),potential=(0,0,0,0),
        witnesses=({t:S.Rational(1,2),x:0,y:0,z:0},),
        assumptions=("Cartesion reparameterized flat chart",
                     "future normal and positive extrinsic curvature convention"))


def offshell_shift():
    t,x,y,z=S.symbols("t x y z",real=True)
    # A time/space dependent spatial geometry with genuinely nontrivial
    # shift, momentum constraint and nonzero spatial evolution residual.
    a=1+t*x
    return ShiftedEinsteinMaxwellSpec(
        claim_id="SHIFTED_OFFSHELL",coordinates=(t,x,y,z),
        spatial_metric=S.diag(1,a*a,1),lapse=1,
        shift=(t/3,0,0),potential=(0,0,0,0),
        witnesses=({t:S.Rational(1,2),x:S.Rational(1,3),y:0,z:0},),
        assumptions=("local a>0 chart","off-shell diagnostic only"))


def node(receipt,name):
    return next(v for v in receipt["nodes"] if v["name"]==name)


class ShiftedADMTests(unittest.TestCase):
    def test_time_dependent_nonzero_shift_flat_solution(self):
        r=evaluate_shifted_einstein_maxwell(flat_shift())
        self.assertEqual(r["status"],"PASS_SCOPED_SHIFTED_EINSTEIN_MAXWELL")
        self.assertTrue(all(v["passed"] for v in r["nodes"]))
        self.assertTrue(r["homogeneous_constraint_propagation_identities_passed"])
        self.assertTrue(r["trace_reversed_hyperbolic_constraint_closure_passed"])
        self.assertTrue(r["symmetric_hyperbolic_principal_symbol_verified"])
        self.assertEqual(len(r["nodes"]),18)
        self.assertTrue(r["independent_oracle"][0]["four_dimensional"]["passed"])
        self.assertTrue(r["independent_oracle"][0]["three_dimensional"]["passed"])
        self.assertFalse(r["global_constraint_propagation_theorem_proven"])

    def test_spatially_dependent_shift_offshell_bianchi(self):
        r=evaluate_shifted_einstein_maxwell(offshell_shift())
        self.assertTrue(node(r,"gauss_hamiltonian_bridge")["passed"])
        self.assertTrue(node(r,"codazzi_momentum_bridge")["passed"])
        self.assertTrue(node(r,"einstein_stress_bianchi_bridge")["passed"])
        self.assertTrue(node(r,"hamiltonian_propagation_bridge")["passed"])
        self.assertTrue(node(r,"momentum_propagation_bridge")["passed"])
        self.assertTrue(node(r,"hamiltonian_hyperbolic_propagation_bridge")["passed"])
        self.assertTrue(node(r,"momentum_hyperbolic_propagation_bridge")["passed"])
        self.assertTrue(node(r,"principal_symbol_symmetrizer")["passed"])
        self.assertTrue(r["independent_oracle"][0]["four_dimensional"]["passed"])
        self.assertFalse(node(r,"einstein_full")["passed"])
        self.assertFalse(node(r,"spatial_einstein_evolution")["passed"])
        self.assertFalse(r["homogeneous_constraint_propagation_identities_passed"])

    def test_shifted_minkowski_with_spatial_shift_gradient(self):
        t,x,y,z=S.symbols("t x y z",real=True)
        # yphys=(1+t)*x: metric hxx=(1+t)^2,
        # beta^x=x/(1+t).  This is flat despite nonzero partial_x beta.
        a=1+t
        case=ShiftedEinsteinMaxwellSpec(
            "SHIFTED_NONTRIVIAL_FLAT",(t,x,y,z),S.diag(a*a,1,1),
            1,(x/a,0,0),(0,0,0,0),
            ({t:0,x:S.Rational(1,3),y:0,z:0},),
            ("t>-1 regular coordinate transformation",))
        r=evaluate_shifted_einstein_maxwell(case)
        self.assertEqual(r["status"],"PASS_SCOPED_SHIFTED_EINSTEIN_MAXWELL")
        self.assertTrue(node(r,"gauss_hamiltonian_bridge")["passed"])
        self.assertTrue(node(r,"momentum_propagation_bridge")["passed"])

    def test_invalid_negative_lapse_witness_refused(self):
        with self.assertRaises(ScopeError):
            evaluate_shifted_einstein_maxwell(replace(flat_shift(),lapse=-1))

    def test_invalid_indefinite_spatial_witness_refused(self):
        with self.assertRaises(ScopeError):
            evaluate_shifted_einstein_maxwell(replace(flat_shift(),
                spatial_metric=S.diag(-1,1,1)))

    def test_wrong_shift_dimension_refused(self):
        with self.assertRaises(ScopeError):
            evaluate_shifted_einstein_maxwell(replace(flat_shift(),shift=(1,2)))

    def test_recompute_receipt_rejects_tampering(self):
        case=flat_shift()
        receipt=evaluate_shifted_einstein_maxwell(case)
        self.assertTrue(replay_shifted_adm(case,receipt))
        tampered=dict(receipt,status="PASS_OMNIPOTENT_QUANTUM_GRAVITY")
        self.assertFalse(replay_shifted_adm(case,tampered))


if __name__=="__main__":
    unittest.main()
