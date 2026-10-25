# PHYSQED — core engine and versioned extensions through v1.1

**Start with the [repository overview](../../README.md) and [v1.1 mathematical note](../../research/physqed-multi-premise-v11/README.md).** The modules below preserve the v0.1–v0.5 scientific core. A separate `method_gate.py` adds generic multi-method checks; later modules provide controlled semantic claims, independent multi-premise rational certificates, and constructive missing-premise counterexamples. External audited research remains outside the engine. Do not claim Lean CI/physical certification based on local tests.

---

# PHYSQED — Proof-Carrying Physics (v0.1 experimental)

**Experimental research software; a certification component prototype, not a general physics theorem prover.**

PHYSQED is designed to add machine-checkable *claim contracts* to physics research. At present it can certify finite exact polynomial identities and check dimensional consistency using separately specified dimensions. It provides two independent exact reasoning paths for polynomial identities:

1. Canonical rational polynomial coefficient normalization (`engine.py`).
2. Multivariate exact grid testing based on the degree-bound polynomial identity lemma (`replay.py`).

Both paths must agree. The bounded grid is complete for its declared polynomial class: a polynomial of degree at most `d_i` in variable `x_i` vanishing at `d_i+1` distinct points in each coordinate is identically zero. Requests that exceed the exact grid budget fail closed.

A separate Lean 4 file (`lean/PhysicsAlgebra.lean`) proves two elementary symbolic identities, one conditional on the oscillator equation of motion. Lean compilation is a separate GitHub Actions job. **A Python certificate does not claim the Lean job passed.**

## Run

```bash
python -m unittest discover -s projects/physqed/tests -v
python projects/physqed/engine.py projects/physqed/fixtures/kinetic_identity.json
python projects/physqed/engine.py projects/physqed/fixtures/newton_dimension.json
```

The exact engine does *not* execute AI-authored Python, use `eval`, accept floating constants, or trust self-asserted verified booleans.

## Meaning of statuses

- `MATHEMATICAL_COMPONENTS_VERIFIED`: the specified polynomial identity checks passed exact coefficient and independent exact-grid checks; **not** a certification of the surrounding physical proposition.
- `CONSISTENCY_CHECKS_PASSED`: only declared dimensional checks passed; **not** a proof of a dynamical law.
- `REJECTED`: at least one specified check failed or was unsupported.

The certificate always sets `physical_law_proven = false` and `lean_kernel_verified = false`. SHA-256 hashes provide reproducibility/integrity checks, not authenticity or peer review.

## Threat model and roadmap

Untrusted submissions may contain mismatched physical definitions, fabricated numerical claims, omitted assumptions, semantic drift, errors in a supposedly independent proof, or misleading provenance. v0.1 does **not** solve these. The next gates are: a canonical physics-problem compiler; dimensional derivations from vetted units rather than only submitted declarations; formal claim-to-Lean statement alignment; machine-parsed Lean toolchain/axiom receipts; independent tensor/PDE/exact/interval backends; counterexample search; traceable data and code provenance; physical/empirical calibration; versioned attestations and no-overclaim report generation.

### Compared systems and background

- Lean 4: https://lean-lang.org
- Physlib: https://physlib.io
- FormalScience (2026): https://aclanthology.org/2026.acl-long.1057/
- Sakana AI Scientist v2: https://github.com/SakanaAI/AI-Scientist-v2

No novelty or superiority claim is established without head-to-head benchmarks and a broader prior-art review.

Author: Tony Newton — Newton Astro Labs, London, UK. The standalone public release repository is `tonynewton79-web/PHYSQED-v1.1`; source provenance is described in its root README.

## v0.2 preview — Physics Statement Compiler

See [the formal contract, trust boundary and examples](PHYSICS_STATEMENT_COMPILER.md). The new `compiler.py` takes a versioned physical statement contract, preserves source/premise/role/unit/context metadata, checks an exact witness relation for each conclusion, replays it independently, and emits a Lean 4 theorem source requiring actual CI compilation. Adversarial fixtures demonstrate refusal on altered signs and witnesses. Run `python projects/physqed/compiler.py projects/physqed/fixtures/oscillator_contract.json` from the repository root; CI is [PHYSQED 0.2 Physics Statement Compiler](../../.github/workflows/physqed-v02.yml). **No semantic or experimental certification is asserted.**

## v0.3 Conservation and statement freeze

See [the calculus proof and adversarial lock audit](PHYSQED_V03_README.md). The Lean calculus proof is **unverified until CI runs successfully**. Local Python proof-obligation and independent SymPy/trajectory tests do not confer physical certification.

## v0.4 — GitHub-evidence-gated proof receipts

See [PHYSQED_V04_README.md](PHYSQED_V04_README.md) for the two-stage reviewer-lock/live-GitHub receipt, its strict proof scopes and adversarial CI evidence tests. A local unit test or a queued CI job can never award Lean proof status.
