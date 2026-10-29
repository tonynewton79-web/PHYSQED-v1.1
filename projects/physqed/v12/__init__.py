"""PHYSQED v1.2 public API. All checks are scoped and fail closed."""
from .geometry import Geometry, ScopeError, cartan_torsion, tetrad_metric, zero
from .gauge import LieAlgebra, GaugeField, matrix_curvature, transformed_connection, transformation_residual
from .quantum import (commutator, anticommutator, is_hermitian,
                      quantum_expectation, heisenberg_residual,
                      robertson_residual, clifford_residual,
                      finite_ccr_obstruction, poisson_bracket,
                      poisson_jacobi_residual, constraint_closure,
                      adm_scalar_constraint)
from .fields import (euler_lagrange, canonical_stress,
                     translation_noether_residual, noether_current,
                     quadratic_propagator, wick, first_order_phi4_two_point)
from .receipts import certify, save_certificate

__version__="1.2.0"

from .contracts import EinsteinMaxwellSpec, ContractNode, evaluate_contract, save_contract
