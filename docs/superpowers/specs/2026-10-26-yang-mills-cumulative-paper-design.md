# Cumulative Yang--Mills Paper Design

## Intent

Prepare Tony Newton's first coherent, professionally typeset research article
about the finite four-dimensional SU(2) Wilson model and its proof-carrying
verification components. The article addresses mathematical readers, not a
software release manager. It integrates rather than simply concatenates the
separate technical notes already reviewed in this repository.

## Main contribution and limits

Place the physical Wilson transfer construction and the verified
strong-coupling estimate `lambda_n/lambda_0 <= 6 beta` for `0<beta<1/6`
at the center. Give a complete mathematical proof, including the S3
Poincare supersolutions, chordal W1 estimate, metric Gibbs comparison and
transfer eigenfunction test. Distinguish independent exact rational tests
and finite computational experiments from analytic proofs. Acknowledge
classical provenance and the unrefereed stronger `beta<2/9` proposal.

Do not describe the finite-lattice estimate as a continuum mass gap, an
original solution of an established problem, or a Lean-kernel proof.

## Audience and design

- Mathematically literate lattice gauge theorists, constructive QFT
  researchers, and verification specialists.
- Maximum eight main manuscript sections, clear notation before use,
  main theorem in the introduction, complete proofs and restrained prose.
- A4, one-column journal/preprint typography, Palatino-style mathematical
  text, readable equations, compact original data-driven figure and table.
- Author `Tony Newton`; no invented coauthors or institutional credentials.
- Reproducibility instructions are short and specific, not an internal
  test diary. No unneeded colored boxes, process boilerplate or decorative
  diagrams.

## Approaches considered

1. Focused theorem note: short and mathematically clean, but omits the
   substantial exact-character, Haar and PHYSQED work.
2. Cumulative research article **selected**: one theorem-centered narrative
   with distinct roles for finite transfer, exact certificates and empirical
   reproducibility. This meets the user's request for the main findings.
3. Broad claimed Millennium solution: excluded because the needed
   continuum construction and physical-units bound are absent.

The user earlier delegated technical presentation choices and now explicitly
requested a cumulative Yang--Mills paper; the selected design applies those
preferences without adding an external-publication action.

## Deliverables

- `research/yang_mills_su2/paper/Yang_Mills_Proof_Carrying_Wilson_SU2.tex`
- Its compiled, visually inspected PDF with the same stem.
- `research/yang_mills_su2/paper/CLAIM_LEDGER.md`: internal source-to-claim
  map; not part of the paper.
- The paper remains in an isolated feature branch until the user selects
  an integration operation.

## Release checks

1. Every cited analytical theorem is traced to a documented derivation and
   original literature; any premise not formalized is not attributed to a
   verifier.
2. Numerical results correspond to retained exact artifacts and do not
   equate character diagnostics with gauge-invariant interacting gaps.
3. The standard Python tests continue to pass. LaTeX compiles without
   undefined references, overfull lines or clipped figures; all PDF pages
   are rendered for visual inspection.
