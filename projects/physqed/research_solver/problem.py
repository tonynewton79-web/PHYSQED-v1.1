"""PHYSQED Research Solver 2.0 alpha: evidence-first, scoped physics workflow.

The 'universal' aspect is a typed orchestration interface for extensible
backends, not an assertion of universal mathematical or physical solvability.
All physically interpreted claims stay unreleased without external validation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import sympy as S

from v12.geometry import ScopeError
from .backends import (exact_identity,hamiltonian_flow,euler_lagrange_system,
                       quantum_commutator,metric_curvature,finite_statistical,
                       typed_obligations)
from .frontiers import rational_linear_system,pde_ansatz_residual
from .discovery import classical_conservation_search,finite_quantum_symmetry_search

SCHEMA="physqed.research-problem.v1"
RESULT_SCHEMA="physqed.research-solver.v2-alpha"
REQUIRED={"schema","id","domain","task","research_question","source",
          "assumptions","conventions","model"}
MAX_INPUT_BYTES=60000
DOMAINS={
    "mathematics","classical","field","quantum","spacetime",
    "gauge","electromagnetism","statistical","plasma","fluid",
    "cosmology","condensed_matter","particle","other"
}
TASKS={
    "exact_identity": (exact_identity,DOMAINS),
    "hamiltonian_flow": (hamiltonian_flow,{"classical"}),
    "euler_lagrange": (euler_lagrange_system,{"field","classical"}),
    "quantum_commutator": (quantum_commutator,{"quantum"}),
    "metric_curvature": (metric_curvature,{"spacetime","cosmology"}),
    "finite_statistical": (finite_statistical,{"statistical","condensed_matter"}),
    "rational_linear_system": (rational_linear_system,DOMAINS),
    "pde_ansatz_residual": (pde_ansatz_residual,{"fluid","plasma","classical","field","spacetime","cosmology"}),
    "classical_conservation_search": (classical_conservation_search,{"classical","field"}),
    "finite_quantum_symmetry_search": (finite_quantum_symmetry_search,{"quantum","condensed_matter"}),
    "typed_obligations": (typed_obligations,
                          {"classical","field","spacetime","gauge",
                           "electromagnetism","plasma","fluid","cosmology"}),
}
RELEASE_MATH={"PROVED_SCOPED_POLYNOMIAL_IDENTITY","PROVED_SCOPED_UNIQUE_LINEAR_SOLUTION"}
ERRONEOUS={"REFUTED_EXACT_POLYNOMIAL_IDENTITY","REJECTED_MODEL_PREDICTION","REFUTED_LINEAR_SYSTEM_FEASIBILITY","REFUTED_PDE_ANSATZ_BY_COUNTEREXAMPLE"}
ABSTAIN={"UNSUPPORTED_TASK","INCONCLUSIVE_ORACLE_DISAGREEMENT","INCONCLUSIVE_SYMBOLIC_ONLY","UNDERDETERMINED_LINEAR_SYSTEM","INCONCLUSIVE_PDE_RESIDUAL"}


def _canon(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True,
                      allow_nan=False)


def _sha(value):
    return hashlib.sha256(_canon(value).encode("utf-8")).hexdigest()


def _parse_input(payload: Any):
    if isinstance(payload,(str,bytes)):
        if len(payload)>MAX_INPUT_BYTES:
            raise ScopeError("research problem exceeds size limit")
        def pairs(kvs):
            d={}
            for k,v in kvs:
                if k in d:
                    raise ScopeError("duplicate JSON key")
                d[k]=v
            return d
        try:
            payload=json.loads(payload,object_pairs_hook=pairs,
                               parse_constant=lambda x: (_ for _ in ()).throw(
                                   ScopeError("nonfinite JSON numeric value")))
        except (ValueError,TypeError) as exc:
            raise ScopeError("invalid JSON research problem") from exc
    if not isinstance(payload,dict) or set(payload)!=REQUIRED:
        raise ScopeError("research input must contain exactly required contract keys")
    try:
        serialized=_canon(payload)
    except (ValueError,TypeError,OverflowError) as exc:
        raise ScopeError("nonfinite/unserializable research input") from exc
    if len(serialized)>MAX_INPUT_BYTES:
        raise ScopeError("research input exceeds byte limit")
    # Reject machine-float approximations throughout exact work.
    def check(node):
        if type(node) is float:
            raise ScopeError("floating values need an explicit numerical error model")
        if isinstance(node,dict):
            if any(not isinstance(k,str) for k in node):
                raise ScopeError("JSON object keys must be strings")
            for x in node.values():
                check(x)
        elif isinstance(node,list):
            for x in node:
                check(x)
    check(payload)
    if payload["schema"]!=SCHEMA:
        raise ScopeError("research schema mismatch")
    if (not isinstance(payload["id"],str) or
        not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,47}",payload["id"])):
        raise ScopeError("invalid research ID")
    if not isinstance(payload["domain"],str) or payload["domain"] not in DOMAINS:
        raise ScopeError("unknown physics domain")
    if (not isinstance(payload["task"],str) or
        not re.fullmatch(r"[a-z][a-z_]{0,63}",payload["task"])):
        raise ScopeError("invalid backend task name")
    for k in ("research_question","source"):
        if (not isinstance(payload[k],str) or not payload[k].strip()
            or len(payload[k])>1600):
            raise ScopeError("bounded nonempty question and provenance required")
    assumptions=payload["assumptions"]
    if (not isinstance(assumptions,list) or not 1<=len(assumptions)<=24 or
        any(not isinstance(x,str) or not x.strip() or len(x)>1000 for x in assumptions)):
        raise ScopeError("1..24 explicit assumption texts required")
    conventions=payload["conventions"]
    if (not isinstance(conventions,dict) or set(conventions)!={"units","frame","domain"}
        or any(not isinstance(v,str) or not v.strip() or len(v)>256 for v in conventions.values())):
        raise ScopeError("units, frame and domain-of-validity conventions required")
    if not isinstance(payload["model"],dict):
        raise ScopeError("model must be a bounded typed JSON object")
    return payload


def _backend_manifest():
    root=Path(__file__).resolve().parents[1]
    filepaths=[
        Path(__file__),
        Path(__file__).with_name("backends.py"),
        Path(__file__).with_name("exact.py"),
        Path(__file__).with_name("frontiers.py"),
        Path(__file__).with_name("discovery.py"),
        root/"v12"/"typed_input.py",
        root/"v12"/"geometry.py",
        root/"v12"/"quantum.py",
        root/"v12"/"fields.py",
    ]
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in filepaths}


def _plan(task):
    plans={
       "exact_identity":["compile typed rational expression","independent Fraction sparse polynomial",
                         "compare with SymPy QQ coefficients","seek rational refutation witness",
                         "audit dimensional claims and excluded singularities"],
       "hamiltonian_flow":["validate canonical variables and H","derive symplectic gradient",
                           "compare with Poisson bracket","test declared dynamics"],
       "euler_lagrange":["check local first-derivative Lagrangian","derive Euler-Lagrange expressions",
                        "compare declared EOM","test translation Noether residual"],
       "quantum_commutator":["check finite operator matrices","derive exact commutator",
                             "independent entrywise multiplication","check Hermiticity and stated commutator"],
       "metric_curvature":["validate nondegenerate chart metric","compute Ricci and Einstein tensors",
                           "test Bianchi and metric inverse","compare claimed scalar curvature"],
       "finite_statistical":["validate finite rational spectrum","derive partition function",
                             "check mean-energy derivative","check finite fluctuation identity"],
       "typed_obligations":["load existing v1.2 typed problem","run all named local obligations",
                            "replay complete certificate","retain physics claim boundaries"],
       "rational_linear_system":["compile exact rational matrix","independent Fraction RREF",
                                "compare SymPy rank","replay candidate solution"],
       "pde_ansatz_residual":["parse local coordinate ansatz","apply bounded linear differential operator",
                              "replay alternative symbolic normal form","search for a rational residual witness"],
       "classical_conservation_search":["compile polynomial Hamiltonian","generate bounded monomial candidates",
                                       "solve exact Lie-derivative nullspace","independently verify every candidate using Fraction polynomial Poisson bracket"],
       "finite_quantum_symmetry_search":["compile real symmetric rational Hamiltonian","build commutator superoperator",
                                        "find its exact nullspace","independently replay Fraction commutators and report candidate generators"],
    }
    return [{"step":i+1,"action":name} for i,name in enumerate(plans.get(
        task,["identify unsupported problem; do not guess or fabricate an answer"]))]


def solve_research_problem(payload: Any) -> dict:
    """Deterministic evidence-first scientific problem pipeline.

    Exceptions are *not* converted to successful certificates. Unknown tasks
    and out-of-domain tasks abstain. Caller-invalid contracts fail closed.
    """
    problem=_parse_input(payload)
    task,domain=problem["task"],problem["domain"]
    route=TASKS.get(task)
    if route is None or domain not in route[1]:
        operation={"status":"UNSUPPORTED_TASK","evidence_level":"none",
                   "results":{"requested_task":task,"requested_domain":domain,
                              "supported_tasks":sorted(TASKS)},
                   "checks":[],"counterexample":None,"independent_exact_backend":False,
                   "recommended_next_step":"Formulate a bounded subproblem supported by a declared backend; seek expert validation."}
    else:
        handler=route[0]
        operation=handler(problem["model"])
    status=operation["status"]
    release="EXACT_FORMAL_MATHEMATICS_ONLY" if status in RELEASE_MATH else "NOT_RELEASED"
    if status=="UNSUPPORTED_TASK":
        decision="UNSUPPORTED"
    elif status in ERRONEOUS:
        decision="REFUTED_WITHIN_FORMAL_SCOPE"
    elif status in ABSTAIN:
        decision="ABSTAIN_OR_NEEDS_INDEPENDENT_PROOF"
    elif status in RELEASE_MATH:
        decision="EXACT_MATHEMATICS_VERIFIED_NOT_PHYSICS"
    elif status.startswith("DERIVED_") or status.startswith("PASS_SCOPED"):
        decision="MODEL_DERIVATION_OR_SCOPED_CHECK_ONLY"
    else:
        decision="RESEARCH_HOLD"
    data={
        "schema":RESULT_SCHEMA,
        "problem_id":problem["id"],
        "domain":domain,
        "task":task,
        "research_question":problem["research_question"],
        "provenance": {"submitter_declared_source":problem["source"],
                       "source_independently_authenticated":False,
                       "literature_priority_audited":False,
                       "external_data_validated":False},
        "assumptions": [{"text":a, "physically_validated":False}
                       for a in problem["assumptions"]],
        "conventions":dict(problem["conventions"]),
        "plan":_plan(task),
        "analysis":operation,
        "research_decision":decision,
        "claim_release_level":release,
        "physical_law_proven":False,
        "global_theorem_proven":False,
        "lean_kernel_verified":False,
        "experimental_validation":False,
        "independent_human_review":False,
        "universal_solver_claim_proven":False,
        "general_ai_reasoning_benchmark_passed":False,
        "model_completeness_proven":False,
        "input_sha256":_sha(problem),
        "implementation_manifest_sha256":_sha(_backend_manifest()),
        "symbolic_dependency":"sympy-"+S.__version__,
        "limitations":"Bounded symbolic models and explicit assumptions; no unrestricted physics, semantic, empirical or novelty certification",
    }
    data["receipt_sha256"]=_sha(data)
    return data


def replay_research_problem(payload: Any, receipt: Any) -> bool:
    if not isinstance(receipt,dict):
        return False
    try:
        return _canon(solve_research_problem(payload))==_canon(receipt)
    except (ScopeError,ValueError,TypeError,KeyError,OverflowError):
        return False


def main(argv=None):
    parser=argparse.ArgumentParser(description="PHYSQED scoped research solver")
    parser.add_argument("input",help="strict research problem JSON")
    parser.add_argument("--output",help="optional receipt JSON path")
    args=parser.parse_args(argv)
    try:
        problem=Path(args.input).read_text(encoding="utf-8")
        receipt=solve_research_problem(problem)
    except (ScopeError,PolynomialErrorProxy,ValueError,TypeError,KeyError) as exc:
        print(json.dumps({"status":"REFUSED_INPUT","reason":str(exc)},indent=2))
        return 2
    encoded=json.dumps(receipt,indent=2,sort_keys=True)+"\n"
    if args.output:
        Path(args.output).write_text(encoded,encoding="utf-8")
    print(encoded,end="")
    return 0 if receipt["research_decision"] in (
        "EXACT_MATHEMATICS_VERIFIED_NOT_PHYSICS",
        "MODEL_DERIVATION_OR_SCOPED_CHECK_ONLY") else 1


class PolynomialErrorProxy(ValueError):
    """CLI catch compatibility; symbolic backend exceptions remain visible."""


if __name__=="__main__":
    raise SystemExit(main())
