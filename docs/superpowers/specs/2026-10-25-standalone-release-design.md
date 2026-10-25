# PHYSQED v1.1 standalone public repository

## Intent and release boundary

Publish the complete PHYSQED research software from private
`tonynewton79-web/theoremlean` to the user's empty public
`tonynewton79-web/PHYSQED-v1.1` repository, without publishing unrelated
theoremlean research or changing the source repository.

## Approach

Selected: a clean source snapshot limited to PHYSQED program files,
tests, examples, associated PHYSQED research notes, and PHYSQED GitHub
workflows. Preserve the existing `projects/physqed/` directory layout so
the established test commands and verification paths continue to work.
An alternative, copying theoremlean's entire history, would expose
unrelated private projects. Flattening all source paths now would require
unnecessary changes to checks and receipt manifests.

## Goals

- Preserve full v0.1-v1.1 PHYSQED functionality and relevant provenance.
- Update hard-coded GitHub receipt binding to the new public repository.
- Provide a root README with accurate run instructions and explicit
  mathematical/physical verification limits.
- Keep all existing PHYSQED workflows and add release-path checks.
- Verify Python, independent SymPy oracle and Lean when possible.
- Never mislabel a queued or unrun CI job as passing.

## Non-goals

- No general semantic certification of real physical laws.
- No website or hosted user interface: the specified destination is a
  GitHub source repository.
- No changes or deletion in the private source repository.
- No pretense that missing supplemental PDF/ZIP files were in PR #48.

## Release gates

1. Enumerate selected source files against exact source SHA
   `efafa326392b5f639e91114bfc36cc396393a667`.
2. Audit selected text for hard-coded credentials and foreign project paths.
3. Demonstrate Python tests and versioned rational benchmarks.
4. Confirm the actual target default-branch tree after publication.
5. Treat remote Lean/CI as unverified until its exact-commit workflow succeeds.
