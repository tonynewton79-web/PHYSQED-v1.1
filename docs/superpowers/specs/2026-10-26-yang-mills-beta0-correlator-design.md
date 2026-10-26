# Exact beta-zero time-correlator benchmark

## Scientific purpose

An apparent negative time-separated connected spatial-plaquette correlation in the finite SU(2) heatbath data may be created by estimating the centring mean from the same finite measurements. This phase supplies a provable beta-zero control and separately labelled numerical corrections so that a sampling artefact is never interpreted as a physical spectral signal.

## Mathematical model

Let the periodic Euclidean lattice have extents `(T,L1,L2,L3)`, with each spatial extent at least two, and let `V=L1*L2*L3`. At beta zero under ideal Haar link sampling, each complete heatbath sweep refreshes all links independently. For spatial-plaquette averages `X_{r,t}` in configuration `r` and time slice `t`, orthogonality of distinct spatial plaquette traces gives

`E[X_{r,t}]=0` and `E[X_{r,t} X_{s,u}]=delta_(r,s) delta_(t,u)/(12V)`.

In particular the **physical finite-lattice connected correlator** has `C(0)=1/(12V)` and `C(t)=0` for nonzero periodic temporal separation. With `M` independent complete sweeps, `N=M*T`, and the empirical shared mean `Xbar`, the existing estimator has exact expectations:

- `E[Chat(0)] = (1-1/N)/(12V)`;
- `E[Chat(t)] = -1/(12VN)` for `t != 0`.

Adding `1/(12VN)` at every lag removes only this known finite-sample centring bias **in expectation**. A corrected realised correlator may still fluctuate negative, and this calculation makes no positive-beta, equilibration, reflection-positivity or continuum claim. The ideal iid Haar model is a mathematical premise, not a guarantee of pseudo-random arithmetic.

## Implementation decisions

1. A standard-library `beta_zero_correlators.py` produces exact `Fraction` covariance/bias targets, bound-checked JSON receipts and a strict replay verifier.
2. A narrow `beta_zero_corrected_correlator(samples, extents)` adapts the existing estimator without modifying its historical meaning. Only an exact `beta == 0` run can emit this diagnostic in `transfer_diagnostics.py`.
3. Test against hand-derived values, exhaustive independent synthetic iid finite samples, a seeded beta-zero heatbath run, and malicious/malformed receipt inputs. Retain all existing raw traces and historical receipts.
4. Register a distinct exact-Haar-correlator evidence kind with the existing PHYSQED evidence ledger. Its source contents and exact verification implementation are hashed; accepting it must never imply that the general PHYSQED engine has formally discharged the Haar/Peter--Weyl premises.
5. Document the proof and its limitations in `research/yang_mills_su2/BETA_ZERO_CORRELATOR_SCOPE.md`. The positive-beta finite transfer operator is a distinct future phase.

## Approaches considered

- **Chosen:** exact beta-zero null model plus corrected finite-chain reporting, providing a falsifiable mathematical anchor with cheap deterministic replay.
- Simulation-only autocorrelation scans would add empirical diagnostics but not settle whether the known beta-zero artefact was from centring.
- Direct finite-beta transfer-operator inequalities are potentially decisive but require separate spectral analysis and cannot be inferred from a short noisy plaquette trace.

## No-go claims

No claim of four-dimensional continuum Yang-Mills existence, physical mass gap, Lean kernel formalization, positive-beta chain mixing, or general transfer-operator spectral lower bound is authorized by this phase.
