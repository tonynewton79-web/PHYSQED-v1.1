# PHYSQED v1.2 — Tensor, Gauge and Einstein Verification

**Experimental proof-carrying symbolic physics infrastructure.**
Version 1.2 extends — and does not replace — the independent 0.1–1.1
polynomial, compiler, multi-premise and essentiality modules. The new
backends live in `projects/physqed/v12/`. No bespoke paper is used as the
primary example: the first benchmark set is textbook physics.

## Runtime

Target **CPython 3.15.2** (25 October 2026 security release), with
`sympy==1.14.0` from `requirements-test.txt`. Compatibility is
**verified only after the precise GitHub Actions run passes**. Earlier
local Python versions may run the same source but do not establish
3.15.2 compatibility.

```bash
python -m pip install -r requirements-test.txt
python -m unittest discover -s projects/physqed/tests -p 'test_physics_v12.py' -v
python -m unittest discover -s projects/physqed/tests -p 'test_engine.py' -v
```

## Implemented, scoped capabilities

| Domain | Executable functions | Main limits |
| --- | --- | --- |
| Coordinate tensor geometry | General lower/upper tensor covariant derivatives, Levi-Civita coefficients, Riemann, Ricci, scalar curvature, geodesic residuals, first and contracted Bianchi checks | One explicitly supplied nondegenerate coordinate chart, dimension <= 4 and rank <= 5 |
| Einstein/GR | Einstein tensor and `G + Lambda g - kappa T` components, FLRW and sphere benchmark | No global boundary conditions or Einstein IVP theorem |
| Tetrad/Cartan | Metric from coframe, torsion of explicitly specified spin connection | No full spin-connection variation or constraint reduction |
| Gauge/Yang–Mills | Lie Jacobi/antisymmetry, U(1), SO(3), SO(1,3) brackets; curvature, Bianchi, covariant divergence, finite matrix gauge transformations, representation commutators | Lie dimension <= 8, spacetime <= 4; no bundle topology or path integral |
| Quantum mechanics | Matrix commutators, Hermiticity, exactly checkable density matrices, expectations, Robertson expression, Clifford algebra, finite CCR impossibility check | Finite square matrices; cannot prove full unbounded-operator domain properties |
| Field/QFT | Euler–Lagrange for first-derivative Lagrangians, canonical stress, translation/Noether identities, inverse finite quadratic kernel, Wick pairings, first-order 0D phi-four correction | Formal finite perturbation theory, **not** renormalized continuum QFT |
| Canonical gravity | Poisson bracket, Jacobi, supplied first-class closure witnesses, ADM scalar density, tetrad and torsion | Does **not** prove full smeared GR Dirac algebra or quantum gravity |

The backend accepts trusted programmatically constructed SymPy expressions.
It does **not** `eval` user expressions or infer the correctness of prose,
field content, boundary conditions, coupling conventions or experiments.

## Textbook reference and failure tests

- 4D Minkowski: vanishing Riemann/Einstein, Bianchi identities.
- 2-sphere: scalar curvature 2/r^2 and zero 2D Einstein tensor,
  with a second Ricci expression derived directly from the connection.
- Flat 4D FLRW: `G_00 = 3 (a'/a)^2` and its spatial equation.
- SO(3) and Lorentz Lie algebra Jacobi; U(1) constant electric field,
  non-Abelian constant-potential curvature and Bianchi identities.
- Matrix pure-gauge transformation covariance and an intentionally
  corrupted representation.
- Pauli commutators, Clifford anticommutators, a saturated
  uncertainty inequality and finite-dimensional CCR obstruction.
- Canonical Poisson/Jacobi and a basic first-class constraint.
- Harmonic oscillator and Klein–Gordon field equations, scalar Noether
  current, 0-dimensional Gaussian/Wick and phi-four correction.
- Deliberately wrong signs, invalid Lie antisymmetry, negative density,
  nonsymmetric/degenerate metric, singular Gaussian kernel, unsupported
  claim domain.

## Receipts and trust boundary

`v12.receipts.certify` emits deterministic JSON with:
source and assumptions, domain, each exact component check, two algebraic
normalization passes, concrete rational substitution counterexamples where
available, backend SHA-256 and certificate SHA-256.

A pass status is **EXACT_SYMBOLIC_COMPONENTS_PASSED__PHYSICS_UNVERIFIED**.
It does not mean a physical law, all boundary conditions, a global theorem,
a Lean proof, a quantum theory or experimental agreement have been proved.
The two passes both use SymPy, so `independent_engine_verified=false`
is mandatory. No hidden automatic Lean proof or arbitrary prose inference
is performed. An external independent backend and explicit formal proof
contracts remain research targets.

## Example

```python
import sys
sys.path.insert(0, "projects/physqed")
import sympy as sp
from v12 import Geometry, certify

t, x, y, z = sp.symbols("t x y z")
metric = Geometry((t,x,y,z), sp.diag(-1,1,1,1))
receipt = certify(
    "GR-MINKOWSKI-0001", "einstein",
    [(metric.einstein, sp.zeros(4))],
    assumptions=("Cartesian Minkowski chart", "Levi-Civita connection"),
    source="standard textbook vacuum GR")
assert receipt["status"].startswith("EXACT_SYMBOLIC")
assert receipt["physical_law_proven"] is False
```

## Future gates for broader verification

1. A safe, typed, validated expression/field/metric input language, with
   explicit hypotheses, chart domains, tensor index conventions and units.
2. Independent backends for curvature and functional calculus; differential
   and global geometry, PDE estimates and physically meaningful boundary
   conditions.
3. Local gauge identity certificates with exact topology/patch gluing and
   anomaly/BRST controls.
4. Higher-dimensional operator representations, domains, spectra and
   Hilbert-space limit theorems.
5. Perturbative diagram combinatorics, regularization, counterterm schemes
   and checked Ward/Slavnov–Taylor identities before asserting QFT validity.
6. ADM/Hamiltonian & momentum constraint *functional* bracket audits,
   tetrad/connection Dirac constraints, then proof-assistant formalization.
7. Human-reviewed provenance, empirical interfaces and adversarial tests.

Do not call this implementation an **unrestricted or complete** physics
verification system. The interfaces are intentionally extensible; their
currently certified mathematical domain is finite and explicit.
