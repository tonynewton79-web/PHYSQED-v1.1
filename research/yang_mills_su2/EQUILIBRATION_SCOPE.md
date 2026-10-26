# Cold/Haar Equilibration Diagnostics for the Finite 4D SU(2) Wilson Model

## Why this extension matters

The first SU(2) pilot revealed strong cold-start transients under short
low-angle Metropolis trajectories. Before finite lattice correlators can be
treated even as exploratory equilibrium observables, runs need explicit
starting-state comparisons and autocorrelation assessment. This extension
retains the original full-action kernel as an independent action oracle.

A single proposed link appears in exactly six positively oriented Wilson
plaquettes in four dimensions: one rooted at the link site and one displaced
backward in each of the other three directions. The local action increment is

\[
\Delta S=\beta\sum_{p\,\ni\,\ell}
  \left[\tfrac12\operatorname{ReTr}U_p^{\rm old}
       -\tfrac12\operatorname{ReTr}U_p^{\rm proposed}\right],
\]

where \(\ell\) denotes the proposed positive-oriented link. The implementation
always restores that link after evaluating the proposal. Independent regression
tests compare the increment and entire seeded Metropolis trajectories with
the old complete-action evaluator on nontrivial SU(2) fields.

On this environment, a single \(3^4\) sweep at coupling \(\beta=0.7\)
and proposal angle 0.3 took 1.957 seconds with global recomputation versus
0.056 seconds locally. The observed 34.9-fold speedup is an illustrative
wall-clock measurement, not a portable performance theorem.

## Protocol and precisely limited conclusions

Two distinct deterministic seeds, 123 and 456, are used for both cold (identity links)
and Haar (independent uniform SU(2) links) initializations. For every chain,
all 16 sweeps are retained. The descriptive *early* window is sweeps 1–8;
the *late* window is sweeps 9–16. Each entry below averages the
normalized spatial plaquette first across a Euclidean-time slice and then
across seeds and the corresponding window.

| Coupling and volume | Cold early | Cold late | Haar early | Haar late | Cold − Haar, late |
| --- | ---: | ---: | ---: | ---: | ---: |
| \(\beta=0\), \(2^4\) | 0.772843 | 0.489004 | 0.039169 | 0.037911 | 0.451092 |
| \(\beta=1/2\), \(2^4\) | 0.789954 | 0.564468 | 0.055750 | 0.032780 | 0.531689 |
| \(\beta=1/2\), \(3^4\) | 0.797455 | 0.571755 | 0.039963 | 0.081483 | 0.490273 |

For \(\beta=0\), product Haar measure makes the exact Wilson-equilibrium
plaquette expectation zero. The Haar-start trace is qualitatively consistent
with this exact benchmark, whereas the cold start stays far above zero.
For the other rows, the cold/Haar differences likewise persist. No
equilibrium, volume convergence, physical scale or mass-gap inference follows.
The reported lag-one correlations are conventional sample Pearson
correlations of consecutive measured values, **not** integrated
autocorrelation-time estimates or effective sample-size certificates.

This experiment is a positive falsification of premature thermalization
claims. It does not show that a physical mass gap is absent, and must not be
described as an equilibrium Yang–Mills measurement.

## Reproduce and reject tampered claims

From the repository root, the three committed receipts can be verified by:

```bash
python -m research.yang_mills_su2.equilibration_cli --verify research/yang_mills_su2/artifacts/equilibration/beta0_volume2.json
python -m research.yang_mills_su2.equilibration_cli --verify research/yang_mills_su2/artifacts/equilibration/beta_half_volume2.json
python -m research.yang_mills_su2.equilibration_cli --verify research/yang_mills_su2/artifacts/equilibration/beta_half_volume3.json
```

Each receipt includes exact rational input parameters, all seeded traces,
source hashes covering both the update kernel and verifier, the exact Python
interpreter version, an integrity fingerprint and false values
for equilibrium, physical-law, continuum-gap and Lean-kernel certification.
Its verifier refuses forged flags, altered numbers and over-budget requests
before replay. Byte-for-byte numerical reproduction may depend on the
interpreter and platform math library; cross-environment agreement has not
been established. Source hashes establish reproducibility, **not authenticity**.

## Open research tasks

1. Establish actual mixing diagnostics using longer chains, genuinely
   independent initial conditions, adaptive but properly reversible kernels,
   blocked uncertainties and integrated autocorrelation-time estimates.
2. Introduce independently implemented Wilson-loop and transfer-matrix
   observables with rigorous finite-size and continuum-limit control.
3. Connect a proven scale-sensitive inequality, rather than a fitted
   finite correlator, to a positive physical spectral lower bound.
4. Integrate exact versioned Newton Solver and EINSTEIN-X Omega executables
   when available; PHYSQED currently certifies only restricted algebra.

The official Millennium problem asks for a mathematically defined
nontrivial four-dimensional Yang–Mills quantum theory and a positive physical
mass gap. None of the present finite diagnostic certificates addresses that
global theorem.
