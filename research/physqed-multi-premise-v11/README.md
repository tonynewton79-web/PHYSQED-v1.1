# PHYSQED v1.1 — Constructive Affine Hypothesis-Essentiality Certificates

Tony Newton — Newton Astro Labs, London, UK

## Theorem and implementation
For linearly independent rational affine premises p_j = A_j-B_j, k=2,3,4, and polynomial target T=C-D, require the exact identity T=Σ W_j p_j, as already checked by PHYSQED v1.0. For each i, v1.0 tests the restriction of T to the other k−1 premise equations is nonzero. Version 1.1 **constructs a rational point** x^(i) at which all other premises hold, while p_i(x^(i)) and T(x^(i)) are both nonzero.

The algorithm rational-row-reduces the remaining affine equations, substitutes into T, and sequentially specializes each free coordinate using the univariate polynomial degree-bound identity lemma. It then verifies each original equation and T in exact Fraction arithmetic. These rational assignments are machine-checkable counterexamples to the conclusion when a named hypothesis is omitted. This is standard polynomial algebra, not a newly discovered theorem of physics or algebra.

## Evidence and test status
- Local external self-contained code + **independently implemented SymPy Gröbner/rank oracle**: 120 seeded systems, 40 each for 2/3/4 assumptions; **360/360** exact missing-premise rational witnesses checked.
- Five independent local regression tests passed, including two-premise normalized energy-flow model and refusals of dependent, nonlinear or nonessential constraints.
- A separate v1.1 GitHub test invokes the full **PHYSQED v1.0 verifier FIRST**, then constructs and rechecks witnesses on all 80 earlier positive benchmark specimens with SymPy. Results remain unconfirmed until exact-SHA CI completes.
- Existing v1.0 full 880-case benchmark and pinned Lean example compilation are likewise remote release gates; previously queued.
- Not independently expert-annotated physical claims. No real experimental input; no semantic-natural-language theorem, Lean kernel proof of the generator, or head-to-head competitor superiority.

## Concrete two-assumption illustration
For normalized energy-flow values e_in, e_mid, e_out, let p1=e_in−e_mid, p2=e_mid−e_out, T=e_in−e_out=p1+p2.
- Drop p1: (e_in,e_mid,e_out)=(0,1,1) gives p2=0, p1=−1, T=−1.
- Drop p2: (0,0,1) gives p1=0, p2=−1, T=−1.

No claim that real energy flows were independently measured is made.

## Reproduction
Local supplementary research ZIP includes pure-Python Fraction code, independent SymPy oracle, 120 full witness records, mathematical note PDF and source. GitHub integration lives at `projects/physqed/constructive_essentiality_v11.py`, with tests under `projects/physqed/tests/test_constructive_essentiality_v11.py` and a dedicated workflow.

**Release status: DRAFT_PENDING_REMOTE_CI / EXACT_MATH_SCOPE_ONLY.**
