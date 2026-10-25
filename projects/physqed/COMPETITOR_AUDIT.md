# PHYSQED Competitive Architecture & Evaluation Contract (2026-10-23)

## Purpose

PHYSQED is an independent **physics claim-verification and certification workflow**, not a replacement for Lean. Its innovation target is an auditable bridge between human physics statements, formal propositions, numerical calculations and empirical evidence. This is a **research and product hypothesis**, not an established novelty claim.

## Prior art and honest competitive baselines

- **Lean 4/mathlib**: the trusted proof kernel and mathematical library, not something PHYSQED should reimplement.
- **Physlib** (formerly PhysLean): community-curated Lean formalizations of physics; high-priority upstream dependency or interoperability target (https://physlib.io).
- **FormalScience / FormalPhysics** (Meadows, Zhang, Freitas, ACL 2026): agentic scientific autoformalisation and a set of 200 physics problems. Its documented semantic-drift risk is a direct test target (https://aclanthology.org/2026.acl-long.1057/).
- **Sakana AI Scientist v2**: autonomous scientific idea generation, experimentation and paper writing; distinct from rigorous claim certification (https://github.com/SakanaAI/AI-Scientist-v2).
- **SciLean**: scientific computing in Lean (https://github.com/lecopivo/SciLean).
- **Axiomatic AI / Lemma / AxQM**: direct contemporary competitor, combining physics modelling, machine-checked reasoning and experiments. AxQM describes 1,019 kernel-checkable proof synthesis tasks over 479 textbook items; proposed benchmark (https://axiomatic.ai/research/). Do **not** claim PHYSQED invented AI formal certification of physics.

## Integration with existing private research

- **Newton scientist layer**: may propose hypotheses, derive relations, design experiments and counterexamples; it is not trusted as a verifier.
- **EINSTEIN-X Ω**: potential independent mathematical and physical execution engines (symbolic, tensor, PDE, interval, SAT/SMT and Lean); validate interfaces and provenance before integration.
- **PHYSQED**: verifier, conservative claims ledger, certificate format, reproducibility and release gates. No self-awarded proof credit.

## Planned claim contract

Every submitted claim should have:
- exact natural-language statement and source;
- explicit assumptions, frame, gauge, regularity, boundary/initial conditions and domain;
- dimensioned typed quantities and precise symbolic conventions;
- formal proposition and an inspectable mapping back to the human statement;
- kernel proof plus axiom-closure review OR rigorously checkable computational witness;
- independent replay from evidence/code and declared tolerances;
- empirical calibration when the claim is about nature rather than abstract mathematics;
- tamper-evident provenance and explicit remaining limitations.

## Severity gates

1. **INPUT/HYGIENE**: invalid parser input, missing assumptions/provenance -> refuse.
2. **DIMENSIONS/GEOMETRY**: incompatible dimensions, index conventions or tensor type -> refuse.
3. **MATH**: failed exact identity, proof kernel check, interval enclosure, or independent replay -> refuse.
4. **SEMANTICS**: proof concerns the wrong statement or smuggles hypotheses into definitions -> HOLD, regardless of kernel success.
5. **PHYSICAL VALIDATION**: theory assumptions not established or experimental data unavailable -> mathematical verification only, NEVER unconditional 'physics certified'.
6. **CERTIFICATE**: scope, provenance, reproducible hashes, runtime/toolchain and reviewer or automated-check signatures included; hash alone is not authentication.

## Competitive evaluation plan

Benchmark against equivalent tasks, not marketing claims:
- FormalPhysics 200 problems: exact human-statement-to-Lean alignment and semantic drift rate.
- AxQM published benchmark: kernel-checked proof validity, prohibited-axiom rate, cost and time where accessible.
- Physlib regression suite: compatibility, portability and definition reuse.
- Physical negative controls: wrong units, sign changes, incorrect covariant/contravariant indices, dropped boundary conditions, misidentified Hamiltonians, false limiting cases.
- Simulated/empirical controls: known conserved quantities, convergence, uncertainty propagation and withheld measured data.
- Adversarial operator: submits a true algebraic lemma behind a false law; **must never receive unconditional physical certification**.
Report coverage, false acceptance and false rejection, failure reasons, execution cost and independently reproduced outcomes.

## v0.1 status (actual)

Exact rational polynomial normalisation and a separate exact full-degree grid check were implemented, together with limited SI-dimension checking, deterministic component receipts and negative controls. This is **not yet** a physics statement compiler, empirical validation engine, or trusted Lean-receipt ingestion mechanism. Python suite passed locally (18 cases); check GitHub Actions separately for Lean compilation.

## Release rule

Do not advertise PHYSQED as superior to Lean/Physlib/Axiomatic or as certifying physical truth before independent matched benchmarks. Keep this research in the private theoremlean repository unless explicitly authorised for publication.
