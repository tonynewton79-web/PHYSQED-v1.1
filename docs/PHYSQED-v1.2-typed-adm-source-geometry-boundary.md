# PHYSQED — Source-Preserving ADM Geometry and Boundary-Flux Certificates

## Exact mathematical objective

The previous rational-energy engine certified two interior inequalities,
\(S\succeq s_*I\) and \(R\preceq CS\), across a rational rectangular
spacetime box, but three proof obligations remained distinct:

1. Preserve **every original denominator restriction** before symbolic
   simplification can hide a pole.
2. Certify a **strictly positive lapse** and **positive-definite spatial
   metric** throughout the spacetime region, rather than at witnesses.
3. Certify the sign of the boundary energy flux on **declared admissible
   trace subspaces** of the symmetric-hyperbolic constraint system.

This implementation provides three explicit, separately auditable
component gates. It does **not** prove a solution of the full Einstein
equations, well-posedness of a nonlinear initial-boundary value problem,
or that a physical solution actually satisfies the asserted boundary
conditions. A 'pass' must therefore be described as **interior and
conditional boundary algebra**.

## A. Original source syntax controls the domain

The file \`v12/typed_adm_domain.py\` uses PHYSQED's safe, bounded
\`RestrictedExpression\` JSON syntax for exact rational functions.
Permitted constructors are exact integer, declared symbol, rational
literal, \`add\`, \`mul\`, \`neg\` and bounded integer \`pow\`.
Any \`pow\` node with a negative exponent causes its **base AST** to
be recorded as a nonvanishing-denominator guard *before the whole
expression is evaluated or simplified by SymPy*. Its source syntax,
exponent, and exact guard sign evidence are retained in the receipt.

Example:

\`\`\`json
{
  "mul": [
    {"add": ["t", {"rational": [-1, 2]}]},
    {"pow": [
      {"add": ["t", {"rational": [-1, 2]}]},
      -1
    ]}
  ]
}
\`\`\`

The resulting expression simplifies to 1, but the extracted guard
remains \(t-\frac12\ne0\). On \(0\le t\le1\) the guard cannot be
certified and the engine declines to certify the domain.
Thus a removable singularity in the **original supplied formula**
cannot be silently erased by the trusted compiler.

Source completeness is established for the **supplied restricted AST**.
It does not retroactively recover poles erased before the AST was
submitted by an external editor or symbolic process. General
trigonometric/square-root branch conditions are outside this rational
mode and are rejected. Every generated rational coefficient denominator
is separately audited by \`rational_energy.py\`.

## B. Strictly positive lapse and positive spatial metric

On the closed spacetime box \(D\), declare exact rational floors
\(N_*>0\) and \(h_*>0\). The implementation seeks a strict rational
Bernstein sign certificate for \(N-N_*>0\). For the symmetric
spatial metric \(h\), it checks all three leading principal minors:

\[
 h_{11}>0,\quad
 \det h_{1:2,1:2}>0,\quad
 \det h>0.
\]

Sylvester's criterion proves \(h(t,x)\succ0\) pointwise throughout
\(D\). In addition, a conservative rational-entry Gershgorin test
certifies the uniform numerical bound

\[
 \boxed{h(t,x)\succeq h_*I_3\quad\text{for all }(t,x)\in D}.
\]

This is a coordinate-component eigenvalue bound in the supplied
spatial basis, not an invariant comparison to a physically preferred
coordinate-free Euclidean metric. Domain and unit conventions must
be supplied and justified independently.

These geometry gates are run **before** construction of the shifted
ADM constraint coefficients. If the lapse/metric proof is inconclusive
or a source denominator sign fails, the energy and boundary gates
are not presented as a passing result.

## C. Boundary energy flux on a declared trace subspace

For the homogeneous symmetric-hyperbolic constraint equation
\(\partial_t U+A^j\partial_j U+B U=0\), with positive symmetrizer
\(S\), define

\[
 e=\tfrac12U^\mathsf TSU,\quad
 F^j=\tfrac12U^\mathsf TSA^jU,\quad
 R=S_t+\partial_j(SA^j)-SB-B^\mathsf TS.
\]

At a spatial box face with outward unit **coordinate** conormal
\(\nu\), the associated flux quadratic form is

\[
 F_\nu(U)=\tfrac12U^\mathsf T(\nu_j S A^j)U.
\]

The user supplies an exact rational **boundary trace frame** \(T\),
meaning that the trace of the *unknown solution* is required to lie
in the column space of \(T\): \(U|_{\partial\Omega}=Tv\). On that
declared space,

\[
 F_\nu(Tv)=\tfrac12v^\mathsf T
 \underbrace{T^\mathsf T(\nu_jSA^j)T}_{B_\nu}v.
\]

The engine restricts the flux matrix to each face and uses exact
rational Bernstein/Gershgorin bounds to certify
\(B_\nu\succeq0\) on the **entire face**, including time.
It requires one frame for each of the six spatial faces.
Source-level rational denominators in these boundary frames are
also tracked. The frame dimensions and flux-matrix symmetry are
checked.

**Critical distinction:** this verifies a flux sign *conditional
on the solution trace lying in the frame*. It does **not** prove
the trace actually does, that the restrictions are maximally
dissipative/Lopatinski-compatible, that they are not overdetermined,
or that a smooth PDE solution exists. Those are further analytical
obligations.

An alternative \`periodic_assumed\` mode checks that the principal
and symmetrizer coefficient matrices match on corresponding opposite
faces. Actual periodicity of the unknown solution is an assumption,
not a demonstrated property. \`unverified\` boundary mode always
holds the boundary gate open.

## D. Exact shifted-ADM model: all six face fluxes

The reference model uses coordinates
\((t,x,y,z)\in[0,1]^4\),

\[
 h=\operatorname{diag}(1+t,1,1),\quad
 N=1+t,\quad\beta=(1/5,0,0).
\]

The previously independently checked variable-ADM coefficient
formulas yield

\[
 S=\operatorname{diag}
  \left(1,\frac4{1+t},4,4\right),\qquad
 R=\operatorname{diag}\left(
  -\frac2{1+t},-\frac8{(1+t)^2},
  -\frac4{1+t},-\frac4{1+t}\right).
\]

The exact interior certificates establish

\[
 \boxed{N>\tfrac12,\quad
 h\succeq I_3,\quad S\succeq I_4,\quad R\preceq0}
\]

throughout the box. Every generated inverse-metric/lapse
denominator is strictly positive on the region.

For outward \(-dx\) and \(+dx\) faces choose one-dimensional trace
frames \(T=(1,+\frac12,0,0)^\mathsf T\) and
\(T=(1,-\frac12,0,0)^\mathsf T\), respectively. For the \(y\)-faces
replace \(M_x\) by \(M_y\), with the same signs; likewise for \(z\).
The exact outward flux coefficients \(F_\nu(T)\) are

\[
\begin{array}{ll}
 x=0:\ \frac{11t+12}{10(1+t)},&
 x=1:\ \frac{9t+8}{10(1+t)},\\[2mm]
 y=0,1:\ 1+t,&z=0,1:\ 1+t.
\end{array}
\]

All are strictly positive on \(0\le t\le1\). Thus for **any
existing smooth homogeneous constraint solution satisfying these
specific trace restrictions**, integration of the energy identity
gives

\[
 \boxed{\mathcal E(t)\le\mathcal E(0)}.
\]

The supplied boundary conditions are only illustrative
one-dimensional trace subspaces of a four-variable constraint
system. They are **not certified to define a well-posed or
physically realizable Einstein initial-boundary problem**. The
positive flux computation therefore should not be promoted as
an existence, stability or global spacetime theorem.

## E. Inputs, verification and replay

\`kind\` is a standalone typed domain model rather than a direct
extension of the existing \`einstein_maxwell_shift\` field-equation
specification. The full JSON schema for this gate is
\`physqed.typed-adm-domain.v1\`.

Use:

\`\`\`bash
PYTHONPATH=projects/physqed python -m v12.adm_domain_cli \
  --input projects/physqed/examples/typed/adm_domain_outgoing_flux.json \
  --output adm_boundary_receipt.json

python -m unittest discover -s projects/physqed/tests \
  -p 'test_physics_v12_typed_adm_domain.py' -v
\`\`\`

Three fixture models are provided:
\`adm_domain_outgoing_flux.json\`,
\`adm_domain_hidden_pole.json\`, and
\`adm_domain_incoming_flux.json\`.

The 18 regression tests cover all-six-face flux signs, hidden
source poles, incoming-flux refusal, bad lapse, indefinite metric,
insufficient metric floor, unsupported rational AST types,
periodic-coefficient-only assumptions, absent boundary evidence,
malformed face declarations, source-guard capture, masked poles in boundary frames, off-domain guard controls, and independent
recomputation of the complete receipt.

Native Python 3.15.2 GitHub CI and inherited legacy regressions
remain required before publication as a stable release.

## Open scientific/engineering obligations

1. Independently replay the new exact source/face integration
   against the actual installed source in native CI.
2. Certify existence, compatible regularity and **maximal
   dissipativity / boundary trace well-posedness** for physically
   specified Einstein constraints.
3. Couple the boundary gate directly to the source-evaluated
   Einstein–Maxwell 18-node shifted field-equation contract and its
   matter-conservation conditions.
4. Extend domain intervals/positivity to rational functions with
   nontrivial coordinate charts, matter source terms, and uniformly
   quantified derivatives.
5. Formalize Bernstein convex-hull, Sylvester, Gershgorin and
   energy integration implications inside a proof assistant.
