"""Behavioral checks for SU(2) unit-quaternion arithmetic."""
import math
import unittest

from research.yang_mills_su2.su2 import (
    axis_angle,
    dagger,
    mul,
    norm2,
    normalized,
    scalar_trace,
)


class SU2ArithmeticTests(unittest.TestCase):
    def assertQuaternionAlmostEqual(self, got, want):
        self.assertEqual(len(got), 4)
        for actual, expected in zip(got, want):
            self.assertAlmostEqual(actual, expected, places=12)

    def test_hamilton_products_and_inverses(self):
        q = (0.5, 0.5, 0.5, 0.5)
        identity = (1.0, 0.0, 0.0, 0.0)
        self.assertQuaternionAlmostEqual(mul(identity, q), q)
        self.assertQuaternionAlmostEqual(mul(q, dagger(q)), identity)
        self.assertQuaternionAlmostEqual(mul((0, 1, 0, 0), (0, 0, 1, 0)), (0, 0, 0, 1))

    def test_pauli_matrix_representation_matches_hamilton_multiplication(self):
        def matrix(q):
            a, b, c, d = q
            return ((a-1j*d, -c-1j*b), (c-1j*b, a+1j*d))

        def matmul(a, b):
            return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2))
                               for j in range(2)) for i in range(2))

        q = (0.5, 0.5, 0.5, 0.5)
        p = (0.5, -0.5, 0.5, -0.5)
        actual = matmul(matrix(q), matrix(p))
        expected = matrix(mul(q, p))
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(actual[i][j].real, expected[i][j].real, places=12)
                self.assertAlmostEqual(actual[i][j].imag, expected[i][j].imag, places=12)

    def test_quaternion_norm_and_trace(self):
        q = (2.0, -1.0, 2.0, 0.0)
        self.assertEqual(norm2(q), 9.0)
        self.assertEqual(scalar_trace(q), 4.0)
        self.assertQuaternionAlmostEqual(normalized(q), (2/3, -1/3, 2/3, 0))

    def test_axis_angle_is_unitary(self):
        q = axis_angle((0.0, 0.0, 3.0), math.pi / 2)
        self.assertQuaternionAlmostEqual(q, (0.0, 0.0, 0.0, 1.0))
        self.assertAlmostEqual(norm2(q), 1.0, places=12)

    def test_zero_nonfinite_and_invalid_shapes_rejected(self):
        for q in [(0, 0, 0, 0), (1, 2), (math.nan, 0, 0, 0), (math.inf, 0, 0, 0)]:
            with self.subTest(q=q), self.assertRaises(ValueError):
                normalized(q)
        for axis in [(0, 0, 0), (0, 1), (0, 0, math.nan)]:
            with self.subTest(axis=axis), self.assertRaises(ValueError):
                axis_angle(axis, 0.2)
        with self.assertRaises(ValueError):
            axis_angle((0, 0, 1), math.inf)


if __name__ == "__main__":
    unittest.main()
