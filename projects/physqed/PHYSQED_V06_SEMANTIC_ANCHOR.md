# PHYSQED v0.6 — reviewer-anchored claim binding (restricted firewall)

This is a **new layer over the v0.5 methods gate**, not a natural-language scientific theorem prover.

## Implemented
- `semantic_alignment_gate.issue_reference`: an **external reviewer** explicitly approves the exact claim text, assumptions, source, and formal check JSON using a reviewer-held HMAC-SHA256 key (>=256 bits).
- `verify_alignment`: validates the review record and refuses altered English statements, mathematics, assumptions, claim identifiers, provenance or escalated scope.
- This mechanism **does not determine whether the reviewer chose a correct statement**, prove that the alleged reviewer is who they claim to be, validate the mathematical checks, compile Lean, establish method independence or verify physics.
- Explicit output fields `semantic_correctness_verified=false`, `physical_law_proven=false`, `lean_kernel_verified=false`.
- There is no default reviewer credential and test keys must never be used for actual review.

## Tests
```bash
python -m unittest discover -s projects/physqed/tests -v
python projects/physqed/benchmarks/adversarial_v06.py /tmp/physqed-v06-120.json
python projects/physqed/benchmarks/semantic_anchor_v06.py /tmp/physqed-v06-anchor.json
```

Local cumulative suite with extra signed/self-approval test: **175/175** tests passed.
Restricted reference challenge: **20/20** altered-English examples refused; **6/6** tampered formal/scope/key variants refused; **20/20** legitimate baseline bindings accepted. These are synthetic matches against an **already reviewed** exact statement.
Original unanchored semantic problem remains: **0/20** automatic recognition of false English physics claims. An explicitly *self-signed false physics statement* correctly obtains only a byte-matching report, never science/Lean certification.

## Known next tasks
1. **External reviewer attestation**: independent reviewer must first examine the exact English-to-formal statement mapping and guard the signing key; HMAC alone authenticates only key possession.
2. **Independent proof receipts**: fully green inherited v0.1–v0.3 GitHub CI at exact SHA, plus Lean mathlib imports/axiom audits.
3. **Semantic review benchmark**: evaluation against gold-annotated external scientific statements (including wrong-but-well-formed formalizations). Track false pass and false refusal rates separately.
4. **Head-to-head comparison**: published equal-task sets (FormalPhysics, AxQM), not raw within-system test counts.

**No claim that PHYSQED beats other physics proof tools.** Local test outcomes and the absence of authenticated external physical evidence must remain separate.
