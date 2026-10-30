# Linked Shifted Einstein–Maxwell and Maximal-Nonnegative Constraint Boundaries

## Precise result and scope

This addition connects, on a **single source-compatible physical
model**, the 18-node shifted Einstein–Maxwell field-equation contract,
the exact rational domain/geometry/constraint-energy certificates, and
a boundary characteristic-inertia test. Its positive control is a
completely explicit vacuum Einstein–Maxwell spacetime.

The program distinguishes three statements:

- **Exact equation result:** each field/constraint residual in the
  18-node symbolic backend vanishes for the submitted spacetime, with
  independent rational 4D/3D curvature checks at specified witnesses.
- **Uniform-domain coefficient result:** lapse, spatial geometry,
  rational function denominators, symmetrizer and energy-defect matrix
  meet precise inequalities throughout a closed rational box.
- **Conditional boundary/energy theorem:** for an *existing smooth
  homogeneous constraint-system solution* whose traces lie in the
  declared boundary subspaces, an energy estimate controls the
  Hamiltonian/momentum constraint norm.

Only the first two are unconditional exact algebraic results about
the submitted model. The third invokes a standard integration
argument with explicit regularity, trace and corner hypotheses.
The implementation does **not** prove strong Lopatinski conditions,
nonlinear Einstein IBVP well-posedness, arbitrary-data existence or
that the Einstein evolution boundary conditions dynamically enforce
the submitted constraint trace spaces.

## Explicit physical reference solution

Take coordinates \((t,x,y,z)\) and define

\[
 h_{ij}=\delta_{ij},\quad N=1,\quad
 \beta^i=(1/5,0,0),\quad A_\mu=0,\quad\Lambda=0.
\]

The resulting spacetime metric is

\[
 ds^2=-dt^2+(dx+\tfrac15dt)^2+dy^2+dz^2.
\]

The affine change \(X=x+t/5\) gives
\(ds^2=-dt^2+dX^2+dy^2+dz^2\): this is exactly flat
Minkowski spacetime. Thus \(R^\alpha{}_{\beta\mu\nu}=0\),
\(F=dA=0\), and every vacuum Einstein–Maxwell tensor residual
vanishes identically. The positive-extrinsic-curvature ADM
convention used in PHYSQED gives \(K_{ij}=0\).
The Hamiltonian/momentum constraints and their Bianchi propagation
identities are therefore exact zero identities.

The source-domain and energy calculations on
\(D=[0,1]^4\) yield

\[
\boxed{N>\tfrac12,\quad h\succeq I_3,\quad
S=\operatorname{diag}(1,4,4,4)\succeq I_4,\quad R=0.}
\]

The restricted AST is preserved *exactly* across field and domain
models: the compiler compares the original source representations
for \(h,N,\beta\), rather than only their simplified SymPy forms.
Negative-power denominators in the Maxwell potential and supplied
coupling terms are separately recorded and must be nonzero on \(D\).

## Maximal nonnegative boundary-characteristic subspaces

The constraint state is \(U=(H,M_x,M_y,M_z)^\mathsf T\).
For spatial metric \(h\), lapse \(N\), shift \(\beta\), and a
coordinate outward conormal \(n_i\), the spatial principal symbol
of the homogeneous constraints has characteristic speeds

\[
  -\beta^i n_i \pm
       N\sqrt{h^{ij}n_i n_j},
 \qquad-\beta^i n_i\quad\text{(twice)}.
\]

Provided \(N^2h^{ij}n_i n_j-(\beta^i n_i)^2>0\),
the wave pair has one positive and one negative speed. The two
transport modes have the opposite sign to \(\beta^i n_i\),
or zero when it vanishes. Because the symmetrizer is SPD,
the quadratic form \(SA(n)\) has the same inertia as the
principal symbol \(A(n)\) by Sylvester's law.

The verifier proves the strict normal-speed gap and the
constant sign of the outward normal shift across **each face**.
It then determines the dimension of a maximal nonnegative
subspace of the symmetric boundary flux matrix \(SA(n)\).

The supplied trace frame \(T\), whose columns specify allowed
boundary states \(U|_{\partial\Omega}=Tv\), must pass:
1. An exact rational face-wide positivity test
   \(T^\mathsf TSA(n)T\succeq0\).
2. A full-rank certificate obtained from a strictly nonzero minor
   throughout that face.
3. Equality between its number of columns and the expected
   maximal nonnegative boundary dimension.

The algorithm does **not** confuse one positive-flux direction
with a maximal boundary condition. If the boundary normal shift
is tangent (zero), the face is characteristic: two transport
speeds vanish; the verifier records this explicitly. It does
not assert that characteristic boundaries satisfy full uniform
Lopatinski or provide regular boundary traces for arbitrary data.

## Exact six-face reference certificate

For the constant-shift Minkowski control, the dimensions of
maximal nonnegative trace spaces are

\[
\begin{array}{c|cccccc}
\text{face} &x=0&x=1&y=0&y=1&z=0&z=1\\
\hline
\dim T&3&1&3&3&3&3 .
\end{array}
\]

On \(x=0\), use the three basis vectors
\((1,\tfrac12,0,0)\), \((0,0,1,0)\), \((0,0,0,1)\).
On \(x=1\), use the single vector
\((1,-\tfrac12,0,0)\).

On \(y=0,1\), take the positive wave vector
\((1,0,\pm\tfrac12,0)\) (plus sign at the lower face),
together with the two transverse pure-momentum vectors.
Use the analogous construction at the \(z\)-faces.

Independent exact arithmetic gives, in the listed basis orders,

\[
\begin{split}
 T_{x=0}^\mathsf T SA(-dx)T_{x=0}
 &=\operatorname{diag}(12/5,\,4/5,\,4/5),\\
 T_{x=1}^\mathsf T SA(+dx)T_{x=1}
 &=(8/5),\\
 T_{y=0,1}^\mathsf T SA(\pm dy)T_{y=0,1}
 &=\operatorname{diag}(2,0,0),\\
 T_{z=0,1}^\mathsf T SA(\pm dz)T_{z=0,1}
 &=\operatorname{diag}(2,0,0).
\end{split}
\]

Every restricted flux is positive semidefinite. The rank-3
frames on \(x=0,y=0,1,z=0,1\) and rank-1 frame on \(x=1\)
are full rank. This is a valid maximal-nonnegative
**constraint-subsystem boundary algebra certificate** for the
explicit reference solution.

It does **not** establish that arbitrary Einstein initial data
admit a compatible nonlinear boundary value solution, or that
boundary restrictions on the spacetime metric naturally induce
those exact constraint trace frames.

## Rigorous conditional energy statement

For the constant-coefficient homogeneous constraint system,
let

\[
 e=\tfrac12H^2+2(M_x^2+M_y^2+M_z^2),\quad
 F^i=\tfrac12U^\mathsf TSA^iU.
\]

As \(S,A^i\) and \(B=0\) are constant,
the exact symmetric-hyperbolic identity is

\[
 \partial_t e+\partial_i F^i=0.
\]

For any sufficiently smooth solution on
\([0,1]\times[0,1]^3\) satisfying the six declared trace
subspaces and the necessary edge/corner compatibility,
integration of the local identity and the nonnegative
outward flux at every face gives

\[
 \boxed{\mathcal E(t)\le\mathcal E(0).}
\]

In particular, zero initial constraints imply identically
zero constraints in the domain of such a smooth solution.
The explicit zero constraint state of the shifted Minkowski
model satisfies the boundary restrictions, but this does
not establish existence of nontrivial arbitrary-data
solutions to those conditions.

The energy theorem uses no unverifiable sign heuristics:
\(R=0\), the symmetrizer is uniformly positive, and the
exact boundary forms are nonnegative. The remaining analytic
assumptions concern the existence, differentiability, and
boundary traces of the unknown solution; those assumptions
remain visibly unproved in the stored certificate.

## Implementation and negative controls

- \`v12/linked_adm_boundary.py\`: one input and combined
  18-node field, domain and boundary-inertia result;
  fails closed when source metric/lapse/shift ASTs differ.
- \`v12/linked_adm_cli.py\`: strict JSON input and distinct exit
  codes (0 scoped success; 2 failed/inconclusive obligations;
  3 invalid/unsupported source).
- \`examples/typed/linked_adm_shifted_minkowski.json\`: positive
  exact Einstein–Maxwell shifted-flat control.
- \`linked_adm_undercomplete_boundary.json\`: still
  positive-flux but too few allowed boundary directions at x=0.
  Must **not** be certified compatible.
- \`linked_adm_mismatched_geometry.json\`: source geometry mismatch
  between field and domain contracts; rejected.
- \`linked_adm_unconserved_matter.json\`: flat metric with
  time-dependent Maxwell field; the linked physical model fails
  the 18-node Einstein–Maxwell equations.

The independent negative tests additionally cover a negative-flux
face, rank-deficient supplied frames, masked source-domain poles
in geometry or Maxwell potential, unsupported growth rates,
non-proven periodic boundary compatibility, characteristic
zero-speed faces and receipt tampering.

\`\`\`bash
PYTHONPATH=projects/physqed python -m v12.linked_adm_cli \
 --input projects/physqed/examples/typed/linked_adm_shifted_minkowski.json \
 --output linked_adm_boundary_receipt.json

python -m unittest discover -s projects/physqed/tests \
 -p 'test_physics_v12_linked_adm_boundary.py' -v
\`\`\`

All code remains on the draft PHYSQED v1.2 feature branch
until native GitHub Python 3.15.2 and inherited regressions pass.
No Lean-kernel proof of the continuum PDE or nonlinear Einstein
boundary-value theorem is claimed.
