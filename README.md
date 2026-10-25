# PHYSQED v1.1 — Proof-Carrying Physics

**Experimental exact-mathematics verification software by Tony Newton (Newton Astro Labs).**

PHYSQED attaches reproducible, machine-checkable evidence to *restricted mathematical claims* found in physics research. It aims to separate algebraic verification, interpretation of scientific language, formal proof compilation, and empirical validation instead of treating them as interchangeable.

The v1.1 extension handles conditional identities of the form

\[
C-D=\sum_{j=1}^{k} W_j(A_j-B_j),\qquad 2\leq k\leq4,
\]

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
| `projects/physqed/lean/` | Pinned, separately compiled Lean examples |
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
