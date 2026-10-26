# Exact beta-zero mixing and a finite SU(2) heatbath

## Why this improves the research instrument

The former low-angle Monte Carlo data were dominated by a cold-start
transient. At beta zero, the Wilson action is constant, so the old
Metropolis method accepts every proposed link update. Writing one such
update as the unit quaternion
\(q=(\cos\theta,\hat n\sin\theta)\), with uniform
\(\theta\in[-\varepsilon,\varepsilon]\) and isotropic axis
\(\hat n\in S^2\), the average of its fundamental SU(2) matrix is
\([\sin\varepsilon/\varepsilon]I\). Consequently the cold-start
normalized fundamental plaquette has the **exact expectation**

\[
\mathbb E_{\beta=0}^{\mathrm{cold}} P(n)
=\left(\frac{\sin\varepsilon}{\varepsilon}\right)^{4n}.
\]

For epsilon 0.3, the exact mean of sweeps 9 through 16 is approximately
0.475792038130869, explaining the previously observed 0.489004 within
finite two-seed sampling error. At epsilon pi, the mean vanishes after
one sweep; this *does not* mean the complete distribution is already Haar.

## SU(2) representation-spectrum certificate

For epsilon pi, the proposal is a conjugation-invariant SU(2) measure.
With \(j=0,1/2,1,3/2,\ldots\) and character
\(\chi_j(\theta)=\sin((2j+1)\theta)/\sin\theta\), its convolution
eigenvalue on spin j is

\[
\lambda_j=\frac{1}{2j+1}\,\frac1\pi\int_0^\pi\chi_j(\theta)d\theta
=\begin{cases}(2j+1)^{-1},&j\in\mathbb Z_{\ge0},\\
0,&j\in\tfrac12+\mathbb Z_{\ge0}.
\end{cases}
\]

The mean-zero L2 operator norm is exactly 1/3 and its Markov spectral
gap is 2/3 for a complete beta-zero sweep, independent of finite
lattice volume. Cold identity links are a delta measure, so the L2
contraction estimate does not directly apply at sweep zero. After at
least two complete sweeps, for \(N\) independent links,

\[
\|p_n-1\|_{L^2(\mathrm{Haar}^N)}^2
=\left(1+\sum_{j=1}^\infty(2j+1)^{2-2n}\right)^N-1.
\]

The module `mixing_certificates.py` encloses this expression with exact
`Fraction` arithmetic, using the integral upper bound on the omitted
positive odd-power sum. It *assumes*, but does not Lean-formalize, the
Peter--Weyl character decomposition. The formula is for a simulation
**update operator**, emphatically not the Yang--Mills Hamiltonian.
The `replay_mixing_receipt` verifier recomputes every bound from the
declared finite input and rejects altered values, extra fields, and
forged physical or Lean proof flags.

## Heatbath law and PHYSQED's existing Bessel ratio

For any link, the six affected Wilson plaquettes yield a real-linear
functional \(h\cdot q\). Its conditional distribution is

\[
d\mathbb P(q\mid\text{other links})
\propto e^{\beta h\cdot q}\,d\mathrm{Haar}(q).
\]

The new sampler evaluates the four components of h independently by
substituting four quaternion basis elements and recomputing the local
plaquettes. It is checked against complete Wilson-action differences.
It draws the scalar \(t=(h/|h|)\cdot q\) from the correct distribution
proportional to \(e^{\kappa t}\sqrt{1-t^2}\), with
\(\kappa=\beta|h|\), then draws the transverse axis uniformly.

**Exact mathematical connection:** conditional mean link alignment is

\[
\mathbb E[t\mid h]=\frac{I_2(\kappa)}{I_1(\kappa)}.
\]

For \(\kappa=2\), the ratio's pre-existing rational PHYSQED certificate
therefore becomes an independent finite-Gibbs-kernel oracle. This does
not give the physical mass gap; the earlier diagnostic
\(-\log(I_2/I_1)\) must not be relabelled a four-dimensional spectral
excitation.

## Time-separated observables and falsifiability

The heatbath timeslice runner collects a spatial plaquette average at
each Euclidean time on a lattice with time extent at least four.
This observable is gauge invariant. Its connected sampled covariance
is folded around the periodic boundary. The optional cosh value

\[
m_\mathrm{cosh}(t)=\operatorname{arccosh}\!
\left(\frac{C(t-1)+C(t+1)}{2C(t)}\right)
\]

is emitted only when its three observed correlations are positive and
the ratio is at least one. A returned number is **not** a bound on the
lowest transfer-matrix energy, nor evidence of equilibration. For a
statistically credible exploratory study we still need longer,
independent chains, autocorrelation bounds, multiple lattice spacings,
volume checks and a continuum construction.

The classical finite-lattice reflection-positivity result of
Osterwalder--Seiler (1978) motivates the transfer-matrix direction.
It is not newly proved by this simulator. The Clay problem additionally
requires a nontrivial continuum theory in four dimensions and a
positive physical spectral mass gap.

Reference: K. Osterwalder and E. Seiler, *Gauge field theories on a
lattice*, Annals of Physics 110 (1978), 440–471,
https://doi.org/10.1016/0003-4916(78)90039-8.
