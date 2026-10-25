# PHYSQED v1.0 — Three/Four Independent Affine Premises and Exact Essentiality

Tony Newton — Newton Astro Labs, London, UK

## Mathematically sound conditional certificate

Let p_j=A_j-B_j and T=C-D be rational polynomials in n real variables. For 2<=k<=4, verify the exact identity

T = sum_{j=1}^k W_j p_j

with explicit rational-polynomial witness polynomials W_j. Then every simultaneous zero of p_1,...,p_k is a zero of T. This standard polynomial-ideal argument is conditional algebra, **not a newly discovered universal scientific law**.

### Additional rank and essentiality theorem

Assume all p_j are affine-linear and their gradients have rank k over Q (the full row rank of the k-by-n coefficient matrix). Then the affine system p_1=...=p_k=0 is jointly feasible over R; no premise is an affine consequence of the others. But this DOES NOT establish that a particular conclusion T=0 needs all k premises.

For each i, consider the weaker system p_j=0 for all j != i, with affine variety V_i. Because the k-1 retained constraints are independent affine equations, exact rational row reduction parameterizes V_i by free coordinates over Q. Substituting this parameterization into T yields an exact polynomial T_i in the remaining n-k+1 coordinates. We have:

- If T_i is the zero polynomial, **premise i is not essential** for the displayed conclusion: all points satisfying the other equations already satisfy T=0.
- If T_i is nonzero, **premise i is essential**: a real (indeed rational) choice of free coordinates with T_i != 0 satisfies every other premise but violates the conclusion.

Thus the v1.0 per-premise non-vanishing test is an exact decision method for premise essentiality within the declared affine-linear rational domain. The construction uses no tolerances, random sampling or learned truth criterion. Computational refusal on a declared term/degree budget does not imply mathematical falsity.

Proof sketch: Exact Gaussian elimination with full row rank gives rational affine expressions for pivot variables in free variables, with no inconsistent row. Evaluation of T under these substitutions is exactly the restriction of T to V_i. A nonzero polynomial over Q does not vanish at every point of Q^d, proving the witness of failure without premise i. The zero case vanishes identically on all of V_i. The original ideal identity proves T=0 when all premises hold.

### Examples

For three equalities v=u, a=b, t=s, the exact energy-dimension identity is

v*a*t-u*b*s = (a*t)(v-u) + (u*t)(a-b) + (u*b)(t-s).

For four equalities m=n, v=u, a=b, t=s:

m*v*a*t-n*u*b*s = (v*a*t)(m-n) + (n*a*t)(v-u)
                  + (n*u*t)(a-b) + (n*u*b)(t-s).

The variables may be assigned declared SI dimensions: m,n mass, v,u velocity, a,b acceleration, t,s time. Both conclusion terms then have units of energy, and so do all witness-times-premise terms.

### Verification evidence and release gates

- Local independent **SymPy mathematical replay of the 80 positive benchmark specimens**: 80/80 identities, ranks, and essentiality checks passed. This checks the case formulas with independently implemented SymPy/Gröbner arithmetic, not the v1.0 verifier source.
- In GitHub: 12 direct tests and a total of **880 synthetic internally labelled examples** (80 positive, 800 deliberately invalid), plus a separate independent SymPy/AST/SI oracle over those challenges. Their exact-SHA GitHub test outcome must be checked before any all-880 pass claim.
- Generic Lean lemmas and fully concrete 3-/4-premise identities are provided in `projects/physqed/lean/MultiPremise.lean`; **compilation is pending**. Even successful compilation of these generic lemmas would not certify untrusted JSON-to-Lean translation.
- Independent external human-annotated physics semantics, full real-paper claim grading, physical/experimental validation, and matched FormalPhysics/AxQM head-to-head evaluation remain outstanding.
- All PHYSQED mathematical claims here require controlled input grammar and **synthetic provenance**; do not upgrade them to physical-law certification.

### Replay

```sh
python -m unittest discover -s projects/physqed/tests -v
python projects/physqed/benchmarks/multi_premise_v10.py /tmp/v10-results.json
python research/physqed-multi-premise-v10/independent_oracle.py /tmp/v10-oracle.json
cd projects/physqed && lake env lean lean/MultiPremise.lean
```

**Status:** locally independently checked 80 positive mathematical examples; GitHub actual v1.0 benchmark and Lean still require confirmed results. No scientific or competitive superiority claim.
