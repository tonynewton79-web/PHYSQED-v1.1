# PHYSQED v1.2 — Typed Coupled Physics Contracts

The EinsteinMaxwellSpec in projects/physqed/v12/contracts.py is a typed,
fail-closed, 16-node proof-carrying contract for one standard physical
model. A PASS means exact chart-local component equations and independent
curvature point checks passed under the user's explicit premises. It does NOT
mean the physical theory, all domain assumptions, or quantum gravity is proved.

## Explicit conventions

Signature (-,+,+,+), zero shift, g00=-N², positive lapse, 3-metric hij=gij,
future normal n=(1/N,0,0,0), Kij=+(partial_t hij)/(2N).

Fμν=∂μAν-∂νAμ, Tμν=Fμα Fν^α -(1/4)gμν Fρσ F^ρσ,
Eμν=Gμν+Λgμν-κTμν. The standard geometrized R-F² action has κ=2.

The matter/curvature divergence bridge checks
∇^μTμν=Fνλ J^λ where J^λ=∇μ F^μλ, and
∇^μ Eμν + κ ∇^μ Tμν=0.

## 3+1 Hamiltonian and momentum checks

ρ=T00/N², H=R3+K²-KijK^ij-2Λ-2κρ and
Mi=DjK^j_i-DiK-κT0i/N. With the *positive* extrinsic curvature convention,
the independently generated geometric identities are H=2 E00/N² and
Mi=E0i/N. These are off-shell identities. A model may satisfy both bridges
while failing the Einstein equations and thus remain REJECTED.

## Sixteen typed nodes

1. Unit normal.
2. Potential and declared two-form consistency.
3. Declared stress and Maxwell constitutive agreement.
4. Electromagnetic Bianchi.
5. Maxwell source-free Euler–Lagrange equation.
6. Matter Noether/divergence bridge.
7. Stress-energy conservation.
8. Einstein field equations.
9. Contracted Einstein Bianchi.
10. Einstein/stress-energy divergence bridge.
11. ADM Hamiltonian constraint.
12. ADM momentum constraints.
13. Hamiltonian Gauss projection identity.
14. Momentum Codazzi projection identity.
15. Optional claimed Hamiltonian certificate.
16. Optional claimed momentum certificate.

All nodes must pass, including optional claimed certificate agreements when
provided. A separate exact Fraction 2-jet oracle recomputes 4D and 3D
curvature at every admissible rational witness. SymPy supplies the jets,
but not the oracle curvature calculation. Rational point agreement does
NOT establish a global theorem.

## Textbook standard

Reissner–Nordström electrovacuum M=1, Q=1/2 at r=4, θ=π/2 passes all
16 nodes and 52 independent Ricci/Einstein/scalar pointwise comparisons.
Wrong κ, Λ, stress, F, lapse, ADM claims and domain witness are rejected.
A nontrivial off-shell momentum example passes Codazzi while rejecting
Einstein; a flat time-varying electric field passes the Noether bridge
while failing sourceless Maxwell and stress conservation.

## Run

    python -m pip install -r requirements-test.txt
    PYTHONPATH=projects/physqed python -m v12.contract_benchmark --out-dir /tmp/physqed-v12-contracts
    python -m unittest discover -s projects/physqed/tests -p test_physics_v12_contract.py -k test_valid_einstein_maxwell_full_linked_contract -v

GitHub Actions runs all eleven methods (including a receipt-replay tamper test) in separate Python processes so
large SymPy symbolic caches do not accumulate across cases. Outputs are JSON
receipts with original assumptions, exact residual indices and source/
oracle file SHA-256 digests. SHA-256 attests reproducibility rather than
an independently checked proof. The native Python 3.15.2 CI gate remains
PENDING until GitHub reports an actual successful run.

## Roadmap and scope

Nonzero ADM shift; arbitrary foliations and domain assumptions; nonabelian
Yang–Mills stress and currents; independent variational derivations;
full constraint propagation; well-posed PDE estimates; external proof
assistant, Hilbert-space operator domains, renormalisation and functional
quantum gravity remain separate research and engineering tasks.

## Full receipt replay

Calling replay_contract_receipt(spec, receipt) recomputes every component, both rational curvature-oracle comparisons, and the verifier source digests from the original typed specification. It compares the full canonical serialized receipt, not merely its self-reported checksum. A changed JSON result is rejected. A replayed *rejection* is not mislabelled as a positive solution certificate. This checks reproducibility of the specific local symbolic implementation and still does not constitute a proof assistant's formal verification of continuum physics.
