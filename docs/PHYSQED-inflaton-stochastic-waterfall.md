# Stochastic waterfall: scope, results, and Einstein constraints

The current canonical two-field inflaton potential was tested with a
**Gaussian waterfall-scale seed** sigma_z=3.80e-7, estimated from
H_w/(2*pi*mu). This variance is *not* obtained from complete canonical
3D Bunch-Davies mode matching through the waterfall.

## Distinct experiments

1. The portable CI module
   projects/physqed/research/stochastic_waterfall_deltaN.py
   evolves 96 independent homogeneous Friedmann patches with Gaussian
   waterfall seeds and records the change of e-folds to a uniform-density
   slice. Passing this check verifies a conditional numerical regression.
2. The separate 1,024-patch and 128-cell periodic **one-dimensional**
   nonlinear gradient experiments were completed in a local
   reproducibility packet. Their sources and figures are part of a
   32-page, 29-figure cumulative research paper, not a claim of a
   hosted full Einstein lattice calculation.

The large ensemble returned std(deltaN)=0.01888575, skewness=1.62575,
excess kurtosis=4.73611 and Corr(deltaN,log|z_seed|)=-0.999790.
The fitted log dependence was deltaN≈-0.29872-0.0185527*log|z_seed|.
For an *exactly* logarithmic transform of a Gaussian seed, the
standardized skewness would instead be 1.53514, excess kurtosis 4.

These are local waterfall-scale expansion proxies, not a CMB-scale
curvature spectrum. They cannot be substituted into the separate
linear-mode result r≈0.0699.

The 1D reference lattice reaches its first mean-field epsilon_H=1
around N=34.244 after the waterfall, and has 16 waterfall-field sign
changes. However, fixed-comoving-grid spacing at exit exceeds inverse
vacuum mass scales by factors 1.20e14 and 1.15e16 on a 128-site box.
This is a *severe loss of defect-scale resolution*. Reported tiny
late gradient energy cannot be interpreted as physical wall energy.

## Exact obstruction to homogeneous metric backreaction

In a spatially flat FLRW metric with homogeneous unit lapse and zero
shift, extrinsic curvature K^j_i=-H(t)*delta^j_i implies
D_j(K^j_i-delta^j_i K)=2 partial_i H(t)=0.
The canonical inhomogeneous scalar momentum source is generally
J_i=-sum_I dot(phi_I)*partial_i phi_I !=0.
Thus the momentum constraint cannot hold locally. Likewise a
homogeneous left-hand side 3 M_Pl^2 H(t)^2 cannot match nonconstant
local density on the Hamiltonian-constraint right-hand side.

The lattice therefore uses mean-field gravity and DOES NOT solve
the 3+1 Einstein constraints.

With the *imposed* Gamma=15 energy-transfer law, the toy global
radiation bath becomes >90% dominant around N=70.34 after the waterfall.
This is not microscopic reheating or thermal equilibrium, and late
field gradients remain unresolved.

Relevant prior art: Murata and Tada, JCAP 09 (2026) 061, DOI
10.1088/1475-7516/2026/09/061; Launay, Rigopoulos and Shellard,
Phys. Rev. D 113 (2026) 123515, DOI 10.1103/h2cb-q1mt;
Saha, Tada and Urakawa, arXiv:2604.00978.

The remaining scientific gates are: quantum-consistent scale-dependent
stochastic noise, 3+1 constrained metric evolution, adaptive defect
resolution, entropy-to-curvature transfer, microscopic reheating, and
a canonical ABJM source-to-bulk field map. None is certified here.
