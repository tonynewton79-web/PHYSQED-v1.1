# SU(2) Character and Gap-Counterexample Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Produce standard-library exact rational interval certificates for selected SU(2) Bessel character ratios, plus an exact counterexample to the finite-gap/continuum-gap inference.

**Architecture:** Use positive rational series terms to enclose the modified Bessel functions I_1(beta), I_2(beta), then monotone rational bounds on c=I_2/I_1 and the positive atanh-series bounds on -log(c). Require an independent SymPy numerical oracle and a fail-closed contract distinguishing pointwise certificates from uniform theorems.

**Tech Stack:** Python 3.11+ fractions.Fraction; unittest; independently SymPy 1.14.0 (already declared in requirements-test.txt).

**Spec:** docs/superpowers/specs/2026-10-25-yang-mills-three-track-design.md

## Global Constraints

- Exact rational input beta>0 for certificates; no floats in trusted bounds.
- Certified outputs concern only the finite character model and specified beta values.
- No inference from a finite Bessel-character gap to the physical 4D Yang–Mills mass gap.
- The large-beta limit 3/2 is a known analytic asymptotic requiring a separately cited proof, not implied by finitely many interval checks.
- Preserve existing PHYSQED semantics and executable source.

## Review Focus

1. Very large beta and too few terms: refuse until geometric tail ratio is strictly below 1.
2. Beta=0, negative beta, non-rational beta and nonpositive term counts: reject.
3. If ratio interval does not certify 0<c<1, refuse a positive gap receipt.
4. Atanh log bounds near c=0 or c=1 must be outward and tighten as terms increase.
5. Finite positive delta(a,L) with vanishing delta/a must be accepted as a counterexample, not mislabeled a mass-gap proof.

---

## Files and interfaces

- Create research/yang_mills_su2/character_bounds.py for exact Bessel/log bounds.
- Create research/yang_mills_su2/limit_obstruction.py for exact scaling counterexamples.
- Create research/yang_mills_su2/character_cli.py for input/output JSON.
- Create tests/test_character_bounds.py and tests/test_limit_obstruction.py under research/yang_mills_su2/tests.
- Create research/yang_mills_su2/CHARACTER_CERTIFICATES.md for algebraic derivation, scope and literature comparison.

### Task 1: Positive-series rational Bessel enclosures

**Files:** character_bounds.py, tests/test_character_bounds.py.

**Interfaces:** bessel_i_bounds(order:int,beta:Fraction,terms:int)->tuple[Fraction,Fraction]; character_ratio_bounds(beta:Fraction,terms:int)->tuple[Fraction,Fraction].

- [ ] Step 1: Write tests for I_1(2), I_2(2) enclosing independently evaluated SymPy besseli values; intervals strictly tighten when terms increase; invalid beta/order/terms and nonconvergent chosen terms are rejected. Test rational inequality for c(beta) at beta=2,4,8 only after bounds certify it.
- [ ] Step 2: Run python -m unittest research.yang_mills_su2.tests.test_character_bounds -v; expect missing implementation failure.
- [ ] Step 3: Implement t_k=(beta/2)^(2k+order)/(k! (k+order)!), sum k=0..terms-1, and upper tail t_terms/(1-r_terms) with r_terms=(beta/2)^2/((terms+1)*(terms+order+1))<1. All operations use Fraction.
- [ ] Step 4: Derive ratio interval [I2_low/I1_high,I2_high/I1_low], refusing if positive denominator or ratio-to-one is not certified.
- [ ] Step 5: Run the focused test; expect PASS. Commit Bessel bounds and tests.

### Task 2: Exact logarithmic gap and finite-to-continuum obstruction

**Files:** character_bounds.py, limit_obstruction.py, tests/test_character_bounds.py, tests/test_limit_obstruction.py.

**Interfaces:** negative_log_bounds(q:Fraction,terms:int)->tuple[Fraction,Fraction]; character_gap_bounds(beta:Fraction,bessel_terms:int,log_terms:int)->tuple[Fraction,Fraction]; collapsing_gap(n:int)->dict[str,Fraction].

- [ ] Step 1: Test q=1/2 and q=3/4: interval encloses independent high-precision SymPy -log(q), positive and narrows as terms rise; q<=0 and q>1 rejected.
- [ ] Step 2: Test the exact family a_n=1/n, delta_n=1/n^2 for n=1,2,5,100: all delta_n>0 while delta_n/a_n=1/n tends to zero; reject n<1.
- [ ] Step 3: Run the two test modules; expect failures.
- [ ] Step 4: Implement -log(q)=2*sum_{k>=0} z^(2k+1)/(2k+1), z=(1-q)/(1+q), with upper remainder 2*z^(2m+1)/((2m+1)*(1-z^2)) after m terms. Propagate monotonicity to an enclosure of -log(c).
- [ ] Step 5: Implement collapsing_gap with exact Fraction output and an explicit tag COUNTEREXAMPLE_TO_FINITE_GAP_INFERENCE, not a field-theoretic result.
- [ ] Step 6: Run tests; expect PASS. Commit log and obstruction certificates.

### Task 3: Reproducible evidence CLI and independent audit

**Files:** character_cli.py, CHARACTER_CERTIFICATES.md, tests/test_character_bounds.py.

**Interfaces:** certify_character(beta_numer:int,beta_denom:int,bessel_terms:int,log_terms:int)->dict; main(argv:list[str]|None=None)->int.

- [ ] Step 1: Test canonical JSON output with numerator/denominator fields for every rational bound, input parameters, exact-scope label, absence of unsupported theorem flags, deterministic fingerprint, and rejections of missing/invalid input.
- [ ] Step 2: Run targeted test; expect failure.
- [ ] Step 3: Implement certificate generation and a separate replay path that recomputes the bounds from input rather than trusting embedded intervals; include reproducible source identity metadata.
- [ ] Step 4: Add documentation deriving the series/tail formula and explaining why the beta*g(beta)->3/2 asymptotic is known external analysis, not a pointwise computational theorem.
- [ ] Step 5: Run focused suite and two identical CLI invocations, compare outputs. Commit CLI, documentation and tests.

## Completion gate

- [ ] No floating point enters accepted rational certificates.
- [ ] SymPy independently checks representative values; exact verifier replays every bound.
- [ ] Public outputs distinguish finite character evidence, a mathematical no-go example, and global Yang–Mills proof obligations.
