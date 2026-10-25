# PHYSQED v0.4 — Proof receipts with two independent trust gates

**Research stage:** Private development alpha. Not a general physics proof checker.

## Why this matters

A Lean file compiling does **not** imply that the natural-language physical claim was formalised correctly. A Python test passing does **not** imply that Lean compiled. A GitHub run JSON asserting success is **not authenticated evidence**. The v0.4 verifier separates:

1. **Review integrity:** an independent, reviewer-held HMAC key authenticates the exact approved claim contract, context, compiler output, proof source, Lean toolchain, mathlib pin, and workflow code. No reviewer key may be stored in Git.
2. **Lean CI gate:** the verifier makes fresh authenticated HTTPS requests to the GitHub API, demands an actual successful `push` workflow run and the specific named Lean job and compile steps, and checks the committed source/workflow bytes at the run's SHA against the reviewed hashes.
3. **Physics semantic / empirical validity:** STILL OPEN. Neither an HMAC nor a successful Lean compilation establishes that the natural-language claim is true of nature.

## Commands

From repository root, for reviewer-held key stored **outside** the repository:

```sh
# An operator must generate and privately retain a strong random 32+ byte key.
# Store it as standard base64, in a file outside Git.
python projects/physqed/proof_receipt.py \
  --root . \
  --contract projects/physqed/fixtures/oscillator_contract.json \
  --key-file /secure/location/reviewer-key.base64 \
  --review /secure/location/approved-v04.json \
  --reviewer-label reviewed-by-person \
  --freeze

# Offline verification: **does not award Lean credit**.
python projects/physqed/proof_receipt.py \
  --root . \
  --contract projects/physqed/fixtures/oscillator_contract.json \
  --key-file /secure/location/reviewer-key.base64 \
  --review /secure/location/approved-v04.json

# Live check: requires token with repo read and Actions read permissions.
# Uses HTTPS GitHub API only; refuses queued, failed, and PR merge-checkout runs.
GITHUB_TOKEN=... python projects/physqed/proof_receipt.py \
  --root . \
  --contract projects/physqed/fixtures/oscillator_contract.json \
  --key-file /secure/location/reviewer-key.base64 \
  --review /secure/location/approved-v04.json \
  --sha FULL_40_CHARACTER_PUSH_HEAD_SHA \
  --run-id REAL_PUSH_WORKFLOW_RUN_ID
```

The workflow targeted for Lean proof checks is **`.github/workflows/physqed-v03.yml`**, job **`lean-calculus`**, with the precisely named steps pinned in `proof_receipt.py`. This is distinct from `.github/workflows/physqed-v04.yml`, which tests *the receipt system itself*. A synthetic CI test key is intentionally used only in test code and must never be accepted as real human review authority.

## Status language

- `REVIEW_LOCK_VERIFIED__LEAN_CI_NOT_CONFIRMED` — exact contract and source unchanged relative to the reviewer-held key. No independent Lean compilation confirmation.
- `LEAN_CI_CONFIRMED__SEMANTICS_UNREVIEWED` — **only when** live GitHub API confirms a successful *push* run for the exact SHA and reviewed files, with all required Lean steps successful. The claim's physical interpretation remains unreviewed.
- Input, HMAC, GitHub API, source mismatch or missing steps: **refuse** or remain unverified.

## Strong negative controls

Wrong equations/units, altered claim English or frame, fake signatures, changed proofs, changed workflow or toolchain, forged proof file unrelated to compiler output, self-reported success, mismatched GitHub head SHA, missing/failed Lean steps, and `pull_request` merge checkouts are all blocked in the test suite.

**Important PR caveat:** existing v0.3 workflows use default `actions/checkout`, which in a `pull_request` event generally checks out a synthetic merge commit rather than the advertised PR head. Since that actual checkout is not independently attested in v0.3, v0.4 deliberately accepts **only `push` events** for proof credit. Future workflows can add measured checkout attestations instead of this restriction.

## Verification and release ledger

As of initial v0.4 development on October 23, 2026, the v0.3 GitHub CI runs are **queued**, so no Lean certification is claimed. Local suite: **115 tests**, passed; independent SymPy audits of conditional oscillators passed. These checks validate narrow examples, not an automatic physics semantics verifier.

Next: instrument Lean to emit a trusted no-sorry/axiom-audited proof receipt, disallow unsafe meta features, version a physics ontology, separate human-reviewed semantic equivalence from HMAC integrity, and benchmark against prior physics formalisation work.

Tony Newton — Newton Astro Labs, London, UK.
