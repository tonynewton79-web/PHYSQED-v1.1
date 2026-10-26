"""Finite SU(2) Monte Carlo pilot checks; no continuum inference."""
import json
import math
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from research.yang_mills_su2.lattice import Lattice4D
from research.yang_mills_su2.simulation import (
    connected_timeslice,
    haar_su2,
    metropolis_sweep,
    run_chains,
    timeslice_plaquette,
)
from research.yang_mills_su2.run_pilot import main


class SimulationTests(unittest.TestCase):
    def test_positive_beta_uphill_acceptance_and_rollback(self):
        class ControlledRNG:
            def __init__(self, threshold):
                self.threshold = threshold
                self.proposals = 0
                self.gauss_calls = 0

            def gauss(self, center, spread):
                value = (0.0, 0.0, 1.0)[self.gauss_calls % 3]
                self.gauss_calls += 1
                return value

            def uniform(self, low, high):
                self.proposals += 1
                return math.pi / 3 if self.proposals == 1 else 0.0

            def random(self):
                return self.threshold

        accepted_lattice = Lattice4D((2, 2, 2, 2))
        rejected_lattice = Lattice4D((2, 2, 2, 2))
        self.assertEqual(metropolis_sweep(accepted_lattice, 1.0, math.pi/3,
                                          ControlledRNG(0.04)), (64, 64))
        self.assertEqual(metropolis_sweep(rejected_lattice, 1.0, math.pi/3,
                                          ControlledRNG(0.06)), (63, 64))
        self.assertAlmostEqual(accepted_lattice.wilson_action(1.0), 3.0, places=11)
        self.assertEqual(rejected_lattice.wilson_action(1.0), 0.0)

    def test_zero_beta_accepts_all_symmetric_proposals(self):
        lattice = Lattice4D((2, 2, 2, 2))
        accepted, attempted = metropolis_sweep(lattice, 0.0, 0.2, random.Random(1))
        self.assertEqual((accepted, attempted), (64, 64))
        self.assertTrue(any(abs(v[0] - 1.0) > 1e-6 for v in lattice.links.values()))

    def test_time_slices_and_connected_covariance(self):
        self.assertEqual(timeslice_plaquette(Lattice4D((2, 2, 2, 2))), (1.0, 1.0))
        c = connected_timeslice([(1.0, 2.0), (3.0, 4.0)])
        self.assertEqual(len(c), 2)
        self.assertAlmostEqual(c[0], 1.25)
        self.assertAlmostEqual(c[1], 0.75)

    def test_seeded_independent_chains_repeat(self):
        options = dict(extents=(2, 2, 2, 2), beta=0.5, seeds=(123, 456),
                       warmup=1, sweeps=2, thin=1, epsilon=0.12)
        record = run_chains(**options)
        self.assertEqual(record, run_chains(**options))
        self.assertEqual(record["status"], "FINITE_LATTICE_NUMERICAL")
        self.assertFalse(record["continuum_mass_gap_proven"])
        self.assertFalse(record["equilibrium_claim"])
        self.assertEqual(record["thermalization_status"], "UNTHERMALIZED_COLD_START_TRANSIENT")
        self.assertEqual(len(record["connected_correlator"]), 2)
        self.assertEqual(len(record["per_chain"]), 2)
        self.assertGreater(record["acceptance_rate"], 0.0)
        self.assertEqual([m["sweep"] for m in record["per_chain"][0]["measurements"]], [1, 2])
        self.assertEqual(len(record["per_chain"][0]["measurements"][0]["timeslice"]), 2)

    def test_reject_invalid_inputs_and_insufficient_independence(self):
        good = dict(extents=(2, 2, 2, 2), beta=1.0, seeds=(1, 2),
                    warmup=0, sweeps=2, thin=1, epsilon=0.2)
        for name, value in [
            ("beta", -1), ("beta", math.nan), ("epsilon", 0),
            ("epsilon", math.pi + 0.01), ("extents", (1, 2, 2, 2)),
            ("sweeps", 0), ("thin", 0), ("warmup", -1),
            ("seeds", (1,)), ("seeds", (1, 1)),
            ("seeds", (7, -7)),
            ("initialization", "adversarial"),
        ]:
            with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                run_chains(**{**good, name: value})

    def test_haar_start_centering_and_beta_zero_negative_control(self):
        rng = random.Random(919)
        quats = [haar_su2(rng) for _ in range(1200)]
        self.assertTrue(all(abs(sum(x*x for x in q)-1) < 1e-12 for q in quats))
        self.assertLess(abs(sum(q[0] for q in quats) / len(quats)), 0.07)
        opts = dict(extents=(2, 2, 2, 2), beta=0.0, seeds=(123, 456),
                    warmup=2, sweeps=4, thin=1, epsilon=0.15)
        cold = run_chains(**opts, initialization="cold")
        hot = run_chains(**opts, initialization="haar")
        self.assertEqual(hot, run_chains(**opts, initialization="haar"))
        self.assertEqual(hot["parameters"]["initialization"], "haar")
        self.assertEqual(hot["thermalization_status"], "UNTHERMALIZED_HAAR_START_TRANSIENT")
        self.assertLess(abs(hot["spatial_plaquette"]["mean"]), 0.3)
        self.assertGreater(cold["spatial_plaquette"]["mean"], 0.8)

    def test_cli_writes_reproducible_scoped_json(self):
        args = ["--extents", "2,2,2,2", "--beta", "0.0", "--seeds", "2,3",
                "--warmup", "0", "--sweeps", "2", "--thin", "1", "--epsilon", "0.1"]
        with tempfile.TemporaryDirectory() as td:
            first = Path(td)/"first.json"
            second = Path(td)/"second.json"
            self.assertEqual(main(args+["--output", str(first)]), 0)
            self.assertEqual(main(args+["--output", str(second)]), 0)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            data = json.loads(first.read_text())
            self.assertEqual(data["status"], "FINITE_LATTICE_NUMERICAL")
            self.assertIn("seeds", data["parameters"])

    def test_actual_module_entry_point_generates_json_and_refuses_invalid(self):
        arguments = [sys.executable, "-m", "research.yang_mills_su2.run_pilot",
                     "--extents", "2,2,2,2", "--beta", "0", "--seeds", "2,3",
                     "--warmup", "0", "--sweeps", "2", "--thin", "1",
                     "--epsilon", "0.1"]
        completed = subprocess.run(arguments, capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "FINITE_LATTICE_NUMERICAL")
        refused = subprocess.run(arguments[:-1] + ["-0.1"], capture_output=True,
                                 text=True, check=False)
        self.assertNotEqual(refused.returncode, 0)


if __name__ == "__main__":
    unittest.main()
