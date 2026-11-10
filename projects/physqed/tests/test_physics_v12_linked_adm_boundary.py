"""Linked 18-node shifted Einstein--Maxwell and exact boundary compatibility.

Tests assert the distinction between one-direction positive flux and
maximal nonnegative boundary trace rank; no nonlinear IBVP claims.
"""
import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.linked_adm_boundary import (
    certify_linked_adm_boundary, replay_linked_adm_boundary, DomainScopeError)

ROOT=Path(__file__).resolve().parents[1]/"examples"/"typed"

def read(name="linked_adm_shifted_minkowski.json"):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))


class LinkedADMBoundaryTests(unittest.TestCase):
    def test_explicit_shifted_vacuum_solution_and_maximal_flux_faces(self):
        result=certify_linked_adm_boundary(read())
        self.assertEqual(result["status"],
            "PASS_LINKED_EXACT_MODEL_AND_CONDITIONAL_CONSTRAINT_ENERGY")
        self.assertTrue(result["all_18_field_nodes_passed"])
        self.assertEqual(len(result["field_contract"]["shifted_contract"]["nodes"]),18)
        self.assertTrue(result["uniform_interior_energy_bounds_passed"])
        self.assertTrue(result["all_face_flux_forms_passed"])
        self.assertTrue(result["maximal_nonnegative_constraint_trace_spaces_passed"])
        faces=result["compatibility"]["faces"]
        self.assertEqual(len(faces),6)
        sizes={v["name"]:v["expected_maximal_dimension"] for v in faces}
        self.assertEqual(sizes,{"x_lower":3,"x_upper":1,
             "y_lower":3,"y_upper":3,"z_lower":3,"z_upper":3})
        self.assertTrue(all(v["rank_certificate"]["passed"] for v in faces))
        self.assertTrue(all(v["inertia"]["constant_boundary_inertia_proven"]
                            for v in faces))
        self.assertFalse(result["smooth_constraint_solution_existence_proven"])
        self.assertFalse(result["nonlinear_Einstein_IBVP_well_posedness_proven"])

    def test_undercomplete_positive_flux_is_not_maximal(self):
        result=certify_linked_adm_boundary(read(
            "linked_adm_undercomplete_boundary.json"))
        self.assertTrue(result["all_18_field_nodes_passed"])
        self.assertTrue(result["all_face_flux_forms_passed"])
        self.assertFalse(result["maximal_nonnegative_constraint_trace_spaces_passed"])
        self.assertFalse(next(f for f in result["compatibility"]["faces"]
            if f["name"]=="x_lower")["dimension_matched"])

    def test_source_mismatch_rejected_before_any_field_claim(self):
        with self.assertRaises(DomainScopeError):
            certify_linked_adm_boundary(read("linked_adm_mismatched_geometry.json"))

    def test_unconserved_maxwell_stress_prevents_joint_pass(self):
        result=certify_linked_adm_boundary(read(
            "linked_adm_unconserved_matter.json"))
        self.assertFalse(result["all_18_field_nodes_passed"])
        self.assertTrue(result["uniform_interior_energy_bounds_passed"])
        self.assertEqual(result["status"],"REJECTED_OR_INCONCLUSIVE_LINKED_OBLIGATIONS")

    def test_incoming_trace_flux_rejects_joint_contract(self):
        case=read()
        case["domain_model"]["boundary_frames"]["x_upper"]=[[1,{"rational":[1,2]},0,0]]
        result=certify_linked_adm_boundary(case)
        self.assertFalse(result["all_face_flux_forms_passed"])
        self.assertFalse(result["maximal_nonnegative_constraint_trace_spaces_passed"])

    def test_rank_deficient_three_column_face(self):
        case=read()
        frame=case["domain_model"]["boundary_frames"]["x_lower"]
        frame[2]=copy.deepcopy(frame[1])
        result=certify_linked_adm_boundary(case)
        self.assertFalse(result["maximal_nonnegative_constraint_trace_spaces_passed"])
        self.assertFalse(next(f for f in result["compatibility"]["faces"]
             if f["name"]=="x_lower")["rank_certificate"]["passed"])

    def test_hidden_original_metric_pole_not_accepted(self):
        case=read()
        base={"mul":[{"rational":[1,2]},"t"]}  # length-consistent; pole at t=0
        cancel={"mul":[base,{"pow":[base,-1]}]}
        case["field_model"]["lapse"]=cancel
        case["domain_model"]["lapse"]=copy.deepcopy(cancel)
        result=certify_linked_adm_boundary(case)
        self.assertTrue(result["all_18_field_nodes_passed"])
        self.assertFalse(result["uniform_interior_energy_bounds_passed"])
        self.assertFalse(result["domain_contract"]["all_source_guards_certified"])

    def test_cancelled_electromagnetic_source_pole_refused(self):
        case=read()
        base={"mul":[{"rational":[1,2]},"t"]}  # length-consistent; pole at t=0
        case["field_model"]["potential"][0]={
             "mul":[base,{"pow":[base,-1]}]}
        result=certify_linked_adm_boundary(case)
        self.assertFalse(result["matter_source_domain"]["passed"])
        self.assertEqual(result["matter_source_domain"]["guard_count"],1)
        self.assertEqual(result["status"],
                         "REJECTED_OR_INCONCLUSIVE_LINKED_OBLIGATIONS")

    def test_negative_growth_declaration_refused(self):
        case=read()
        case["domain_model"]["energy_growth"]=-1
        with self.assertRaises(DomainScopeError):
            certify_linked_adm_boundary(case)

    def test_periodic_assumption_does_not_prove_frame_compatibility(self):
        case=read()
        case["domain_model"]["boundary_mode"]="periodic_assumed"
        case["domain_model"]["boundary_frames"]={}
        result=certify_linked_adm_boundary(case)
        self.assertTrue(result["uniform_interior_energy_bounds_passed"])
        self.assertFalse(result["maximal_nonnegative_constraint_trace_spaces_passed"])

    def test_tampered_receipt_replay_and_changed_input(self):
        case=read()
        result=certify_linked_adm_boundary(case)
        self.assertTrue(replay_linked_adm_boundary(case,result))
        tampered=copy.deepcopy(result)
        tampered["nonlinear_Einstein_IBVP_well_posedness_proven"]=True
        self.assertFalse(replay_linked_adm_boundary(case,tampered))
        altered=copy.deepcopy(case)
        altered["domain_model"]["energy_coercivity"]=2
        self.assertFalse(replay_linked_adm_boundary(altered,result))

    def test_characteristic_zero_speed_faces_are_not_called_noncharacteristic(self):
        result=certify_linked_adm_boundary(read())
        for face in result["compatibility"]["faces"]:
            if face["name"][0] in "yz":
                self.assertTrue(face["inertia"]["characteristic_boundary"])
                self.assertEqual(face["inertia"]["outward_shift_sign"],"zero")
            else:
                self.assertFalse(face["inertia"]["characteristic_boundary"])


if __name__=="__main__":
    unittest.main()
