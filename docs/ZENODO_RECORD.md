# PHYSQED v1.1 — Suggested Zenodo record metadata

This is a **metadata preparation sheet**, not a claim that a Zenodo record or DOI already exists.

| Field | Suggested entry |
| --- | --- |
| Title | PHYSQED v1.1: Exact Certificates for Restricted Conditional Claims in Physics |
| Creator | Newton, Tony |
| Affiliation | Newton Astro Labs |
| Publication date | 2026-10-25 (use the actual date of the archived release if later) |
| Version | 1.1 |
| Resource type | Software for a tagged source-code release; alternatively, Publication / Technical report if depositing the paper as a separate record |
| Keywords | formal verification; computational physics; exact rational arithmetic; polynomial identities; proof-carrying claims; hypothesis essentiality; constructive counterexamples; Lean 4 |
| Related identifier | https://github.com/tonynewton79-web/PHYSQED-v1.1 |
| License | **Author must choose before deposit.** The public repository currently has no open-source license. |
| DOI | **Not yet assigned.** Do not invent one. |

## Abstract to paste into Zenodo

Scientific arguments combine mathematical deductions with assumptions about models, symbol meanings and observations. PHYSQED (Proof-Carrying Physics) is experimental software for attaching reproducible, machine-checkable evidence to a restricted class of conditional claims while distinguishing algebraic verification from physical and empirical validation. Version 1.1 accepts two to four independent affine rational-polynomial premises and an explicit polynomial-ideal certificate for a conclusion. It checks the exact identity, alignment with a bounded mathematical statement grammar, and consistency with declared SI dimensions. Acceptance requires every premise to be essential to the stated conclusion. For each premise of such an accepted contract, the v1.1 extension constructs a rational assignment satisfying every retained premise while falsifying both the omitted premise and the conclusion; the assignment is rechecked using exact rational arithmetic. The public repository includes Python implementation code, adversarial and synthetic tests, selected independent SymPy replays and separate Lean 4 examples. These standard algebraic methods do not establish the truth of real-world premises, unrestricted natural-language semantic equivalence, experimental validity or a Lean-kernel proof of the complete Python generator. The work is an auditable research prototype for a more comprehensive scientific verification architecture.

## Files to archive

1. A **specific tagged release** or immutable commit of the [public repository](https://github.com/tonynewton79-web/PHYSQED-v1.1), including the executable code, tests, research notes and workflows.
2. The complete [technical report](PHYSQED-v1.1-technical-overview.md), either as Markdown or as a carefully typeset PDF derived from the same text.
3. A manifest stating the exact commit SHA, tool versions, replay commands, checksums and which CI workflows actually completed for that commit.
4. Only supplementary witness datasets and PDF/TeX files whose original bytes have been recovered and verified; the separately discussed 120-system/360-witness packet is **not currently in this repository**.

## Before publication

- **Choose the license** for the software and the report. A public GitHub repository without a license does not by itself grant reuse rights.
- Decide whether this should be a single **software** record or separate linked **software** and **technical report** records. Avoid publishing duplicate records of the same artifact without clear relationships.
- Check that a GitHub release archive contains the report and all files being described in the abstract and supporting evidence.
- Use the precise GitHub Actions run results for that immutable release. As of 25 October 2026, the new public repository's jobs were queued; do not label remote Python or Lean checks as passed.
- On Zenodo, record the DOI it assigns, then add the DOI badge and formal citation back to the repository. Do not guess a DOI or link the repository to a nonexistent Zenodo record.

For the full mathematical claims, hypotheses, proof and limitations, use the [technical report](PHYSQED-v1.1-technical-overview.md), not this short metadata sheet.
