# Evidence provenance and claim boundary

The three components of the finite SU(2) pilot are deliberately separated.
Each record is tied to SHA256 of its input file, its own bounded replay method,
and a fixed, restricted verification status. Neither a SHA256 digest nor a
successful replay authenticates the author or validates a physical theory.

| Evidence kind | What is actually checked | What it does not establish |
| --- | --- | --- |
| `PHYSQED_EXACT_POLYNOMIAL` | The unchanged `projects/physqed/engine.py` and `replay.py` evaluate the declarative quaternion scalar-norm polynomial identity, with exact polynomial comparison and independent finite grid replay. | The norm-one hypothesis, gauge dynamics, Osterwalder–Schrader reconstruction, a physical law, Lean kernel verification, or any gap. |
| `EXACT_RATIONAL_INTERVAL` | Exact rational enclosures for a finite positive-term SU(2) Bessel-character ratio and its negative logarithm, recomputed from receipt inputs under resource limits. | A spectrum of a four-dimensional transfer matrix or continuum quantum field. |
| `FINITE_LATTICE_NUMERICAL` | The seeded, finite-cutoff four-dimensional periodic Wilson SU(2) run reproduces byte-canonical numerical results from recorded parameters and all sampled time slices, under a small replay budget. | A thermalized ensemble average, a lower spectral-gap bound, continuum/infinite-volume extrapolation, or experimental evidence. |

The `external_solver_integrations` ledger entries distinguish
`SOURCE_UNAVAILABLE_NOT_EXECUTED` from `SOURCE_LOCATED_UNTESTED`. Merely locating
the Newton Solver or EINSTEIN-X Ω source is never equivalent to execution or
validation. Their versioned executable archives and integration tests are not
currently present in this repository.

## Scope of PHYSQED's polynomial claim

For a quaternion \(q=a+bi+cj+dk\) and conjugate
\(\overline q=a-bi-cj-dk\), scalar algebra gives

\[
\operatorname{Sc}(q\overline q)
  =a^2-b(-b)-c(-c)-d(-d)
  =a^2+b^2+c^2+d^2.
\]

The declarative fixture encodes this identity without inserting the
assumption that the right-hand side equals one. Its verification is elementary
polynomial algebra, not a formalization of a matrix-valued gauge theory.

## Reproduce each claim

From the repository root:

```bash
python projects/physqed/engine.py research/yang_mills_su2/fixtures/quaternion_scalar_norm_identity.json
python -m research.yang_mills_su2.character_cli --beta-num 2 --beta-den 1 --bessel-terms 12 --log-terms 12 --output /tmp/ym-character.json
python -m research.yang_mills_su2.character_cli --verify /tmp/ym-character.json
python -m research.yang_mills_su2.run_pilot --extents 2,2,2,2 --beta 0.5 --seeds 123,456 --warmup 2 --sweeps 4 --thin 1 --epsilon 0.15 --output /tmp/ym-su2-pilot.json
python -m unittest discover -s research/yang_mills_su2/tests -v
python -m unittest discover -s projects/physqed/tests -q
```

To assemble one verified report, call the Python API, using the actual file
paths from the preceding commands:

```python
from pathlib import Path
from research.yang_mills_su2.evidence_bridge import assemble_pilot_report

report = assemble_pilot_report(
    Path("/tmp/ym-character.json"),
    Path("/tmp/ym-su2-pilot.json"),
    Path("research/yang_mills_su2/fixtures/quaternion_scalar_norm_identity.json"),
)
```

Alternatively, the repository includes an exact sample character receipt,
the ordered finite numerical samples, and a replayable integrated evidence
report under `research/yang_mills_su2/artifacts/`. Verify the committed
report from the repository root with:

```bash
python -m research.yang_mills_su2.evidence_bridge --verify research/yang_mills_su2/artifacts/integrated_evidence_report.json
```

For the two matched starting-state controls and report regeneration:

```bash
python -m research.yang_mills_su2.run_pilot --extents 2,2,2,2 --beta 0 --seeds 123,456 --warmup 2 --sweeps 4 --thin 1 --epsilon 0.15 --initialization cold --output research/yang_mills_su2/artifacts/cold_beta0_negative_control.json
python -m research.yang_mills_su2.run_pilot --extents 2,2,2,2 --beta 0 --seeds 123,456 --warmup 2 --sweeps 4 --thin 1 --epsilon 0.15 --initialization haar --output research/yang_mills_su2/artifacts/haar_beta0_negative_control.json
python -m research.yang_mills_su2.evidence_bridge --character research/yang_mills_su2/artifacts/character_beta2_exact.json --simulation research/yang_mills_su2/artifacts/finite_su2_2x2x2x2_pilot.json --algebra research/yang_mills_su2/fixtures/quaternion_scalar_norm_identity.json --cold-control research/yang_mills_su2/artifacts/cold_beta0_negative_control.json --haar-control research/yang_mills_su2/artifacts/haar_beta0_negative_control.json --output research/yang_mills_su2/artifacts/integrated_evidence_report.json
```

The report pins the verification implementation hashes and the generating
Python runtime version. Replay on a different interpreter version must
regenerate a new report, not silently reinterpret the old one as unchanged.

The analytical character diagnostic at \(\beta=2\) and finite lattice simulation
at \(\beta=1/2\) are **independent controls**; their values must not be
interpreted as two measurements of the same physical mass gap.

## Haar-start negative control for thermalization bias

At Wilson coupling \(\beta=0\), the action vanishes and the finite-volume
Gibbs measure is the product Haar measure over lattice links. Every
plaquette contains an independent SU(2) link, and the Haar average of its
normalized trace is exactly zero:

\[
\mathbb E_{\beta=0}\,\frac12\operatorname{ReTr}U_p=0.
\]

The **same** short protocol on the \(2^4\) lattice with seeds 123 and 456,
two warm-up sweeps, four measurements per chain, and angular proposal 0.15
has the following deterministic outcomes:

| Starting state | Mean normalized spatial plaquette | Two-chain exploratory standard error |
| --- | ---: | ---: |
| Identity (cold) | 0.9330307123 | 0.0084944796 |
| Independent Haar links | 0.0288225183 | 0.0569052805 |
| Exact \(\beta=0\) equilibrium mean | 0 | — |

The cold-start discrepancy demonstrates that the original short-run
observables are dominated by the starting state. The Haar-start control is
compatible with the exact equilibrium expectation, but two short chains do
not constitute a convergence study. Neither run provides an empirical mass
gap. Full measurements are saved as `cold_beta0_negative_control.json` and
`haar_beta0_negative_control.json`, source-hashed and independently rerun by
the integrated evidence report.

## Remaining obligations

A Yang–Mills existence-and-mass-gap proof still needs an actual nontrivial
four-dimensional continuum quantum theory with reflection positivity and
appropriate Osterwalder–Schrader properties, controlled ultraviolet and
infinite-volume limits, a positive lower bound for its entire physical
spectrum, and treatment of every compact simple gauge group. None has been
discharged by these finite calculations.
