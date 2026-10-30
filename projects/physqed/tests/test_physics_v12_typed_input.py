"""PHYSQED typed-input safety, mathematical and adversarial tests.

These test a bounded structured JSON grammar and its generated exact
obligations, not unrestricted scientific claims. 2026 v1.2 release gate.
"""
import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.typed_input import (SCHEMA, load_physics_input, plan_physics_obligations,
                              execute_physics_input, replay_physics_input)
from v12.geometry import ScopeError


def common(kind, coords, claims):
    return {"schema":SCHEMA,"kind":kind,
            "claim_id":"STANDARD_"+kind.upper(),
            "source":"standard textbook control",
            "coordinates":coords,
            "assumptions":["explicit regular coordinate chart"],
            "claims":claims}


def minkowski():
    d=common("metric",["t","x","y","z"],
             ["metric_compatibility","first_bianchi",
              "contracted_bianchi","vacuum_einstein"])
    d["metric"]=[[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    return d


def flrw_wrong_vacuum():
    d=common("metric",["t","x","y","z"],["vacuum_einstein"])
    a={"add":[1,{"pow":["t",2]}]}
    gii={"pow":[a,2]}
    d["metric"]=[[-1,0,0,0],[0,gii,0,0],[0,0,gii,0],[0,0,0,gii]]
    return d


def kg():
    d=common("lagrangian",["t","x"],
             ["euler_lagrange","translation_noether"])
    d["parameters"]=["m"]
    d["fields"]=["phi"]
    dt={"derivative":["phi","t"]}
    dx={"derivative":["phi","x"]}
    mphi2={"mul":[{"pow":["m",2]},{"pow":["phi",2]}]}
    d["lagrangian"]={"mul":[{"rational":[1,2]},
                 {"add":[{"pow":[dt,2]},
                         {"neg":{"pow":[dx,2]}},
                         {"neg":mphi2}]}]}
    d["expected_eom"]=[{"add":[
        {"neg":{"derivative":["phi","t",2]}},
        {"derivative":["phi","x",2]},
        {"neg":{"mul":[{"pow":["m",2]},"phi"]}}]}]
    return d


def oscillator():
    d=common("hamiltonian",["t"],
             ["hamilton_equations","poisson_jacobi"])
    d["positions"]=["q"]; d["momenta"]=["p"]
    d["hamiltonian"]={"mul":[{"rational":[1,2]},
                    {"add":[{"pow":["q",2]},{"pow":["p",2]}]}]}
    d["expected_dq"]=["p"]
    d["expected_dp"]=[{"neg":"q"}]
    d["jacobi_test"]=["q","p",d["hamiltonian"]]
    return d


def electromagnetism():
    d=common("gauge",["t","x"],
             ["gauge_bianchi","yang_mills_vacuum"])
    d["algebra"]="u1"
    d["connection"]=[[0],["t"]]
    d["metric"]=[[-1,0],[0,1]]
    return d


class TypedPhysicsTests(unittest.TestCase):
    def test_metric_minkowski_four_obligations(self):
        result=execute_physics_input(json.dumps(minkowski()))
        self.assertTrue(result["status"].startswith("PASS_SCOPED_"))
        self.assertEqual(len(result["checks"]),4)
        self.assertTrue(all(x["passed"] for x in result["checks"]))
        self.assertFalse(result["physical_truth_proven"])
        self.assertFalse(result["lean_kernel_verified"])

    def test_flrw_false_vacuum_refused(self):
        result=execute_physics_input(flrw_wrong_vacuum())
        self.assertEqual(result["status"],"REJECTED_UNSATISFIED_PHYSICS_OBLIGATION")
        self.assertFalse(result["checks"][0]["passed"])

    def test_lagrangian_euler_lagrange_and_noether(self):
        result=execute_physics_input(kg())
        self.assertTrue(result["status"].startswith("PASS_SCOPED_"))
        self.assertEqual(len(result["checks"]),2)

    def test_lagrangian_wrong_sign_refused(self):
        data=kg()
        data["expected_eom"]=[{"derivative":["phi","t",2]}]
        result=execute_physics_input(data)
        self.assertFalse(result["checks"][0]["passed"])

    def test_explicit_coordinate_dependent_noether_refused(self):
        data=kg()
        data["claims"]=["translation_noether"]
        data.pop("expected_eom")
        data["lagrangian"]={"mul":["t",{"pow":[{"derivative":["phi","t"]},2]}]}
        self.assertFalse(execute_physics_input(data)["checks"][0]["passed"])

    def test_oscillator_hamilton_equations_and_jacobi(self):
        result=execute_physics_input(oscillator())
        self.assertTrue(result["status"].startswith("PASS_SCOPED_"))
        self.assertEqual(len(result["checks"]),2)

    def test_hamilton_wrong_velocity_refused(self):
        data=oscillator()
        data["expected_dq"]=[{"neg":"p"}]
        self.assertFalse(execute_physics_input(data)["checks"][0]["passed"])

    def test_gauge_maxwell_bianchi_and_sourcefree_equations(self):
        result=execute_physics_input(electromagnetism())
        self.assertTrue(result["status"].startswith("PASS_SCOPED_"))

    def test_gauge_nonflat_connection_refused(self):
        data=electromagnetism()
        data["claims"]=["flat_connection"]
        self.assertFalse(execute_physics_input(data)["checks"][0]["passed"])

    def test_nonabelian_constant_connection_not_yang_mills_vacuum(self):
        data=common("gauge",["t","x"],["gauge_bianchi","yang_mills_vacuum"])
        data["algebra"]="so3"
        data["connection"]=[[1,0,0],[0,1,0]]
        data["metric"]=[[-1,0],[0,1]]
        result=execute_physics_input(data)
        self.assertTrue(result["checks"][0]["passed"])
        self.assertFalse(result["checks"][1]["passed"])

    def test_tampering_refused_on_full_replay(self):
        data=oscillator()
        receipt=execute_physics_input(data)
        self.assertTrue(replay_physics_input(data,receipt))
        tampered=copy.deepcopy(receipt)
        tampered["checks"][0]["passed"]=False
        self.assertFalse(replay_physics_input(data,tampered))

    def test_duplicate_json_keys_refused(self):
        original=json.dumps(minkowski())
        hostile=original[:-1] + ', "kind": "hamiltonian"}'
        with self.assertRaises(ScopeError):
            load_physics_input(hostile)

    def test_unsupported_derivative_ast_structure_refused(self):
        data=kg()
        data["lagrangian"]={"derivative":[["phi"],"t"]}
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_no_premature_certificate_on_plan(self):
        plan=plan_physics_obligations(load_physics_input(minkowski()))
        self.assertTrue(all("comparison" in obligation for obligation in plan))
        self.assertFalse(any("passed" in obligation for obligation in plan))

    def test_unknown_symbols_and_code_strings_refused(self):
        data=oscillator()
        data["hamiltonian"]="__import__('os').system('echo unsafe')"
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_unknown_expression_function_refused(self):
        data=oscillator()
        data["hamiltonian"]={"func":{"name":"eval","arg":"q"}}
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_unknown_theorem_refused_at_load(self):
        data=minkowski()
        data["claims"]=["unrestricted_quantum_gravity"]
        with self.assertRaises(ScopeError):
            load_physics_input(data)

    def test_malformed_nested_claim_refused(self):
        data=minkowski()
        data["claims"]=[{"exploit":"object"}]
        with self.assertRaises(ScopeError):
            load_physics_input(data)

    def test_unknown_physics_fields_refused(self):
        data=oscillator()
        data["arbitrary_code"]="print('oops')"
        with self.assertRaises(ScopeError):
            load_physics_input(data)

    def test_wrong_input_operators_rejected(self):
        data=oscillator()
        data["hamiltonian"]={"pow":["q",100000]}
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_missing_hamiltonian_equations_refused(self):
        data=oscillator()
        data.pop("expected_dp")
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_missing_field_target_refused(self):
        data=kg()
        data.pop("expected_eom")
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_invalid_two_dimensional_einstein_physics_claim_refused(self):
        data=common("metric",["x","y"],["vacuum_einstein"])
        data["metric"]=[[1,0],[0,1]]
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_missing_stress_refused_for_einstein_source(self):
        data=minkowski()
        data["claims"]=["einstein_source"]
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_missing_domain_assumptions_refused(self):
        data=minkowski()
        data["assumptions"]=[]
        with self.assertRaises(ScopeError):
            load_physics_input(data)

    def test_duplicate_coordinates_and_parameter_names_refused(self):
        data=oscillator()
        data["parameters"]=["t"]
        with self.assertRaises(ScopeError):
            load_physics_input(data)

    def test_reject_json_float_in_matrix(self):
        data=minkowski()
        data["metric"][0][0]=-1.0
        with self.assertRaises(ScopeError):
            execute_physics_input(data)

    def test_provenance_and_plan_separate_from_proof(self):
        spec=load_physics_input(oscillator())
        plan=plan_physics_obligations(spec)
        self.assertEqual(tuple(x["claim"] for x in plan),
                         ("hamilton_equations","poisson_jacobi"))
        self.assertEqual(plan[0]["category"],"asserted_dynamics")
        self.assertEqual(plan[1]["category"],"structural_identity")


if __name__=="__main__":
    unittest.main()
