"""Typed source-domain, global box geometry, and boundary flux gate tests.

No result proves the existence of a solution satisfying the trace
subspaces or the Einstein equations. CI tests exact coefficient claims.
"""
import copy
import json
import sys
import unittest
from pathlib import Path
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.typed_adm_domain import (
    certify_typed_adm_domain,replay_typed_adm_domain,
    parse_rational_sources,DomainScopeError)

ROOT=Path(__file__).resolve().parents[1]/"examples"/"typed"


def example(name="adm_domain_outgoing_flux.json"):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))


class TypedDomainTests(unittest.TestCase):
    def test_all_face_fluxes_and_geometry_certified(self):
        r=certify_typed_adm_domain(example())
        self.assertEqual(r["status"],
            "PASS_INTERIOR_AND_CONDITIONAL_BOUNDARY_ALGEBRA__PDE_ASSUMPTIONS_PENDING")
        self.assertTrue(r["all_source_guards_certified"])
        self.assertTrue(r["geometric_bounds"]["passed"])
        self.assertTrue(r["interior_domain_bounds_proven"])
        self.assertTrue(r["conditional_boundary_flux_algebra_proven"])
        self.assertEqual(len(r["boundary_flux"]["faces"]),6)
        self.assertTrue(all(f["passed"] for f in r["boundary_flux"]["faces"]))
        self.assertFalse(r["boundary_trace_conditions_satisfied_by_solution_proven"])
        self.assertFalse(r["evolution_solution_existence_proven"])
        self.assertFalse(r["global_constraint_propagation_theorem_proven"])

    def test_original_cancelled_pole_remains_an_obligation(self):
        r=certify_typed_adm_domain(example("adm_domain_hidden_pole.json"))
        self.assertGreater(r["source_guard_count"],0)
        self.assertTrue(r["source_guard_original_ast"])
        self.assertFalse(r["all_source_guards_certified"])
        self.assertFalse(r["interior_domain_bounds_proven"])
        self.assertEqual(r["status"],"INCONCLUSIVE_OR_UNVERIFIED_DOMAIN_OBLIGATIONS")

    def test_incoming_flux_sign_refused(self):
        r=certify_typed_adm_domain(example("adm_domain_incoming_flux.json"))
        self.assertTrue(r["geometric_bounds"]["passed"])
        self.assertTrue(r["interior_domain_bounds_proven"])
        self.assertFalse(r["conditional_boundary_flux_algebra_proven"])
        self.assertFalse(next(f for f in r["boundary_flux"]["faces"]
                         if f["name"]=="x_upper")["passed"])

    def test_source_ast_nontrivial_nested_negative_powers_recorded(self):
        ast={"mul":[{"pow":[{"add":["t",1]},-1]},
                    {"pow":[{"add":["t",2]},-2]}]}
        parsed=parse_rational_sources(("t","x","y","z"),[ast])
        self.assertEqual(len(parsed["guard_expressions"]),2)
        self.assertTrue(parsed["provenance_complete_for_supplied_AST"])
        self.assertEqual(parsed["guard_exponents"],(-1,-2))

    def test_source_zero_denominator_is_never_silently_accepted(self):
        ast={"mul":[{"add":["t",-1]},
                    {"pow":[{"add":["t",-1]},-1]}]}
        parsed=parse_rational_sources(("t","x","y","z"),[ast])
        self.assertEqual(parsed["values"],(S.Integer(1),))
        self.assertEqual(len(parsed["guard_expressions"]),1)

    def test_reject_nonrational_sqrt_ast_before_backend(self):
        with self.assertRaises(DomainScopeError):
            parse_rational_sources(("t","x","y","z"),
                [{"func":{"name":"sqrt","arg":"t"}}])

    def test_reject_unsafe_unparsed_expression_string(self):
        with self.assertRaises(Exception):
            parse_rational_sources(("t","x","y","z"),
                ["__import__('os').system('echo unsafe')"])

    def test_negative_lapse_cannot_receive_geometry_certificate(self):
        v=example()
        v["lapse"]=-1
        r=certify_typed_adm_domain(v)
        self.assertFalse(r["geometric_bounds"]["passed"])
        self.assertFalse(r["interior_domain_bounds_proven"])

    def test_indefinite_spatial_metric_is_refused(self):
        v=example()
        v["spatial_metric"][1][1]=-1
        r=certify_typed_adm_domain(v)
        self.assertFalse(r["geometric_bounds"]["passed"])

    def test_spatial_metric_floor_too_high_inconclusive(self):
        v=example()
        v["metric_floor"]=2
        r=certify_typed_adm_domain(v)
        self.assertFalse(r["geometric_bounds"]["passed"])
        self.assertEqual(r["status"],"INCONCLUSIVE_OR_UNVERIFIED_DOMAIN_OBLIGATIONS")

    def test_boundary_periodic_coefficients_only_conditional(self):
        v=example()
        v["boundary_mode"]="periodic_assumed"
        v["boundary_frames"]={}
        r=certify_typed_adm_domain(v)
        self.assertTrue(r["boundary_flux"]["passed"])
        self.assertFalse(r["boundary_trace_conditions_satisfied_by_solution_proven"])

    def test_undeclared_boundary_does_not_prove_flux(self):
        v=example()
        v["boundary_mode"]="unverified"
        v["boundary_frames"]={}
        r=certify_typed_adm_domain(v)
        self.assertTrue(r["interior_domain_bounds_proven"])
        self.assertFalse(r["conditional_boundary_flux_algebra_proven"])

    def test_one_missing_boundary_face_is_scope_error(self):
        v=example()
        del v["boundary_frames"]["z_upper"]
        with self.assertRaises(DomainScopeError):
            certify_typed_adm_domain(v)

    def test_nonrational_expression_refused(self):
        v=example()
        v["spatial_metric"][0][0]={"func":{"name":"sin","arg":"t"}}
        with self.assertRaises(DomainScopeError):
            certify_typed_adm_domain(v)

    def test_changed_input_and_receipt_tampering_refused(self):
        v=example()
        r=certify_typed_adm_domain(v)
        self.assertTrue(replay_typed_adm_domain(v,r))
        altered=copy.deepcopy(r)
        altered["evolution_solution_existence_proven"]=True
        self.assertFalse(replay_typed_adm_domain(v,altered))
        changed=copy.deepcopy(v)
        changed["energy_growth"]=1
        self.assertFalse(replay_typed_adm_domain(changed,r))

    def test_coordinate_domain_inverted_refused(self):
        v=example()
        v["box"]["x"]=[1,0]
        with self.assertRaises(DomainScopeError):
            certify_typed_adm_domain(v)


if __name__=="__main__":
    unittest.main()
