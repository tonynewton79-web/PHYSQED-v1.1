"""Maxwell moving-boundary benchmark source-linked to 18-node shifted ADM."""
import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12.linked_maxwell_ibvp import (
    verify_linked_maxwell_positive_control as verify,
    replay_linked_maxwell_positive_control as replay)
ROOT=Path(__file__).resolve().parents[1]/"examples"/"typed"


def model():
    full=json.loads((ROOT/"linked_adm_shifted_minkowski.json").read_text())
    return full["field_model"]


class LinkedMaxwellTests(unittest.TestCase):
    def test_same_minkowski_source_18_nodes_and_maxwell_boundary(self):
        r=verify(model())
        self.assertEqual(r["status"],
            "PASS_FIELD_AND_MAXWELL_POSITIVE_CONTROL__GR_BOUNDARY_LINK_OPEN")
        self.assertTrue(r["all_18_Einstein_Maxwell_nodes_passed"])
        self.assertTrue(r["Maxwell_moving_wall_energy_flux_and_Gauss_verified"])
        self.assertFalse(r["constraint_energy_boundary_from_GR_evolution_proven"])
        self.assertFalse(r["GR_and_Maxwell_boundaries_identical_spacetime_domain"])

    def test_nonzero_electromagnetic_field_refused_from_positive_control(self):
        m=model()
        m["potential"]=[0,"t",0,0]
        with self.assertRaises(ValueError):
            verify(m)

    def test_nonflat_spatial_metric_refused(self):
        m=model()
        m["spatial_metric"][0][0]=2
        with self.assertRaises(ValueError):
            verify(m)

    def test_spacetime_dependent_shift_refused(self):
        m=model()
        m["shift"]=["t",0,0]
        with self.assertRaises(ValueError):
            verify(m)

    def test_exact_receipt_tampering_rejected(self):
        m=model()
        r=verify(m)
        self.assertTrue(replay(m,r))
        bad=copy.deepcopy(r)
        bad["constraint_energy_boundary_from_GR_evolution_proven"]=True
        self.assertFalse(replay(m,bad))


if __name__=="__main__":
    unittest.main()
