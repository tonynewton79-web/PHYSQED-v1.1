# PHYSQED v0.5 — Standalone proof-carrying physics research system

**Private alpha — research software; not a certified scientific proof system.**

## Purpose and package boundaries

This package contains the **reusable PHYSQED engine only**. It deliberately excludes every audited manuscript, numerical-relativity dataset, publication draft, bespoke physical solver, and paper-specific verification result. Each future paper receives its **own external audit folder**. Only generally useful improvements are promoted into this versioned engine after regression and independent checks.

The core v0.1–v0.4 modules are preserved intact from the frozen full v0.4 source package: exact rational-polynomial identities; independent grid replay; SI dimensional/role checking; typed statement compiler and generated Lean source; tamper-evident semantic review lock; symbolic and oscillator sanity/negative controls; and evidence-gated GitHub/Lean proof receipts. The v0.4 receipt does not award CI or Lean credit without successful GitHub evidence for the frozen commit and reviewed source.

**New in v0.5: `method_gate.py`.** A research project can export a *generic* method-neutral JSON manifest for PHYSQED to check, without uploading its manuscript into the engine. Checks include:

1. Matching claim/input/context digests across multiple declared methods, including optional verification of the actual frozen input and context bytes; refusal of incomplete, conflicting, pending, duplicated, or non-finite results.
2. Pairwise comparison of complex results using **exact decimal arithmetic** and a declared total tolerance/error budget. This is a consistency test, **not** a rigorous error enclosure unless the error estimates have themselves been independently validated.
3. Declared separation of method family, algorithm, implementation and source code; optional requirement to use different equation families. Labels are untrusted declarations, **not proof of independence**.
4. A mandatory negative-control test and three numerical sensitivity/stability settings, each with explicit acceptance thresholds. A failed control or unstable result blocks a pass.
5. **New source integrity binding:** `--source-root` verifies the SHA256 of the frozen input and context and every referenced on-disk method implementation, rejects symlink traversal and path escape, and refuses altered source bytes. Source integrity does **not** prove that the referenced code generated the asserted result.
6. Conservative report states: `LOCAL_METHOD_AND_SOURCE_INTEGRITY_PASSED__PROOF_UNVERIFIED` or `LOCAL_METHOD_CONSISTENCY_PASSED__SOURCE_UNVERIFIED__PROOF_UNVERIFIED`. Neither can claim kernel, scientific semantic, physical, or empirical verification.

## Quick start

Requires Python 3.11+ for unit tests and basic generic checks. Optional SymPy is required for the bundled independent symbolic audits. A Lean toolchain and a pinned mathlib checkout are required to compile Lean code locally; those are **not provided nor compiled** by the ZIP itself.

From the extracted package root:

```sh
python -m unittest discover -s projects/physqed/tests -v

# Real source-integrity gate on toy example (the input is synthetic, not a paper):
python projects/physqed/method_gate.py \
  --manifest projects/physqed/fixtures/generic_method_fixture.json \
  --source-root projects/physqed \
  --output generic_demo_report.json

# Run the independently written numerical/safety replay:
python projects/physqed/independent_v05_audit.py

# Optional, when SymPy is available:
python projects/physqed/audit_sympy.py
python projects/physqed/audit_conservation.py
```

The generated JSON is intentionally **not a formal proof certificate**. Do not treat synthetic fixture metadata as actual independently audited physical evidence.

## Integrating a new paper without bundling it

Create a private audit workspace *outside* this package. Its export should be a JSON manifest with the same field structure as `fixtures/generic_method_fixture.json`, plus the referenced method source files. Run the gate with `--source-root <path-to-that-workspace>`. Retain all raw inputs, logs, calibration conventions and exact software/toolchain versions **with the external paper audit**, not inside PHYSQED. A project may be tested repeatedly without changing the engine or expanding its distributable.

If a numerical analysis has only one real implementation, do **not** invent a second method to obtain a pass. Likewise, do not pretend that using different solvers of the same differential equation provides different physical equations. The reporting fields make the distinction explicit.

## Formal proof and release boundaries

A local numerical result cannot be promoted into a Lean proof receipt. The existing `proof_receipt.py` v0.4 module retains its requirements for an independently observed successful **push** workflow run at the exact SHA, the approved reviewed sources and successful named Lean proof steps. GitHub `queued`, `in_progress`, `failed`, or unauthenticated reports do not qualify.

The present release has **not** obtained a complete PHYSQED Lean-kernel confirmation for all bundled physics claims, verified human semantic-equivalence review, or empirical physics validation. The historical GH jobs previously observed were queued. Current GitHub state must be rechecked before any future release or employer demonstration.

## Threat model and limitations

- An operator can forge method inputs or metrics before freezing them: PHYSQED does not automatically attest execution, hardware, peer review, or independence of physical data.
- It verifies the content hash of supplied method files, but a valid hash does not prove a numerical program was run, that the source is good, or that its declared result is true.
- Finite sampled checks do not establish uniform validity across an unbounded domain. Nominal tolerances are not rigorous interval bounds.
- A shared convention or gauge error can infect multiple independent implementations. Domain review remains required.
- SHA256 manifests are for integrity and provenance. They are not signatures, not reviewer approval, and not substitutes for proof checking.
- Existing v0.4 proof receipt has an explicit fixed-claim oscillator scope. Extending it to arbitrary papers requires new formal contracts and separately compiled Lean declarations. V0.5 does **not** claim that the v0.4 oscillator Lean receipt automates arbitrary-theorem formalisation.

## Release version and ownership

Version 0.5, standalone distribution. Owner: Tony Newton, Newton Astro Labs, London, UK. Private research material; no licence to redistribute is granted by inclusion in this package.
