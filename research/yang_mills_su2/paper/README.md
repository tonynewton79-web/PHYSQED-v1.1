# Four-dimensional Wilson SU(2) research paper

The cumulative journal-style manuscript is
Yang_Mills_Proof_Carrying_Wilson_SU2.tex. A verified compiled PDF
with the same stem is committed alongside it.

Compile from this directory:

    pdflatex -interaction=nonstopmode -halt-on-error Yang_Mills_Proof_Carrying_Wilson_SU2.tex
    pdflatex -interaction=nonstopmode -halt-on-error Yang_Mills_Proof_Carrying_Wilson_SU2.tex

Requirements: pdfLaTeX, AMS packages, Palatino mathpazo, mathrsfs,
microtype, hyperref, and pgfplots. The original figure is rendered
directly from the analytic spectral-ratio curves; no external artwork
is needed. The Monte Carlo table comes from the committed, replayable
finite-lattice experiment receipts.

CLAIM_LEDGER.md is an internal check of which source supports each
statement; it is not submitted as part of the manuscript.

The paper establishes no four-dimensional continuum mass gap.
Its PHYSQED receipts certify exact finite algebra and provenance,
not the full infinite-dimensional analytic argument in Lean.
