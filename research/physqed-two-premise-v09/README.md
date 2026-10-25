# PHYSQED v0.9 — Two independent affine premises

Tony Newton — Newton Astro Labs, London, UK

## Exact mathematical certificate

For rational multivariate polynomials, PHYSQED v0.9 checks the exact identity

C - D = W1*(A-B) + W2*(E-F).

Consequently, if A=B and E=F then C=D. This is a standard polynomial-ideal membership argument, not a newly invented general mathematical theorem. Both premises must be affine-linear with rational coefficient gradients of rank two: this certifies their independence and guarantees joint satisfiability as real affine constraints. Nonlinear premise independence is deliberately unsupported.

## Input/output

The two_premise_claims.py module accepts a fixed JSON schema with exactly two premise equations, two polynomial witness expressions and a conclusion; it checks exact polynomial arithmetic, each side of bounded controlled language, rank-two affine gradients and declared SI dimensional consistency. Outputs explicitly retain physical_law_proven=false and lean_kernel_verified=false. Provenance class is synthetic-scoped only.

## Reproduce

- python -m unittest discover -s projects/physqed/tests -v
- python projects/physqed/benchmarks/two_premise_v09.py /tmp/physqed_v09.json
- python research/physqed-two-premise-v09/independent_oracle.py /tmp/v09_oracle.json
- python projects/physqed/standalone_guard.py

Local isolated development replay using v0.6 packaged inherited sources and the new v0.9 overlay:
- 192/192 Python tests passed (175 inherited and 17 new). This is not a full v0.7/v0.8+v0.9 test run.
- 540/540 deterministic synthetic challenge classifications, with 60 accepted and 480 refused.
- 540/540 independent SymPy algebra, AST and dimensional oracle agreements, but from the same internal challenge generator.
- Current GitHub branch has the complete intervening v0.7 and v0.8 source. Its own all-inherited-test results require a new remote CI run on the exact SHA.

Lean: projects/physqed/lean/TwoPremise.lean contains a generic conditional soundness lemma and concrete example; CI compilation must pass before calling it kernel verified. A successful compilation of the general lemma would not prove that every JSON proof certificate is accurately translated into Lean.

NOT YET DELIVERED: independently annotated real scientific statements, nonaffine polynomial ideal-independence certificates, empirical physics validation or matched competitor superiority results.
