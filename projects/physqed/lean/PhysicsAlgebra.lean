/-! PHYSQED 0.1: elementary algebraic physics examples.
    These results are not empirical validations or proofs of physical laws.
    Lean proves only the formally stated propositions below. -/
import Mathlib

namespace PHYSQED

/-- Quadratic kinetic-energy cross-term identity under a scalar velocity shift. -/
theorem kinetic_shift (m u v : ℝ) :
    m * ((v + u)^2 - v^2) = m * (2 * v * u + u^2) := by
  ring

/-- Energy-derivative algebra conditional on the stated oscillator equation. -/
theorem oscillator_energy_derivative (m k x v a : ℝ)
    (equation_of_motion : m * a = -k * x) :
    k * x * v + m * v * a = 0 := by
  calc
    k * x * v + m * v * a = v * (k * x + m * a) := by ring
    _ = 0 := by rw [equation_of_motion]; ring

end PHYSQED
