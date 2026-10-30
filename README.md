## PHYSQED v1.2 — Single-source Einstein–Maxwell boundary and energy verification

The **linked ADM boundary contract** combines a single exact
shifted Einstein–Maxwell spacetime's 18 field/constraint identities,
source-preserving rational-domain lapse and spatial-metric bounds,
and the symmetric-hyperbolic constraint subsystem's *maximal
nonnegative boundary trace* algebra.

For the shifted Minkowski vacuum
`h=I, N=1, beta=(1/5,0,0), A=0`, the exact reference
constraint energy has `S=diag(1,4,4,4)`, `R=0`. The verifier
checks all six outward boundary flux forms, full rank and maximal
nonnegative frame dimension (3,1,3,3,3,3). The old undercomplete
positive-flux boundary control is now **rejected**.

```bash
PYTHONPATH=projects/physqed python -m v12.linked_adm_cli \
  --input projects/physqed/examples/typed/linked_adm_shifted_minkowski.json \
  --output linked_adm_boundary_receipt.json
```

[Mathematics and six-face boundary proof](
docs/PHYSQED-v1.2-linked-adm-boundary-compatibility.md).

This proves the exact reference model equations and supplies a
**conditional constraint-energy uniqueness argument** for existing
smooth solutions satisfying the declared trace and corner conditions.
It does not prove arbitrary nonlinear Einstein boundary-data
existence, strong Lopatinski compatibility or a general
initial-boundary well-posedness theorem. The new code remains
unmerged pending native Python 3.15.2 CI and earlier regressions.

## PHYSQED v1.2 — Original denominator, ADM geometry and boundary-flux proof gates

The typed ADM-domain compiler preserves **negative-power source denominators
before SymPy simplification**, certifies a strictly positive lapse,
positive-definite spatial metric, and uniform metric/constraint-energy
matrix bounds on a rational spacetime box.

It checks outward energy-flux quadratic forms on **all six spatial faces**
for a user-declared boundary trace subspace, or checks matching coefficients
for *assumed* periodic boundary traces. These are conditional boundary
algebra checks, **not proof of boundary trace realizability or PDE
well-posedness**.

```bash
PYTHONPATH=projects/physqed python -m v12.adm_domain_cli \
  --input projects/physqed/examples/typed/adm_domain_outgoing_flux.json \
  --output adm_domain_receipt.json
```

The included ADM reference model has `h=diag(1+t,1,1)`, `N=1+t`
and `beta=(1/5,0,0)` on `[0,1]^4`. It admits exact
`S>=I`, `R<=0`, and positive outward energy-flux tests on the
**declared one-dimensional trace subspaces**. Separate negative controls
refuse a cancelled source pole and an incoming-flux boundary.

[Derivation, restricted JSON grammar and mathematical claim boundaries](
docs/PHYSQED-v1.2-typed-adm-source-geometry-boundary.md).

**Release:** draft branch, pending native Python 3.15.2 and inherited
CI; no merge or formal global Einstein theorem claimed.

## PHYSQED v1.2 — Exact rational-function ADM domain certification

The existing polynomial-only domain-energy checker now has a
**rational-function extension**, needed for inverse spatial metrics,
lapse factors and 3+1 connection coefficients.

`v12/rational_energy.py` proves nonvanishing signs of denominators
over *entire rational coordinate boxes* using exact Bernstein
polynomial bounds, combines certified numerator/denominator intervals,
and checks the matrix inequalities
`S >= s*I`, `R <= CS` by sufficient Gershgorin bounds.
Deterministic dyadic box refinement can close cases that one global
Bernstein enclosure cannot certify.

All received rational coefficient denominators are audited **before**
derived-matrix cancellations. If earlier source simplification erased a
pole, supply its original denominator in `denominator_guards`.
Complete source-domain provenance is a caller assertion, not yet an
independently established guarantee.

A nonzero-shift **ADM example with h=diag(1+t,1,1), N=1+t** and
`beta=(1/5,0,0)` certifies `S >= I` and `R <= 0` on
`[0,1]^4` by exact arithmetic. It does **not** certify the
underlying Einstein equations, nonlinear existence, periodic solution
data or boundary flux.

[Mathematical theorem, exact example and failure boundaries](
docs/PHYSQED-v1.2-rational-energy-certificates.md).

New 14-case rational-domain regression suite:
`projects/physqed/tests/test_physics_v12_rational_energy.py`.

**Release status:** Still a draft feature branch, subject to the
actual Python 3.15.2 and legacy GitHub CI results.

## PHYSQED v1.2 — Exact spacetime-box energy certificates

The **domain-wide energy gate** checks (S\succeq s_*I) and
(R\preceq CS) across a declared rational spacetime rectangle,
using **exact multivariate Bernstein coefficients and Gershgorin
matrix inequalities**. Unlike pointwise tensor checks, its positive
result certifies each polynomial inequality throughout the box.

It supports exact rational-polynomial symmetric-hyperbolic
coefficients, emits a replayable component certificate, and
distinguishes successful interior bounds from inconclusive
sufficient bounds. Smooth PDE existence and boundary flux are
separate explicit assumptions, never silently certified.

[Bounded-domain theorem and examples](
docs/PHYSQED-v1.2-domain-energy-certificates.md).

This is still an experimental feature-branch component pending
native Python 3.15.2 CI and inherited regression results.

## PHYSQED v1.2 — Constraint energy and conditional PDE uniqueness checks

Two new checks complement the shifted-ADM Einstein–Maxwell contract:

- **Independent Fraction frozen-energy oracle:** for a constant
  positive-definite spatial metric, constant positive lapse and
  shift on a periodic three-torus, verify exact characteristic
  polynomial, symmetrizer and constraint-energy flux conservation.
- **Variable-coefficient energy identity:** generate the full
  symmetric-hyperbolic principal and lower-order ADM matrices
  including shift gradients, extrinsic curvature, spatial
  connections and lapse acceleration; check the exact differentiated
  matrix-energy identity and issue fully replayed receipts.

The resulting conditional theorem requires global positivity,
bounded coefficients, conserved matter, spatial evolution,
appropriate boundary flux and a smooth solution. The program
does **not** assert these global hypotheses from pointwise tests.

[Explicit frozen periodic energy theorem](
docs/PHYSQED-v1.2-frozen-adm-energy.md) ·
[Variable-coefficient identity and energy estimate obligations](
docs/PHYSQED-v1.2-variable-adm-energy.md)

The implementation remains experimental pending native Python
3.15.2 GitHub CI and legacy regression results.

## PHYSQED v1.2 — Nonzero ADM shift and conditional constraint propagation

The general typed JSON compiler can now generate a **shifted 3+1
Einstein–Maxwell contract** for spatial metric `h_ij`, lapse `N`,
contravariant shift `beta^i` and electromagnetic potential.

The 18-node suite checks the full Einstein/Maxwell system, Hamiltonian
and momentum projections, off-shell Gauss/Codazzi and projected Bianchi
propagation identities, trace-reversed spatial evolution, and the
symmetric-hyperbolic principal-symbol identity. Tensor index rank,
variance and coordinate-aware physical length dimensions are enforced
before solving symbolic components.

```bash
PYTHONPATH=projects/physqed python -m v12.typed_cli \
  --input projects/physqed/examples/typed/einstein_maxwell_shifted_flat.json \
  --output shifted_adm_receipt.json
```

[Shifted-ADM propagation mathematics and explicit assumptions](
docs/PHYSQED-v1.2-shifted-adm-propagation.md).
**This is not a global Einstein Cauchy-problem proof.** The conditional
energy uniqueness statement requires smooth coefficients, proper
boundary flux and trace-reversed evolution/matter conservation
throughout the spacetime domain. All new code remains subject to
Python 3.15.2 CI and inherited regression tests; the PR is unmerged.

## PHYSQED v1.2 — Automatic Einstein–Maxwell/ADM type-checked contracts

The general JSON physics-input compiler is now connected directly to
the **16-node Einstein–Maxwell/ADM consistency contract**. A single
typed input produces linked Einstein and Maxwell equations, covariant
conservation, Hamiltonian/momentum constraints, off-shell Gauss/Codazzi
bridges and independent rational 4D/3D curvature checks.

**New:** strict covariant tensor signatures (index rank/variance) and
**coordinate-aware physical length dimensions in geometrized units**.
These safeguards correctly distinguish spherical radial and angular
metric-component dimensions. They do not yet provide general SI units
or unrestricted index-expression algebra.

```bash
PYTHONPATH=projects/physqed python -m v12.typed_cli \
  --input projects/physqed/examples/typed/einstein_maxwell_reissner_nordstrom.json \
  --output typed_einstein_maxwell_receipt.json
```

[Complete Einstein–Maxwell/ADM bridge specification](
docs/PHYSQED-v1.2-typed-einstein-maxwell-bridge.md) ·
[15 adversarial and textbook type/physics tests](
projects/physqed/tests/test_physics_v12_typed_em_bridge.py)

**Release gate:** still a draft feature branch until Python 3.15.2 CI
and inherited regression suites pass. Local component checks are not
global physics proofs.

## PHYSQED v1.2 typed physics input (experimental)

A safe, restricted JSON input layer now accepts **metrics, scalar-field
Lagrangians, canonical Hamiltonians and gauge connections** and constructs
a typed list of supported mathematical verification obligations. See
[typed-input user guide](docs/PHYSQED-v1.2-typed-input.md) and
[five textbook JSON fixtures](projects/physqed/examples/typed/).

```bash
PYTHONPATH=projects/physqed python -m v12.typed_cli \
  --input projects/physqed/examples/typed/metric_minkowski.json --plan
PYTHONPATH=projects/physqed python -m v12.typed_cli \
  --input projects/physqed/examples/typed/metric_minkowski.json \
  --output minkowski_receipt.json
```

No text is evaluated as Python source. Unsupported expressions, claims,
missing target equations and unverified identities are refused. This
**does not imply unrestricted global physics proofs** or proof of
user-supplied premises. The linked [Einstein–Maxwell/ADM contract](
docs/PHYSQED-v1.2-typed-coupled-contract.md) remains a complementary,
more specialised multi-law verification backend. The v1.2 feature branch
is not a stable release until Python 3.15.2 and legacy CI pass.

# PHYSQED v1.2 — Proof-Carrying Physics

**General-purpose *architecture* for scoped verification of classical and quantum physics.**
The v1.2 expansion provides executable symbolic backends for tensor geometry,
Einstein equations, Lie and Yang–Mills gauge fields, finite quantum operators,
Euler–Lagrange and finite Gaussian perturbative field theory, and canonical
constraint checks. Existing v0.1–v1.1 proof-carrying components remain intact.

**New:** [Typed Einstein–Maxwell and ADM 16-node proof-carrying contract](docs/PHYSQED-v1.2-typed-coupled-contract.md), with separately computed 4D/3D rational-jet curvature certificates, adversarial rejection cases, and reproducible JSON receipts.

**Read the new [v1.2 physics backend guide](docs/PHYSQED-v1.2-physics-backends.md)**,
which starts with standard textbook physics, lists implemented capabilities,
explicit restrictions, reproducible tests, adversarial refusals, and receipt
status rules. CI targets **CPython 3.15.2** and checks existing v0.1 regressions.

```bash
python -m pip install -r requirements-test.txt
python -m unittest discover -s projects/physqed/tests -p 'test_physics_v12.py' -v
```

The title does **not** imply unrestricted mathematical or physical
certification: chart-local tensor expressions, exact finite-dimensional
algebra and controlled symbolic calculations are supported; a general
quantum gravity proof engine, arbitrary continuum QFT, global PDE
dynamics, physical-model validation and independent proof-assistant
certification are not yet established.

---

## Previous v1.1 release documentation (retained)

**Experimental exact-mathematics verification software by Tony Newton (Newton Astro Labs).**

**[Read the full PHYSQED v1.1 scientific and engineering report](docs/PHYSQED-v1.1-technical-overview.md)** — a self-contained account of the formal claim model, constructive rational-witness theorem and proof, worked examples, implementation, exact tests and limits. A [Zenodo record preparation guide](docs/ZENODO_RECORD.md) supplies an abstract and metadata for an eventual archived release.

PHYSQED attaches reproducible, machine-checkable evidence to *restricted mathematical claims* found in physics research. It aims to separate algebraic verification, interpretation of scientific language, formal proof compilation, and empirical validation instead of treating them as interchangeable.

The v1.1 extension handles conditional identities of the form

$$
C-D=\sum_{j=1}^{k} W_j(A_j-B_j),\qquad 2\leq k\leq4,
$$

where the premise differences are independent rational affine polynomials and the remaining expressions are within the supported exact rational-polynomial domain. After the v1.0 verifier accepts a contract and checks claim-specific essentiality, v1.1 constructs an *exact rational counterexample for each omitted premise*: an assignment satisfying every retained premise while falsifying both the omitted premise and the conclusion. The algorithm combines rational row reduction, polynomial restriction and finite rational specialization. Its output is rechecked in exact `fractions.Fraction` arithmetic.

This is a scoped mathematical capability, **not a demonstration that the supplied premises are true physical laws**. The present software does not automatically establish natural-language semantic equivalence, validate experimental data, or provide a Lean kernel proof of the Python certificate generator. Existing Lean examples are separate formal artifacts.

## Run locally

Requirements: Python 3.11+ for the Python suite; SymPy 1.14.0 for independent symbolic tests. Lean examples use the pinned Lean 4.24.0/mathlib toolchain under `projects/physqed`.

```bash
python -m pip install -r requirements-test.txt
python -m unittest discover -s projects/physqed/tests -v
python projects/physqed/benchmarks/multi_premise_v10.py /tmp/physqed-v10.json
python research/physqed-multi-premise-v10/independent_oracle.py /tmp/physqed-oracle.json
python projects/physqed/standalone_guard.py
```

To compile the pinned existing Lean examples, install [elan](https://github.com/leanprover/elan), then:

```bash
cd projects/physqed
lake update
lake exe cache get
lake env lean lean/TwoPremise.lean
lake env lean lean/MultiPremise.lean
```

For the constructive v1.1 tests specifically:

```bash
python -m unittest discover -s projects/physqed/tests -p 'test_constructive_essentiality_v11.py' -v
```

## Contents

| Path | Purpose |
| --- | --- |
| `projects/physqed/` | Exact checking engine, compiler, receipt gate, semantic controls and v1.1 extension |
| `projects/physqed/lean/` | Pinned Lean source examples; public-repository compilation is still pending |
| `projects/physqed/tests/` | Unit, adversarial, refusal and independent-oracle tests |
| `projects/physqed/benchmarks/` | Deterministic conditional-claim benchmark generators |
| `research/physqed-*/` | Mathematical notes, verification protocols and independent audit code |
| `.github/workflows/physqed*.yml` | Automated Python, SymPy and Lean checks |

See [the v1.1 theorem and limitations](research/physqed-multi-premise-v11/README.md) and [the engine documentation](projects/physqed/README.md).

## Provenance and evidence

This standalone repository is a scoped copy of the PHYSQED-specific paths at private source commit
`efafa326392b5f639e91114bfc36cc396393a667` (theoremlean PR #48) plus the documented standalone-release adjustments. Unrelated private theoremlean projects are not included; the original source PR is not generally accessible to public readers.

The existing v1.0 deterministic benchmark consists of 880 generated cases; the independent SymPy oracle checks its mathematical tasks separately. Version 1.1 additionally constructs rational witnesses to the essentiality of hypotheses. The fixture labels are synthetic, not blinded expert annotations. Source-code tests or queued CI jobs do **not** confer Lean or empirical-physics certification. Check the current [GitHub Actions runs](https://github.com/tonynewton79-web/PHYSQED-v1.1/actions) for the exact commit before citing a remote pass.

**Status:** public research source; v1.1 release validation is gated on exact-commit automated verification.

## Publication and supplementary-material notes

- The v1.1 research note refers to a **separate, locally produced** 120-system/360-witness evaluation and companion ZIP/PDF/LaTeX materials. These files were **not present** in the source PR's GitHub tree and have not been published here. Reproducibility from this checkout covers the committed v1.1 tests on 80 earlier positive multi-premise specimens, the two-premise illustration, and the v1.0 880-case benchmark and independent oracle. The separate 120/360 evidence must not be represented as reproduced by this repository alone.
- Older v0.3–v0.5 research notes retain historical references to private development. The current public-release boundary is this repository and its specifically selected PHYSQED paths; those historical statements are not instructions to republish unrelated private work.
- **License:** no open-source license has been selected for this release. Public source visibility does not itself grant redistribution or other reuse rights. A future license requires the author's decision.
