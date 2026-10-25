import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from audit_conservation import independent_symbolic_replay, numerical_replay, trajectory, energy


class ConservationTests(unittest.TestCase):
    def test_symbolic_ode_derivative(self):
        self.assertTrue(independent_symbolic_replay()['passed'])

    def test_undamped_closed_form(self):
        m,k=2.,8.
        first=energy(m,k,*trajectory(0,m,k,0.))
        self.assertAlmostEqual(first,energy(m,k,*trajectory(1.7,m,k,0.)),places=12)

    def test_damped_closed_form(self):
        m,k,c=2.,8.,1.
        e0=energy(m,k,*trajectory(0,m,k,c))
        e1=energy(m,k,*trajectory(3,m,k,c))
        self.assertLess(e1,e0)

    def test_wrong_damped_conservation_is_false(self):
        m,k,c=2.,8.,1.
        e0=energy(m,k,*trajectory(0,m,k,c))
        e1=energy(m,k,*trajectory(3,m,k,c))
        self.assertGreater(e0-e1,0.1)

    def test_strict_damping_at_nonzero_speed(self):
        m,k,c=2.,8.,1.
        _,v=trajectory(0,m,k,c)
        self.assertLess(-c*v*v,0)

    def test_all_numerical_controls(self):
        self.assertTrue(numerical_replay()['undamped_constant'])

    def test_lean_source_bans_admitted_proofs(self):
        txt=(HERE/'lean'/'Conservation.lean').read_text()
        for ln in txt.splitlines():
            stripped=ln.strip()
            if stripped.startswith(('--','/-','*','This','BEFORE')):continue
            self.assertNotRegex(ln,r'\bsorry\b|\badmit\b|^\s*axiom\b')
        self.assertIn('HasDerivAt',txt)
        self.assertIn('is_const_of_deriv_eq_zero',txt)

if __name__=='__main__': unittest.main()
