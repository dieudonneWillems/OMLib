import unittest

from omlib.constants import SI
from omlib.exceptions.unitidentityexception import ScaleIdentityException
from omlib.scale import Scale
from omlib.unit import Unit


class TestScales(unittest.TestCase):

    def test__scale_eq_1(self):
        scale1 = Scale.get_ratio_scale(SI.METRE, "metre-scale", "http://example.org/metre-scale")
        scale2 = Scale.get_ratio_scale(SI.KILOGRAM, "kilogram-scale", "http://example.org/kilogram-scale")
        self.assertNotEqual(scale1, scale2)
        self.assertEqual(SI.METRE, scale1.unit)
        self.assertEqual("http://example.org/metre-scale", str(scale1.identifier))
        self.assertEqual("metre-scale", str(scale1.label()))
        self.assertEqual(SI.KILOGRAM, scale2.unit)
        self.assertEqual("http://example.org/kilogram-scale", str(scale2.identifier))
        self.assertEqual("kilogram-scale", str(scale2.label()))

    def test__scale_eq_2(self):
        scale1 = Scale.get_ratio_scale(SI.METRE, "metre-scale", "http://example.org/metre-scale")
        scale2 = Scale.get_ratio_scale(SI.METRE, "metre-scale", "http://example.org/metre-scale")
        self.assertEqual(scale1, scale2)
        self.assertEqual(SI.METRE, scale1.unit)
        self.assertEqual("http://example.org/metre-scale", str(scale1.identifier))
        self.assertEqual("metre-scale", str(scale1.label()))
        self.assertEqual(SI.METRE, scale2.unit)
        self.assertEqual("http://example.org/metre-scale", str(scale2.identifier))
        self.assertEqual("metre-scale", str(scale2.label()))

    def test__scale_eq_2a(self):
        scale1 = Scale.get_ratio_scale(SI.METRE, "metre-scale", "http://example.org/metre-scale")
        scale2 = Scale.get_ratio_scale(SI.METRE, "metre-scale", "http://example.org/metre-scale-2")
        self.assertNotEqual(scale1, scale2)
        self.assertEqual(SI.METRE, scale1.unit)
        self.assertEqual("http://example.org/metre-scale", str(scale1.identifier))
        self.assertEqual("metre-scale", str(scale1.label()))
        self.assertEqual(SI.METRE, scale2.unit)
        self.assertEqual("http://example.org/metre-scale-2", str(scale2.identifier))
        self.assertEqual("metre-scale", str(scale2.label()))

    def test__scale_eq_3(self):
        scale1 = Scale.get_ratio_scale(SI.METRE, "metre-scale", "http://example.org/metre-scale")
        scale2 = Scale.get_ratio_scale(SI.METRE, "metre-scale")
        self.assertEqual(scale1, scale2)
        self.assertEqual(SI.METRE, scale1.unit)
        self.assertEqual("http://example.org/metre-scale", str(scale1.identifier))
        self.assertEqual("metre-scale", str(scale1.label()))
        self.assertEqual(SI.METRE, scale2.unit)
        self.assertEqual("http://example.org/metre-scale", str(scale2.identifier))
        self.assertEqual("metre-scale", str(scale2.label()))

    def test__scale_eq_4(self):
        scale1 = Scale.get_ratio_scale(SI.METRE, "metre-scale")
        scale2 = Scale.get_ratio_scale(SI.METRE, "metre-scale", "http://example.org/metre-scale")
        self.assertEqual(scale1, scale2)
        self.assertEqual(SI.METRE, scale1.unit)
        self.assertEqual("http://example.org/metre-scale", str(scale1.identifier))
        self.assertEqual("metre-scale", str(scale1.label()))
        self.assertEqual(SI.METRE, scale2.unit)
        self.assertEqual("http://example.org/metre-scale", str(scale2.identifier))
        self.assertEqual("metre-scale", str(scale2.label()))

    def test__scale_eq_5(self):
        scale1 = Scale.get_ratio_scale(SI.METRE, "metre-scale", "http://example.org/metre-scale")
        scale2 = Scale.get_interval_scale(scale1, SI.METRE, off_set=0.0, label="metre-scale",
                                          identifier="http://example.org/metre-scale")
        self.assertNotEqual(scale1, scale2)
        self.assertNotEqual(scale2, scale1)
        self.assertEqual(SI.METRE, scale1.unit)
        self.assertEqual("http://example.org/metre-scale", str(scale1.identifier))
        self.assertEqual("metre-scale", str(scale1.label()))
        self.assertEqual(SI.METRE, scale2.unit)
        self.assertEqual("http://example.org/metre-scale", str(scale2.identifier))
        self.assertEqual("metre-scale", str(scale2.label()))

    def test__scale_eq_6(self):
        scale = Scale.get_ratio_scale(SI.METRE, "metre-scale", "http://example.org/metre-scale-base")
        try:
            scale1 = Scale.get_interval_scale(scale, SI.METRE, off_set=0.0, label="metre-scale",
                                              identifier="http://example.org/metre-scale-eq6")
            Scale.get_interval_scale(scale1, SI.METRE, off_set=0.0, label="metre-scale",
                                              identifier="http://example.org/metre-scale-eq6")
            self.fail("Singular units that do not have a common base should not be converted between each other")
        except ScaleIdentityException as error:
            self.assertTrue(True)

    def test__scale_eq_7(self):
        scale = Scale.get_ratio_scale(SI.METRE, "metre-scale", "http://example.org/metre-scale-base")
        scale1 = Scale.get_interval_scale(scale, SI.METRE, off_set=1.0, label="metre-scale",
                                          identifier="http://example.org/metre-scale-eq7")
        scale2 = Scale.get_interval_scale(scale, SI.METRE, off_set=1.0, label="metre-scale",
                                          identifier="http://example.org/metre-scale-eq7")
        self.assertEqual(scale1, scale2)
        self.assertEqual(scale2, scale1)
        self.assertEqual(SI.METRE, scale1.unit)
        self.assertEqual("http://example.org/metre-scale-eq7", str(scale1.identifier))
        self.assertEqual("metre-scale", str(scale1.label()))
        self.assertEqual(SI.METRE, scale2.unit)
        self.assertEqual("http://example.org/metre-scale-eq7", str(scale2.identifier))
        self.assertEqual("metre-scale", str(scale2.label()))

    def test__scale_eq_8(self):
        scale = Scale.get_ratio_scale(SI.METRE, "metre-scale", "http://example.org/metre-scale-base")
        scale1 = Scale.get_interval_scale(scale, SI.METRE, off_set=1.0, label="metre-scale",
                                          identifier="http://example.org/metre-scale-eq8")
        scale2 = Scale.get_interval_scale(scale, SI.METRE, off_set=2.0, label="metre-scale",
                                          identifier="http://example.org/metre-scale-eq8-2")
        self.assertNotEqual(scale1, scale2)
        self.assertNotEqual(scale2, scale1)
        self.assertEqual(SI.METRE, scale1.unit)
        self.assertEqual("http://example.org/metre-scale-eq8", str(scale1.identifier))
        self.assertEqual("metre-scale", str(scale1.label()))
        self.assertAlmostEqual(1.0, scale1.offSet, delta=0.00001)
        self.assertEqual(SI.METRE, scale2.unit)
        self.assertEqual("http://example.org/metre-scale-eq8-2", str(scale2.identifier))
        self.assertEqual("metre-scale", str(scale2.label()))
        self.assertAlmostEqual(2.0, scale2.offSet, delta=0.00001)

    def test_scale_conversion_1(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        c_unit = Unit.get_singular_unit("degree Celsius", "°C", base_unit=SI.KELVIN, factor=1.0)
        c = Scale.get_interval_scale(k, c_unit, -273.15, "Celsius scale")
        self.assertNotEqual(k, c)
        conversion_factor = Scale.conversion_factor(c, k)
        conversion_off_set = Scale.conversion_off_set(c, k)
        self.assertAlmostEqual(1.0, conversion_factor, delta=0.00001)
        self.assertAlmostEqual(273.15, conversion_off_set, delta=0.00001)

    def test_scale_conversion_2(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        f_unit = Unit.get_singular_unit("degree Fahrenheit", "°F", base_unit=SI.KELVIN, factor=1.0/1.8)
        f = Scale.get_interval_scale(k, f_unit, -459.67, "Fahrenheit scale")
        self.assertNotEqual(k, f)
        conversion_factor = Scale.conversion_factor(f, k)
        conversion_off_set = Scale.conversion_off_set(f, k)
        self.assertAlmostEqual(1.0/1.8, conversion_factor, delta=0.00001)
        self.assertAlmostEqual(255.37222222, conversion_off_set, delta=0.00001)

    def test_scale_conversion_3(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        c_unit = Unit.get_singular_unit("degree Celsius", "°C", base_unit=SI.KELVIN, factor=1.0)
        c = Scale.get_interval_scale(k, c_unit, -273.15, "Celsius scale")
        f_unit = Unit.get_singular_unit("degree Fahrenheit", "°F", base_unit=SI.KELVIN, factor=1.0/1.8)
        f = Scale.get_interval_scale(k, f_unit, -459.67, "Fahrenheit scale")
        self.assertNotEqual(k, f)
        conversion_factor = Scale.conversion_factor(f, c)
        conversion_off_set = Scale.conversion_off_set(f, c)
        self.assertAlmostEqual(1.0/1.8, conversion_factor, delta=0.00001)
        self.assertAlmostEqual(-17.77777777, conversion_off_set, delta=0.00001)

    def test_scale_conversion_4(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        c_unit = Unit.get_singular_unit("degree Celsius", "°C", base_unit=SI.KELVIN, factor=1.0)
        c = Scale.get_interval_scale(k, c_unit, -273.15, "Celsius scale")
        f_unit = Unit.get_singular_unit("degree Fahrenheit", "°F", base_unit=SI.KELVIN, factor=1.0/1.8)
        f = Scale.get_interval_scale(k, f_unit, -459.67, "Fahrenheit scale")
        self.assertNotEqual(k, f)
        conversion_factor = Scale.conversion_factor(c, f)
        conversion_off_set = Scale.conversion_off_set(c, f)
        self.assertAlmostEqual(1.8, conversion_factor, delta=0.00001)
        self.assertAlmostEqual(32.0, conversion_off_set, delta=0.00001)

    def test_scale_conversion_5(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        c_unit = Unit.get_singular_unit("degree Celsius", "°C", base_unit=SI.KELVIN, factor=1.0)
        c10_unit = Unit.get_singular_unit("10 degree Celsius", "°C", base_unit=SI.KELVIN, factor=10.0)
        c = Scale.get_interval_scale(k, c_unit, -273.15, "Celsius scale")
        c10 = Scale.get_interval_scale(c, c10_unit, -10.0, "10 Celsius scale")
        f_unit = Unit.get_singular_unit("degree Fahrenheit", "°F", base_unit=SI.KELVIN, factor=1.0/1.8)
        f = Scale.get_interval_scale(k, f_unit, -459.67, "Fahrenheit scale")
        conversion_factor = Scale.conversion_factor(c, c10)
        conversion_off_set = Scale.conversion_off_set(c, c10)
        self.assertAlmostEqual(0.1, conversion_factor, delta=0.00001)
        self.assertAlmostEqual(-10.0, conversion_off_set, delta=0.00001)
        conversion_factor = Scale.conversion_factor(c10, f)
        conversion_off_set = Scale.conversion_off_set(c10, f)
        self.assertAlmostEqual(18, conversion_factor, delta=0.00001)
        self.assertAlmostEqual(212.0, conversion_off_set, delta=0.00001)
