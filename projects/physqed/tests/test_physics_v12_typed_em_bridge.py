"""Typed Einstein--Maxwell/ADM bridge: exact type/dimension/dynamics controls.

Execute the larger Reissner--Nordstrom test in its own Python process.
These tests are local mathematical model checks, not full physical theorems.
"""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import json
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.geometry import ScopeError
from v12.typed_input import execute_physics_input,load_physics_input
from v12.typed_input import plan_physics_obligations,replay_physics_input

ROOT=Path(__file__).resolve().parents[1]/"examples"/"typed"


def model(name="einstein_maxwell_flat.json"):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))


class TypedEinsteinMaxwellBridgeTests(unittest.TestCase):
    def test_flat_all_sixteen_linked(self):
        data=model()
        receipt=execute_physics_input(data)
        self.assertEqual(receipt["status"],"PASS_TYPED_EINSTEIN_MAXWELL_ADM__SCOPED")
        self.assertEqual(len(receipt["linked_obligations"]),16)
        self.assertEqual(len(receipt["coupled_contract"]["nodes"]),16)
        self.assertTrue(all(v["passed"] for v in receipt["coupled_contract"]["nodes"]))
        self.assertTrue(receipt["coupled_contract"]["independent_oracle"][0]["four_dimensional"]["passed"])
        self.assertTrue(receipt["coupled_contract"]["independent_oracle"][0]["three_dimensional"]["passed"])
        self.assertTrue(all(v["passed"] for v in receipt["physical_dimension_checks"]))
        self.assertEqual(len(receipt["tensor_index_signature_checks"]),5)
        self.assertFalse(receipt["physical_truth_proven"])
        self.assertFalse(receipt["global_theorem_proven"])
        self.assertFalse(receipt["full_SI_units_supported"])

    def test_nonflat_electrovacuum_reissner_nordstrom(self):
        data=model("einstein_maxwell_reissner_nordstrom.json")
        receipt=execute_physics_input(data)
        self.assertEqual(receipt["status"],"PASS_TYPED_EINSTEIN_MAXWELL_ADM__SCOPED")
        self.assertTrue(all(v["passed"] for v in receipt["coupled_contract"]["nodes"]))
        self.assertGreater(len(receipt["physical_dimension_checks"]),20)
        self.assertTrue(receipt["coupled_contract"]["independent_oracle"][0]["four_dimensional"]["passed"])
        self.assertTrue(receipt["coupled_contract"]["independent_oracle"][0]["three_dimensional"]["passed"])

    def test_wrong_electric_source_fails_physics_after_type_pass(self):
        data=model("einstein_maxwell_inconsistent_flat.json")
        result=execute_physics_input(data)
        self.assertEqual(result["status"],"REJECTED_LINKED_PHYSICS_OBLIGATIONS")
        self.assertTrue(all(x["passed"] for x in result["physical_dimension_checks"]))
        self.assertTrue(all(x["passed"] for x in result["tensor_index_signature_checks"]))
        self.assertFalse(next(v for v in result["coupled_contract"]["nodes"]
                         if v["name"]=="einstein_field_equation")["passed"])

    def test_plan_exposes_sixteen_but_does_not_prove(self):
        planned=plan_physics_obligations(load_physics_input(model()))
        self.assertEqual(len(planned),16)
        self.assertFalse(any(x["executed"] for x in planned))
        self.assertNotIn("passed",planned[0])

    def test_wrong_covariant_index_variance_refused(self):
        data=model()
        data["tensor_types"]["stress"]["variance"]="uu"
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_wrong_tensor_rank_refused(self):
        data=model()
        data["tensor_types"]["metric"]["rank"]=1
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_missing_unit_system_refused(self):
        data=model()
        data.pop("units")
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_dimensionally_inconsistent_potential_refused(self):
        data=model()
        # A_t should be L^(1-d_t)=L^0, whereas x is L.
        data["potential"][0]="x"
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_dimensionally_inconsistent_spherical_metric_refused(self):
        data=model("einstein_maxwell_reissner_nordstrom.json")
        data["metric"][2][2]=1  # theta-theta should have dimension L^2
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_wrong_parameter_dimension_refused(self):
        data=model("einstein_maxwell_reissner_nordstrom.json")
        data["units"]["parameters"]["M"]=0  # M/r no longer dimensionless
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_nontrivial_trigonometric_argument_dimension_refused(self):
        data=model("einstein_maxwell_reissner_nordstrom.json")
        data["metric"][3][3]={"mul":[{"pow":["r",2]},
                         {"pow":[{"func":{"name":"sin","arg":"r"}},2]}]}
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_nonzero_shift_refused_by_existing_ADM_backend(self):
        data=model()
        data["metric"][0][1]=1
        data["metric"][1][0]=1
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_claimed_hamiltonian_false_but_dimension_correct(self):
        data=model()
        data["parameters"]=["k"]
        data["units"]["parameters"]={"k":-2}
        data["parameter_values"]={"k":1}
        data["declared_hamiltonian"]="k"
        result=execute_physics_input(data)
        self.assertEqual(result["status"],"REJECTED_LINKED_PHYSICS_OBLIGATIONS")
        self.assertFalse(next(v for v in result["coupled_contract"]["nodes"]
             if v["name"]=="claimed_hamiltonian_agreement")["passed"])

    def test_wrong_cosmological_constant_dimension_refused(self):
        data=model()
        data["cosmological_constant"]="t"
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_tampered_linked_receipt_refused_by_full_replay(self):
        data=model()
        correct=execute_physics_input(data)
        self.assertTrue(replay_physics_input(data,correct))
        altered=deepcopy(correct)
        altered["tensor_index_signature_checks"][0]["passed"]=False
        self.assertFalse(replay_physics_input(data,altered))


if __name__=="__main__":
    unittest.main()
