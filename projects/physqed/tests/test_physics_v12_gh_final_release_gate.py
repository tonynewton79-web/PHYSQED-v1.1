"""Final release refusal: exact high-frequency source and flux counterexamples."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.gh_final_release_gate import (
    arbitrary_source_weighted_obstruction as source,
    boundary_standard_energy_obstruction as boundary,
    certify_final_gh_release_gate as final,
    replay_final_gh_release_gate as replay)


class FinalGHReleaseTests(unittest.TestCase):
    def test_all_forced_first_order_equations(self):
        self.assertTrue(source(8)["all_forced_first_order_equations_zero"])

    def test_zero_initial_first_order_and_auxiliary_data(self):
        self.assertTrue(source(8)["all_initial_first_order_and_reduction_fields_zero"])

    def test_homogeneous_first_order_boundary_rows(self):
        self.assertTrue(source(8)["first_order_incoming_and_harmonic_boundary_rows_zero"])

    def test_source_norm_independent_of_transverse_frequency(self):
        self.assertEqual(source(2)["volume_source_spacetime_L2_squared"],
                         source(64)["volume_source_spacetime_L2_squared"])

    def test_exact_transverse_H1_growth(self):
        self.assertEqual(source(8)["H1_psi_transverse_at_t1_squared"],"64*pi**2")

    def test_source_solution_ratio_diverges(self):
        self.assertEqual(source(16)["squared_solution_source_ratio"],"192")

    def test_auxiliary_defect_is_not_zero(self):
        self.assertEqual(source(8)["reduction_defect_at_t1_squared"],"65*pi**2")

    def test_bad_frequency_input_refused(self):
        for n in (0,-1,1.5,"8",100001,True):
            with self.subTest(n=n),self.assertRaises(ValueError):
                source(n)

    def test_boundary_six_adapted_rows_exactly_zero(self):
        self.assertTrue(boundary()["six_adapted_Sommerfeld_rows_zero"])

    def test_boundary_four_harmonic_rows_exactly_zero(self):
        self.assertTrue(boundary()["four_first_order_harmonic_boundary_rows_zero"])

    def test_incoming_outgoing_norms(self):
        r=boundary()
        self.assertEqual((r["incoming_norm_squared"],r["outgoing_norm_squared"]),
                         ("2","1"))

    def test_exact_negative_outward_flux(self):
        r=boundary()
        self.assertEqual(r["outward_standard_energy_flux"],"-1/4")
        self.assertTrue(r["outward_flux_negative"])

    def test_incoming_operator_full_rank(self):
        self.assertTrue(boundary()["ten_incoming_boundary_rows_independent"])

    def test_transfer_operator_is_not_contractive(self):
        self.assertEqual(boundary()["boundary_transfer_squared_singular_values"]["3"],1)

    def test_release_hold_recorded(self):
        self.assertEqual(final()["status"],
             "HOLD_STRONG_WELLPOSEDNESS__TWO_EXACT_SCOPE_OBSTRUCTIONS")

    def test_no_false_natural_unweighted_theorem_refutation(self):
        r=final()
        self.assertFalse(r["natural_unweighted_first_order_L2_wellposedness_disproved"])
        self.assertFalse(r["modified_symmetrizer_or_Kreiss_proof_disproved"])

    def test_no_false_einstein_wellposedness_promotion(self):
        self.assertFalse(final()["nonlinear_Einstein_IBVP_proven"])

    def test_replay_recomputes_full_claim(self):
        r=final()
        self.assertTrue(replay(r))
        bad=copy.deepcopy(r)
        bad["nonlinear_Einstein_IBVP_proven"]=True
        self.assertFalse(replay(bad))


if __name__=="__main__":
    unittest.main()
