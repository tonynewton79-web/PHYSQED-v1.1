import Mathlib

/-!
PHYSQED v1.0: generic soundness for three or four conditional algebraic
premises, supplied with an exact polynomial witness identity.
Lean theorem compilation is NOT a certificate that any JSON source matched
this theorem, and no physical law or semantic equivalence is asserted.
-/

namespace PHYSQEDMultiPremise

theorem three_premise_sound
    (A₁ B₁ A₂ B₂ A₃ B₃ C D W₁ W₂ W₃ : ℝ)
    (hcertificate : C - D =
      W₁ * (A₁ - B₁) + W₂ * (A₂ - B₂) + W₃ * (A₃ - B₃))
    (h₁ : A₁ = B₁) (h₂ : A₂ = B₂) (h₃ : A₃ = B₃) :
    C = D := by
  have hzero : C - D = 0 := by
    simpa [h₁, h₂, h₃] using hcertificate
  exact sub_eq_zero.mp hzero

theorem four_premise_sound
    (A₁ B₁ A₂ B₂ A₃ B₃ A₄ B₄ C D W₁ W₂ W₃ W₄ : ℝ)
    (hcertificate : C - D =
      W₁ * (A₁ - B₁) + W₂ * (A₂ - B₂) +
      W₃ * (A₃ - B₃) + W₄ * (A₄ - B₄))
    (h₁ : A₁ = B₁) (h₂ : A₂ = B₂)
    (h₃ : A₃ = B₃) (h₄ : A₄ = B₄) : C = D := by
  have hzero : C - D = 0 := by
    simpa [h₁, h₂, h₃, h₄] using hcertificate
  exact sub_eq_zero.mp hzero

theorem three_premise_product_example
    (v u a b t s : ℝ)
    (h₁ : v = u) (h₂ : a = b) (h₃ : t = s) :
    v * a * t = u * b * s := by
  have hcert :
      v * a * t - u * b * s =
      (a * t) * (v - u) +
      (u * t) * (a - b) +
      (u * b) * (t - s) := by
    ring
  exact three_premise_sound v u a b t s
    (v*a*t) (u*b*s) (a*t) (u*t) (u*b) hcert h₁ h₂ h₃

theorem four_premise_product_example
    (m n v u a b t s : ℝ)
    (h₁ : m = n) (h₂ : v = u) (h₃ : a = b) (h₄ : t = s) :
    m * v * a * t = n * u * b * s := by
  have hcert :
      m * v * a * t - n * u * b * s =
      (v * a * t) * (m - n) +
      (n * a * t) * (v - u) +
      (n * u * t) * (a - b) +
      (n * u * b) * (t - s) := by
    ring
  exact four_premise_sound m n v u a b t s
    (m*v*a*t) (n*u*b*s)
    (v*a*t) (n*a*t) (n*u*t) (n*u*b)
    hcert h₁ h₂ h₃ h₄

end PHYSQEDMultiPremise
