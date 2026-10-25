# PHYSQED v0.7 — Controlled Semantic Alignment Prototype

**Research status:** restricted exact mathematical-English/formal-JSON agreement only. No unrestricted natural-language understanding, physics certification, new Kerr computation, or Lean-kernel proof is asserted.

## Implemented
`projects/physqed/controlled_semantics.py` checks a tightly controlled mathematical statement, for example:

> For all real scalars x, y, z, the polynomial identity 2*(x+y)**2 == 2*x**2 + 4*x*y + 2*y**2 holds. This checks only the algebraic identity; no physical law is established.

The gate parses its two expressions through Python's safe restricted AST grammar (no calls, attributes, float literals or arbitrary code), independently reconstructs their rational polynomial coefficients, checks **both sides individually** against the submitted formal expression, and invokes PHYSQED's exact polynomial identity checker. It refuses changed quantifiers, extraneous physical claims, unknown symbols, unsupported assumptions, mathematically changed wording, and unrelated but true algebra.

## Validation
- 50/50 positive controlled equations accepted.
- 200/200 synthetic changed-claim challenges refused, in four separate categories.
- 187/187 cumulative local Python regressions passed, including 12 new tests.
- A separately written SymPy oracle checked all 50 identities and four mutation categories independently.
- GitHub v0.7 CI is required before claiming a remote pass; inherited Lean v0.3 remains pending on exact-source CI.

## Limits
This is proof of restricted **text-to-equation alignment**, not that a variable correctly represents a physical observable. The grammar refuses valid free-form PDE, relativity, quantum, conditional ODE or natural-language claims because those domains are unsupported. Input source and physical premise truth are not authenticated. Synthetic generator labels are not independently annotated public benchmarks. No comparative superiority claim is warranted.

To reproduce: `python -m unittest discover -s projects/physqed/tests -v` and `python projects/physqed/benchmarks/controlled_semantics_v07.py`. Independent SymPy oracle and full local release ZIP are available as separately prepared research artifacts.
