"""Separate two-jet Einstein curvature oracle: standard GR positive controls.

The oracle uses only fractions.Fraction and Gaussian elimination. SymPy
supplies the symbolic chart jets in this test, but does not perform the
oracle's curvature calculation. Comparison is componentwise, not fitted.
"""
import sys
import unittest
from fractions import Fraction
from pathlib import Path
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v12 import Geometry, ScopeError
from v12.jet_oracle import curvature_from_jet


def jets_at(coords, metric, at):
    g=S.Matrix(metric)
    n=len(coords)
    def f(expr):
        v=S.simplify(expr.subs(at))
        if v.free_symbols:
            raise ValueError("inexact test point")
        return str(v)
    return ([ [f(g[i,j]) for j in range(n)] for i in range(n)],
            [[[f(S.diff(g[i,j],coords[k])) for j in range(n)]
               for i in range(n)] for k in range(n)],
            [[[[f(S.diff(g[i,j],coords[k],coords[l]))
                 for j in range(n)] for i in range(n)]
                 for l in range(n)] for k in range(n)])


def as_sympy(frac):
    return S.Rational(frac.numerator,frac.denominator)


def check_geometry(test,geom,at,check_riemann=True):
    result=curvature_from_jet(*jets_at(geom.x,geom.g,at))
    n=geom.n
    for b in range(n):
        for d in range(n):
            test.assertEqual(as_sympy(result["ricci"][b][d]),
                             S.simplify(geom.ricci[b,d].subs(at)))
            test.assertEqual(as_sympy(result["einstein"][b][d]),
                             S.simplify(geom.einstein[b,d].subs(at)))
            for a in range(n):
                test.assertEqual(as_sympy(result["connection"][a][b][d]),
                                 S.simplify(geom.connection[a][b][d].subs(at)))
                if check_riemann:
                    for c in range(n):
                        test.assertEqual(
                            as_sympy(result["riemann"][a][b][c][d]),
                            S.simplify(geom.riemann[a][b][c][d].subs(at)))
    test.assertEqual(as_sympy(result["scalar"]),S.simplify(geom.scalar.subs(at)))
    return result


class ExactJetOracleTests(unittest.TestCase):
    def test_4d_minkowski(self):
        x=S.symbols("t x y z")
        geo=Geometry(x,S.diag(-1,1,1,1))
        got=check_geometry(self,geo,{i:S.Rational(j,3) for j,i in enumerate(x)})
        self.assertEqual(got["scalar"],Fraction(0))

    def test_nonconstant_warped_surface(self):
        x,y=S.symbols("x y")
        f=1+x*x
        geo=Geometry((x,y),S.diag(1,f*f))
        got=check_geometry(self,geo,{x:S.Rational(1,2),y:S.Rational(3,4)})
        self.assertEqual(got["scalar"],Fraction(-16,5))

    def test_curved_coordinates_flat_plane(self):
        x,y=S.symbols("x y")
        # Euclidean plane in nonlinear coordinates (u=x,v=y+x^2).
        geo=Geometry((x,y),[[1+4*x*x,2*x],[2*x,1]])
        got=check_geometry(self,geo,{x:Fraction(2,3),y:Fraction(1,5)})
        self.assertEqual(got["scalar"],0)
        self.assertEqual(got["connection"][1][0][0],2)

    def test_flrw_point_and_friedmann_sign(self):
        t,x,y,z=S.symbols("t x y z")
        a=1+t*t
        geo=Geometry((t,x,y,z),S.diag(-1,a*a,a*a,a*a))
        got=check_geometry(self,geo,{t:S.Rational(1,2),x:0,y:0,z:0})
        H=Fraction(1,1)/Fraction(5,4) # a'=1 at t=1/2
        self.assertEqual(got["einstein"][0][0],3*H*H)

    def test_schwarzschild_vacuum_and_tidal_curvature(self):
        t,r,theta,phi=S.symbols("t r theta phi",real=True)
        F=1-2/r  # M=1; r>2 domain of this chart
        geo=Geometry((t,r,theta,phi),
                     S.diag(-F,1/F,r*r,r*r*S.sin(theta)**2))
        # Exact comparison on this nonflat vacuum at r=4, theta=pi/2.
        at={t:0,r:4,theta:S.pi/2,phi:0}
        got=check_geometry(self,geo,at)
        self.assertEqual(got["scalar"],Fraction(0))
        self.assertTrue(all(v==0 for row in got["ricci"] for v in row))
        n=4
        R=got["riemann"];g=tuple(tuple(Fraction(s) for s in row)
                                 for row in jets_at(geo.x,geo.g,at)[0])
        # R_abcd=g_ae R^e_bcd, K=R_abcd R^abcd, diagonal metric at point.
        inv=got["inverse"]
        K=Fraction(0)
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for d in range(n):
                        # Diagonal metric: K = sum_a,b,c,d
                        # g_aa g^bb g^cc g^dd (R^a_bcd)^2.
                        K += (g[a][a]*inv[b][b]*inv[c][c]*inv[d][d] *
                              R[a][b][c][d]**2)
        self.assertEqual(K,Fraction(3,256))

    def test_jet_rejects_bad_metric(self):
        with self.assertRaises(ValueError):
            curvature_from_jet([[0,0],[0,0]],
                               [[[0,0],[0,0]]]*2,
                               [[[[0,0],[0,0]]]*2]*2)
        with self.assertRaises(ValueError):
            curvature_from_jet([[1.0]],[[[0]]],[[[[0]]]])


if __name__=="__main__":
    unittest.main()
