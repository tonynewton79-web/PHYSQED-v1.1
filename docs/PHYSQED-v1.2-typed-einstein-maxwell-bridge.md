# PHYSQED v1.2 — Typed Einstein–Maxwell/ADM bridge

## Research objective and exact scope

This implementation connects the general **safe declarative physics-input
compiler** to the previously implemented **16-node Einstein–Maxwell/ADM
consistency contract**. A single JSON model provides a metric,
electromagnetic potential, lapse, coordinates, geometric-unit declarations,
tensor index signatures and exact witness points. PHYSQED generates and
checks all 16 linked obligations without requiring the caller to construct
the EinsteinMaxwellSpec Python object by hand.

The outcome is a **chart-local exact symbolic component certificate with
pointwise independent rational-curvature checks**, not a complete physical
proof, independently formalized theorem, general ADM foliation validator
or empirical finding.

## Coordinate-aware geometrized physical dimensions

The initial physically meaningful unit type system has **one base
dimension: geometric length L**. Its declared normalization is
geometrized Einstein–Maxwell with signature -+++ and `c=G=1` (together
with a compatible electromagnetic charge normalization). This is not a
full metre/kilogram/second/coulomb dimensional-analysis engine.

Declare coordinate exponents `d_a` by `[x^a]=L^(d_a)`.
For a four-dimensional metric with line element `[ds]=L`,
the checker enforces:

```text
[g_ab]     = L^(2-d_a-d_b)
[A_a]      = L^(1-d_a)
[F_ab]     = L^(1-d_a-d_b)
[T_ab]     = L^(-d_a-d_b)
[N]        = L^(1-d_0)
[Lambda]   = L^(-2)
[kappa]    = L^(0)  (under the chosen geometric action normalization)
```

For a Schwarzschild/Reissner–Nordström chart
`(t,r,theta,phi)`, the correct coordinate exponents are
`(1,1,0,0)`: thus `g_tt` and `g_rr` are dimensionless
while `g_thetatheta` and `g_phiphi` have dimension
`L^2`. The checker does **not** incorrectly demand a single
uniform dimension for every metric component.

Exact zero components may occupy any dimension. Sums of nonzero
expressions must have identical dimensions, products add exponents,
powers multiply exponents, square roots halve them, and `sin`, `cos`,
`exp` require dimensionless arguments. Numeric parameter values are
interpreted as magnitudes in declared geometrized units, and are
substituted only after all dimensional obligations pass.

## Tensor rank and variance

The current declaration checker expects these fixed index signatures:

| Tensor | Covariant/contravariant variance | Rank |
|---|---|---|
| Metric `g` | `dd` | 2 |
| Potential `A` | `d` | 1 |
| Maxwell strength `F` | `dd` | 2 |
| Stress `T` | `dd` | 2 |
| Lapse `N` | empty | 0 |

Invalid ranks or variance declarations are refused. This is **not**
yet a full symbolic tensor expression/type checker for arbitrary mixed
indices, free/dummy index matching or Einstein summation.

## Full mathematical verification

A `kind: einstein_maxwell` model requesting
`linked_einstein_maxwell_adm` is lowered into the established
`EinsteinMaxwellSpec`, which enforces **zero shift** and checks:

1. Unit timelike normal
2. Potential/field-strength agreement
3. Maxwell constitutive stress
4. Electromagnetic Bianchi identity
5. Source-free Maxwell dynamics
6. Matter off-shell Noether/divergence bridge
7. Stress-energy conservation
8. Einstein dynamics (including the selected Lambda and coupling)
9. Contracted Einstein Bianchi identity
10. Einstein/matter divergence bridge
11. ADM Hamiltonian constraint
12. ADM momentum constraints
13. Off-shell Hamiltonian Gauss projection bridge
14. Off-shell momentum Codazzi projection bridge
15. Agreement with any supplied Hamiltonian certificate
16. Agreement with any supplied momentum certificate

The already existing `fractions.Fraction` 2-jet oracle independently
computes local 4D/3D curvature from exact metric jets and compares it
componentwise with the SymPy result at the declared witnesses.
This independence is **limited to curvature arithmetic** because
the metric derivatives are generated symbolically by the primary backend.

Dimension/index-type errors raise `ScopeError` *before*
contract evaluation; a well-typed but incorrect solution receives a
`REJECTED_LINKED_PHYSICS_OBLIGATIONS` certificate.

## Included standard and negative examples

- `projects/physqed/examples/typed/einstein_maxwell_flat.json`:
  zero-field Minkowski, all 16 linked nodes expected to pass.
- `projects/physqed/examples/typed/einstein_maxwell_reissner_nordstrom.json`:
  M=1, Q=1/2 electrovacuum at r=4, theta=pi/2 in standard exterior
  coordinates; tests coordinate-aware physical dimensions and both oracles.
- `projects/physqed/examples/typed/einstein_maxwell_inconsistent_flat.json`:
  flat metric carrying a nonzero electrostatic field with no gravitational
  backreaction; dimensions and index types are valid but Einstein dynamics
  must fail.

Further negative tests refuse incorrect index variance/rank,
potential units, spherical angular metric units, parameter units,
dimensionful trigonometric arguments, nonzero shift, incorrect
claimed ADM constraint and altered certificates.

## Run

```bash
python -m pip install -r requirements-test.txt

# Plan 16 linked checks, without claiming they passed
PYTHONPATH=projects/physqed python -m v12.typed_cli \
  --input projects/physqed/examples/typed/einstein_maxwell_reissner_nordstrom.json \
  --plan

# Compute the 16 linked checks and both independent pointwise oracles
PYTHONPATH=projects/physqed python -m v12.typed_cli \
  --input projects/physqed/examples/typed/einstein_maxwell_reissner_nordstrom.json \
  --output typed_einstein_maxwell_receipt.json

# Standalone test suite
python -m unittest discover -s projects/physqed/tests \
  -p test_physics_v12_typed_em_bridge.py -v
```

The complete standalone suite uses larger curved examples; the CI
workflow runs each bridge test in a fresh interpreter to avoid
unbounded accumulation of shared SymPy caches.

## Release and claim boundaries

The typed declarations are checked for internal formal consistency;
the engine does not prove that the caller's declared coordinate
dimensions, signature, physical action normalization, chart domains
or physical parameters are empirically correct.

The current bridge does **not** support nonzero ADM shift, arbitrary
foliations, a fully dimensionally typed tensor contraction grammar,
general SI conversion, gravitational PDE constraint propagation,
non-Abelian stress, independently formalized variational field
equations or a Lean-kernel certificate for curved-spacetime equations.

All checks remain **pending GitHub Python 3.15.2 CI success**.
Do not merge or publish as a stable release based solely on
source commits, plausible textbook examples or prior local replays.
