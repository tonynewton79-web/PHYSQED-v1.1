# The finite-coupling SU(2) Wilson transfer operator and its certified temporal-link kernel

## 1. The physical finite-lattice question

For a positive Wilson coupling, the pure SU(2) lattice gauge measure is not a product Haar measure. It is nevertheless reflection-positive and possesses a positive transfer-operator formulation [1]. We make that formulation explicit for the finite periodic model implemented in this repository, identify what the earlier Bessel ratio actually measures, and certify the Fourier truncation of its temporal-link kernel. This does not solve the constructive continuum problem posed in [2]. The known lattice transfer-operator result is not claimed as new.

Let the spatial lattice be periodic in three directions with `V=L1 L2 L3` sites and `3V` positive spatial links. Set `W(g)=Re Tr(g)/2`. For a spatial link configuration `U`, let

\[
 B(U)=\sum_{p\,\mathrm{spatial}}W(U_p),\qquad |B(U)|\le 3V.
\]

At coupling `beta>0`, the four-dimensional Wilson Gibbs density is proportional to `exp(beta sum_p W(U_p))`; the usual Wilson action `beta sum_p(1-W(U_p))` differs only by an irrelevant constant in the exponent.

## 2. A genuine Wilson transfer construction

On `H=L²(SU(2)^(3V))` with normalized product Haar measure, let `P` be the orthogonal average over all local spatial site gauge transformations. Its image is the gauge-invariant subspace. Define the temporal convolution

\[
 (\mathcal C_\beta f)(U)
 =\int\prod_{e\,\mathrm{spatial}}
      e^{\beta W(U_e V_e^{-1})}f(V)\,dV,
 \qquad (M_\beta f)(U)=e^{\beta B(U)/2}f(U).
\]

The time transfer on the gauge-invariant subspace is

\[
 \mathcal T_\beta=M_\beta P\mathcal C_\beta P M_\beta,
\]

up to the harmless positive scalar from Wilson's `1-W` convention. Site-gauge invariance of `B` lets `M_beta` commute with `P`; simultaneous gauge covariance of each central temporal kernel lets `C_beta` commute with `P`.

The gauge-integrated kernel is the Haar integral over one group variable `h_x` for each spatial site of a time slab, containing the positive factors

\[
 \exp\!\left(\frac\beta2 B(U)+\frac\beta2 B(V)\right)
 \prod_{e=(x,y)}\exp\bigl(\beta W(U_e h_y V_e^{-1}h_x^{-1})\bigr).
\]

Using invariance of `Re Tr` under inversion and cyclic permutations, each product factor is the timelike Wilson plaquette connecting the two spatial fields, with `h_x` the temporal links. Multiplying periodic slabs and integrating intermediate spatial links therefore reproduces the original finite Wilson partition function. The independently executed `wilson_transfer_slabs.py` checks compare each unaveraged link-kernel product directly against the time-oriented Wilson plaquette, and the full half-cap/slab sum against the original four-dimensional Wilson action, before and after local gauge transformations.

For any real gauge-invariant spatial observable `A` (for example the average spatial plaquette), write the finite-period centered observable `A_c=A-<A>_beta` and `Z=Tr(T_beta^N)`. Its exact equilibrium temporal correlator is

\[
 C_N(t)=\frac{\operatorname{Tr}(\mathcal T_\beta^{N-t}A_c
          \mathcal T_\beta^t A_c)}{Z},\qquad 0\le t\le N.
\]

Once positivity of `T_beta` is established, an eigenbasis with eigenvalues `lambda_i>=0` gives a positive sum `Z^-1 sum_(i,j) lambda_i^(N-t) lambda_j^t |(A_c)_{ij}|²`. Thus `C_N(t)>=0`, `C_N(t)=C_N(N-t)` and its valid Hankel minors are nonnegative. A finite Monte Carlo shared-mean estimator need not be nonnegative in each realization, and a few cosh mass fits do not certify any excitation gap.

## 3. Positive character coefficients and uniform truncation error

Every SU(2) element has `x=W(g)` in `[-1,1]`. The spin `(d-1)/2` character is the Chebyshev polynomial of the second kind `chi_(d-1)(g)=U_(d-1)(x)` of dimension `d`. Haar orthogonality and the standard Bessel recurrence give the exact expansion

\[
 e^{\beta x}=\sum_{d=1}^\infty a_d(\beta)U_{d-1}(x),
 \qquad a_d(\beta)=I_{d-1}(\beta)-I_{d+1}(\beta)
                     =\frac{2d}{\beta}I_d(\beta).
\]

Each `I_d(beta)>0` for `beta>0` by its positive defining power series. Schur orthogonality therefore makes the convolution eigenvalue on the dimension-`d` matrix coefficients `a_d/d=2I_d(beta)/beta>0`. Products, gauge compression and positive congruence by `M_beta` preserve positivity. The dimension-two fundamental-to-trivial *one-link* eigenvalue ratio is precisely

\[
 q_{\mathrm{fund}}(\beta)=\frac{I_2(\beta)}{I_1(\beta)}.
\]

This identifies the earlier `beta=2` Bessel interval as an actual component of the finite Wilson transfer, **not** as a mass-gap estimate for its interacting, gauge-invariant three-dimensional spatial Hilbert space.

To certify a character cutoff `D`, let `h=beta/2`. From the positive series,

\[
 I_d(\beta)=\sum_{k\ge0}\frac{h^{2k+d}}{k!(k+d)!}
 \le\frac{h^d}{d!}e^{h^2},\qquad |U_{d-1}(x)|\le d.
\]

The summands `d² h^d/d!` for `d>=D+1` have successive ratio at most `r=h(D+2)/(D+1)^2`. If `r<1`, then for **every** `x` in `[-1,1]` the omitted kernel contribution has absolute value at most

\[
 R_D(\beta)\le\frac{2e^{h^2}}{\beta}
  \frac{(D+1)^2 h^{D+1}}{(D+1)!}\frac1{1-r}.
\]

The new bounded Python certificate replaces `e^(h²)` with a rational Taylor-series upper enclosure, replaces every retained `I_d` with an exact rational interval, applies the correct sign of `U_(d-1)(x)`, and adds the global `R_D` on both sides. This yields rigorous pointwise rational intervals and a global uniform tail estimate without a floating-point acceptance threshold. The committed `beta=2, D=8` receipt replays these calculations and preserves all false continuum-proof flags. The PHYSQED evidence bridge also restricts provenance metadata for all evidence categories to explicitly scoped labels; free-form assertions of a physical mass gap are rejected.

## 4. A separate exact finite-beta physical correlator bound

Let `X_t` be the spatial-plaquette average in time slice `t` on a finite four-dimensional periodic lattice with `N4=T L1 L2 L3` sites. Each `|X_t|<=1`. Put `H=sum_p W(U_p)`, so `|H|<=M=6N4`. Differentiation of the normalized Gibbs expectation gives

\[
 \frac{d}{d\beta}\mathbb E_\beta F
 =\operatorname{Cov}_\beta(F,H).
\]

For `|F|<=1`, the Cauchy--Schwarz inequality and the variance-range bound give `|Cov(F,H)|<=M`. At `beta=0`, independent Haar time slices have `E_0 X_t=0` and `E_0(X_0 X_t)=0` for nonzero temporal separation. Integrating from zero to positive `beta` gives `|E_beta X_t|<=M beta` and `|E_beta(X_0 X_t)|<=M beta`. Subtracting the two means and using the independent variance bound `|Cov(X_0,X_t)|<=1` proves the unconditional **finite Wilson Gibbs-model** estimate

\[
 0\le C_\beta(t)\le
 \min\{1,\ M\beta+(M\beta)^2\},
 \quad 1\le t<T,\quad M=6N_4.
\]

The nonnegative left endpoint uses the positive transfer representation above; the absolute upper estimate does not require that positivity premise. `wilson_correlator_bounds.py` computes its right endpoint in exact rational arithmetic with bounded inputs. For extents `(4,2,2,2)` and `beta=1/1000`, the nontrivial upper bound is `3576/15625`. This simple continuity estimate is deliberately coarse and is not presented as a novel strong-coupling theorem.

## 5. Why the continuum uniformity problem remains

On the spatial gauge-invariant subspace, multiplication by `M_beta` lies between `exp(-3 beta V/2)` and `exp(3 beta V/2)`. Standard singular-value/min-max comparison for the positive compact operators `T_beta=M_beta C_beta^G M_beta` and `C_beta^G=P C_beta P` gives, for every ordered eigenvalue `lambda_k`,

\[
 e^{-3\beta V}\lambda_k(\mathcal C_\beta^G)
 \le\lambda_k(\mathcal T_\beta)
 \le e^{3\beta V}\lambda_k(\mathcal C_\beta^G).
\]

Both this comparison and the finite-beta covariance bound deteriorate as the number of sites grows. This proves only that **these particular estimates are insufficient** for volume-uniform control; it does not prove that a Yang--Mills mass gap fails. A genuine next step requires a gauge-invariant, interacting transfer-sector estimate uniform in the spatial thermodynamic limit and, after physical scale setting, in lattice spacing as `beta` approaches its continuum regime. Constructing the nontrivial four-dimensional quantum field theory and a mass gap for every compact simple gauge group remains the Clay problem [2].

## References

1. K. Osterwalder and E. Seiler, *Gauge Field Theories on a Lattice*, Annals of Physics 110 (1978), 440--471, https://doi.org/10.1016/0003-4916(78)90039-8.
2. A. Jaffe and E. Witten, *Quantum Yang--Mills Theory*, Clay Mathematics Institute, https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf.
3. G. Kanwar and M. L. Wagman, *Real-time lattice gauge theory actions: unitarity, convergence, and path integral contour deformations*, 2021, https://arxiv.org/abs/2103.02602 (background on Wilson transfer positivity, not a source for our bounds).
