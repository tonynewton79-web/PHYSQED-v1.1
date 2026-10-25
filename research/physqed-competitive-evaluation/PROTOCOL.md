# PHYSQED v0.6 — independent and competitor evaluation protocol

## Present evidence
Initial **internal** deterministic baseline: 120 synthetic tests of polynomial algebra, declared SI dimensions and withholding unwarranted physics proof credit. All 120 matched their expected scoped component status. However the 20 mathematically valid cases paired with false English physics claims were **not recognized as semantic mismatches** (0/20); they only received mathematics-level status and physical_law_proven=false. No competitor was run and no generic Lean/physics certification follows.

## Equal-task public comparisons (not yet executed)
1. **FormalScience / FormalPhysics**: 200 university-level physics problems; test statement-to-Lean semantic preservation, not just compilation. https://aclanthology.org/2026.acl-long.1057/
2. **AxQM (Axiomatic AI)**: 1,019 kernel-checkable Lean tasks over 479 textbook items; use its actual Lean grader and specify independent or dependency-order regime. https://github.com/Axiomatic-AI/AxQM
3. **Physlib**: verify compatibility with curated reusable physical mathematical definitions and theorems, rather than counting unrelated Python unit tests. https://physlib.io/
4. **AI Scientist v2**: autonomous research generator; compare only certification of its exported results, not output volume. https://github.com/SakanaAI/AI-Scientist-v2

## Frozen scoring protocol
For each task retain: public task id, repo/paper SHA and version, human statement and context, target formal statement, gold verdict and validator, declared assumptions/units/gauge, system output, runtime, source/output hashes, Lean toolchain and genuine kernel outcome, blinded semantic review, failure explanation. Score false acceptance and false rejection separately, treat unattempted/unsupported as such, and report sample size/uncertainties. Compare equal tasks under equal information budgets; if a system does not support the task type, mark it unsupported, not mysteriously failed.

## Safety and honesty gate
Never promote a mathematics-only or syntactic matching result to physical verification. PHYSQED itself presently depends on human domain reviewers for correct English-to-formal semantics and independent validation of declared error budgets and physical data provenance. **Release comparison status: NOT_COMPARABLE; no competitor benchmark executed.**
