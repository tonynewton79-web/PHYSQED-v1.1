# An exact Haar null model for SU(2) spatial-plaquette correlations

## The finite-lattice question

For a four-dimensional periodic Wilson lattice, a time-slice observable is a spatial average of normalized SU(2) plaquette traces. Its Monte Carlo covariance is often centred using the mean of the same finite collection of time slices. Even when distinct time slices are genuinely uncorrelated, this procedure induces a nonzero expected empirical correlation. At zero Wilson coupling this effect can be isolated exactly, without approximations or numerical fitting.

The present result supplies a null model and a correction valid **in expectation** for independent zero-coupling heatbath configurations. It is not a spectral theorem at positive coupling.

## Haar covariance at zero coupling

Write the lattice extents as \((T,L_1,L_2,L_3)\), with all spatial lengths at least two, and put \(V=L_1L_2L_3\). At time \(t\) and spatial site \(x\), let

\[
 p_{ij}(t,x)=\tfrac12\operatorname{Re}\operatorname{Tr}
 \bigl(U_i(t,x)U_j(t,x+e_i)U_i(t,x+e_j)^{-1}U_j(t,x)^{-1}\bigr),
 \quad 1\le i<j\le3.
\]

The gauge-invariant spatial-plaquette average is

\[
 X_t=\frac1{3V}\sum_{x}\sum_{1\le i<j\le3}p_{ij}(t,x).
\]

**Proposition.** Under the product Haar probability measure on the finite set of SU(2) links at \(\beta=0\),

\[
 \mathbb E X_t=0,\qquad
 \mathbb E[X_tX_u]=\frac{\mathbf1_{t=u}}{12V}.
\]

**Proof.** A single positively oriented plaquette contains four distinct link variables. Holding three fixed, the remaining link is Haar, hence the plaquette product is Haar. Under the identification of SU(2) with the unit three-sphere of quaternions, \(\operatorname{Re}\operatorname{Tr}(U)/2\) is the first coordinate. Rotational symmetry gives its expectation zero and its second moment \(1/4\).

Two distinct positively oriented spatial plaquettes cannot use precisely the same set of four oriented positive links, even on a periodic spatial torus of side length two. Indeed, the link-direction labels identify the unordered pair \(\{i,j\}\); the starting vertices of its two positive \(i\)-links are \(\{x,x+e_j\}\), and of its two positive \(j\)-links are \(\{x,x+e_i\}\). Their unique intersection is \(\{x\}\) when both side lengths are at least two. Thus the link support identifies the plaquette root and directions. Consequently at least one link appears in exactly one of any two distinct plaquettes. Integrating over that independent Haar link first sends the trace of its plaquette to zero, while the other trace does not depend on it. Their covariance is therefore zero. (The test suite also checks the distinct four-link supports for representative wrapped side-length-two and three tori.)

There are exactly \(3V\) spatial plaquettes in a time slice. Summing their diagonal variances \(1/4\) and the vanishing cross terms gives \(\operatorname{Var}(X_t)=1/(12V)\). Different times use disjoint spatial links under the product Haar law, so they are independent. This proves the proposition.

## The exact finite-sample centring artefact

At zero coupling, an *ideal* complete conditional heatbath sweep independently refreshes every link from Haar measure. For \(M\) independent refreshed configurations, write \(X_{r,t}\) for their \(N=MT\) time-slice measurements. All \(X_{r,t}\) are independent, have mean zero and variance \(v=1/(12V)\). Define the empirical shared mean and the existing periodically translated connected estimator by

\[
 \bar X=\frac1N\sum_{r,t}X_{r,t},\qquad
 \widehat C(s)=\frac1N\sum_{r,t}
 (X_{r,t}-\bar X)(X_{r,t+s\bmod T}-\bar X).
\]

**Proposition.** The exact expectations for every periodic lag are

\[
 \mathbb E\widehat C(0)=v\left(1-\frac1N\right),\qquad
 \mathbb E\widehat C(s)=-\frac vN\quad(1\le s<T).
\]

**Proof.** For any indices \(a,b\) among the \(N\) independent centred measurements,

\[
 \mathbb E[(X_a-\bar X)(X_b-\bar X)]
 =v\mathbf1_{a=b}-\frac vN.
\]

Indeed \(\mathbb E[X_a\bar X]=v/N\) and \(\mathbb E[\bar X^2]=v/N\). In the periodic sum \(a=b\) holds exactly for zero lag. Averaging this identity proves both expressions.

It follows that

\[
 \widehat C_{\mathrm{corrected}}(s)
 =\widehat C(s)+\frac1{12VMT}
\]

has expectation \(v\) at zero lag and zero at every nonzero lag. The operation does **not** impose positivity on an individual sample, repair autocorrelation for positive \(\beta\), or estimate a physical mass. At \(\beta>0\), the independent-Haar premise fails and this correction must not be applied.

For \((T,L_1,L_2,L_3)=(4,2,2,2)\) and \(M=2\), the exact target vector is \((1/96,0,0,0)\), the uncorrected expected vector is \((7/768,-1/768,-1/768,-1/768)\), and the correction added to each lag is \(1/768\). Exhaustive enumeration of all \(2^8=256\) equally weighted scaled independent Rademacher time-slice arrays reproduces these expectations, independent of the SU(2) simulation engine.

## Reproducible certification and limits

`beta_zero_correlators.py` issues bounded, strict-type JSON receipts containing the exact rational target, expected uncorrected estimator, and correction. The checked example is `artifacts/beta_zero_correlator_4x2x2x2_m2.json`. `replay_beta_zero_correlator_receipt` reconstructs all expected fields and rejects edited values, extra fields, changed types, and forged law/proof flags. The `EXACT_HAAR_CORRELATOR` evidence kind also enters the existing PHYSQED evidence bridge, which binds its source and verification implementation by hash and independently replays it before accepting a ledger. This is a **proof-component** check conditional on the written Haar premises, not a Lean formalization of the premises.

The finite heatbath timeslice report retains its historical raw and folded correlators. Only a run with exact input \(\beta=0\) receives additional `beta_zero_exact_receipt` and `beta_zero_bias_corrected_correlator` fields. All continuum, physical-law, equilibrium and Lean certification flags remain false.

These identities show why a nonzero short-chain estimate at zero coupling must be interpreted carefully. They do not construct the four-dimensional continuum quantum Yang–Mills theory, control the ultraviolet and infinite-volume limits, or prove a positive lower bound for the physical excitation spectrum. Finite-lattice reflection positivity and positive transfer-matrix existence have older rigorous foundations, including Osterwalder and Seiler, *Gauge field theories on a lattice*, *Annals of Physics* **110** (1978), 440–471, https://doi.org/10.1016/0003-4916(78)90039-8. A uniform physical mass-gap theorem would require substantive new estimates beyond this exact null model.
