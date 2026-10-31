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

from .contracts import replay_contract_receipt

from .typed_input import (PhysicsInput, RestrictedExpression,
                          load_physics_input, plan_physics_obligations,
                          execute_physics_input, replay_physics_input)

from .physical_types import TensorType, GeometrizedDimensions, check_tensor_signatures
from .typed_em_bridge import run_typed_einstein_maxwell

from .adm_shift import (ShiftedEinsteinMaxwellSpec,
                        evaluate_shifted_einstein_maxwell, replay_shifted_adm)
from .typed_shift_bridge import run_typed_shifted_adm

from .frozen_energy import audit_frozen_adm
from .variable_energy import audit_matrix_energy, adm_constraint_matrices
from .energy_receipts import issue_energy_receipt, replay_energy_receipt

from .domain_energy import (DomainScopeError, bernstein_bounds,
                            certify_domain_energy, replay_domain_energy)

from .rational_energy import (certify_rational_domain_energy,
                              replay_rational_domain_energy)

from .typed_adm_domain import (parse_rational_sources,
                               certify_typed_adm_domain,
                               replay_typed_adm_domain)

from .linked_adm_boundary import (certify_linked_adm_boundary,
                                  replay_linked_adm_boundary)

from .maxwell_ibvp_control import (
    verify_maxwell_shifted_boundary, replay_maxwell_shifted_boundary)
from .linked_maxwell_ibvp import (
    verify_linked_maxwell_positive_control, replay_linked_maxwell_positive_control)
from .harmonic_boundary_obstruction import (
    verify_harmonic_boundary_obstruction, replay_harmonic_boundary_obstruction)

from .gh_boundary_map import (
    general_differential_intertwiner, normal_mode_symbol, first_corner_gate,
    certify_explicit_linearized_metric, certify_symbol_and_controls,
    replay_gh_metric)

from .gh_glancing_corners import (
    glancing_obstruction, glancing_summary, higher_corner_hierarchy,
    verify_scalar_sommerfeld_reference,
    certify_glancing_and_corners, replay_glancing_corners)
from .gh_curved_ppwave import verify_curved_ppwave, replay_curved_ppwave

from .gh_glancing import (
    symbolic_glancing_obstruction, off_glancing_constant,
    certify_glancing_gate, replay_glancing_gate)
from .gh_higher_corners import (
    initial_jet_hierarchy, certify_metric_corners, replay_metric_corners)
from .gh_curved_plane_wave import (
    verify_curved_gh_control, replay_curved_gh)

from .gh_first_order_uniform import (
    first_order_characteristics, adapted_normal_symbol,
    stable_mode_reduction, analytic_uniform_bound,
    glancing_diagnostic, certify_first_order_gh, replay_first_order_gh)

from .gh_curved_timelike_frozen import (
    verify_ppwave_timelike_frozen, replay_ppwave_timelike_frozen)

from .gh_forced_resolvent import (
    first_order_forcing_normal_form, boundary_source_lift,
    exact_exponential_volume_and_boundary_solution,
    prove_regular_source_resolvent, replay_regular_source_resolvent,
    nonzero_reduction_defect_solution)
from .gh_forced_corners import (
    check_sourced_harmonic_corners, sourced_wave_positive_control)

from .gh_final_release_gate import (
    arbitrary_source_weighted_obstruction, boundary_standard_energy_obstruction,
    certify_final_gh_release_gate, replay_final_gh_release_gate)
