# Cumulative Yang--Mills Paper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a self-contained, visually verified mathematical paper summarizing the correct finite SU(2) Wilson findings.

**Architecture:** Audit existing notes and exact receipts into an internal claim ledger; integrate precise analytic results into one journal-style LaTeX manuscript; compile and inspect a cumulative PDF. Keep the published mathematical scope separate from PHYSQED exact arithmetic evidence.

**Tech Stack:** LaTeX/AMS, PGFPlots, pdfLaTeX, Poppler, existing Python unittest suite, Git.

**Spec:** `docs/superpowers/specs/2026-10-26-yang-mills-cumulative-paper-design.md`

## Global Constraints

- No claim of constructive 4D continuum Yang--Mills or a positive physical-units mass gap.
- State `0<beta<1/6` and `lambda_n/lambda_0<=6beta` with the actual Wilson transfer normalization.
- Attribute classical comparison tools and distinguish the unverified proposed `2/9` threshold.
- Maximum eight main manuscript sections; all displayed mathematical objects defined before use.
- Preserve the previous reviewed branches and their files.

## Review Focus

1. A bare character Bessel ratio must never be described as the interacting transfer spectral gap.
2. A positive lattice-unit gap cannot be translated into a continuum physical mass gap.
3. Finite centered Monte Carlo covariances cannot be represented as exact equilibrium correlators.
4. The sharp one-quarter W1 constant has not passed our independent proof review.
5. PDF charts and mathematical expressions must not overlap, clip or conceal errors.

---

### Task 1: Claim audit

**Files:** Create `research/yang_mills_su2/paper/CLAIM_LEDGER.md`.

**Interfaces:** Consumes `*_SCOPE.md` notes, committed JSON artifacts and source literature; produces a reader-oriented map of permissible theorem and diagnostic claims.

- [ ] Record exact Haar, Bessel, transfer, Dobrushin, S3 and experimental claims, with assumptions and file source.
- [ ] Mark the difference between analytic proof, exact rational replay and stochastic diagnostic.
- [ ] Independently check every number intended for the manuscript against a committed receipt.
- [ ] Review the ledger for accidental continuum/priority claims.

### Task 2: Journal manuscript

**Files:** Create `research/yang_mills_su2/paper/Yang_Mills_Proof_Carrying_Wilson_SU2.tex`.

**Interfaces:** Consumes the claim ledger; produces eight or fewer coherent sections with complete mathematical arguments and verified source attribution.

- [ ] Write problem-first abstract, introduction and early main theorem.
- [ ] Explain Wilson geometry, gauge projection and positive transfer kernel.
- [ ] Prove SU2 character intervals, finite Haar null identities and the chordal mixing spectral theorem.
- [ ] Add only two relevant data-based elements: a spectral-window plot and a short seeded-transient table.
- [ ] State original work, established literature and unresolved continuum work precisely.

### Task 3: Build, verify and commit

**Files:** Produce the matching paper PDF and localized build ignore rules.

**Interfaces:** Consumes the source; produces a reproducible PDF with the source in an isolated committed branch.

- [ ] Mark PDF creation and compile twice using `pdflatex -interaction=nonstopmode -halt-on-error`.
- [ ] Run `pdfinfo`, render all pages with `pdftoppm`, inspect page images and detect overfull/undefined references.
- [ ] Rerun full Yang--Mills and PHYSQED test suites on the final paper-only branch.
- [ ] Verify `git diff --check`, commit the source, ledger and PDF, leaving the worktree clean.
