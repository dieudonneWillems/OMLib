import unittest

from omlib.dimension import Dimension
from omlib.exceptions.dimensionexception import DimensionalException


class TestDimensions(unittest.TestCase):

    def test__dimension_print(self):
        time_dim = Dimension(1, 2, -3, 0, -1, 0, 1)
        result_str = time_dim.__str__()
        self.assertEqual("(T=1, L=2, M=-3, I=0, θ=-1, N=0, J=1)", result_str)

    def test__dimension_equal(self):
        time_dim = Dimension(1, 2, -3, 0, -1, 0, 1)
        dim1 = Dimension(1, 0, 3, 0, 2, 1, 0)
        dim2 = Dimension(1, 0, 3, 0, 2, 1, 0)
        self.assertEqual(dim2, dim1)
        self.assertNotEqual(dim1, time_dim)
        self.assertNotEqual(dim2, time_dim)

    def test__dimension_addition(self):
        dim1 = Dimension(1, 0, 3, 0, 2, 1, 0)
        dim2 = Dimension(1, 0, 3, 0, 2, 1, 0)
        dim_add = Dimension(1, 0, 3, 0, 2, 1, 0)
        dim3 = Dimension(1, 2, -3, 0, -1, 0, 1)
        self.assertEqual(dim_add, dim1)
        self.assertEqual(dim_add, dim2)
        try:
            dim4 = dim3 + dim2
            self.fail("Dimensions should not be allowed to be added.")
        except DimensionalException as error:
            self.assertTrue(True)

    def test__dimension_subtraction(self):
        dim1 = Dimension(1, 0, 3, 0, 2, 1, 0)
        dim2 = Dimension(1, 0, 3, 0, 2, 1, 0)
        dim_sub = Dimension(1, 0, 3, 0, 2, 1, 0)
        dim3 = Dimension(1, 2, -3, 0, -1, 0, 1)
        self.assertEqual(dim_sub, dim1)
        self.assertEqual(dim_sub, dim2)
        try:
            dim4 = dim3 - dim2
            self.fail("Dimensions should not be allowed to be subtracted.")
        except DimensionalException as error:
            self.assertTrue(True)

    def test__dimension_multiplication(self):
        dim1 = Dimension(1, 2, 3, 0, 2, 1, -3)
        dim2 = Dimension(1, 0, 3, 0, 2, 1, 0)
        dim_mul = Dimension(2, 2, 6, 0, 4, 2, -3)
        dim4 = dim1 * dim2
        self.assertEqual(dim_mul, dim4)

    def test__dimension_division(self):
        dim1 = Dimension(1, 2, 3, 0, 2, 1, -3)
        dim2 = Dimension(1, 0, 3, 0, 2, 1, 1)
        dim_div = Dimension(0, 2, 0, 0, 0, 0, -4)
        dim4 = dim1 / dim2
        self.assertEqual(dim_div, dim4)
