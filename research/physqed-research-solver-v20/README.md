# PHYSQED Research Solver 2.0 Alpha
**Tony Newton · 10 November 2026**

## Scope and architecture

PHYSQED's research solver is a typed, evidence-first framework for doing controlled mathematical physics research. It compiles assumptions and conventions, routes a bounded mathematical task to a backend, derives candidate answers, independently checks what can be checked exactly, searches for explicit obstructions, and emits a deterministic replayable receipt.

**It is NOT a universal physics solver in the theorem-solving sense.** The universal interface is an engineering ambition; most physical theories, arbitrary PDEs, quantum field theory and quantum gravity are outside the verified backends. Refusing unsupported work is a desired outcome, not a failed mathematics test.

## Supported task router

| Task | Methods | Claim boundary |
| --- | --- | --- |
| exact_identity | SymPy rational coefficients + independently implemented Python Fraction polynomial ring, counterexamples and declared dimensions | Exact formal algebra only; rational/domain singularities and nonpolynomial expressions remain on hold |
| rational_linear_system | Independent Fraction Gauss-Jordan + SymPy rank/substitution | Exact linear equations; underdetermined systems clearly reported |
| hamiltonian_flow | Canonical gradients and Poisson brackets | Formal Hamilton equations, not measured physical validity |
| euler_lagrange | Local first-derivative variation and Noether check | Local field EOM, no existence theorem or quantization |
| quantum_commutator | Finite matrix commutators and independent entrywise sum | Exact finite operator algebra, no continuum QFT |
| metric_curvature | Ricci, Einstein, inverse metric and Bianchi via v1.2 | Chart-local; signature/global domain are not independently proved |
| finite_statistical | Finite partition function, mean energy, fluctuation identity | No thermodynamic limit |
| pde_ansatz_residual | Linear PDE operator on supplied ansatz, algebraic residual, rational witnesses | Substitution only; no global PDE well-posedness |
| typed_obligations | Existing v1.2 metric/gauge/ADM/Einstein–Maxwell inputs, full replay | Inherits native status and all release holds |

The system does not infer physical laws from unrestricted prose, independently retrieve literature, prove experimental data, benchmark a competitor or confer Lean-kernel verification. It requires the researcher to freeze provenance, assumptions, conventions and formal statements; all remain visible in the auditable output.

## Verification status contract

- **Mathematically proven within formal scope:** rational polynomial identity or unique rational linear solution using two exact implementations; neither proves a surrounding physical claim.
- **Refuted:** nonzero polynomial coefficient, inconsistent exact rank, false expected equation or safe counterexample witness.
- **Derived with restrictions:** finite matrix, mechanics, Lagrangian, chart curvature, finite ensemble or PDE-ansatz calculations.
- **Abstained or held:** unknown task/domain; missing domain proof (such as x/x = 1 at x = 0); unsupported expression; underdetermined equations; symbolic-only simplification.

Input is strict typed JSON, not arbitrary Python or free-form sympify. All numeric inputs must be exact integers or rational objects; binary floating-point values are rejected. The input and implementation receive SHA256 digests for deterministic replay/integrity, not authenticated provenance.

## Run (from repository root)

Use Python 3.11 and pinned SymPy 1.14.0:

    python -m pip install sympy==1.14.0
    PYTHONPATH=projects/physqed python -m research_solver research/physqed-research-solver-v20/fixtures/exact_identity.json --output receipt.json
    python -m unittest discover -s projects/physqed/tests -p 'test_research_solver_v20.py' -v

Programmatic API:

    import sys
    sys.path.insert(0, "projects/physqed")
    from research_solver import solve_research_problem, replay_research_problem
    result = solve_research_problem(your_typed_dict)
    assert replay_research_problem(your_typed_dict, result)

Schema physqed.research-problem.v1 requires exactly: schema, id, domain, task, research_question, source, assumptions, conventions, model. The conventions object must contain units, frame and domain, all nonempty. A convention is caller-declared, not automatically physically verified.

## Validation and next steps

The earlier main-branch Benchmark 13 (105 probes) and Benchmark 14 (1,440 deterministic synthetic cases) remain release checks. The new v2 suite exercises intentionally false equations, singular-domain refusal, inconsistent and underdetermined exact linear systems, finite quantum operators, harmonic oscillator, Minkowski and 2-sphere geometry, wave PDE ansatz and finite canonical partition function.

Research-level independent comparison will require external blind formal challenges (e.g. FormalScience, AxQM, Physlib as appropriate), competitor systems evaluated on equal tasks under equal computational budgets, full versioned false-positive/refusal statistics, expert semantic audits and independent physical data/predictions.

The strong generalized-harmonic Einstein IBVP and other physics claims remain subject to their pre-existing release holds. All receipts set physical_law_proven=false, global_theorem_proven=false, lean_kernel_verified=false and universal_solver_claim_proven=false.

**The next genuine frontier is reliable research reasoning under open-ended adversarial tasks, not increasing synthetic test totals.**
