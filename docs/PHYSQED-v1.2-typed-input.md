# PHYSQED v1.2 — Typed Physics Input and Obligation Compiler

The `v12.typed_input` module accepts **bounded declarative JSON**, not
arbitrary Python or free-form textbook prose. It constructs a typed
SymPy model and executes only the exact theorem obligations explicitly
supported for that kind of model. This is the first *general-input
interface*, not a verifier of all of theoretical physics.

## Input workflow

1. Choose `kind`: `metric`, `lagrangian`, `hamiltonian` or `gauge`.
2. Declare `coordinates`, optional `parameters`, and model-specific
   fields or canonical variables. Supply a claim ID, scientific
   provenance and explicit assumption strings.
3. Construct mathematical expressions using the restricted JSON AST;
   never enter raw Python or uncontrolled SymPy text.
4. Choose supported `claims`. The planner generates a separate list
   of mathematical obligations and identifies identities versus
   asserted dynamical equations.
5. Execute the model. Each obligation receives a scoped component
   receipt, with both its pass/fail result and reproducibility hashes.
6. Replay the same typed input against a stored certificate. Any
   mutation of the certificate or input is refused.

## JSON example — four-dimensional vacuum general relativity

```json
{
  "schema": "physqed.typed-input.v1",
  "kind": "metric",
  "claim_id": "METRIC_MINKOWSKI",
  "source": "standard textbook Minkowski metric",
  "assumptions": ["global Cartesian chart of Minkowski space"],
  "coordinates": ["t", "x", "y", "z"],
  "claims": [
    "metric_compatibility",
    "first_bianchi",
    "contracted_bianchi",
    "vacuum_einstein"
  ],
  "metric": [
    [-1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
  ]
}
```

Save this as `model.json` and run:

```bash
python -m pip install -r requirements-test.txt
PYTHONPATH=projects/physqed python -m v12.typed_cli --input model.json --plan
PYTHONPATH=projects/physqed python -m v12.typed_cli --input model.json --output receipt.json
```

Exit status 0 means all requested mathematical component checks passed;
2 means a supported claim failed; 3 means unsupported/invalid input.
A *plan* has status `NOT_EXECUTED` and does not mean anything passed.

## Supported physics families and obligations

| Input kind | Supported claims | Essential inputs |
|---|---|---|
| Metric | metric compatibility, first/contracted Bianchi, vacuum Einstein, Einstein with user-supplied stress | Regular 1–4 dimensional metric; physical Einstein claims require 4D |
| Lagrangian | Euler–Lagrange equation agreement; translation Noether identity | 1–8 evaluated scalar fields, first-derivative Lagrangian, explicit expected field equations for E–L checks |
| Hamiltonian | canonical Hamilton equations; Poisson Jacobi identity | Named canonical position/momentum pairs, scalar Hamiltonian, expected dq/dt and dp/dt for dynamics |
| Gauge | gauge Bianchi, flatness, source-free Yang–Mills | Explicit local Lie connection; U(1), so(3), Lorentz algebra; metric required for Yang–Mills equations |

For `euler_lagrange` and `hamilton_equations`, PHYSQED
**derives** the proposed field/flow equations and compares them to
**user-provided expected expressions**. If the expected equations are
absent, it refuses certification rather than inventing a theorem.
An identity such as Bianchi or Jacobi does not automatically certify
the corresponding dynamical equations.

## Expression grammar

A scalar may be an exact integer or a declared name string. The
single-tag JSON constructors are:

```json
{"rational": [1, 2]}
{"add": ["x", {"pow": ["t", 2]}]}
{"mul": [3, "x"]}
{"neg": "x"}
{"pow": ["x", 2]}
{"func": {"name": "sin", "arg": "theta"}}
{"derivative": ["phi", "t", 2]}
```

Supported built-in functions: `sin`, `cos`, `exp`, `sqrt`.
Powers are bounded integers from -8 to 8; field derivative orders
from 1 to 4; the expression AST has fixed depth, node and byte
limits. Unknown constructors, symbols, functions, theorem names,
floating-point quantities, mismatched shapes, and code-looking
strings are rejected. There is no `eval`, `exec`, arbitrary
`sympify`, user Python expression parser, or expression macro.
Python callers should still treat programmatically constructed
SymPy models as trusted objects and subject them to resource limits.

## Textbook fixture set

The directory `projects/physqed/examples/typed` contains:

- `metric_minkowski.json`: positive 4D vacuum tensor geometry
- `lagrangian_free_scalar.json`: positive scalar E–L and translation identity
- `hamiltonian_oscillator.json`: positive Hamilton equations and Jacobi
- `gauge_maxwell.json`: positive Maxwell Bianchi and source-free Yang–Mills
- `negative_nonflat_field.json`: intentionally false flatness theorem

The native unit test module is
`projects/physqed/tests/test_physics_v12_typed_input.py`.
The v1.2 CI workflow runs these unit tests and the five CLI
fixtures in addition to legacy and coupled Einstein–Maxwell tests.

## Claim boundaries and current limitations

This layer generates exact, componentwise obligations, not proofs of
globally regular solutions, well-posed Cauchy problems, observational
agreement or absence of anomalies. The `assumptions` field records
caller declarations; it does **not** prove those assumptions. Real
symbols, finite dimensions and chart-local coordinates are enforced
by the engine. It does not have a physical-unit type checker,
differential-form gluing, arbitrary tensor variance in input JSON,
arbitrary gauge groups, formal proof-assistant kernel or
fully independent symbolic backend. The existing Fraction curvature
oracle belongs to the *separate typed Einstein–Maxwell ADM contract*;
the current general-input interface does not automatically use that
oracle for every model.

The source hash and receipt hash establish deterministic evidence
and replay, not external trust or Lean proof certification.
The Python **3.15.2** GitHub Actions result remains a required
release gate and must be read from the actual run before merging.

## Next gates

- Explicit units/dimensions and tensor rank/variance type rules
- Typed chart assumptions and domain-proof obligations
- Map this generic metric input into the existing multi-law
  Einstein–Maxwell/ADM specification when compatible
- Support nonzero ADM shift and arbitrary regular foliations
- Lie-valued matter currents, Yang–Mills stress-energy and
  independently varied gauge/matter actions
- Independent differential-form/variation oracle and proof assistant
- Constraint propagation and PDE regularity/energy estimates
