# Four-dimensional SU(2) finite-lattice pilot

This package simulates a **finite** four-dimensional Euclidean pure SU(2)
Wilson lattice with periodic boundaries, using unit quaternions and a
local symmetric Metropolis proposal. It is an exploratory physical-model
instrument, not a continuum Yang–Mills construction or Clay mass-gap proof.

Run from the repository root:

    python -m research.yang_mills_su2.run_pilot --extents 2,2,2,2 --beta 0.5 --seeds 123,456 --warmup 2 --sweeps 4 --thin 1 --epsilon 0.15 --output /tmp/ym-su2-pilot.json
    python -m unittest discover -s research/yang_mills_su2/tests -v

The first coordinate is Euclidean time. Each positive oriented link carries
an SU(2) element; each plaquette enters the Wilson action once, for mu<nu.
Measurements are the mean normalized spatial plaquette Re Tr(U_p)/2 and its
translation-averaged connected time-slice covariance. The covariance is a
finite-sample diagnostic, *not* a certified spectral gap. Independent chain
standard errors do not account for full autocorrelation or discretization
systematics. The connected covariance subtracts the sample ensemble mean;
its finite-sample mean-subtraction bias is not removed by averaging equally
short independent chains. Ordered raw time-slice measurements and sweep
indices are retained for future independent covariance and resampling audits.
Very small lattices do not furnish controlled physical
scale setting. The source of every random run is listed by seed.

**Crucial equilibrium caveat:** by default every chain starts with identity
links, and the demonstration has only two warm-up sweeps. This is an
*unthermalized cold-start dynamics smoke test*, not a Wilson-ensemble
expectation value. The `--initialization haar` option samples starting links
independently from Haar-distributed SU(2); neither option certifies
thermalization. Two matched beta-zero negative controls expose cold-start
bias. See [EVIDENCE_SCOPE.md](EVIDENCE_SCOPE.md).

Two additional, separately scoped components are now available:

- `character_cli.py` computes and independently replays bounded exact rational
  character/Bessel diagnostic certificates. This is **not** a calculation of
  the full four-dimensional transfer-matrix spectrum.
- `evidence_bridge.py` invokes the existing PHYSQED engine on a local
  quaternion norm identity, independently replays character receipts and
  seeded finite-lattice results, and assembles a source-hashed evidence ledger.
  It does not modify PHYSQED's proof semantics. See [EVIDENCE_SCOPE.md](EVIDENCE_SCOPE.md)
  for commands, check boundaries, and open mathematical obligations.

The `artifacts/` directory contains one small, actual two-chain run, two
beta-zero starting-state controls, its independent finite character interval
receipt, and an integrated JSON evidence report. All five sources can be
replayed using the commands in the scope document;
the dedicated GitHub Actions workflow also runs the whole test suite and
refuses stale or forged report records.

Newton Solver and EINSTEIN-X Ω integration remains
`SOURCE_UNAVAILABLE_NOT_EXECUTED` until their exact executable sources are
available. **No continuum theory or positive physical mass gap is proved.**

For the follow-up, six-plaquette local Wilson updates have been independently
compared with the original global action, and a separate matched cold/Haar
trajectory experiment now documents residual non-equilibration on \(2^4\)
and \(3^4\) lattices. See [EQUILIBRATION_SCOPE.md](EQUILIBRATION_SCOPE.md).
The new receipts do not supersede or change the five original evidence files.
