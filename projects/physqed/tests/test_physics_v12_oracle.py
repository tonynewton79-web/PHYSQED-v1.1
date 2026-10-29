"""Independent stdlib-Fraction vs SymPy v1.2 reference comparisons."""
import sys
import unittest
from fractions import Fraction
from pathlib import Path
import sympy as S

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12 import Geometry, LieAlgebra, wick, first_order_phi4_two_point, poisson_bracket
from v12.oracle import (warped_surface_scalar,cross3,normal_even_moment,
                         phi4_two_point_first_order,polynomial_poisson_reference)


class IndependentTextbookOracle(unittest.TestCase):
    def test_warped_curvature_rational_point(self):
        x,y=S.symbols("x y")
        f=1+x*x
        geometry=Geometry((x,y),S.diag(1,f*f))
        independently=warped_surface_scalar(Fraction(5,4),Fraction(2))
        self.assertEqual(independently,Fraction(-16,5))
        self.assertEqual(S.simplify(geometry.scalar.subs(x,S.Rational(1,2))),
                         S.Rational(independently.numerator,independently.denominator))

    def test_so3_bracket_cross_product(self):
        v,w=(2,3,5),(7,-2,11)
        independent=cross3(v,w)
        got=LieAlgebra.so3().bracket(v,w)
        self.assertEqual([int(c) for c in got],list(independent))

    def test_wick_sixth_moment(self):
        variance=Fraction(3,5)
        ref=normal_even_moment(variance,6)
        self.assertEqual(ref,Fraction(81,25))
        got=wick([0]*6,S.Matrix([[S.Rational(3,5)]]))
        self.assertEqual(got,S.Rational(ref.numerator,ref.denominator))

    def test_first_order_phi_four_correction(self):
        variance=Fraction(2,3)
        ref=phi4_two_point_first_order(variance)
        self.assertEqual(ref,Fraction(-4,27))
        got=first_order_phi4_two_point(S.Matrix([[S.Rational(2,3)]]),0,0,[1])
        self.assertEqual(got,S.Rational(ref.numerator,ref.denominator))

    def test_quadratic_poisson_reference(self):
        q,p=S.symbols("q p")
        got=poisson_bracket(q*q*p,q*p*p,[q],[p]).subs({q:2,p:3})
        self.assertEqual(got,polynomial_poisson_reference(2,3))


if __name__=="__main__":
    unittest.main()
