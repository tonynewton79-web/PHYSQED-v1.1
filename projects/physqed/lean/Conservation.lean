import Mathlib

/-!
PHYSQED v0.3. Calculus-level conditional energy balance for a classical
one-dimensional oscillator. No unproved placeholders or empirical claims.
Lean 4 / mathlib v4.24.0. THIS FILE REQUIRES A SUCCESSFUL LEAN CI RUN
BEFORE ANY STATEMENT IS LABELLED LEAN-KERNEL VERIFIED.
-/

namespace PHYSQEDConservation

/-- Mechanical energy. Valid interpretation requires x'=v and v'=a. -/
def energy (m k : ℝ) (x v : ℝ → ℝ) (t : ℝ) : ℝ :=
  (m / 2) * (v t) ^ 2 + (k / 2) * (x t) ^ 2

/-- Exact power balance, conditional on the declared differentiability and
    damped Hooke-Newton equation. No conclusion about measured systems. -/
theorem energy_hasDerivAt (m k c : ℝ) (x v a : ℝ → ℝ) (t : ℝ)
    (hx : HasDerivAt x (v t) t)
    (hv : HasDerivAt v (a t) t)
    (hODE : m * a t + c * v t + k * x t = 0) :
    HasDerivAt (energy m k x v) (-c * (v t) ^ 2) t := by
  have hquad : HasDerivAt (energy m k x v)
      ((m / 2) * (2 * (v t) * a t) + (k / 2) * (2 * (x t) * v t)) t := by
    convert ((hv.pow 2).const_mul (m / 2)).add
      ((hx.pow 2).const_mul (k / 2)) using 1 <;> ring
  have hrate : (m / 2) * (2 * (v t) * a t) +
      (k / 2) * (2 * (x t) * v t) = -c * (v t) ^ 2 := by
    calc
      _ = (v t) * (m * a t + c * v t + k * x t) - c * (v t) ^ 2 := by ring
      _ = -c * (v t) ^ 2 := by rw [hODE]; ring
  rw [hrate] at hquad
  exact hquad

/-- The undamped oscillator has constant mechanical energy on the whole real
    time domain, provided the ODE and derivative hypotheses hold everywhere. -/
theorem undamped_energy_constant (m k : ℝ) (x v a : ℝ → ℝ)
    (hx : ∀ t, HasDerivAt x (v t) t)
    (hv : ∀ t, HasDerivAt v (a t) t)
    (hODE : ∀ t, m * a t + k * x t = 0)
    (t : ℝ) : energy m k x v t = energy m k x v 0 := by
  have hzero : ∀ s : ℝ, HasDerivAt (energy m k x v) 0 s := by
    intro s
    convert energy_hasDerivAt m k 0 x v a s (hx s) (hv s) (by simpa using hODE s)
      using 1 <;> ring
  have hdiff : Differentiable ℝ (energy m k x v) := by
    intro s
    exact (hzero s).differentiableAt
  have hder : ∀ s : ℝ, deriv (energy m k x v) s = 0 := by
    intro s
    exact (hzero s).deriv
  exact is_const_of_deriv_eq_zero hdiff hder t 0

/-- For a strictly damped oscillator, its energy derivative is nonpositive. -/
theorem damped_energy_nonpositive (m k c : ℝ) (x v a : ℝ → ℝ) (t : ℝ)
    (hc : 0 ≤ c)
    (hx : HasDerivAt x (v t) t)
    (hv : HasDerivAt v (a t) t)
    (hODE : m * a t + c * v t + k * x t = 0) :
    deriv (energy m k x v) t ≤ 0 := by
  rw [(energy_hasDerivAt m k c x v a t hx hv hODE).deriv]
  nlinarith [mul_nonneg hc (sq_nonneg (v t))]

/-- Negative control: nonzero velocity and positive damping imply strict
    energy decrease, so unconditional energy conservation must be rejected. -/
theorem damped_energy_strict (m k c : ℝ) (x v a : ℝ → ℝ) (t : ℝ)
    (hc : 0 < c) (hvel : v t ≠ 0)
    (hx : HasDerivAt x (v t) t)
    (hv : HasDerivAt v (a t) t)
    (hODE : m * a t + c * v t + k * x t = 0) :
    deriv (energy m k x v) t < 0 := by
  rw [(energy_hasDerivAt m k c x v a t hx hv hODE).deriv]
  have hvsq : 0 < (v t) ^ 2 := sq_pos_of_ne_zero hvel
  nlinarith [mul_pos hc hvsq]

end PHYSQEDConservation
