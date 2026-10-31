# PHYSQED v1.2 — Final Strong-Well-Posedness Release Gate

## Release verdict: HOLD

An independent replay of the previous regular-source reference packet passed **24/24 tests**, with a valid SHA-256 manifest. A further **19/19 exact local tests** independently certified two counterexamples to *overstrong proposed release claims*. The combined test run was **43/43 passing**. The matching 18-case GitHub regression suite has been committed but is not counted as native-green until Python 3.15.2 GitHub CI reports success.

The exact results do **not** refute known harmonic Einstein well-posedness results or the established **homogeneous decaying stable-mode** bound for the separate null-adapted problem. They show that the previous proof gates must **not** be promoted to an arbitrary-source frequency-weighted strong IBVP theorem or a standard-Euclidean maximal-dissipation theorem.

## 1. Counterexample to unrestricted L2 volume source → frequency-weighted metric norm

For each of ten symmetric trace-reversed metric components, the flat first-order reduction with independent source channels is

\[
\partial_t\psi+\Pi=F_0,\quad
\partial_t\Pi+\partial_i\Phi_i=F_\Pi,\quad
\partial_t\Phi_i+\partial_i\Pi=F_i.
\]

Let \(x\ge0\) and let \(y,z\) be periodic of period \(2\pi\). For an integer \(n\ge1\), choose **one** metric component

\[
\psi_n=t^2e^{-x}\cos(ny),\qquad
\Pi_n=\Phi_{x,n}=\Phi_{y,n}=\Phi_{z,n}=0,
\]
\[
F_{0,n}=2te^{-x}\cos(ny),\qquad
F_{\Pi,n}=F_{i,n}=0.
\]

Every forced equation holds exactly, and every first-order and auxiliary reduction field vanishes at \(t=0\). The first-order incoming characteristic conditions \(P(\Pi+\Phi_x)=0\) and the four first-order constraint boundary forms \(C_\nu^{(1)}=\Pi_{t\nu}+\Phi_{x,x\nu}+\Phi_{y,y\nu}+\Phi_{z,z\nu}=0\) are homogeneous.

Nevertheless the independent full-spatial and spacetime \(L^2\) calculations give

\[
\|e^{-x}\cos(ny)\|_{L^2(\Omega)}^2=\pi^2,\quad
\|F_{0,n}\|_{L^2([0,1]\times\Omega)}^2=\frac{4\pi^2}{3},
\]
\[
\|\partial_y\psi_n(1)\|_{L^2(\Omega)}^2=n^2\pi^2,\quad
\|D_n(1)\|_{L^2(\Omega)}^2=(1+n^2)\pi^2,
\]
where \(D_i=\partial_i\psi-\Phi_i\). Thus

\[
\boxed{\frac{\|\partial_y\psi_n(1)\|}
  {\|F_{0,n}\|_{L^2([0,1]\times\Omega)}}
 =\frac{\sqrt3}{2}n\longrightarrow\infty.}
\]

No universal estimate controlling the **full frequency-weighted norm containing tangential derivatives of \(\psi\)** by unrestricted first-order \(L^2\) volume sources alone is possible. The obstruction is the freely source-driven reduction defect, not a failure of the standard scalar wave equation. It does **not** preclude a *natural unweighted* first-order \(L^2\) energy theorem or an estimate under source compatibility \(F_i=\partial_iF_0\).

**Important:** the first-order expression \(C^{(1)}\) equals the actual metric harmonic constraint only when the reduction constraints vanish. The example makes their distinction explicit.

## 2. Exact failure of standard Euclidean first-order maximal dissipativity

At \(x=0\), the incoming/outgoing wave-characteristic amplitudes are \(w_+=\Pi+\Phi_x\), \(w_-=\Pi-\Phi_x\) in the ten-dimensional independent-metric-component Euclidean norm.

Set

\[
w_+=e_{tt}-e_{xx},\qquad w_-=e_{tx},\qquad
\Phi_y=\Phi_z=0.
\]

The six null-adapted homogeneous Sommerfeld rows satisfy \(Pw_+=0\). The four first-order harmonic rows \(\Pi_{t\nu}+\Phi_{x,x\nu}=0\) also hold **exactly**. However,

\[
\|w_+\|^2=2,\quad \|w_-\|^2=1,\quad
\boxed{F_{\text{outward}}
=-\Pi\cdot\Phi_x
=\frac{\|w_-\|^2-\|w_+\|^2}{4}
=-\frac14.}
\]

Therefore this homogeneous boundary space is **not maximally dissipative for the standard Euclidean symmetrizer**. The exact outgoing-to-incoming transfer has squared singular values \(3,3/8,1,1\) (plus zeros); it is not contractive.

The counterexample does **not** refute the previous uniformly controlled *decaying stable-mode* boundary operator: general boundary traces need not satisfy the Laplace–Fourier stable subspace or geometric reduction constraints. Nor does it refute any alternative positive symmetrizer or frequency-dependent Kreiss multiplier.

## 3. Verification and release gates

- Historical 24-case regular-source proof packet: **24/24 PASS** and SHA-256 integrity.
- Independent counterexample verifier: **19/19 PASS**, including exact frequency-unbounded family, zero initial data, zero incoming/harmonic first-order boundary rows, negative outward flux, boundary transfer Gram spectrum, and receipt-tampering rejection.
- Combined local replay: **43/43 PASS**, Python 3.13.5 / SymPy 1.14.0. The independently constructed ZIP was extracted and its manifest verified.
- Repository modules: \`projects/physqed/v12/gh_final_release_gate.py\`, \`projects/physqed/tests/test_physics_v12_gh_final_release_gate.py\`. These require **native GitHub Python 3.15.2 CI** before marking the committed branch green.
- PR #14 remains **DRAFT/UNMERGED**. All historical/ongoing GitHub Actions conclusions must be checked on the *exact* latest commit, not inferred from a prior prototype.

**Remaining necessary proof architecture:** (i) specify the legitimate unweighted first-order state/energy norm and a boundary symmetrizer or Kreiss multiplier; (ii) handle \(F_0,F_\Pi,F_i\in L^2\) without differentiation loss where the chosen norm and boundary data admit it; (iii) propagate the auxiliary reduction constraints or impose source/boundary compatibility; (iv) close the Sobolev/corner conditions and compare against the classical established theorems. A claim of general nonlinear Einstein–Maxwell existence or arbitrary-data GH IBVP well-posedness remains **unproved**.

## Literature context

- Kreiss, Reula, Sarbach and Winicour, *Well-posed initial-boundary value problem for the harmonic Einstein equations using energy estimates*, **Classical and Quantum Gravity 24** (2007), 5973–5984, DOI: 10.1088/0264-9381/24/23/017.
- Kreiss, Reula, Sarbach and Winicour, *Boundary Conditions for Coupled Quasilinear Wave Equations with Application to Isolated Systems*, **Communications in Mathematical Physics 289** (2009), 1099–1129, DOI: 10.1007/s00220-009-0788-2.
- Rinne, *Stable radiation-controlling boundary conditions for the generalized harmonic Einstein equations* (2006), arXiv:gr-qc/0606053.

The counterexamples are scoped **mathematical consistency checks**, not priority claims over the pre-existing well-posedness literature.
