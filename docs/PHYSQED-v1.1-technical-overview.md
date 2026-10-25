# PHYSQED v1.1: Exact Certificates for Restricted Conditional Claims in Physics

**Tony Newton**  
Newton Astro Labs  
**Software and technical report, version 1.1 — 25 October 2026**  
Repository: <https://github.com/tonynewton79-web/PHYSQED-v1.1>

## Abstract

Scientific arguments combine mathematical deductions with assumptions about models, the meaning of symbols, and observations. A correct algebraic calculation does not by itself establish that a model describes nature, and a plausible scientific sentence does not by itself constitute a checked proof. PHYSQED (Proof-Carrying Physics) is experimental software intended to keep these forms of evidence separate while attaching reproducible certificates to a deliberately restricted class of claims.

The principal capability of version 1.1 concerns conditional polynomial equalities over the rationals. Given two to four independent affine premises and an explicitly supplied polynomial-ideal certificate for a conclusion, the verifier checks the exact identity, a controlled correspondence between the formal expressions and a bounded statement grammar, and consistency with declared SI dimensions. It also requires every premise to be essential to that particular conclusion. Version 1.1 strengthens the latter result constructively: for every premise of an **accepted** contract, it produces a rational assignment satisfying all the other premises while falsifying both the omitted premise and the conclusion. The assignments are independently re-evaluated with exact rational arithmetic.

The repository contains a Python implementation, adversarial and symbolic tests, an independent SymPy oracle for selected tasks, and separate Lean 4 examples. The mathematics is an application of standard polynomial algebra; it is not a new physical law. Neither the controlled grammar nor a Python receipt establishes the truth of a real-world premise, a general interpretation of unrestricted natural language, or a Lean-kernel proof of the certificate generator. The project is presented as an auditable component toward a broader system of scientific certification.

**Keywords:** formal verification; computational physics; proof-carrying claims; polynomial ideals; exact rational arithmetic; premise essentiality; counterexamples; Lean 4; reproducibility.

## 1. The verification problem

A scientific statement can fail for several distinct reasons. An equation may be algebraically false; two sides of an equality may have incompatible physical dimensions; a derivation may use a hypothesis that was never stated; the formal proposition checked by software may differ from the sentence read by a scientist; or a mathematically sound result may depend on a physical model unsupported by measurements. A single undifferentiated label such as “verified physics” would conceal these differences.

PHYSQED therefore treats a claim as an explicit contract comprising a controlled statement, formal expressions, named variables and declared dimensions, a list of premises, witnesses for the mathematical deduction, and provenance metadata. Each layer has a separate purpose and trust boundary. The current strongest mathematical layer covers finite rational-polynomial identities with two, three, or four independent affine premises. The exact certificates can support a limited **conditional** conclusion; they cannot supply evidence that the premises actually hold in an experiment.

The v1.1 contribution is constructive rather than merely declarative. Once the v1.0 conditions are met, the program returns checkable rational counterexamples showing what fails when any one hypothesis is removed. This directly addresses a common weakness in mechanized presentations of scientific arguments: a list of assumptions can be sufficient without each assumption being necessary for the stated conclusion.

## 2. The claim and its exact certificate

Let $x=(x_1,\ldots,x_n)$ be real scalar variables. All formal polynomial coefficients belong to the rational numbers $\mathbb{Q}$. Write the $k$ premises as

$$
p_j(x)=A_j(x)-B_j(x)=0,\qquad 1\leq j\leq k,\qquad 2\leq k\leq4,
$$

and let the conclusion be $T(x)=C(x)-D(x)=0$. In the present multi-premise domain, each $p_j$ is affine in $x$, while $T$ and the supplied witness polynomials $W_j$ may have higher degree within implementation limits. The formal statement is

$$
\bigwedge_{j=1}^{k}[p_j(x)=0]\quad\Longrightarrow\quad T(x)=0.
$$

Its certificate is the **exact identity**

$$
T(x)=\sum_{j=1}^{k}W_j(x)p_j(x).\tag{1}
$$

The verifier expands both sides as sparse rational polynomials and compares canonical coefficients without floating-point tolerances. Equation (1) immediately proves the conditional claim: if every $p_j(x)$ vanishes, every term on the right vanishes, hence $T(x)=0$. This conclusion is valid over any field in which the displayed polynomial identity is interpreted, in particular over the reals.

### 2.1 Independence is not essentiality

Write $p_j(x)=a_j\cdot x+b_j$, with $a_j\in\mathbb Q^n$, and let $M$ be the $k\times n$ matrix whose rows are the $a_j$. The accepted multi-premise contracts require

$$
\operatorname{rank}_{\mathbb Q}(M)=k.
$$

Exact rational row reduction verifies this condition. Since $M$ has full row rank, the affine equations $Mx=-b$ are jointly feasible over $\mathbb Q$, and none of the premise equalities follows from the remaining affine equations alone. That fact does **not** show that all of the premises are needed for the particular conclusion $T=0$. For example, a conclusion equal to $p_1$ does not need an unrelated independent premise $p_2$.

For each $i$, let

$$
V_{-i}=\{x\in\mathbb R^n:p_j(x)=0\text{ for all }j\ne i\}.
$$

Premise $i$ is *essential to the stated conclusion* if an $x\in V_{-i}$ exists for which $T(x)\ne0$. The predicate is claim-specific, not an absolute ranking of the scientific importance of the assumption.

### 2.2 The controlled-language boundary

The v1.0 gate accepts only a versioned, bounded input schema and a fixed grammar for universally quantified real-scalar equalities. It checks that each controlled equality parses to the same polynomial as the corresponding formal input. It also checks compatibility of declared SI dimension exponents, including each witness-times-premise term in (1). In this version the number of variables is bounded by eight, and polynomial expansions have term budgets; unsupported or over-budget inputs are refused.

This is a useful **syntactic and algebraic alignment check**, not unrestricted scientific-language understanding. Dimension declarations are supplied as part of the contract: the program checks consistency under those declarations but does not independently discover the physical meaning of a variable or verify the experimental provenance of its units. The accepted provenance class in this module is the explicit synthetic/scoped class, not a certificate of external scientific review.

## 3. The v1.1 constructive essentiality theorem

The key mathematical fact underlying v1.1 is that a nonzero rational polynomial cannot vanish at every rational point. The implementation makes that existence argument finite and constructive.

**Theorem (rational missing-premise witnesses).** Suppose $2\leq k\leq4$, the affine rational premises $p_1,\ldots,p_k$ have independent coefficient rows, and the exact identity (1) holds. Fix $i$. Use rational row reduction on the remaining $k-1$ equations to parameterize their rational solution points as

$$
x=\phi_i(y),\qquad y\in\mathbb Q^{n-k+1}.
$$

The same rational affine map $\phi_i$ parameterizes all real solutions when its free parameters range over $\mathbb R^{n-k+1}$. Let $R_i(y)=T(\phi_i(y))\in\mathbb Q[y_1,\ldots,y_{n-k+1}]$. If $R_i\not\equiv0$, there is a constructible rational assignment $x^{(i)}$ such that

$$
p_j(x^{(i)})=0\ (j\ne i),\qquad
p_i(x^{(i)})\ne0,\qquad T(x^{(i)})\ne0.
\tag{2}
$$

Conversely, if $R_i\equiv0$, the conclusion holds under the remaining premises alone, so premise $i$ is not essential to that conclusion.

**Proof.** Full row rank of the retained $k-1$ affine equations allows exact Gaussian elimination. Their solution set has $n-k+1\geq1$ rational free parameters, and all pivot variables are rational affine functions of them. Substitution into $T$ gives the exact polynomial $R_i$.

If $R_i\equiv0$, every point satisfying the retained equations also satisfies $T=0$, which is precisely nonessentiality. Otherwise take a nonzero $R_i$. For a single variable, a polynomial of degree $d$ has at most $d$ distinct roots; one of $0,1,\ldots,d$ must therefore give a nonzero value. For several variables, regard $R_i$ as a polynomial in the first variable with polynomial coefficients in the remaining variables. Evaluate the first variable successively at $0,1,\ldots,d_1$ until the resulting polynomial is nonzero. Repeat for the remaining variables. Each choice preserves a nonzero polynomial and terminates after a finite number of exact rational tests. The resulting $y^{(i)}\in\mathbb Q^{n-k+1}$ satisfies $R_i(y^{(i)})\ne0$. Put $x^{(i)}=\phi_i(y^{(i)})$. All retained premises vanish by construction and $T(x^{(i)})\ne0$. If the omitted premise also vanished, equation (1) would force $T(x^{(i)})=0$, a contradiction. Thus $p_i(x^{(i)})\ne0$. $\square$

The Python implementation explicitly checks every equality and inequality in (2) again in `fractions.Fraction` arithmetic before emitting a record. It refuses dependent or nonlinear premise systems, a vanishing restriction, or computations exceeding its configured term budget. The theorem describes the accepted mathematical class; it does not promise termination within fixed resource budgets for every conceivable polynomial input.

The distinction is important: **v1.0** decides essentiality through exact polynomial restriction; **v1.1** constructs and rechecks a concrete rational witness for each premise once the v1.0 contract has been accepted. A counterexample is to the *conclusion after omitting an assumption*, not to a physical observation.

## 4. Worked conditional examples

### 4.1 Two-stage normalized energy flow

Consider three abstract scalar quantities $e_{\mathrm{in}},e_{\mathrm{mid}},e_{\mathrm{out}}$. Suppose

$$
p_1=e_{\mathrm{in}}-e_{\mathrm{mid}}=0,\qquad
p_2=e_{\mathrm{mid}}-e_{\mathrm{out}}=0.
$$

The proposed conclusion $T=e_{\mathrm{in}}-e_{\mathrm{out}}=0$ has the explicit certificate $T=p_1+p_2$, so $W_1=W_2=1$. Both assumptions are essential to this particular conclusion:

| Premise omitted | $(e_{\mathrm{in}},e_{\mathrm{mid}},e_{\mathrm{out}})$ | Retained premise | Omitted residual | Conclusion residual |
| --- | --- | --- | ---: | ---: |
| $p_1=0$ | $(0,1,1)$ | $p_2=0$ | $-1$ | $-1$ |
| $p_2=0$ | $(0,0,1)$ | $p_1=0$ | $-1$ | $-1$ |

Each row is a direct rational certificate that the conclusion can fail when one equality is dropped. These are normalized mathematical examples. No measured energy flows or laboratory conservation law are established by the table.

### 4.2 Three and four independent equalities

The polynomial identity

$$
vat-ubs=(at)(v-u)+(ut)(a-b)+(ub)(t-s)
$$

proves the conclusion $vat=ubs$ conditional on $v=u$, $a=b$, and $t=s$. With four equalities $m=n$, $v=u$, $a=b$, $t=s$, an exact certificate is

$$
mvat-nubs=(vat)(m-n)+(nat)(v-u)
+(nut)(a-b)+(nub)(t-s).
$$

Here juxtaposition denotes multiplication. If $v,u$ denote velocity, $a,b$ acceleration, and $t,s$ time, the three-premise terms have dimensions of **energy per unit mass**, $L^2T^{-2}$. With $m,n$ assigned mass dimensions, the four-premise terms have **energy** dimensions, $ML^2T^{-2}$. The examples illustrate typed conditional algebra and do not claim an experimentally established relation among the values.

## 5. Software architecture and trust boundaries

PHYSQED is organized so that a component's successful check is not silently promoted into a stronger kind of certification.

| Component | Principal responsibility | Boundary |
| --- | --- | --- |
| [`engine.py`](../projects/physqed/engine.py), [`replay.py`](../projects/physqed/replay.py) | Canonical rational-polynomial identities and independent exact-grid identity replay | Finite, bounded algebra only |
| [`compiler.py`](../projects/physqed/compiler.py) | Versioned physical statement contracts and explicit witnesses; generation of scoped Lean source | Generated source is not automatically a compiled kernel proof |
| [`controlled_semantics.py`](../projects/physqed/controlled_semantics.py), [`semantic_alignment_gate.py`](../projects/physqed/semantic_alignment_gate.py) | Restricted mathematical-language alignment and refusal checks | No open-ended natural-language interpretation |
| [`two_premise_claims.py`](../projects/physqed/two_premise_claims.py), [`multi_premise_v10.py`](../projects/physqed/multi_premise_v10.py) | Exact conditional identities, declared dimensions, independence and essentiality for two to four premises | No empirical truth of hypotheses |
| [`constructive_essentiality_v11.py`](../projects/physqed/constructive_essentiality_v11.py) | Rational witnesses demonstrating failure after omission of each premise | Depends on prior v1.0 acceptance; remains a Python certificate |
| [`proof_receipt.py`](../projects/physqed/proof_receipt.py) | Evidence-gated proof receipt handling | A locally asserted flag cannot substitute for an actual successful Lean workflow |
| [`lean/`](../projects/physqed/lean/) | Separate, pinned Lean 4 examples of algebraic and conditional statements | Not a Lean formalization of the full verifier or arbitrary scientific semantics |

The exact engine does not evaluate arbitrary user Python, treat floating-point approximate equality as proof, or trust a user-supplied field claiming verification. The multi-premise verifier rejects wrong schemas, mismatches between controlled text and formal sides, inconsistent declared dimensions, incorrect ideal identities, dependent affine premises, and nonessential hypotheses when essentiality is required. Resource ceilings are refusals, not mathematical counterexamples.

The constructor's structured result includes the inherited v1.0 contract SHA-256 digest, each omitted-premise index, a rational assignment and exact residuals. A digest identifies the bytes of a canonicalized contract; by itself it is not a digital signature, a scientific provenance audit, or independent peer review. Its status explicitly keeps `physical_law_proven`, `lean_kernel_verified`, and `independent_expert_semantics_verified` false.

## 6. Evaluation and reproducibility

The repository includes unit tests, adversarial rejections, exact rational witnesses, a separately implemented SymPy oracle for selected algebraic tasks, example Lean files, and GitHub Actions definitions. The evidence must be divided into **committed, reproducible inputs**, **locally executed checks**, and **remotely completed checks**.

### 6.1 Evidence within the repository

- The v1.0 synthetic challenge generator defines **880 cases**: 80 intended valid conditional contracts and 800 deliberately invalid cases. A separate oracle uses SymPy rather than merely trusting the result labels. On 25 October 2026, both local runs evaluated **880/880 cases correctly**, with zero false accepts and zero false refusals in the verifier benchmark. These are internally generated labels, not independent expert annotations.
- The committed v1.1 regression tests call the v1.0 verifier first, then check exact rational assignments for the **80 positive** three-/four-premise benchmark specimens (40 of each size), including independent symbolic substitution with SymPy. Additional tests exercise the two-premise normalized example and refusal of dependent, nonlinear and nonessential cases.
- A fresh local test run on 25 October 2026 with Python 3.12 and pinned SymPy 1.14.0 completed **237 unit tests with zero failures or errors**. The standalone-release guard also passed. This local result does not substitute for a remote workflow result or Lean compilation.
- A distinct earlier **120-system/360-witness** evaluation is described in the research note, but its original ZIP, complete records, PDF and TeX source were not available in the imported GitHub tree. These supplementary artifacts are **not** reproducible from the repository as presently published and should not be cited as an independently archived dataset.
- GitHub Actions for the public v1.1 repository remained **queued awaiting GitHub-hosted runners on 25 October 2026**. A queued job is neither a pass nor a failure of its programmed mathematical checks. Lean compilation in this public repository must not be represented as successful until a corresponding workflow actually completes.

The small mathematical examples here can be checked independently by hand. The larger synthetic tests probe implementation and refusal behavior, but their labels are not independent physicist annotations of real research statements. There is no reported prospective physical dataset, randomized expert-blind semantic evaluation, or matched end-to-end superiority benchmark.

### 6.2 Reproduction from the public checkout

Use Python 3.11 or later and the versions in [`requirements-test.txt`](../requirements-test.txt), including SymPy 1.14.0 for the independent symbolic tests:

```bash
python -m pip install -r requirements-test.txt
python -m unittest discover -s projects/physqed/tests -v
python projects/physqed/benchmarks/multi_premise_v10.py /tmp/physqed-v10.json
python research/physqed-multi-premise-v10/independent_oracle.py /tmp/physqed-oracle.json
python projects/physqed/standalone_guard.py
```

The specific constructive regression test is:

```bash
python -m unittest discover -s projects/physqed/tests \
  -p 'test_constructive_essentiality_v11.py' -v
```

For the existing Lean examples, install the Lean toolchain manager [`elan`](https://github.com/leanprover/elan), then use the pinned toolchain and mathlib project files:

```bash
cd projects/physqed
lake update
lake exe cache get
lake env lean lean/TwoPremise.lean
lake env lean lean/MultiPremise.lean
```

These Lean files demonstrate selected mathematics, not automatic kernel validation of the full Python proof-producing procedure. For a release citation, record the precise Git commit, dependency versions, commands, and the completed status of each independent job.

## 7. Relation to formal methods and remaining limitations

Proof assistants such as [Lean 4](https://lean-lang.org/) and community mathematical libraries such as [mathlib](https://github.com/leanprover-community/mathlib4) aim to check proofs against a small trusted kernel. PHYSQED presently has a different, narrower deliverable: a defined algebraic input language, an exact Python certificate checker, explicit counterexamples for missing assumptions, and cautious handling of evidence receipts. Its Lean examples are useful cross-checks on particular formal statements, but they are not an independent formalization of all Python parsing, normalization, rational elimination, or witness-generation code.

Systems such as [Physlib](https://physlib.io/) explore formalized physics content. PHYSQED has not completed a controlled head-to-head evaluation of correctness, expressiveness, throughput, robustness, or scientific usefulness against Lean, Physlib, or other research systems. Novelty should be assessed at the engineering and integration level rather than attributed to the polynomial algebra theorem, which is classical.

The current technical boundaries are substantial:

1. The accepted claim grammar is intentionally restricted; an arbitrary sentence from a physics paper is not automatically mapped to a semantically equivalent formula.
2. Premise dimensions and meanings are supplied in the contract; consistency is not independent physical interpretation.
3. No experimental measurements or model-fitting conclusions are certified by the rational certificates.
4. Nonlinear or dependent **premise systems**, as well as transcendental, tensor, differential-equation, uncertainty-aware and large-scale claims, are not covered by the v1.1 constructive theorem. Polynomial conclusions and polynomial witnesses may nevertheless be nonlinear.
5. The generator and verifier are written in Python, not proved correct in Lean; software bugs and errors in the specification remain a threat.
6. Synthetic challenges and local symbolic oracles are useful but do not replace independently annotated real scientific statements and completed public CI evidence.

These limitations are part of the claim's correct scientific scope. The system can strengthen the reliability of an algebraic subargument without warranting the larger assertion that a physical theory has been certified.

## 8. Development priorities and how to cite this version

The immediate engineering priorities are to obtain completed exact-commit GitHub Python and Lean checks; publish the missing supplementary witness records if they can be audited; introduce independently annotated real-paper contracts and explicit disagreement adjudication; and formalize a trustworthy connection between the accepted contract, its rational certificate, and a Lean theorem statement. Subsequent work can enlarge the language and mathematics cautiously, with negative tests for semantic drift, dimensional ambiguity, missing hypotheses and inappropriate inference from data.

For citation before a DOI is assigned, use:

> Newton, Tony (2026). *PHYSQED v1.1: Exact Certificates for Restricted Conditional Claims in Physics*. Newton Astro Labs. Software and technical report, version 1.1. <https://github.com/tonynewton79-web/PHYSQED-v1.1>.

A future Zenodo deposit should be linked to a specific immutable GitHub release or archived commit and should cite only artifacts actually included in that deposit. Record the eventual DOI here once Zenodo issues it; **none is claimed by this document**. The repository currently has **no chosen redistribution license**. Public GitHub visibility alone does not establish permission for third-party reuse; the author must select appropriate repository and deposit terms before publication under a license.

### Sources and project materials

1. [PHYSQED public source repository](https://github.com/tonynewton79-web/PHYSQED-v1.1), including the full [v1.1 mathematical note](../research/physqed-multi-premise-v11/README.md), [v1.0 exact essentiality note](../research/physqed-multi-premise-v10/README.md), [tests](../projects/physqed/tests/) and [workflows](../.github/workflows/).
2. [Lean 4 documentation](https://lean-lang.org/) and [mathlib source](https://github.com/leanprover-community/mathlib4).
3. [Physlib project](https://physlib.io/), referenced as related formalized-physics work, not as a benchmark result.

