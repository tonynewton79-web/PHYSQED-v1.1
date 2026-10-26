# A weak-spectral-weight obstruction for positive transfer correlators

## Why a decaying finite correlator is not yet a mass gap

The Wilson lattice construction is a useful physical model, but proving a positive gap in a four-dimensional *continuum* quantum field theory requires more than positive and apparently exponentially decaying lattice measurements. Osterwalder and Seiler's foundational lattice analysis establishes positivity and transfer-operator structure for gauge approximations [1]. The Clay problem asks for existence and a positive gap after the relevant continuum construction [2]. Here we give a simple **abstract** counterexample to an invalid intermediate inference. It neither improves [1] nor resolves [2].

## The exact counterexample

For every integer `n >= 3`, let

\[
  a=\tfrac12,\qquad b_n=1-\tfrac1n,\qquad w_n=\tfrac1n,
  \qquad m_n(t)=(1-w_n)a^t+w_n b_n^t\quad(t\in\mathbb N_0).
\]

The finite-dimensional Hilbert space has an orthonormal basis `e0,e1,e2`. Define a positive self-adjoint transfer operator `T_n=diag(1,a,b_n)` and the self-adjoint observable

\[
 A_n=\sqrt{1-w_n}(|e_0\rangle\langle e_1|+|e_1\rangle\langle e_0|)
  +\sqrt{w_n}(|e_0\rangle\langle e_2|+|e_2\rangle\langle e_0|).
\]

Then `e0` is the unique vacuum, `A_n` is vacuum-centered, and direct multiplication gives

\[
  \langle e_0,A_n T_n^t A_n e_0\rangle=m_n(t).
\]

Thus the moments are genuine positive-transfer correlation functions, not a fabricated sequence of unrelated numbers. Positivity alone gives no uniform excitation bound: both excited modes are coupled to the observable, and the smallest coupled excitation energy is

\[
 \Delta_n=-\log b_n=-\log(1-1/n)>0,
 \qquad 0<\Delta_n\le\frac1{n-1}\longrightarrow0.
\]

The upper bound follows by integrating `1/(1-x)` from zero to `1/n`. But because `0<a<b_n<1`, at **every** integer time, not merely at the measured times,

\[
 0\le m_n(t)-2^{-t}=w_n(b_n^t-a^t)\le\frac1n.
\]

Consequently, even uniform absolute closeness to an exponentially decaying reference does not establish a uniformly positive spectral gap. For finite but very late times the slow mode becomes detectable in *relative* asymptotics: `m_n(t+1)/m_n(t)` tends to `b_n` for fixed `n`. The counterexample therefore does **not** say that complete exact long-time spectral information is useless.

The positive 2-by-2 moment/Hankel minor can also be calculated without approximation:

\[
 m_n(t)m_n(t+2)-m_n(t+1)^2
 =w_n(1-w_n)(ab_n)^t(b_n-a)^2\ge0.
\]

For `n=10`, the independently hand-derived checks are `m(1)=27/50`, `m(2)=153/500`, `D(0)=9/625`, `D(1)=81/12500`. The exact standard-library certificate checks such fractions with strict input and receipt validation, but does not formally certify the real-analytic logarithm limit in Lean.

## Finite-period transfer fixture

For the separate positive operator `T=diag(1,q)` and swap observable `A`, the period-`N` trace correlator is

\[
 C_N(t)=\frac{\operatorname{Tr}(T^{N-t}AT^tA)}{\operatorname{Tr}(T^N)}
       =\frac{q^t+q^{N-t}}{1+q^N}.
\]

With `q=1/2`, `N=4`, exact values for `t=0,1,2,3` are `(1,10/17,8/17,10/17)`; `C(0)C(2)-C(1)^2=36/289>0`, and `(C(0)+C(2))/(2C(1))=5/4` is the exact cosh ratio. In general, writing the trace correlator in an eigenbasis of a positive transfer operator gives a positive sum of exponential sequences, making the valid Hankel minors nonnegative by Cauchy--Schwarz. This is a *necessary positivity diagnostic*, not a sufficient mass-gap criterion.

## Meaning for PHYSQED and the Yang--Mills programme

`artifacts/abstract_transfer_moments_n10.json` is a replayable exact rational certificate. The evidence kind `EXACT_TRANSFER_MOMENT_OBSTRUCTION` records and replays its source with a separate abstract-only scope and an implementation digest. It permits only empty metadata or the exact model label `positive-transfer-abstract`; conflicting physical classifications and duplicate JSON keys are refused during ingestion. The claim that `T_n` is a Wilson lattice transfer operator would be false; it is explicitly *not* made. The evidence does not establish reflection positivity of the continuum limit, strong convergence of transfer operators, or an excitation-energy lower bound for any Wilson gauge theory.

A productive next step is model-specific analysis: formulate a gauge-invariant set of Wilson observables that is sufficiently rich to detect low-energy states, then seek **uniform in lattice spacing and volume** estimates on the reconstructed semigroup or spectral projections, rather than fits to a fixed short time window. Such estimates must survive the reconstruction/continuum-limit passage to address [2]. No such estimate is supplied by this document.

## Sources

1. K. Osterwalder and E. Seiler, *Gauge Field Theories on a Lattice*, **Annals of Physics** 110 (1978), 440--471, https://doi.org/10.1016/0003-4916(78)90039-8.
2. A. Jaffe and E. Witten, *Quantum Yang--Mills Theory*, Clay Mathematics Institute problem description, https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf.
