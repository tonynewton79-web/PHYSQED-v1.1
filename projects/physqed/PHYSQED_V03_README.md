# PHYSQED v0.3 — Conservation and Frozen Statement Contract

**Research status: local Python verification completed, Lean proof compilation unverified unless the GitHub `lean-calculus` job succeeds.** Branch and PR remain private. This is not a claim of a new physics theorem.

## Mathematics, not just algebra

Define E(t) = (m/2)v(t)^2 + (k/2)x(t)^2. If x and v have derivatives v and a, respectively, and the damped oscillator force balance holds at each required t,

    m a(t) + c v(t) + k x(t) = 0,

then the chain and product rules give

    E'(t) = m v(t) a(t) + k x(t) v(t) = -c v(t)^2.

If c=0 and these hypotheses hold for all t in the connected domain ℝ, the mean value theorem gives E(t)=E(0). If c>=0 then E'(t)<=0. If c>0 and v(t)!=0 then E'(t)<0. Our Lean file `lean/Conservation.lean` states all these assumptions, including pointwise `HasDerivAt` hypotheses, rather than assuming energy constancy. **Its Lean compilation is not attested by this text; inspect the GitHub CI job.** No general existence/uniqueness theorem for x and v has been formalised. No comparison with measured oscillators has been made. Formal theorem uses real constants m,k,c; physical interpretation normally also assumes m>0 and k>0. Those are not logically needed for the power identity.

## Independent replay and falsification

The independent `audit_conservation.py` uses SymPy to differentiate E and substitute x'=v and v'=(-cv-kx)/m (valid m>0), independently reconstructing -cv². Separate analytic underdamped trajectories are evaluated for c=0 and c=1, with a quadrature cross-check of ∆E=-∫c v² dt. A deliberately false c>0 conservation claim is rejected. These computations are synthetic mathematical controls, not empirical measurements.

## Reviewed-statement integrity, NOT semantic truth

`semantic_lock.py` freezes the exact canonicalised v0.2 structured statement including text, source, physical context, symbol meanings, assumptions, proof witnesses and generated Lean theorem bytes. The offline reviewer holds a secret 256-bit-or-longer HMAC key outside Git and out of the AI tool. The lock verifies content integrity against the approved snapshot, not whether the English claim is actually equivalent to the Lean proposition. Human approval itself is not inferred from the existence of a signature; possession of a key alone does not establish reviewer identity. In particular, an internally consistent but semantically wrong statement can be signed and will still carry `semantic_alignment_verified=false` and `physical_law_proven=false`. **Do not commit real reviewer keys.** The CI uses only a public synthetic test key.

Commands (repo root):

    python -m unittest discover -s projects/physqed/tests -v
    python projects/physqed/audit_conservation.py
    python projects/physqed/audit_sympy.py

To freeze one exact structured contract using an externally held base64 reviewer key in a local file:

    python projects/physqed/semantic_lock.py projects/physqed/fixtures/oscillator_contract.json --lock review-lock.json --key-file /secure/path/reviewer-key.b64 --freeze --reviewer-label "external-reviewer-id"

To verify without renewing approval:

    python projects/physqed/semantic_lock.py projects/physqed/fixtures/oscillator_contract.json --lock review-lock.json --key-file /secure/path/reviewer-key.b64

## Trust boundaries and next gaps

1. No machine proof yet that a free-form human scientific claim matches its typed mathematical counterpart. HMAC is an integrity control, not a semantic proof, and the reviewer-label field is not identity verification.
2. CI needs to compile the Lean source on the pinned toolchain; a queued, skipped, or cancelled GitHub job is **not** a successful compilation.
3. No measured data or uncertainty budgets, no boundary-value/PDE/tensor formalisation, no formal domain-interval extension, and no independent code-reconstruction of Lean proofs yet.
4. The v0.2 compiler covers polynomial equalities; v0.3 conservation is currently a separately authored Lean theorem. Unifying calculus AST parsing and code generation is a later target.
5. The novel engineering claim is a *prototype integration*, not discovery of the harmonic oscillator power identity or priority over Physlib, Lean, or similar formal physics systems.

Research: Tony Newton, Newton Astro Labs, London, UK.
