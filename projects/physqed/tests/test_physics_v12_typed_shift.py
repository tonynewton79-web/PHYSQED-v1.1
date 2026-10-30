"""Typed nonzero shift/constraint propagation JSON integration tests.

The old zero-shift Einstein--Maxwell contract remains unchanged.
The shifted contract never labels off-shell Bianchi identities as solutions.
"""
import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.geometry import ScopeError
from v12.typed_input import (load_physics_input,plan_physics_obligations,
                              execute_physics_input,replay_physics_input)

ROOT=Path(__file__).resolve().parents[1]/"examples"/"typed"

def fixture(name):
    return json.loads((ROOT/name).read_text())


class TypedShiftedADMTests(unittest.TestCase):
    def test_time_dependent_shifted_minkowski_full_contract(self):
        model=fixture("einstein_maxwell_shifted_flat.json")
        result=execute_physics_input(model)
        self.assertEqual(result["status"],"PASS_TYPED_SHIFTED_ADM__SCOPED")
        self.assertEqual(len(result["linked_obligations"]),14)
        self.assertEqual(len(result["index_type_checks"]),6)
        self.assertTrue(all(x["passed"] for x in result["unit_component_checks"]))
        shifted=result["shifted_contract"]
        self.assertTrue(shifted["homogeneous_constraint_propagation_identities_passed"])
        self.assertTrue(shifted["oracle_passed"])
        self.assertFalse(shifted["global_constraint_propagation_theorem_proven"])

    def test_offshell_shift_retains_bianchi_but_refuses_field_equations(self):
        model=fixture("einstein_maxwell_shifted_offshell.json")
        result=execute_physics_input(model)
        self.assertEqual(result["status"],"REJECTED_TYPED_SHIFTED_ADM")
        checks={v["name"]:v["passed"] for v in result["shifted_contract"]["nodes"]}
        self.assertTrue(checks["gauss_hamiltonian_bridge"])
        self.assertTrue(checks["codazzi_momentum_bridge"])
        self.assertTrue(checks["hamiltonian_propagation_bridge"])
        self.assertTrue(checks["momentum_propagation_bridge"])
        self.assertFalse(checks["einstein_full"])
        self.assertFalse(result["shifted_contract"]["homogeneous_constraint_propagation_identities_passed"])

    def test_shift_dimension_wrong_refused_before_equations(self):
        with self.assertRaises(ScopeError):
            execute_physics_input(fixture("einstein_maxwell_shifted_invalid_dimension.json"))

    def test_covariant_shift_signature_refused(self):
        model=fixture("einstein_maxwell_shifted_flat.json")
        model["shift_type"]["variance"]="d"
        with self.assertRaises(ScopeError):
            execute_physics_input(model)

    def test_shift_missing_declared_refused(self):
        model=fixture("einstein_maxwell_shifted_flat.json")
        del model["shift"]
        with self.assertRaises(ScopeError):
            execute_physics_input(model)

    def test_wrong_spatial_metric_units_refused(self):
        model=fixture("einstein_maxwell_shifted_flat.json")
        model["spatial_metric"][1][1]="tau"  # L vs required L^0
        with self.assertRaises(ScopeError):
            execute_physics_input(model)

    def test_wrong_shift_rank_refused(self):
        model=fixture("einstein_maxwell_shifted_flat.json")
        model["shift_type"]["rank"]=2
        with self.assertRaises(ScopeError):
            execute_physics_input(model)

    def test_planning_is_not_execution(self):
        plan=plan_physics_obligations(
            load_physics_input(fixture("einstein_maxwell_shifted_flat.json")))
        self.assertEqual(len(plan),14)
        self.assertTrue(all(x["executed"] is False for x in plan))
        self.assertNotIn("passed",plan[0])

    def test_receipt_tampering_caught_by_recomputation(self):
        model=fixture("einstein_maxwell_shifted_flat.json")
        receipt=execute_physics_input(model)
        self.assertTrue(replay_physics_input(model,receipt))
        altered=copy.deepcopy(receipt)
        altered["shifted_contract"]["nodes"][0]["passed"]=False
        self.assertFalse(replay_physics_input(model,altered))


if __name__=="__main__":
    unittest.main()
