# Yang–Mills PHYSQED Evidence Bridge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Attach strictly scoped, fail-closed PHYSQED v1.1 algebra receipts and traceable external evidence to the SU(2) pilot without implying continuum or physical certification.

**Architecture:** One declarative algebra fixture certifies the quaternion link inverse/scalar norm identity through PHYSQED's unchanged v0.1 engine. A separate evidence ledger correlates finite-model numerical and rational interval records by source hash and status; unexecuted Newton Solver/EINSTEIN-X integrations are explicitly pending.

**Tech Stack:** Python 3.11+, standard library, existing projects/physqed/engine.py and replay.py; unittest and the existing PHYSQED tests.

**Spec:** docs/superpowers/specs/2026-10-25-yang-mills-three-track-design.md

## Global Constraints

- Do not change existing PHYSQED verifier/replay semantics to accommodate this pilot.
- Never assert physical_law_proven or lean_kernel_verified.
- A numerical measurement, an exact character-series bound, and a PHYSQED polynomial receipt are distinct evidence classes.
- Newton Solver and EINSTEIN-X Ω actual execution requires the exact executable source archives/commits; until then, preserve status SOURCE_UNAVAILABLE_NOT_EXECUTED.
- No global Yang–Mills proof claim, public release claim, or auto-merge.

## Review Focus

1. Corrupted PHYSQED fixture or wrong algebraic sign must be refused, not ignored.
2. Forged receipt booleans or changed embedded hash must not override independent re-execution.
3. Missing finite-model result must not be silently substituted with sample values.
4. Unknown evidence type or unknown certificate status must fail closed.
5. An unavailable external solver must never display EXECUTED, VALIDATED or CERTIFIED.

---

## Files and interfaces

- Create research/yang_mills_su2/fixtures/quaternion_inverse_identity.json: v0.1 PHYSQED algebra contract.
- Create research/yang_mills_su2/evidence_bridge.py: engine invocation and ledger validation.
- Create research/yang_mills_su2/tests/test_evidence_bridge.py: contract, adversarial and status tests.
- Create research/yang_mills_su2/EVIDENCE_SCOPE.md: machine evidence taxonomy and claim boundary.

### Task 1: Exact quaternion algebra fixture

**Files:** fixtures/quaternion_inverse_identity.json; tests/test_evidence_bridge.py.

**Interfaces:** The fixture is a PHYSQED physqed-0.1 JSON claim with id YM-SU2-ALG-001 and one algebra_identity check over variables a,b,c,d. Its lhs is the scalar quaternion component a*a-b*(-b)-c*(-c)-d*(-d); rhs is a^2+b^2+c^2+d^2. No assumption that a^2+b^2+c^2+d^2=1 is automatically discharged.

- [ ] Step 1: Write unittest spawning python projects/physqed/engine.py research/yang_mills_su2/fixtures/quaternion_inverse_identity.json from repository root, asserting returncode 0, status MATHEMATICAL_COMPONENTS_VERIFIED, physical_law_proven=false, lean_kernel_verified=false, one passing algebra check.
- [ ] Step 2: Run test_evidence_bridge; expect fixture-missing failure.
- [ ] Step 3: Create fixture with the exact recursive JSON expression schema from projects/physqed/fixtures/kinetic_identity.json; explicitly label it a local quaternion algebra identity, not gauge theory existence.
- [ ] Step 4: Run fixture test; expect PASS. Commit fixture and test.

### Task 2: Evidence ledger with hard status boundaries

**Files:** evidence_bridge.py, EVIDENCE_SCOPE.md, tests/test_evidence_bridge.py.

**Interfaces:** verify_physqed_fixture(path:Path)->dict (invokes existing engine without modifying it); record_evidence(kind:str,source_path:Path|None,metadata:dict)->dict; build_ledger(records:list[dict],newton_source:Path|None=None,einstein_source:Path|None=None)->dict; validate_ledger(ledger:dict)->None.

- [ ] Step 1: Test three allowed evidence kinds PHYSQED_EXACT_POLYNOMIAL, EXACT_RATIONAL_INTERVAL, FINITE_LATTICE_NUMERICAL; all must have source identity and their correct limited scope. Invalid kind/status/hash and missing source must raise ValueError.
- [ ] Step 2: Test empty solver paths force both external engine fields to SOURCE_UNAVAILABLE_NOT_EXECUTED, and reject a forged EXECUTED status without a verified source receipt.
- [ ] Step 3: Test changing a coefficient in a copied fixture forces PHYSQED REJECTED, and that a modified certificate hash or self-reported verified boolean cannot bypass subprocess re-execution.
- [ ] Step 4: Run tests; expect failure.
- [ ] Step 5: Implement ledger as canonical JSON with SHA256 of actual input bytes, no authenticity claims. Record solver source presence only as SOURCE_LOCATED_UNTESTED until an actual versioned integration test is added in a later approved plan; never mark it executed on path presence alone.
- [ ] Step 6: Document evidence status semantics and the unproved requirements (full physical spectrum, reflection positivity/OS axioms, cutoff and volume limits, nontriviality, all compact simple G).
- [ ] Step 7: Run bridge tests and full existing PHYSQED unittest discovery; expect PASS. Commit bridge, scope document and tests.

### Task 3: Cross-workstream pilot report assembly

**Files:** evidence_bridge.py, tests/test_evidence_bridge.py; modify research/yang_mills_su2/README.md after physical and character plans complete.

**Interfaces:** assemble_pilot_report(character_certificate:Path,simulation_result:Path,algebra_fixture:Path)->dict with explicit sections math, physical_numerical, physqed, external_solver_integrations, open_obligations.

- [ ] Step 1: Test two independent finite records and the verified algebra fixture are all cited by hashes, no data is fabricated, and unprovided records cause refusal.
- [ ] Step 2: Run test; expect failure.
- [ ] Step 3: Implement assembler with verified file schemas and fail-closed cross-references; document independent replay commands, scope and provenance, and refrain from automatically generating a scholarly manuscript until novelty/proof audits.
- [ ] Step 4: Run bridge tests and all new physical/character suites together; expect PASS. Commit assembler and test.

## Completion gate

- [ ] The unchanged PHYSQED v1.1 engine accepts the honest algebra fixture and rejects an altered sign.
- [ ] Every pilot evidence item has a replayable source and a truthful scope.
- [ ] Missing Newton Solver/EINSTEIN-X executable sources are unambiguously marked unexecuted.
- [ ] No statement suggests a Clay prize solution, empirical proof, full Lean verification, or an established continuum gap.
