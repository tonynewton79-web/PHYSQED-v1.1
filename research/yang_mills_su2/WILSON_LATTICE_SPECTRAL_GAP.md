# A uniform lattice spectral gap at strong coupling

The exact Dobrushin--Föllmer estimate in `STRONG_COUPLING_SCOPE.md` can
control more than one plaquette observable. Applied to every bounded
gauge-invariant spatial-slice function, it implies a volume-uniform bound
on *all* excited eigenvalue ratios of the genuine Wilson transfer operator.
This is a restricted lattice strong-coupling application of known methods,
not a new continuum Yang--Mills theorem.

## Definitions and theorem

Let `L1,L2,L3 >= 2` be periodic spatial periods, let `V=L1 L2 L3`,
and let `m=3V` count spatial positive-link variables. With normalized Haar
measure on `SU(2)^m`, let `P_G` project onto site-gauge-invariant functions.
Let `B(U)` be the sum of the `3V` spatial Wilson plaquette traces
`W(g)=Re Tr(g)/2`, and let `M_beta` multiply by `exp(beta B(U)/2)`.
Let `C_beta` be the *normalized* product temporal convolution, whose
one-link kernel is proportional to `exp(beta W(U_e V_e^-1))`. Set

\[
 T_\beta=M_\beta P_G C_\beta P_G M_\beta
\]

on the gauge-invariant Hilbert space. The normalization of `C_beta`
does not affect eigenvalue ratios. Enumerate eigenvalues in decreasing
order `lambda_0 >= lambda_1 >= ... >= 0`.

**Theorem (uniform strong-coupling lattice-unit gap).** For
`0 < beta < 1/18`, writing `q=18 beta`, the top eigenvalue is simple and

\[
 0\le\frac{\lambda_n(T_\beta)}{\lambda_0(T_\beta)}\le q<1,
 \quad n\ge1,\qquad
 \Delta_{\rm lattice}\ge-\log(18\beta)>0.
\]

The bound is independent of the three spatial periods. It controls the
physical *gauge-invariant lattice* transfer spectrum, **not** the
continuum mass gap.

An improved **chordal-metric** argument using the spherical SU(2)
single-link conditional law obtains `lambda_n/lambda_0 <= 6 beta`
for `0<beta<1/6`. See `WILSON_CHORDAL_MIXING.md`; the present
total-variation theorem remains a separate valid, more elementary route.

## Proof

**Positive compact transfer.** The Wilson temporal-link convolution
has positive Peter--Weyl eigenvalues `2 I_d(beta)/beta` of rapidly
decreasing size. The sum including multiplicities converges, so the
finite product is trace class. Gauge projection and multiplication by
bounded positive `M_beta` preserve trace class and positivity. On the
finite compact spatial configuration quotient the gauge-integrated
transfer kernel is continuous and strictly positive: it integrates a
product of strictly positive functions `exp(beta W)>0` against Haar
measure. Perron--Jentzsch gives a simple top eigenvalue `lambda_0>0`
and a continuous strictly positive normalized eigenfunction `phi_0`.
Its minimum is positive on the compact quotient. Each nonzero excited
eigenfunction `phi_n` is also continuous, since it equals a scalar
multiple of the integral operator applied to itself. Because the kernel
is real symmetric, the eigenfunctions can be chosen real, gauge
invariant and orthonormal.

**Mixing for arbitrary bounded spatial observables.** Let `F` be a
bounded real gauge-invariant function of a complete spatial slice,
and set `M=||F||_infty`. On a four-dimensional periodic Euclidean
torus of temporal period `T`, consider copies of `F` separated by
`0<t<T` steps and set `r=min(t,T-t)`. Each of the `m` spatial link
coordinate oscillations of `F` is at most `2M`, whence the sum is
at most `2mM`. The Wilson conditional-link influence matrix has row
sum at most `q`; any path of shared-plaquette link interactions from
time `0` to time `t` has length at least `r`. The resolvent row sum
from one slice to the other is therefore at most `q^r/(1-q)`.
The classical Föllmer covariance estimate (factor `1/4`) yields

\[
 |\operatorname{Cov}_{\beta,T}(F_0,F_t)|
 \le \frac14(2mM)(2M)\frac{q^r}{1-q}
 =\frac{mM^2}{1-q}q^r. \tag{1}
\]

The prefactor need **not** be uniform in spatial volume: it is
finite and independent of temporal separation, which is all the
spectral argument requires.

**Infinite Euclidean time.** Write `M_F` for multiplication by `F`.
The genuine Wilson periodic-time formula is

\[
 \operatorname{Cov}_{\beta,T}(F_0,F_t)=
 \frac{\operatorname{Tr}(T_\beta^{T-t}M_FT_\beta^tM_F)}
      {\operatorname{Tr}(T_\beta^T)}-
 \left(\frac{\operatorname{Tr}(T_\beta^TM_F)}
      {\operatorname{Tr}(T_\beta^T)}\right)^2.
\]

Since `T_beta` is trace class and its Perron root is simple, at fixed
spatial volume and fixed `t`, the limit `T -> infinity` is

\[
 C_F(t)=\sum_{n\ge1}|
   \langle\phi_n,F\phi_0\rangle|^2
    (\lambda_n/\lambda_0)^t\ge0. \tag{2}
\]

Taking the same limit in (1) yields
`C_F(t) <= m M^2 q^t/(1-q)` for every integer `t>=1`.

**Detection of every excited eigenvector.** Choose a real unit
eigenfunction `phi_n` (`n>=1`) with nonzero eigenvalue and define
`F_n=phi_n/phi_0`. The positivity and regularity above make `F_n`
bounded, real and gauge invariant. Moreover,
`<phi_0,F_n phi_0>=<phi_0,phi_n>=0`, and
`F_n phi_0=phi_n`. Thus (2) has a single term:

\[
 (\lambda_n/\lambda_0)^t=C_{F_n}(t)
 \le \frac{m\|F_n\|_\infty^2}{1-q}q^t.
\]

Take `t`th roots and then let `t` tend to infinity to obtain
`lambda_n/lambda_0 <= q`, independently of `m`. Zero eigenvalues
already satisfy the conclusion. Applying `-log` gives the asserted
uniform lattice-unit excitation gap. This completes the proof.

## Exact certificate and scope

For rational `0<beta<1/18`, `wilson_spectral_gap.py` exactly returns
the spectral-ratio ceiling `q=18 beta`. With
`y=(1-q)/(1+q)`, the positive partial sum

\[
 0<2\sum_{j=0}^{K-1}\frac{y^{2j+1}}{2j+1}
 <-\log(q),\qquad K\ge1,
\]

is a rational lower bound on the lattice logarithmic gap. PHYSQED
replays this arithmetic and its source hash; it does *not* kernel-prove
Föllmer's theorem, Perron--Jentzsch, trace-class transfer construction,
or the continuum limit.

This theorem bypasses the `exp(3 beta V)` multiplier of the separate
Fourier **cutoff comparison** for normalized spectral ratios; it does not
improve the absolute operator-norm cutoff itself. The actual
four-dimensional continuum scaling regime has `beta=4/g² -> infinity`,
outside the interval `beta<1/18`, so no physical-units continuum mass
gap follows. A lattice gap at small bare coupling is known in the
classical strong-coupling literature; no novelty claim is made here.

## Literature

1. K. Osterwalder and E. Seiler, *Gauge Field Theories on a Lattice*,
   Annals of Physics **110** (1978), 440--471.
2. H. Föllmer, *A Covariance Estimate for Gibbs Measures*, Journal of
   Functional Analysis **46** (1982), 387--395.
3. S. Chatterjee, *One version of the mass gap problem* (2018),
   https://www.math.columbia.edu/department/probability/CFT18/Chatterjee.pdf.
4. D. Bhattacharjee and U. Bhattacharya, recent unrefereed claimed sharper
   strong-coupling lattice bounds (Zenodo, 2026),
   https://zenodo.org/records/23487516; **not independently verified here**.
