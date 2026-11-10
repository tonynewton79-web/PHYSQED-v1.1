"""Regression and scientific refusal tests for PHYSQED research solver 2.0.

All tests use public exact textbook objects or synthetic mathematical controls.
They do not prove general AI reasoning, global GR, or experimental physics.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research_solver import solve_research_problem,replay_research_problem
from v12.geometry import ScopeError

SCHEMA="physqed.research-problem.v1"
def add(*v):return {"add":list(v)}
def mul(*v):return {"mul":list(v)}
def pow_(v,k):return {"pow":[v,k]}
def neg(v):return {"neg":v}
def rat(n,d):return {"rational":[n,d]}
def deriv(name,coord,order=1):return {"derivative":[name,coord,order]}
def sample(task, domain, model):
    return {"schema":SCHEMA, "id":"Scope_Test", "domain":domain,
            "task":task, "research_question":"What follows exactly from this explicit bounded model?",
            "source":"Synthetic textbook mathematical example, no empirical data",
            "assumptions":["All symbols mean exactly what the formal AST declares; no physical validation"],
            "conventions":{"units":"natural","frame":"explicit coordinate/canonical frame",
                           "domain":"formal algebra or stated local chart only"},
            "model":model}


class ResearchSolverTests(unittest.TestCase):
    def test_main_honest_proof_contract(self):
        model={"variables":["x","y"],
          "lhs":add(pow_("x",2),neg(pow_("y",2))),
          "rhs":mul(add("x",neg("y")),add("x","y"))}
        inp=sample("exact_identity","mathematics",model)
        r=solve_research_problem(inp)
        self.assertEqual(r["analysis"]["status"],"PROVED_SCOPED_POLYNOMIAL_IDENTITY")
        self.assertTrue(r["analysis"]["independent_exact_backend"])
        self.assertEqual(r["claim_release_level"],"EXACT_FORMAL_MATHEMATICS_ONLY")
        self.assertTrue(all(c["passed"] is not False for c in r["analysis"]["checks"]))
        for flag in ("physical_law_proven","lean_kernel_verified","global_theorem_proven",
                     "universal_solver_claim_proven","experimental_validation"):
            self.assertFalse(r[flag])
        self.assertTrue(replay_research_problem(inp,r))
        forged=copy.deepcopy(r);forged["physical_law_proven"]=True
        self.assertFalse(replay_research_problem(inp,forged))
        forged2=copy.deepcopy(r);forged2["analysis"]["status"]="PROVED_UNIVERSAL_PHYSICS"
        self.assertFalse(replay_research_problem(inp,forged2))
        self.assertRegex(r["receipt_sha256"],r"^[0-9a-f]{64}$")

    def test_false_identity_exact_refutation(self):
        model={"variables":["x"],"lhs":pow_("x",2),"rhs":add("x",1)}
        r=solve_research_problem(sample("exact_identity","mathematics",model))
        self.assertEqual(r["analysis"]["status"],"REFUTED_EXACT_POLYNOMIAL_IDENTITY")
        witness=r["analysis"]["counterexample"]
        self.assertIsNotNone(witness)
        self.assertNotEqual(witness["residual"],"0")
        self.assertFalse(r["physical_law_proven"])

    def test_rational_coefficients_exact(self):
        model={"variables":["x"],"lhs":mul(rat(2,3),"x"),
               "rhs":add(mul(rat(1,2),"x"),mul(rat(1,6),"x"))}
        r=solve_research_problem(sample("exact_identity","mathematics",model))
        self.assertEqual(r["analysis"]["status"],"PROVED_SCOPED_POLYNOMIAL_IDENTITY")

    def test_cancellation_with_singular_domain_does_not_prove_global(self):
        model={"variables":["x"],"lhs":mul("x",pow_("x",-1)),"rhs":1}
        r=solve_research_problem(sample("exact_identity","mathematics",model))
        self.assertEqual(r["analysis"]["status"],"INCONCLUSIVE_SYMBOLIC_ONLY")
        self.assertEqual(r["claim_release_level"],"NOT_RELEASED")

    def test_trigonometry_sympy_only_not_two_route(self):
        theta={"func":{"name":"sin","arg":"x"}}
        cosine={"func":{"name":"cos","arg":"x"}}
        model={"variables":["x"],"lhs":add(pow_(theta,2),pow_(cosine,2)),"rhs":1}
        r=solve_research_problem(sample("exact_identity","mathematics",model))
        self.assertEqual(r["analysis"]["status"],"INCONCLUSIVE_SYMBOLIC_ONLY")
        self.assertFalse(r["analysis"]["independent_exact_backend"])

    def test_polynomial_units_good_and_bad(self):
        model={"variables":["m","a","f"],"lhs":mul("m","a"),"rhs":"f",
          "dimensions":{"m":{"M":1},"a":{"L":1,"T":-2},"f":{"M":1,"L":1,"T":-2}}}
        result=solve_research_problem(sample("exact_identity","classical",model))
        self.assertEqual(result["analysis"]["status"],"REFUTED_EXACT_POLYNOMIAL_IDENTITY")
        self.assertTrue(result["analysis"]["results"]["units"]["checked"])
        broken=copy.deepcopy(model)
        broken["dimensions"]["f"]={"T":2}
        with self.assertRaises(ScopeError):
            solve_research_problem(sample("exact_identity","classical",broken))

    def test_hamiltonian_harmonic_oscillator(self):
        H=mul(rat(1,2),add(pow_("p",2),pow_("q",2)))
        inp=sample("hamiltonian_flow","classical",{"positions":["q"],"momenta":["p"],
                      "hamiltonian":H,"expected_dq":["p"],"expected_dp":[neg("q")]})
        r=solve_research_problem(inp)
        self.assertEqual(r["analysis"]["status"],"DERIVED_SCOPED_CANONICAL_EQUATIONS")
        self.assertTrue(r["analysis"]["results"]["declared_equations_matched"])
        self.assertTrue(all(c["passed"] is True for c in r["analysis"]["checks"]))
        inp["model"]["expected_dp"]=["q"]
        bad=solve_research_problem(inp)
        self.assertEqual(bad["analysis"]["status"],"REJECTED_MODEL_PREDICTION")

    def test_euler_lagrange_oscillator_and_noether(self):
        L=mul(rat(1,2),add(pow_(deriv("q","t"),2),neg(pow_("q",2))))
        model={"fields":["q"],"coordinates":["t"],"lagrangian":L,
               "expected_eom":[add(neg("q"),neg(deriv("q","t",2)))],
               "translation_noether":True}
        r=solve_research_problem(sample("euler_lagrange","field",model))
        self.assertEqual(r["analysis"]["status"],"DERIVED_SCOPED_EULER_LAGRANGE")
        self.assertTrue(r["analysis"]["results"]["declared_equations_matched"])
        self.assertTrue(r["analysis"]["results"]["translation_noether_zero"])
        model["expected_eom"]=["q"]
        bad=solve_research_problem(sample("euler_lagrange","field",model))
        self.assertEqual(bad["analysis"]["status"],"REJECTED_MODEL_PREDICTION")

    def test_exact_quantum_spin_commutator(self):
        X=[[0,1],[1,0]]
        Z=[[1,0],[0,-1]]
        C=[[0,-2],[2,0]]
        model={"a":X,"b":Z,"expected_commutator":C,"expected_hermitian":[True,True]}
        r=solve_research_problem(sample("quantum_commutator","quantum",model))
        self.assertEqual(r["analysis"]["status"],"DERIVED_SCOPED_FINITE_QUANTUM_ALGEBRA")
        self.assertEqual(r["analysis"]["results"]["trace_commutator"],"0")
        self.assertTrue(r["analysis"]["independent_exact_backend"])
        model["expected_commutator"]=[[0,0],[0,0]]
        bad=solve_research_problem(sample("quantum_commutator","quantum",model))
        self.assertEqual(bad["analysis"]["status"],"REJECTED_MODEL_PREDICTION")

    def test_general_relativity_flat_metric(self):
        model={"coordinates":["t","x","y","z"],
               "metric":[[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],
               "signature":"-+++","expected_scalar_curvature":0,"check_vacuum":True}
        r=solve_research_problem(sample("metric_curvature","spacetime",model))
        self.assertEqual(r["analysis"]["status"],"DERIVED_SCOPED_METRIC_CURVATURE")
        self.assertTrue(r["analysis"]["results"]["vacuum_equations_satisfied"])
        self.assertFalse(r["analysis"]["results"]["signature_independently_verified"])
        self.assertFalse(r["global_theorem_proven"])

    def test_two_sphere_curvature(self):
        sin={"func":{"name":"sin","arg":"theta"}}
        model={"coordinates":["theta","phi"],"metric":[[1,0],[0,pow_(sin,2)]],
               "signature":"++","expected_scalar_curvature":2}
        r=solve_research_problem(sample("metric_curvature","spacetime",model))
        self.assertEqual(r["analysis"]["status"],"DERIVED_SCOPED_METRIC_CURVATURE")
        self.assertTrue(r["analysis"]["results"]["expected_scalar_matched"])

    def test_statistical_two_level_system(self):
        inp=sample("finite_statistical","statistical",
                   {"energies":[0,1],"degeneracies":[1,2],"inverse_temperature":"beta"})
        r=solve_research_problem(inp)
        self.assertEqual(r["analysis"]["status"],"DERIVED_SCOPED_FINITE_CANONICAL_ENSEMBLE")
        self.assertTrue(all(c["passed"] for c in r["analysis"]["checks"]))
        self.assertFalse(r["experimental_validation"])

    def test_existing_typed_physics_is_replayed_not_promoted(self):
        p=ROOT/"examples"/"typed"/"metric_minkowski.json"
        contract=json.loads(p.read_text())
        inp=sample("typed_obligations","spacetime",{"contract":contract})
        r=solve_research_problem(inp)
        self.assertEqual(r["analysis"]["status"],"PASS_SCOPED_TYPED_OBLIGATIONS")
        self.assertFalse(r["physical_law_proven"])
        self.assertTrue(replay_research_problem(inp,r))

    def test_unknown_physics_task_abstains_without_throw(self):
        r=solve_research_problem(sample("solve_all_quantum_gravity","spacetime",{}))
        self.assertEqual(r["analysis"]["status"],"UNSUPPORTED_TASK")
        self.assertEqual(r["research_decision"],"UNSUPPORTED")
        self.assertFalse(r["universal_solver_claim_proven"])

    def test_cross_domain_task_abstains(self):
        r=solve_research_problem(sample("hamiltonian_flow","cosmology",{}))
        self.assertEqual(r["analysis"]["status"],"UNSUPPORTED_TASK")

    def test_bad_schema_rejected(self):
        p=sample("exact_identity","mathematics",{"variables":["x"],"lhs":"x","rhs":"x"})
        p["physical_law_proven"]=True
        with self.assertRaises(ScopeError):solve_research_problem(p)

    def test_missing_provenance_rejected(self):
        p=sample("exact_identity","mathematics",{"variables":["x"],"lhs":"x","rhs":"x"})
        p["source"]=""
        with self.assertRaises(ScopeError):solve_research_problem(p)

    def test_float_and_nonfinite_input_rejected(self):
        p=sample("exact_identity","mathematics",{"variables":["x"],"lhs":1.0,"rhs":1})
        with self.assertRaises(ScopeError):solve_research_problem(p)
        p["model"]={"variables":["x"],"lhs":1,"rhs":1}
        txt=json.dumps(p)
        self.assertEqual(solve_research_problem(txt)["analysis"]["status"],
                         "PROVED_SCOPED_POLYNOMIAL_IDENTITY")
        with self.assertRaises(ScopeError):solve_research_problem(txt[:-1]+', "source": "duplicate"}')
        with self.assertRaises(ScopeError):solve_research_problem(txt.replace('"rhs": 1','"rhs": NaN'))

    def test_invalid_parser_code_injection_refused(self):
        p=sample("exact_identity","mathematics",
                 {"variables":["x"],"lhs":"__import__('os').system('true')","rhs":0})
        with self.assertRaises(ScopeError):solve_research_problem(p)

    def test_bounded_disclosed_generated_challenges(self):
        for n in range(1,26):
            lhs=add(mul(n,"x"),mul(n,"y"))
            rhs=mul(n,add("x","y"))
            inp=sample("exact_identity","mathematics",
                       {"variables":["x","y"],"lhs":lhs,"rhs":rhs})
            good=solve_research_problem(inp)
            self.assertEqual(good["analysis"]["status"],
                             "PROVED_SCOPED_POLYNOMIAL_IDENTITY")
            inp["model"]["rhs"]=add(rhs,1)
            bad=solve_research_problem(inp)
            self.assertEqual(bad["analysis"]["status"],
                             "REFUTED_EXACT_POLYNOMIAL_IDENTITY")
            self.assertIsNotNone(bad["analysis"]["counterexample"])

    def test_unique_exact_linear_solution_and_independent_rref(self):
        model={"variables":["x","y"],"coefficients":[[2,1],[1,-1]],"rhs":[7,1]}
        inp=sample("rational_linear_system","mathematics",model)
        r=solve_research_problem(inp)
        self.assertEqual(r["analysis"]["status"],"PROVED_SCOPED_UNIQUE_LINEAR_SOLUTION")
        self.assertEqual(r["analysis"]["results"]["solution"],{"x":"8/3","y":"5/3"})
        self.assertTrue(r["analysis"]["independent_exact_backend"])
        self.assertTrue(replay_research_problem(inp,r))

    def test_inconsistent_and_underdetermined_linear_systems(self):
        model={"variables":["x","y"],"coefficients":[[1,1],[2,2]],"rhs":[1,3]}
        r=solve_research_problem(sample("rational_linear_system","mathematics",model))
        self.assertEqual(r["analysis"]["status"],"REFUTED_LINEAR_SYSTEM_FEASIBILITY")
        self.assertFalse(r["physical_law_proven"])
        model["rhs"]=[1,2]
        r=solve_research_problem(sample("rational_linear_system","mathematics",model))
        self.assertEqual(r["analysis"]["status"],"UNDERDETERMINED_LINEAR_SYSTEM")
        self.assertEqual(r["research_decision"],"ABSTAIN_OR_NEEDS_INDEPENDENT_PROOF")

    def test_wave_equation_pde_ansatz(self):
        sine={"func":{"name":"sin","arg":add("x",neg("t"))}}
        model={"coordinates":["x","t"],"ansatz":sine,
               "terms":[{"coefficient":1,"derivatives":["t","t"]},
                        {"coefficient":-1,"derivatives":["x","x"]}],
               "source":0}
        r=solve_research_problem(sample("pde_ansatz_residual","field",model))
        self.assertEqual(r["analysis"]["status"],"DERIVED_SCOPED_PDE_SOLUTION_ANSATZ")
        self.assertFalse(r["global_theorem_proven"])

    def test_wrong_wave_ansatz_has_rational_witness(self):
        model={"coordinates":["x","t"],"ansatz":add(pow_("x",2),"t"),
               "terms":[{"coefficient":1,"derivatives":["t","t"]},
                        {"coefficient":-1,"derivatives":["x","x"]}],
               "source":0}
        r=solve_research_problem(sample("pde_ansatz_residual","field",model))
        self.assertEqual(r["analysis"]["status"],"REFUTED_PDE_ANSATZ_BY_COUNTEREXAMPLE")
        self.assertEqual(r["analysis"]["counterexample"]["residual"],"-2")
        self.assertFalse(r["physical_law_proven"])

    def test_pde_derivative_scope_rejection(self):
        model={"coordinates":["x"],"ansatz":"x",
               "terms":[{"coefficient":1,"derivatives":["x"]*5}],"source":0}
        with self.assertRaises(ScopeError):
            solve_research_problem(sample("pde_ansatz_residual","fluid",model))


    def test_classical_polynomial_integral_discovery(self):
        H=mul(rat(1,2),add(pow_("p",2),pow_("q",2)))
        model={"positions":["q"],"momenta":["p"],"hamiltonian":H,"max_degree":2}
        r=solve_research_problem(sample("classical_conservation_search","classical",model))
        self.assertEqual(r["analysis"]["status"],"CANDIDATES_EXACTLY_CERTIFIED_IN_BOUNDED_CLASS")
        self.assertGreaterEqual(r["analysis"]["results"]["nonconstant_integral_basis_dimension"],1)
        self.assertTrue(all(x["fraction_poisson_bracket_zero"]
                            for x in r["analysis"]["results"]["basis"]))
        self.assertFalse(r["analysis"]["results"]["complete_integrability_proven"])
        self.assertFalse(r["analysis"]["results"]["discovery_novelty_proven"])

    def test_two_dimensional_isotropic_oscillator_symmetry_discovery(self):
        H=mul(rat(1,2),add(pow_("p1",2),pow_("p2",2),
                            pow_("q1",2),pow_("q2",2)))
        model={"positions":["q1","q2"],"momenta":["p1","p2"],
               "hamiltonian":H,"max_degree":2}
        r=solve_research_problem(sample("classical_conservation_search","classical",model))
        self.assertEqual(r["analysis"]["status"],"CANDIDATES_EXACTLY_CERTIFIED_IN_BOUNDED_CLASS")
        self.assertGreaterEqual(r["analysis"]["results"]["nonconstant_integral_basis_dimension"],3)

    def test_finite_quantum_degeneracy_symmetry_discovery(self):
        H=[[1,0,0],[0,1,0],[0,0,2]]
        r=solve_research_problem(sample("finite_quantum_symmetry_search","quantum",
                                       {"hamiltonian":H}))
        self.assertEqual(r["analysis"]["status"],"CANDIDATES_EXACTLY_CERTIFIED_IN_BOUNDED_CLASS")
        self.assertEqual(r["analysis"]["results"]["commutant_dimension"],5)
        self.assertTrue(r["analysis"]["results"]["commutant_exceeds_polynomial_H_dimension"])
        self.assertFalse(r["analysis"]["results"]["discovery_novelty_proven"])
        self.assertTrue(all(x["commutator_zero"] for x in r["analysis"]["results"]["commuting_matrices"]))

    def test_nonsymmetric_quantum_discovery_refused(self):
        H=[[1,2],[0,3]]
        with self.assertRaises(ScopeError):
            solve_research_problem(sample("finite_quantum_symmetry_search","quantum",
                                          {"hamiltonian":H}))


if __name__=="__main__":
    unittest.main()
