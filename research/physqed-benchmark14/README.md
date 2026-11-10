# PHYSQED Benchmark 14 — frozen deterministic exact challenge (10 November 2026)

**Claim boundary:** This benchmark evaluates a *bounded exact rational polynomial implication checker*, and its controlled statement, units, and provenance refusal gates. It does **not** verify physical laws, arbitrary mathematical propositions, natural-language semantics, experimental evidence, complete Lean formalization, or global Einstein equations.

## Benchmark design

- Three arities: 2, 3 and 4 independent affine equalities.
- 48 independently generated cases per arity, each with nine adversarial mutations.
- Total: **1,440** challenges (**144 positives**, **1,296 negative controls**).
- Gold mathematical checks: **independent SymPy expansion** and rational assignments demonstrating essential premises and falsity of deliberately modified conclusions.
- Policy controls: changed quantifier, provenance, dimension declarations, malformed schema, text/formal drift and explicit physical overclaims.
- All case definitions are deterministic and published. This is **not a secret, blinded, or external-human-labelled benchmark**.
- Any unsupported or mismatched type must be refused rather than promoted into a new physics or theorem claim.
- v1.3 companion regression: 105 exact arithmetic, tensor, controlled-claim and linked Einstein–Maxwell test probes.

## Reproduce

From repository root, with Python 3.11 and SymPy 1.14.0 installed:

    python research/physqed-benchmark14/benchmark.py
    python research/physqed-v13-independent/benchmark.py

The scripts write \`benchmark14_receipt.json\` and \`benchmark_receipt.json\` with per-case verdicts and SHA-256 row ledgers.

## Verified hosted reference

- Benchmark 14: 1,440/1,440, zero false acceptances, zero false refusals, zero unexpected exceptions.
  https://github.com/tonynewton79-web/PHYSQED-v1.1/actions/runs/42832152307
- Prior three-fix A/B version of v1.3: 105/105.
  https://github.com/tonynewton79-web/PHYSQED-v1.1/actions/runs/42827714268

**The stronger global physics release holds in the main README and v1.2 GH audit remain in force.**
Existing automated research tests and mathematical certificate checks are not equivalent to external peer review.
