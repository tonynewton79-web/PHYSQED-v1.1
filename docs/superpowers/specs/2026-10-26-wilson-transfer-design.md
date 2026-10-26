# Finite-coupling Wilson SU(2) transfer reconstruction

## Aim

Advance the established finite Wilson SU(2) pilot beyond abstract positive transfer models. At strictly positive rational coupling, reconstruct the **actual Wilson temporal transfer form** on the gauge-invariant spatial-link Hilbert space, produce exact certified Fourier-character truncation errors for its temporal-link convolution, and cross-check the factorization against gauge-invariant four-dimensional Wilson lattice data. These are finite-lattice results. No physical continuum mass gap or fully diagonalized interacting transfer spectrum is asserted.

## Mathematical model

For a periodic spatial lattice with V sites, write E for the 3V oriented positive spatial links and S for its 3V spatial plaquettes. Let W(g)=Re Tr(g)/2, and let the spatial potential be B(U)=sum_{p in S} W(U_p). On H=L2(SU(2)^E) let P be the Haar-averaged orthogonal projection onto the site-gauge-invariant subspace. Define the temporal convolution operator

`(C_beta f)(U)=int product_{e in E} exp(beta W(U_e V_e^-1)) f(V) dV`.

Define `M_beta` by multiplication with `exp(beta B(U)/2)`. The positive Wilson transfer form on the gauge-invariant Hilbert space is `T_beta=M_beta P C_beta P M_beta`, with irrelevant overall scalar factors from the constant term in Wilson's action. Gauge-averaged temporal link integrations reproduce its periodic-slab kernel.

At `beta>0`, the one-link class function has the SU(2) character expansion

`exp(beta W(g))=sum_{d>=1} (2d/beta) I_d(beta) chi_(d-1)(g)`

where `chi_(d-1)(g)=U_(d-1)(W(g))` has dimension d. All Fourier eigenvalues `2 I_d(beta)/beta` are strictly positive, and the fundamental-to-trivial ratio is `I_2(beta)/I_1(beta)`. This ratio is **only a temporal one-link factor**, not the full interacting physical mass gap.

## Exact tail certificate

Let h=beta/2 and retain dimensions `d=1,...,D`. Since `|chi_(d-1)|<=d` and `I_d(beta)<=h^d exp(h^2)/d!`, if `r=h(D+2)/(D+1)^2<1`, the omitted character tail is uniformly bounded by

`R_D <= (2/beta) exp(h^2) ((D+1)^2 h^(D+1)/(D+1)!)/(1-r)`.

Use exact rational Taylor upper bounds for `exp(h^2)` and positive rational Bessel intervals for each retained coefficient. Record a global tail bound and rigorous kernel-value intervals at several rational trace values. Bound request parameters and certificate arithmetic before expensive calculations.

## Physical numerical cross-check

For a full periodic 4D Wilson configuration, split each period into slabs:

`L_t=beta*(T_t+(S_t+S_(t+1))/2)`, where `T_t` sums timelike plaquette traces based at time t and `S_t` sums spatial traces at time t. Verify `sum_t L_t=beta sum_all W_p`, up to rounding in the existing float-quaternion representation, and invariance of every slab under independent site gauge transformations. Existing positive-beta heatbath timeslice receipts remain numerical, not equilibrium-certified.

Independently evaluate the unaveraged transfer-link product `U_e h_y V_e^-1 h_x^-1` and verify its trace equals the timelike Wilson plaquette on each temporal slice, including a gauge-transformed configuration.

The transfer-trace identity for an actual centered gauge-invariant spatial observable A is `C_N(t)=Tr(T^(N-t) A T^t A)/Tr(T^N)`. In a transfer eigenbasis its terms are nonnegative and reflection symmetric. The numerical covariance estimator can fluctuate in sign and does not certify this identity pointwise.

For the exact finite-volume Wilson Gibbs expectation, differentiating with respect to coupling gives `d E_beta[F]/d beta = Cov_beta(F, H)` for `H=sum_p W(U_p)` with `|H|<=6 N4`. Applying this to bounded single-time observables and their nonzero-time product, starting from the independent Haar beta-zero expectation, gives the coarse but unconditional rational bound `|C_beta(t)|<=min(1, M beta+(M beta)^2)` with `M=6 N4`. This bound explicitly grows with total volume; it is not an estimate of exponential decay in time.

## Uniformity gate

Since `|B(U)|<=3V`, multiplication `M_beta` lies between `exp(-3 beta V/2)` and `exp(3 beta V/2)`. Min-max singular-value bounds compare indexed eigenvalues of `T_beta` with those of the compressed convolution by factors `exp(+-3 beta V)`. The bound deteriorates exponentially in volume and cannot establish an infinite-volume or continuum gap. A uniform physical spectral estimate and continuum construction remain open.

## Approaches

- **Selected:** exact Wilson temporal convolution coefficients and error control, paired with a true Wilson action slab-identity check and strictly scoped PHYSQED evidence.
- Heatbath cosh fits alone cannot distinguish excited-state contamination or prove equilibration.
- Full interacting transfer-matrix diagonalization at finite volume requires a controlled gauge-invariant representation cutoff and is a subsequent phase, not claimed here.
