# A constrained inflationary waterfall benchmark for PHYSQED

This research integration treats the polynomial potential from a Euclidean
Einstein-scalar saddle programme as an **explicitly new** canonically normalized
Lorentzian two-field model. It does not identify the scalar with a fundamental
inflaton or an ABJM bulk degree of freedom.

## Canonical model

In units where the reduced Planck mass is M, set x=phi/mu, z=chi/mu,
tau=Lambda^2 t/mu, h=H mu/Lambda^2 and R=rho_rad/Lambda^4. Let

    U(x,z)=3-alpha*x^2+(1/2)*x^4
            +(kappa/2)*(yc-x^2)*z^2+(lambda/4)*z^4,
    alpha=(4+delta)/2, delta=0.016202803686105016,
    yc=0.81, mu/M=10.05, kappa=10000,
    v=3-alpha^2/2, beta=v/((alpha-yc)^2+2*v),
    lambda=kappa^2/(4*beta).

The potential has the exact identity

    U=(lambda/4)*(z^2-(kappa/lambda)*(x^2-yc))^2
      +(1/2-beta)*(x^2-yv)^2,
    yv=(alpha-2*beta*yc)/(1-2*beta).

Therefore U>=0 and its four global minima have
x=+/-sqrt(yv), z=+/-sqrt(kappa/lambda*(yv-yc)), U=0.
The z=0 valley becomes tachyonically unstable at |x|=sqrt(yc)=0.9.

## Conservative PHYSQED exact symbolics

The restricted typed-input fixture in
`projects/physqed/examples/typed/inflaton_waterfall_minisuperspace.json`
is a flat-FLRW homogeneous **lapse-fixed** variational model with scale
factor b(tau). Its Lagrangian is

    L=-3*xi*b*(b')^2+(b^3/2)*((x')^2+(z')^2)-b^3*U(x,z),
    xi=(M/mu)^2.

PHYSQED compares all three Euler-Lagrange components to explicitly
submitted target expressions, checks the translation Noether identity,
and records an input/implementation hash and scoped receipt.
Adversarial tests invert the z equation and require rejection.

The Hamiltonian/Friedmann constraint is a **separate** condition:
`3*xi*h^2=U+((x')^2+(z')^2)/2+R` with h=b'/b.
The lapse-fixed E-L equation alone is not a proof that this constraint
holds for arbitrary initial data. The numerical module initializes
with the positive Friedmann root, integrates the scalar equations
and obtains h from the constrained energy density.

Run from the repository root:

    python -m pip install sympy==1.14.0
    python -m unittest discover -s projects/physqed/tests \
      -p 'test_inflaton_waterfall_typed.py' -v
    PYTHONPATH=projects/physqed python -m v12.typed_cli \
      --input projects/physqed/examples/typed/inflaton_waterfall_minisuperspace.json \
      --output inflaton_typed_receipt.json

A PHYSQED `PASS_SCOPED_SYMBOLIC_OBLIGATIONS__PHYSICS_UNVERIFIED`
is **not** a proof of successful cosmological dynamics.

## Open-system numerical experiment

For the phenomenological extension define nonnegative
`Gamma_phi(x),Gamma_chi(x)`, measured in units Lambda^2/mu.
Primes denote d/dtau. The equations are

    x''+(3h+Gamma_phi)*x'+U_x=0
    z''+(3h+Gamma_chi)*z'+U_z=0
    R'+4h R=Gamma_phi*(x')^2+Gamma_chi*(z')^2
    h=(mu/M)*sqrt((U+((x')^2+(z')^2)/2+R)/3)
    N'=h.

The radiation source term exactly cancels scalar energy removed by the
Gamma terms. Hence dE/dtau=-3h*((x')^2+(z')^2)-4h*R, giving the
Raychaudhuri identity
`h'=-(mu/M)^2*((x')^2+(z')^2+(4/3)*R)/2` where h>0.
This identity concerns the specified effective system, not quantum
thermalization or the existence of a microscopic decay channel.

The switch is
`Gamma_phi=Gamma_chi=gamma*(1+tanh((x-0.9)/0.005))/2`
with gamma in {0,15,30}. The smooth switch has exponentially small,
but nonzero, effects on x below threshold. The initial pivot is chosen
using **r=0.02629 as an input**, not a prediction. At the first x=0.9
crossing a seed `z=10^-7` is imposed; this is a stochastic-fluctuation
proxy, not a self-consistent quantum mode calculation. Its added
dimensionless potential energy is lambda*(10^-7)^4/4.

Numerical command:

    python -m pip install numpy==1.26.4 scipy==1.13.1
    python projects/physqed/research/inflaton_waterfall_dynamics.py \
      --post-duration 55 --output inflaton_dynamics_receipt.json

Exploratory integrations with a longer 120-tau horizon and more stringent
step controls found the initial waterfall at N~=55.26, with first
epsilon_H>1 at about N=89.52 (gamma=0), N=124.85 (gamma=15) and
N=160.55 (gamma=30). Radiation is absent without Gamma and may dominate
only after prolonged additional inflation with Gamma. The numerical
measurements are conditional on the seed, friction prescription,
resolution, and runtime horizon. They are not PHYSQED exact theorems.
The CI script uses a shorter 55-tau diagnostic window and writes its
own result; it must be consulted before describing a hosted run as passed.

## ABJM boundary-map gate

The homogeneous two-saddle suppression rate
A(q)=2 log(cosh C/cosh(C sqrt(1-q^2))) has
A(q)=C tanh(C)q^2+(C/4)(tanh(C)-C sech(C)^2)q^4+... .
Both coefficients are positive for C>0. Simply identifying
V=V0-K*A(s*phi), K>0 with constant real s cannot reproduce the
benchmark negative quadratic and positive quartic terms.
This excludes only that shortcut. A genuine top-down match requires
canonical kinetic normalization, the bulk/boundary source-to-field
map, the Dirichlet-to-Neumann response, the complete perturbation
spectrum and globally regular saddle pairing.

## Scope

The source potential is borrowed from a Euclidean benchmark; the field
scale mu and gamma law are additional model choices. No actual
cosmological observations are fit independently, the radiation fluid
is not a thermalizing microscopic plasma, ABJM fluctuations are not
calculated, and a publishable fundamental inflaton identification is
not claimed. This is a falsifiable diagnostic of a conditional model.

The exact two-field algebra is a standard hybrid-inflation style
construction, not presently established as a new fundamental mechanism.
