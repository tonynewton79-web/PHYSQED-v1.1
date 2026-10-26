# Claim ledger for the cumulative Yang--Mills manuscript

This is an internal authoring audit, not part of the manuscript or an
assertion that PHYSQED proves the listed analytic premises.

| Manuscript claim | Source within this repository | Verification status and permitted conclusion |
| --- | --- | --- |
| Physical Wilson SU(2) four-dimensional action, local gauge invariance and seeded update kernel | `lattice.py`, `su2.py`, `simulation.py`, `WILSON_TRANSFER_SCOPE.md` | Implemented model and independent lattice tests. Classical Wilson formulation, not original. |
| Positive gauge-projected temporal transfer `T=M P C P M` with character coefficients `2d I_d(beta)/beta` | `WILSON_TRANSFER_SCOPE.md`, `wilson_transfer_characters.py`, `wilson_transfer_slabs.py` | Analytic derivation using established reflection positivity and Peter--Weyl theory. Exact finite rational character receipts; analytic theorem not Lean formalized. |
| `I_2(2)/I_1(2)=0.433127426722311758...`, negative log `0.836723306231588913...` | `CHARACTER_CERTIFICATES.md`, `artifacts/character_beta2_exact.json` | Exact rational enclosures verified by tests; decimals independently checked with 50-digit mpmath. ONE-LINK coefficient, not interacting transfer gap. |
| Spatial Haar plaquette mean zero, variance `1/(12V)`, and expected sample-mean centering offset `-1/(12VMT)` at nonzero lag | `BETA_ZERO_CORRELATOR_SCOPE.md`, `artifacts/beta_zero_correlator_4x2x2x2_m2.json` | Exact finite product-Haar theorem and regression. Requires independent refreshed configurations at exact `beta=0`. |
| Abstract three-mode weak-weight example `m_n(t)` has an excitation gap tending to zero despite `sup_t|m_n(t)-2^-t|<=1/n` | `TRANSFER_MOMENT_SCOPE.md`, `artifacts/abstract_transfer_moments_n10.json` | Exact abstract transfer statement only, not a Wilson transfer example. |
| Old finite strong-coupling temporal correlation row sum `18 beta` and all-spectrum transfer bound at `beta<1/18` | `STRONG_COUPLING_SCOPE.md`, `WILSON_LATTICE_SPECTRAL_GAP.md` | Specialization of classical Dobrushin--Follmer and Perron ratio methods. Separate exact rational PHYSQED receipt; not novel. |
| New SU2 chordal inequality `W1(nu_b,nu_b')<=|b-b'|/3`, `lambda_n/lambda_0<=6 beta` for `0<beta<1/6` | `WILSON_CHORDAL_MIXING.md`, `wilson_chordal_mixing.py`, `artifacts/wilson_chordal_beta1_over_10.json` | Analytic proof independently reviewed (Barta identities symbolically differentiated, metric comparison and transfer positivity checked). PHYSQED replays only exact rational consequences. Recent unrefereed literature states at least the `1/6` range. |
| Necessary **single-link method ceiling** `sum_f c_ef >= 9 beta/2` on 4D tori with all periods at least three | `WILSON_SINGLE_LINK_CEILING.md`, `wilson_dobrushin_ceiling.py`, `artifacts/wilson_single_link_ceiling_beta2_over_9.json` | Explicit central-sign Wilson background, geometric 18-neighbor count, analytic Haar derivative `1/4` and independent quaternion plaquette perturbation tests. This excludes unweighted single-link row contraction at `beta>=2/9`; it does not prove the global sharp upper bound or a physical mass gap. Related ceiling is prior art in unrefereed Bhattacharjee--Bhattacharya work. |
| Conditional two-sided block physical-energy window and residual power telescope | `CONTINUUM_SCALE_BRIDGE.md`, `continuum_scale_bridge.py`, `artifacts/abstract_physical_scale_bridge_n2.json` | Elementary positive-transfer functional analysis and exact rational consequences, with abstract diagonal toy control. The required Wilson weak-coupling block contraction and positive correlator witness are **not** established. |
| Necessary lower value `K>=1/4` for any global chordal `W1(nu_b,nu_b')<=K|b-b'|` | Direct derivative of the normalized spherical exponential tilt at Haar `b=0`; Haar covariance `Var(h.x)=1/4` | Complete elementary proposition included in the manuscript. This is a **lower** bound on the candidate constant, not the unverified sharp `K=1/4` upper bound. |
| At `beta=1/10`, exact `q=3/5` and the lattice log lower `-log(3/5)=0.510825623765990683...` | `wilson_chordal_mixing.py`, `artifacts/wilson_chordal_beta1_over_10.json` | Rational eight-term atanh lower certificate; logarithmic decimal independently computed at 50 digits. |
| 16-sweep cold/Haar differences at `beta=0,1/2`, volume `2^4,3^4` | `EQUILIBRATION_SCOPE.md`, `artifacts/equilibration/*.json` | Seeded finite diagnostics; **not** equilibrium, physical mass, independent trials or a thermodynamic limit. |
| `beta<2/9` via sharp `1/4` chordal parameter sensitivity | Bhattacharjee--Bhattacharya v3.3.1 unrefereed longer `strong-coupling/prd/main.tex`, *Mass Gap of Lattice Yang--Mills Theory up to the Dobrushin Ceiling*. The shorter `strong-coupling/paper/main.tex`, *Sharp Curvature and Finite-Box Criteria*, provides the separate `1/6` statement. | **Do not include as a proved result of this paper.** Our independent proof verification covers the conservative `1/3` coefficient only. |

## Rulings for the paper

- Ruling: use the analytic `6 beta` transfer theorem as the main result,
  with explicit prior-art attribution, because it is the strongest result
  whose complete proof was independently checked. If wrong, a reader could
  confuse historical priority with our contribution.
- Ruling: show the temporal Monte Carlo cold/Haar contrast as a diagnostic
  negative control, not a mass estimate. The retained table uses local
  Metropolis proposals with epsilon=3/10 and averages all time slices
  at each of 16 sweeps for seeds 123 and 456; it is not an exact-Haar
  heatbath trajectory. If wrong, short-chain bias could be disguised
  as a physical signal.
- Ruling: state a lattice-unit gap and separately explain why `beta` must
  enter a regime beyond `1/6` in the continuum problem. If wrong, a false
  Clay-problem implication would result.

- Ruling: cite two distinct unrefereed v3.3.1 sources separately.
  The short Sharp Curvature paper covers the conservative 1/6 route;
  the longer Dobrushin Ceiling paper states the 2/9 claim. If wrong,
  historical attribution would be misleading.

- Ruling: distinguish the **necessary** method-ceiling row lower `9 beta/2`
  from the sufficient chordal row upper `6 beta`; the former does not justify
  a sharp coefficient of `1/4` at arbitrary fields. If wrong, a lower
  sensitivity bound could be misreported as a complete mixing theorem.

## Reproducibility checks

- Previous branch final tests: 142 Yang--Mills, 237 PHYSQED; rerun on the
  finished paper branch before release.
- Reference value independently recomputed on 2026-10-26:
  `I2(2)/I1(2)=0.4331274267223117583171834557759918204315`.
- At `beta` = `1/100`, `1/20`, `1/10`, `1/8`, the new logarithmic lower
  analytic values are approximately `2.813410716760`, `1.203972804326`,
  `0.510825623766`, `0.287682072452`, respectively. Use the explicit
  formulas in the manuscript, not these decimals as independent proofs.
