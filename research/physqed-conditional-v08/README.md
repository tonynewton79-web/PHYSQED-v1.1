# PHYSQED v0.8 — Conditional Polynomial Claim Firewall

**Status: restricted research prototype, not physics proof certification.**

This edition extends v0.7's controlled unconditional polynomial statements to one **conditional** real-polynomial claim:

\[
\text{For all real variables, } A=B \implies C=D,
\]

by checking a supplied exact polynomial witness

\[
(C-D)=W(A-B).
\]

The implication follows algebraically, without invoking an assumption about the reality or physical validity of \(A=B\). The implemented detector independently parses the controlled statement and compares **each individual side** with the formal JSON expression, checks dimensional consistency under *declared* SI-exponent vectors, and refuses inconsistent nonzero-constant premises, arbitrary extra prose or changed quantifier. It does not prove time derivatives, causal dynamics, experimental physics, data authenticity, Lean-kernel formalization, or natural-language semantics outside its grammar.

## Positive restricted example

Premise: \`m*a + c*v + k*x == 0\`.

Conditional conclusion: \`m*a*v + k*x*v == -c*v**2\`.

Certificate: \`v*(m*a+c*v+k*x) = m*a*v+k*x*v+c*v**2\`.

This is the algebra beneath an oscillator energy-rate calculation, **not** a proof of \(v=dx/dt\), \(a=dv/dt\), or the model equations; those are not represented here. SI units are self-declared, not independently verified from physics data.

## Reproduction

- \`python -m unittest discover -s projects/physqed/tests -v\`
- \`python projects/physqed/benchmarks/conditional_v08.py conditional-results.json\`
- \`python research/physqed-conditional-v08/independent_oracle.py independent-results.json\`
- \`python research/physqed-conditional-v08/fuzz_refusal.py malformed-results.json\`
- \`python projects/physqed/standalone_guard.py\`

Latest LOCAL results: **201/201 regression tests**; **560/560** synthetic conditional accept/reject classifications; independent SymPy/AST oracle **560/560** agreements; **300/300** malformed contract variants refused without unhandled exceptions. The 560 labels come from an internal deterministic generator; not an external blinded scientific corpus. This is NOT a head-to-head comparison against Lean/Physlib/AxQM/FormalScience.

## Formal release gates

Inherited v0.1-v0.3 GitHub CI and Lean mathlib proofs must pass on the exact release commit; jobs previously inspected were **queued**, not confirmed green. Successful Python/SymPy tests do not confer Lean proof receipts. No externally trusted reviewer has established physics-model applicability or semantic alignment for unrestricted human language.

## Decisive next challenge

Generalize the single-witness \`C-D=W(A-B)\` to independently certified multi-premise ideal membership with an auditable witness; add a restricted differential/ODE contract only with its analytic assumptions explicitly stated, and score against external, genuinely annotated physics-to-formal claim mappings.

### Adversarial second-pass correction

The polynomial budget gate initially emitted a lower-level `ControlledLanguageRefusal` for an oversized supplied witness. v0.8 now consistently raises `ConditionalRefusal`, with a dedicated regression test; the revised full suite passed **201/201** locally. This is fail-closed API consistency, not a new mathematical theorem.
