# PHYSQED v1.1 Standalone Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the complete scoped PHYSQED v1.1 source in `tonynewton79-web/PHYSQED-v1.1` with independently runnable checks.

**Architecture:** Copy an exact file inventory from the PR #48 head SHA into a separate source tree. Retain existing paths, change the receipt's repository boundary, add top-level release documentation and test that the new boundary is enforced.

**Tech Stack:** Python 3.11, SymPy 1.14.0, Lean 4.24.0/mathlib, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-25-standalone-release-design.md`

## Global Constraints

- Source commit: `efafa326392b5f639e91114bfc36cc396393a667`
- Destination: `tonynewton79-web/PHYSQED-v1.1`, currently public and empty.
- Preserve `theoremlean` exactly.
- No scientific/Lean over-certification; reject claims outside exact algebra scope.
- Publish only PHYSQED-specific source, research and CI paths.

## Review Focus

- Public repository might accidentally include non-PHYSQED material: audit exact file manifest.
- Hard-coded GitHub paths could still refer to the private source: assert receipt repository and tests.
- A Python pass could be confused with Lean success: README distinguishes them.
- A GitHub push might succeed with missing files: compare remote tree with local manifest.
- A CI run might remain queued: report actual remote status, not inferred success.

---

### Task 1: Import the PHYSQED-only snapshot

**Files:** `projects/physqed/**`, `research/physqed-*/**`, `.github/workflows/physqed*.yml`

- [ ] Import the 83 selected source blobs from the exact PR head.
- [ ] Confirm no unrelated files or credentials, and compare Git blob SHA for every unchanged file.
- [ ] Run the preexisting Python unit suite and the v1.0 880-case dual checks.

### Task 2: Bind PHYSQED to the new public repository

**Files:** `projects/physqed/proof_receipt.py`, `projects/physqed/README.md`, `projects/physqed/tests/test_standalone_release.py`, `README.md`

- [ ] Write a failing test asserting `REPO == 'tonynewton79-web/PHYSQED-v1.1'`.
- [ ] Run the targeted test; expect an old-repository assertion failure.
- [ ] Update the allowed GitHub repository constant and obsolete private-alpha wording.
- [ ] Add the clear top-level README and rerun targeted and whole Python suites.
- [ ] Run independent benchmarks and a source/credential scope audit.

### Task 3: Publish and verify

**Files:** Target GitHub repository `main` branch.

- [ ] Create a clean initial target commit with PHYSQED-specific source.
- [ ] Verify target GitHub tree paths, hashes and default branch.
- [ ] Inspect exact-commit GitHub Actions results (or report pending).
- [ ] Do not announce a verified v1.1 stable release before all gates pass.
