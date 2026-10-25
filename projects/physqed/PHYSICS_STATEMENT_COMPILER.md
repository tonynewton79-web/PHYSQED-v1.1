# PHYSQED 0.2 — Physics Statement Compiler: proof obligations and trust contract

**Status: experimental alpha.** No claim of physical truth, empirical validation, automatic natural-language interpretation, or Lean-kernel compilation is made by the Python report.

## Purpose

A physicist or an AI specifies a precise, inspectable contract. The compiler tracks what symbols mean, checks units against a fixed role registry, rejects malformed or ungrounded claim representations, and demands that each proposed conclusion have an explicit exact-polynomial proof obligation. A claim cannot be approved by changing its hypotheses or introducing undeclared premises inside a witness.

## Versioned contract schema

Required exact keys: `contract_version`, `id`, `statement`, `provenance`, `context`, `symbols`, `assumptions`, `conclusions`, `proofs`, `mapping`. Unknown extra keys are rejected. `context` requires domain, frame, regime, regularity, boundary conditions and gauge (an explicit `not_applicable` is allowed). Each typed symbol has a controlled `role` and `unit`; unlike v0.1, the submitter cannot redefine unit dimensions. Every assumption has a source and must appear as an explicit Lean theorem hypothesis. `mapping.statement_conclusion_ids` exhaustively enumerates conclusions, but its explanation is **self-declared**, not verified against natural language.

For each formal equality C_L=C_R, the compiler verifies the exact polynomial certificate

    C_L - C_R == sum_i W_i (A_i,L - A_i,R)

where the A_i are exactly the listed assumptions. The tests use rational canonical polynomial coefficients and a separately implemented exact multivariate grid-replay algorithm. All powers are nonnegative bounded integers; division by variables, inequalities, differential operators, tensors, integrals, arbitrary uploaded code, and empirical uncertainty are **outside this version's trusted language**. A zero on one side of an equation is unit polymorphic, but untyped dimensionless constants are not silently added to physical quantities.

A verified certificate establishes an implication between algebraic equalities for commutative real scalars. The compiler also generates a Lean/mathlib theorem with explicit physical assumptions as hypotheses and a proof script using `linear_combination` or `ring`. These emitted source bytes receive a SHA256 digest, but **the compiler never sets `lean_kernel_verified` true**. The GitHub Lean job must compile the generated file separately, and even a successful Lean build does not validate natural-language semantics or experimental claims.

## Case study: oscillator work-rate balance

**Hypothesis:** m a = -k x. **Conditional algebraic conclusion:** k x v + m v a = 0.

A witness W=v gives k x v + m v a = v (m a + k x), so the conclusion follows from the hypothesis. The equation has SI dimension kg m² s^-3. This is compatible with the time derivative of an energy but does **not** yet prove that x'=v, v'=a, that motion is smooth, or that the physical Hooke-Newton model applies. These additional hypotheses and calculus steps require separate formal proofs or physical validation.

## Adversarial invariants

- No untrusted unit definitions, no undeclared or colliding symbols or hypotheses, no unknown input keys or executable payloads.
- Every conclusion checked; no circular use of other conclusions in a certificate.
- Dimensionally incorrect equalities and proof multipliers fail closed.
- Incorrect coefficients/signs fail independent exact-polynomial verification.
- Direct restatement of an assumption as a derived claim is refused; explicit constant contradictions are refused. General consistency of nonlinear assumption systems is **not** established.
- No model is ever reported as physically verified, even when its algebraic conclusion is exact.
- SHA256 receipts are integrity metadata, not authentication or proof of semantic alignment.

## Tests and independent audits

`python -m unittest discover -s projects/physqed/tests -v`

`python projects/physqed/audit_sympy.py` (separate SymPy 1.14.0 reconstruction)

`python projects/physqed/compiler.py projects/physqed/fixtures/oscillator_contract.json --output /tmp/physqed-v02-report.json --lean-output /tmp/CompiledOscillator.lean`

`cmp /tmp/CompiledOscillator.lean projects/physqed/lean/CompiledOscillator.lean`

CI executes the independently rebuilt SymPy check, compares Lean bytes and compiles the generated theorem under pinned Lean 4/mathlib. GitHub CI status must be inspected separately before claiming Lean verified.

## Remaining research challenges

The difficult unsolved engineering work is the **semantic bridge**: natural-language claims to precise machine statements with reviewable human authority; completeness of physical hypotheses and model interpretation; explicit spacetime/tensor geometry; conservation from differential identities; distributional/weak and boundary conditions; trusted Lean proof receipts; interval analysis and PDE/numerical error envelopes; calibrated experimental evidence; formal provenance identities; and benchmarked false-acceptance rates against Physlib, FormalScience and Axiomatic AI's Lemma.

Development: Tony Newton / Newton Astro Labs, private research prototype.
