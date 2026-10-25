import Mathlib

/-!
PHYSQED v0.9: generic two-premise certificate soundness in Lean 4.
This theorem proves a conditional algebraic implication if the witness
identity and both premise equalities are supplied as hypotheses.
It does not certify that PHYSQED generated a correct certificate for
an arbitrary input or that a physical model is true.
-/

namespace PHYSQEDTwoPremises

theorem two_premise_certificate_sound
    (A B E F C D W₁ W₂ : ℝ)
    (hcertificate : C - D = W₁ * (A - B) + W₂ * (E - F))
    (h₁ : A = B) (h₂ : E = F) : C = D := by
  have hzero : C - D = 0 := by
    simpa [h₁, h₂] using hcertificate
  exact sub_eq_zero.mp hzero

theorem independent_linear_example
    (x y z w : ℝ)
    (h₁ : x + y = z)
    (h₂ : x - y = w) :
    x ^ 2 - y ^ 2 = z * w := by
  have hcert :
      (x ^ 2 - y ^ 2) - z * w =
        (x - y) * ((x + y) - z) + z * ((x - y) - w) := by
    ring
  exact two_premise_certificate_sound
    (x + y) z (x - y) w (x ^ 2 - y ^ 2) (z * w)
    (x - y) z hcert h₁ h₂

end PHYSQEDTwoPremises
