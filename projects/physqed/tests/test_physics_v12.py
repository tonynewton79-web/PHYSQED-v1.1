"""Standard textbook physics benchmarks and adversarial refusals.

No test begins with a bespoke research paper. All claims are scoped.
"""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import sympy as S
from v12 import *
from sympy.physics.matrices import msigma


def all_zero(items):
    if isinstance(items,(S.MatrixBase,S.NDimArray)):
        return all(zero(x) for x in items)
    if isinstance(items,(list,tuple)):
        return all(all_zero(x) for x in items)
    return zero(items)


class GeometryBenchmarks(unittest.TestCase):
    def test_minkowski_flat_and_bianchi(self):
        t,x,y,z=S.symbols("t x y z",real=True)
        g=Geometry((t,x,y,z),S.diag(-1,1,1,1))
        self.assertTrue(all_zero(g.riemann))
        self.assertTrue(all_zero(g.einstein))
        self.assertTrue(all_zero(g.contracted_bianchi_residual()))
        self.assertTrue(all_zero(g.first_bianchi_residual()))

    def test_sphere_curvature_and_independent_ricci(self):
        r,theta,phi=S.symbols("r theta phi",positive=True)
        g=Geometry((theta,phi),S.diag(r**2,r**2*S.sin(theta)**2))
        self.assertTrue(zero(g.scalar-2/r**2))
        self.assertTrue(all_zero(g.einstein))
        self.assertTrue(all_zero(g.contracted_bianchi_residual()))
        # Independent Ricci reconstruction directly from connection.
        C=g.connection
        for j,k in ((0,0),(1,1)):
            independent=S.simplify(sum(
                S.diff(C[i][j][k],g.x[i]) -
                S.diff(C[i][i][j],g.x[k]) +
                sum(C[i][i][a]*C[a][j][k] -
                    C[i][k][a]*C[a][i][j] for a in range(2))
                for i in range(2)))
            self.assertTrue(zero(independent-g.ricci[j,k]))

    def test_flrw_friedmann_components(self):
        t,x,y,z=S.symbols("t x y z")
        a=S.Function("a")(t)
        g=Geometry((t,x,y,z),S.diag(-1,a**2,a**2,a**2))
        H=S.diff(a,t)/a
        self.assertTrue(zero(g.einstein[0,0]-3*H**2))
        self.assertTrue(zero(g.einstein[1,1]+a**2*(
            2*S.diff(a,t,2)/a+H**2)))

    def test_metric_compatibility(self):
        theta,phi=S.symbols("theta phi")
        g=Geometry((theta,phi),S.diag(1,S.sin(theta)**2))
        for k in range(2):
            self.assertTrue(all_zero(g.covariant_derivative(
                S.MutableDenseNDimArray(g.g), "dd", k)))

    def test_tetrad_and_zero_torsion(self):
        t,x=S.symbols("t x")
        E=S.eye(2)
        self.assertEqual(tetrad_metric(E,S.diag(-1,1)),S.diag(-1,1))
        self.assertTrue(all_zero(cartan_torsion(
            E,[S.zeros(2),S.zeros(2)],(t,x))))

    def test_reject_nonsymmetric_and_degenerate(self):
        x,y=S.symbols("x y")
        with self.assertRaises(ScopeError):
            Geometry((x,y),[[1,1],[0,1]])
        with self.assertRaises(ScopeError):
            Geometry((x,y),S.diag(1,0))


class GaugeBenchmarks(unittest.TestCase):
    def test_u1_and_so3_jacobi(self):
        self.assertTrue(LieAlgebra.u1().check_jacobi())
        self.assertTrue(LieAlgebra.so3().check_jacobi())
        self.assertTrue(LieAlgebra.lorentz().check_jacobi())

    def test_invalid_structure_refused(self):
        f=S.MutableDenseNDimArray.zeros(3,3,3)
        f[0,1,2]=1
        with self.assertRaises(ScopeError):
            LieAlgebra(f)

    def test_so3_bracket(self):
        L=LieAlgebra.so3()
        self.assertEqual(L.bracket([1,0,0],[0,1,0]),S.Matrix([0,0,1]))

    def test_maxwell_field_and_equations(self):
        t,x=S.symbols("t x")
        E=S.Symbol("E",real=True)
        A=GaugeField(LieAlgebra.u1(),(t,x),[[0],[E*t]])
        self.assertEqual(A.field[0][1],S.Matrix([E]))
        self.assertTrue(all_zero(A.bianchi_residual()))
        self.assertTrue(all_zero(A.yang_mills_residual(S.diag(-1,1))))

    def test_nonabelian_curvature_and_bianchi(self):
        t,x,y=S.symbols("t x y")
        u,v=S.symbols("u v")
        A=GaugeField(LieAlgebra.so3(),(t,x,y),
                     [[0,0,0],[u,0,0],[0,v,0]])
        self.assertEqual(A.field[1][2],S.Matrix([0,0,u*v]))
        self.assertTrue(all_zero(A.bianchi_residual()))

    def test_matrix_gauge_transform(self):
        t,x=S.symbols("t x")
        U=S.diag(S.exp(t),S.exp(-t))
        A=[S.zeros(2),S.zeros(2)]
        self.assertTrue(all_zero(transformation_residual((t,x),A,U)))
        self.assertTrue(all_zero(matrix_curvature(
            (t,x),transformed_connection((t,x),A,U))))

    def test_representation_commutator(self):
        L=LieAlgebra.so3()
        T=[S.Matrix(3,3,lambda row,col:L.f[i,col,row]) for i in range(3)]
        self.assertTrue(L.representation_valid(T))
        T[0]=-T[0]
        self.assertFalse(L.representation_valid(T))


class QuantumBenchmarks(unittest.TestCase):
    def test_pauli_commutator(self):
        x,y,z=msigma(1),msigma(2),msigma(3)
        self.assertTrue(all_zero(commutator(x,y)-2*S.I*z))
        self.assertTrue(all_zero(anticommutator(x,y)))

    def test_clifford_euclidean_2d(self):
        x,y=msigma(1),msigma(2)
        self.assertTrue(all_zero(clifford_residual([x,y],S.eye(2))))

    def test_robertson_saturated(self):
        x,y=msigma(1),msigma(2)
        rho=S.diag(1,0)
        self.assertTrue(zero(robertson_residual(x,y,rho)))

    def test_density_rejection(self):
        with self.assertRaises(ScopeError):
            quantum_expectation(S.eye(2),S.diag(2,-1))

    def test_finite_ccr_trace_obstruction(self):
        self.assertEqual(finite_ccr_obstruction(S.eye(2),S.zeros(2)),-2*S.I)

    def test_canonical_poisson_and_jacobi(self):
        q,p=S.symbols("q p")
        self.assertEqual(poisson_bracket(q,p,[q],[p]),1)
        self.assertTrue(zero(poisson_jacobi_residual(
            q**2,p**2,q*p,[q],[p])))

    def test_first_class_constraints(self):
        q1,q2,p1,p2=S.symbols("q1 q2 p1 p2")
        coefficients=[[[0,0] for _ in range(2)] for _ in range(2)]
        self.assertTrue(all_zero(constraint_closure(
            [p1,p2],coefficients,[q1,q2],[p1,p2])))

    def test_adm_scalar_density(self):
        self.assertEqual(adm_scalar_constraint(S.eye(3),
                         S.diag(1,0,0),0),S.Rational(1,2))


class FieldBenchmarks(unittest.TestCase):
    def test_harmonic_oscillator_equation(self):
        t=S.symbols("t")
        w=S.symbols("w")
        f=S.Function("f")(t)
        L=(S.diff(f,t)**2-w**2*f**2)/2
        self.assertTrue(zero(euler_lagrange(L,[f],[t])[0]+
                             S.diff(f,t,2)+w**2*f))
        self.assertTrue(all_zero(translation_noether_residual(
            L,[f],[t])))

    def test_klein_gordon_equation(self):
        t,x,m=S.symbols("t x m")
        f=S.Function("f")(t,x)
        L=(S.diff(f,t)**2-S.diff(f,x)**2-m**2*f**2)/2
        self.assertTrue(zero(euler_lagrange(L,[f],[t,x])[0]+
            S.diff(f,t,2)-S.diff(f,x,2)+m**2*f))
        self.assertTrue(all_zero(translation_noether_residual(
            L,[f],[t,x])))

    def test_noether_two_real_scalar_rotation(self):
        t=S.symbols("t")
        f,g=S.Function("f")(t),S.Function("g")(t)
        L=(S.diff(f,t)**2+S.diff(g,t)**2-f**2-g**2)/2
        j=noether_current(L,[f,g],[-g,f],[t])[0]
        el=euler_lagrange(L,[f,g],[t])
        self.assertTrue(zero(S.diff(j,t)+el[0]*(-g)+el[1]*f))

    def test_gaussian_wick_and_propagator(self):
        C=quadratic_propagator([[2]])
        self.assertEqual(C,S.Matrix([[S.Rational(1,2)]]))
        self.assertEqual(wick([0,0,0,0],C),S.Rational(3,4))
        self.assertEqual(wick([0,0,0],C),0)
        self.assertEqual(first_order_phi4_two_point(C,0,0,[1]),
                         -S.Rational(1,16))

    def test_unsupported_singular_propagator(self):
        with self.assertRaises(ScopeError):
            quadratic_propagator([[0]])


class ReceiptBenchmarks(unittest.TestCase):
    def test_exact_verified_and_serializable(self):
        x=S.symbols("x")
        r=certify("STD-POLY-001","quantum",[(x**2-1,(x-1)*(x+1))],
                  ("commuting real scalar",),source="textbook algebra")
        self.assertIn("PASSED",r["status"])
        self.assertFalse(r["physical_law_proven"])
        self.assertFalse(r["lean_kernel_verified"])
        self.assertTrue(len(r["certificate_sha256"])==64)
        json.dumps(r)

    def test_wrong_sign_counterexample_and_refusal(self):
        x=S.symbols("x")
        r=certify("STD-NEG-001","field",[(x**2,-x**2)],
                  source="intentional error control")
        self.assertEqual(r["status"],"REJECTED")
        self.assertIsNotNone(r["checks"][0]["counterexample"])

    def test_domain_refusal(self):
        with self.assertRaises(ScopeError):
            certify("bad","unrestricted_qft",[(1,1)],source="test")


if __name__ == "__main__":
    unittest.main()
