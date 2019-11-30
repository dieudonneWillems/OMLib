import unittest

from omlib.constants import OM, SI, IMPERIAL
from omlib.dimension import Dimension
from omlib.measure import Measure, Point, om
from omlib.scale import Scale
from omlib.unit import Unit, UnitMultiplication, UnitDivision


class TestUnits(unittest.TestCase):

    def test_singular_unit_measure_conversion(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        inch = Unit.get_singular_unit('inch', '\'', base_unit=m, factor=2.54e-2, identifier=OM.NAMESPACE + 'inch')
        feet = Unit.get_singular_unit('feet', 'ft', base_unit=inch, factor=12, identifier=OM.NAMESPACE + 'feet')
        measure = Measure(1.75, m)
        measure.convert(feet)
        self.assertAlmostEqual(float(5.74147), float(measure.numericalValue), delta=0.0001)
        self.assertEqual(str(OM.NAMESPACE + 'feet'), str(measure.unit.identifier))

    def test_singular_unit_measure_conversion_by_creation(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        inch = Unit.get_singular_unit('inch', '\'', base_unit=m, factor=2.54e-2, identifier=OM.NAMESPACE + 'inch')
        feet = Unit.get_singular_unit('feet', 'ft', base_unit=inch, factor=12, identifier=OM.NAMESPACE + 'feet')
        measure = Measure(1.75, m)
        new_measure = Measure.create_by_converting(measure, feet)
        self.assertAlmostEqual(float(5.74147), float(new_measure.numericalValue), delta=0.0001)
        self.assertEqual(str(OM.NAMESPACE + 'feet'), str(new_measure.unit.identifier))

    def test_measure_conversion_1(self):
        l_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m_dim = Dimension(0, 0, 1, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', l_dim, identifier=OM.NAMESPACE + 'metre')
        inch = Unit.get_singular_unit('inch', '\'', base_unit=m, factor=2.54e-2, identifier=OM.NAMESPACE + 'inch')
        inch2 = Unit.get_unit_exponentiation(inch, 2)
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        g = Unit.get_singular_unit('gram', 'g', m_dim, identifier=OM.NAMESPACE + 'gram')
        kg = Unit.get_prefixed_unit(SI.KILO, g, OM.NAMESPACE + 'kilogram')
        lb = Unit.get_singular_unit("pound", "lb", base_unit=kg, factor=0.45359237)
        s2 = Unit.get_unit_exponentiation(s, 2)
        ms_2 = Unit.get_unit_division(m, s2)
        gn = Unit.get_singular_unit("gravity", "g", base_unit=ms_2, factor=9.80665)
        kg_ms_2 = Unit.get_unit_multiplication(kg, ms_2)
        n = Unit.get_singular_unit("Newton", "N", base_unit=kg_ms_2, identifier=OM.NAMESPACE + 'Newton')
        lbf = Unit.get_unit_multiplication(lb, gn, "lbf")
        m2 = Unit.get_unit_exponentiation(m, 2)
        n_m2 = Unit.get_unit_division(n, m2)
        pa = Unit.get_singular_unit("Pascal", "Pa", base_unit=n_m2, identifier=OM.NAMESPACE + 'Pascal')
        psi = Unit.get_unit_division(lbf, inch2, symbol="psi", identifier=OM.NAMESPACE + 'psi')
        measure = Measure(12.2, psi)
        self.assertAlmostEqual(12.2, measure.numericalValue, delta=0.1)
        self.assertEqual(str(OM.NAMESPACE + 'psi'), str(measure.unit.identifier))
        measure.convert(pa)
        self.assertAlmostEqual(84116, measure.numericalValue, delta=1)
        self.assertEqual(str(OM.NAMESPACE + 'Pascal'), str(measure.unit.identifier))

    def test_add_measures(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        cm = Unit.get_prefixed_unit(SI.CENTI, m, identifier=OM.NAMESPACE + 'centimetre')
        value_1 = Measure(2, m)
        value_2 = Measure(50, cm)
        result_value_1 = value_1 + value_2
        self.assertAlmostEqual(2.5, result_value_1.numericalValue, delta=0.01)
        self.assertEqual(str(OM.NAMESPACE + 'metre'), str(result_value_1.unit.identifier))
        result_value_2 = value_2 + value_1
        self.assertAlmostEqual(250, result_value_2.numericalValue, delta=0.01)
        self.assertEqual(str(OM.NAMESPACE + 'centimetre'), str(result_value_2.unit.identifier))

    def test_subtract_measures(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        cm = Unit.get_prefixed_unit(SI.CENTI, m, identifier=OM.NAMESPACE + 'centimetre')
        value_1 = Measure(2, m)
        value_2 = Measure(50, cm)
        result_value_1 = value_1 - value_2
        self.assertAlmostEqual(1.5, result_value_1.numericalValue, delta=0.01)
        self.assertEqual(str(OM.NAMESPACE + 'metre'), str(result_value_1.unit.identifier))
        result_value_2 = value_2 - value_1
        self.assertAlmostEqual(-150, result_value_2.numericalValue, delta=0.01)
        self.assertEqual(str(OM.NAMESPACE + 'centimetre'), str(result_value_2.unit.identifier))

    def test_multiply_measures(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        value_1 = Measure(2, m)
        value_2 = Measure(50, s)
        result_value_1 = value_1 * value_2
        self.assertAlmostEqual(100, result_value_1.numericalValue, delta=0.01)
        self.assertTrue(isinstance(result_value_1.unit, UnitMultiplication))
        self.assertEqual(str(OM.NAMESPACE + 'metre'), str(result_value_1.unit.multiplier.identifier))
        self.assertEqual(str(OM.NAMESPACE + 'second'), str(result_value_1.unit.multiplicand.identifier))
        result_value_2 = value_2 * value_1
        self.assertAlmostEqual(100, result_value_2.numericalValue, delta=0.01)
        self.assertTrue(isinstance(result_value_2.unit, UnitMultiplication))
        self.assertEqual(str(OM.NAMESPACE + 'metre'), str(result_value_2.unit.multiplicand.identifier))
        self.assertEqual(str(OM.NAMESPACE + 'second'), str(result_value_2.unit.multiplier.identifier))
        Unit.get_unit_multiplication(m, s, identifier=OM.NAMESPACE + 'metreSecond')
        self.assertEqual(str(OM.NAMESPACE + 'metreSecond'), str(result_value_1.unit.identifier))

    def test_divide_measures(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        value_1 = Measure(2, m)
        value_2 = Measure(50, s)
        result_value_1 = value_1 / value_2
        self.assertAlmostEqual(0.04, result_value_1.numericalValue, delta=0.01)
        self.assertTrue(isinstance(result_value_1.unit, UnitDivision))
        self.assertEqual(str(OM.NAMESPACE + 'metre'), str(result_value_1.unit.numerator.identifier))
        self.assertEqual(str(OM.NAMESPACE + 'second'), str(result_value_1.unit.denominator.identifier))
        result_value_2 = value_2 / value_1
        self.assertAlmostEqual(25, result_value_2.numericalValue, delta=0.01)
        self.assertTrue(isinstance(result_value_2.unit, UnitDivision))
        self.assertEqual(str(OM.NAMESPACE + 'second'), str(result_value_2.unit.numerator.identifier))
        self.assertEqual(str(OM.NAMESPACE + 'metre'), str(result_value_2.unit.denominator.identifier))
        Unit.get_unit_division(m, s, identifier=OM.NAMESPACE + 'metrePerSecond')
        self.assertEqual(str(OM.NAMESPACE + 'metrePerSecond'), str(result_value_1.unit.identifier))

    def test_equality_measures_equal(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        hm = Unit.get_prefixed_unit(SI.HECTO, m, identifier=OM.NAMESPACE + 'hectometre')
        value_1 = Measure(200, m)
        value_2 = Measure(2, hm)
        self.assertTrue(value_1 == value_2)
        self.assertFalse(value_1 != value_2)
        self.assertFalse(value_1 < value_2)
        self.assertFalse(value_1 > value_2)
        self.assertTrue(value_1 <= value_2)
        self.assertTrue(value_1 >= value_2)

    def test_equality_measures_greater_then(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        hm = Unit.get_prefixed_unit(SI.HECTO, m, identifier=OM.NAMESPACE + 'hectometre')
        value_1 = Measure(210, m)
        value_2 = Measure(2, hm)
        self.assertFalse(value_1 == value_2)
        self.assertTrue(value_1 != value_2)
        self.assertFalse(value_1 < value_2)
        self.assertTrue(value_1 > value_2)
        self.assertFalse(value_1 <= value_2)
        self.assertTrue(value_1 >= value_2)

    def test_equality_measures_smaller_then(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        hm = Unit.get_prefixed_unit(SI.HECTO, m, identifier=OM.NAMESPACE + 'hectometre')
        value_1 = Measure(190, m)
        value_2 = Measure(2, hm)
        self.assertFalse(value_1 == value_2)
        self.assertTrue(value_1 != value_2)
        self.assertTrue(value_1 < value_2)
        self.assertFalse(value_1 > value_2)
        self.assertTrue(value_1 <= value_2)
        self.assertFalse(value_1 >= value_2)

    def test_conversion_to_base_units(self):
        m = SI.METRE
        hm = Unit.get_prefixed_unit(SI.HECTO, m, identifier=OM.NAMESPACE + 'hectometre')
        s = SI.SECOND
        hour = Unit.get_singular_unit('hour', 'h', base_unit=s, factor=3600)
        m_s = Unit.get_unit_division(m, s)
        hm_hour = Unit.get_unit_division(hm, hour)
        measure = Measure(2.4, hm_hour)
        measure.convert_to_base_units()
        self.assertEqual(m_s, measure.unit)
        self.assertAlmostEqual(0.0667, measure.numericalValue, delta=0.0001)

    def test_conversion_to_convenient_unit_1(self):
        m = SI.METRE
        um = Unit.get_prefixed_unit(SI.MICRO, m)
        mm = Unit.get_prefixed_unit(SI.MILLI, m)
        Unit.get_prefixed_unit(SI.CENTI, m)
        Unit.get_prefixed_unit(SI.DECI, m)
        Unit.get_prefixed_unit(SI.DECA, m)
        Unit.get_prefixed_unit(SI.HECTO, m)
        km = Unit.get_prefixed_unit(SI.KILO, m)
        m1 = Measure(0.0043, m)
        m1.convert_to_convenient_units()
        self.assertEqual(mm, m1.unit)
        self.assertAlmostEqual(4.3, m1.numericalValue, delta=0.001)
        m2 = Measure(0.0000893, m)
        m2.convert_to_convenient_units()
        self.assertEqual(um, m2.unit)
        self.assertAlmostEqual(89.3, m2.numericalValue, delta=0.001)
        m5 = Measure(0.0002893, m)
        m5.convert_to_convenient_units()
        self.assertEqual(um, m5.unit)
        self.assertAlmostEqual(289.3, m5.numericalValue, delta=0.001)
        m3 = Measure(203324.2434, m)
        m3.convert_to_convenient_units()
        self.assertEqual(km, m3.unit)
        self.assertAlmostEqual(203.3242434, m3.numericalValue, delta=0.00000001)
        m4 = Measure(203324.2434, m)
        m4.convert_to_convenient_units(use_prefixes=False)
        self.assertEqual(m, m4.unit)
        self.assertAlmostEqual(203324.2434, m4.numericalValue, delta=0.00001)

    def test_conversion_to_convenient_unit_2(self):
        s2 = Unit.get_unit_exponentiation(SI.SECOND, 2)
        m1_s2 = Unit.get_unit_multiplication(SI.METRE, s2)
        kg_m1_s2 = Unit.get_unit_division(SI.KILOGRAM, m1_s2)
        Unit.get_singular_unit("Pascal", "Pa", base_unit=kg_m1_s2)
        m1 = Measure(12.343, kg_m1_s2)
        m1.convert_to_convenient_units()
        self.assertEqual(kg_m1_s2, m1.unit)  # Pa not in correct system of units
        self.assertAlmostEqual(12.343, m1.numericalValue, delta=0.00001)
        m2 = Measure(12.343, kg_m1_s2)
        m2.convert_to_convenient_units(system_of_units=SI.SYSTEM_OF_UNITS)
        self.assertEqual(kg_m1_s2, m2.unit)
        self.assertAlmostEqual(12.343, m2.numericalValue, delta=0.00001)
        pa2 = Unit.get_singular_unit("Pascal", "Pa", base_unit=kg_m1_s2, system_of_units=SI.SYSTEM_OF_UNITS)
        m3 = Measure(12.343, kg_m1_s2)
        m3.convert_to_convenient_units()
        self.assertEqual(pa2, m3.unit)
        self.assertAlmostEqual(12.343, m3.numericalValue, delta=0.00001)
        self.assertNotEqual(kg_m1_s2, m3.unit)

    def test_conversion_to_convenient_unit_3(self):
        m = SI.METRE
        Unit.get_prefixed_unit(SI.MICRO, m)
        Unit.get_prefixed_unit(SI.MILLI, m)
        Unit.get_prefixed_unit(SI.CENTI, m)
        Unit.get_prefixed_unit(SI.DECI, m)
        Unit.get_prefixed_unit(SI.DECA, m)
        Unit.get_prefixed_unit(SI.HECTO, m)
        Unit.get_prefixed_unit(SI.KILO, m)
        yd = IMPERIAL.YARD
        m2 = Measure(1, yd)
        m2.convert_to_convenient_units()
        self.assertEqual(yd, m2.unit)
        self.assertAlmostEqual(1, m2.numericalValue, delta=0.00001)
        m1 = Measure(0.95, m)
        m1.convert_to_convenient_units(use_prefixes=False)
        self.assertEqual(m, m1.unit)
        self.assertAlmostEqual(0.95, m1.numericalValue, delta=0.00001)

    def test_conversion_between_scales_1(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        c_unit = Unit.get_singular_unit("degree Celsius", "°C", base_unit=SI.KELVIN, factor=1.0)
        c = Scale.get_interval_scale(k, c_unit, -273.15, "Celsius scale")
        f_unit = Unit.get_singular_unit("degree Fahrenheit", "°F", base_unit=SI.KELVIN, factor=1.0/1.8)
        f = Scale.get_interval_scale(k, f_unit, -459.67, "Fahrenheit scale")
        p1 = Point(32, f)
        self.assertEqual(f, p1.scale)
        self.assertEqual(f_unit, p1.scale.unit)
        self.assertAlmostEqual(32.0, p1.numericalValue, delta=0.00001)
        p1.convert(c)
        self.assertEqual(c, p1.scale)
        self.assertEqual(c_unit, p1.scale.unit)
        self.assertAlmostEqual(0.0, p1.numericalValue, delta=0.00001)

    def test_conversion_between_scales_2(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        c_unit = Unit.get_singular_unit("degree Celsius", "°C", base_unit=SI.KELVIN, factor=1.0)
        c = Scale.get_interval_scale(k, c_unit, -273.15, "Celsius scale")
        f_unit = Unit.get_singular_unit("degree Fahrenheit", "°F", base_unit=SI.KELVIN, factor=1.0/1.8)
        f = Scale.get_interval_scale(k, f_unit, -459.67, "Fahrenheit scale")
        p1 = Point(100, f)
        self.assertEqual(f, p1.scale)
        self.assertEqual(f_unit, p1.scale.unit)
        self.assertAlmostEqual(100.0, p1.numericalValue, delta=0.00001)
        p1.convert(c)
        self.assertEqual(c, p1.scale)
        self.assertEqual(c_unit, p1.scale.unit)
        self.assertAlmostEqual(37.7777777778, p1.numericalValue, delta=0.00001)

    def test_conversion_between_scales_3(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        c_unit = Unit.get_singular_unit("degree Celsius", "°C", base_unit=SI.KELVIN, factor=1.0)
        c = Scale.get_interval_scale(k, c_unit, -273.15, "Celsius scale")
        f_unit = Unit.get_singular_unit("degree Fahrenheit", "°F", base_unit=SI.KELVIN, factor=1.0/1.8)
        f = Scale.get_interval_scale(k, f_unit, -459.67, "Fahrenheit scale")
        p1 = Point(100, c)
        self.assertEqual(c, p1.scale)
        self.assertEqual(c_unit, p1.scale.unit)
        self.assertAlmostEqual(100.0, p1.numericalValue, delta=0.00001)
        p1.convert(f)
        self.assertEqual(f, p1.scale)
        self.assertEqual(f_unit, p1.scale.unit)
        self.assertAlmostEqual(212, p1.numericalValue, delta=0.00001)

    def test_conversion_between_scales_4(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        c_unit = Unit.get_singular_unit("degree Celsius", "°C", base_unit=SI.KELVIN, factor=1.0)
        c = Scale.get_interval_scale(k, c_unit, -273.15, "Celsius scale")
        f_unit = Unit.get_singular_unit("degree Fahrenheit", "°F", base_unit=SI.KELVIN, factor=1.0/1.8)
        f = Scale.get_interval_scale(k, f_unit, -459.67, "Fahrenheit scale")
        p1 = Point(67, c)
        self.assertEqual(c, p1.scale)
        self.assertEqual(c_unit, p1.scale.unit)
        self.assertAlmostEqual(67.0, p1.numericalValue, delta=0.00001)
        p1.convert(f)
        self.assertEqual(f, p1.scale)
        self.assertEqual(f_unit, p1.scale.unit)
        self.assertAlmostEqual(152.6, p1.numericalValue, delta=0.00001)

    def test_point_comparison_1(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        p1 = Point(45.33, k)
        p2 = Point(65.23, k)
        self.assertFalse(p1 == p2)
        self.assertTrue(p1 != p2)
        self.assertTrue(p1 < p2)
        self.assertTrue(p1 <= p2)
        self.assertFalse(p1 > p2)
        self.assertFalse(p1 >= p2)

    def test_point_comparison_2(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        p1 = Point(145.33, k)
        p2 = Point(65.23, k)
        self.assertFalse(p1 == p2)
        self.assertTrue(p1 != p2)
        self.assertFalse(p1 < p2)
        self.assertFalse(p1 <= p2)
        self.assertTrue(p1 > p2)
        self.assertTrue(p1 >= p2)

    def test_point_comparison_3(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        p1 = Point(145.33, k)
        p2 = Point(145.33, k)
        self.assertTrue(p1 == p2)
        self.assertFalse(p1 != p2)
        self.assertFalse(p1 < p2)
        self.assertTrue(p1 <= p2)
        self.assertFalse(p1 > p2)
        self.assertTrue(p1 >= p2)

    def test_point_comparison_4(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        c_unit = Unit.get_singular_unit("degree Celsius", "°C", base_unit=SI.KELVIN, factor=1.0)
        c = Scale.get_interval_scale(k, c_unit, -273.15, "Celsius scale")
        f_unit = Unit.get_singular_unit("degree Fahrenheit", "°F", base_unit=SI.KELVIN, factor=1.0/1.8)
        f = Scale.get_interval_scale(k, f_unit, -459.67, "Fahrenheit scale")
        p1 = Point(-45.33, c)
        p2 = Point(45.33, f)
        self.assertFalse(p1 == p2)
        self.assertTrue(p1 != p2)
        self.assertTrue(p1 < p2)
        self.assertTrue(p1 <= p2)
        self.assertFalse(p1 > p2)
        self.assertFalse(p1 >= p2)

    def test_point_comparison_5(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        c_unit = Unit.get_singular_unit("degree Celsius", "°C", base_unit=SI.KELVIN, factor=1.0)
        c = Scale.get_interval_scale(k, c_unit, -273.15, "Celsius scale")
        f_unit = Unit.get_singular_unit("degree Fahrenheit", "°F", base_unit=SI.KELVIN, factor=1.0/1.8)
        f = Scale.get_interval_scale(k, f_unit, -459.67, "Fahrenheit scale")
        p1 = Point(23.22, c)
        p2 = Point(33.4, f)
        self.assertFalse(p1 == p2)
        self.assertTrue(p1 != p2)
        self.assertFalse(p1 < p2)
        self.assertFalse(p1 <= p2)
        self.assertTrue(p1 > p2)
        self.assertTrue(p1 >= p2)

    def test_point_comparison_6(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        c_unit = Unit.get_singular_unit("degree Celsius", "°C", base_unit=SI.KELVIN, factor=1.0)
        c = Scale.get_interval_scale(k, c_unit, -273.15, "Celsius scale")
        f_unit = Unit.get_singular_unit("degree Fahrenheit", "°F", base_unit=SI.KELVIN, factor=1.0/1.8)
        f = Scale.get_interval_scale(k, f_unit, -459.67, "Fahrenheit scale")
        p1 = Point(0.0, c)
        p2 = Point(32.0, f)
        self.assertAlmostEqual(0.0, (p1-p2).numericalValue, delta=0.00001)

    def test_om(self):
        m1 = om(13.2, SI.METRE)
        self.assertTrue(isinstance(m1, Measure))
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        m2 = om(321.33, k)
        self.assertTrue(isinstance(m2, Point))

    def test_addition_1(self):
        m1 = om(13.5, SI.METRE)
        m2 = om(32.1, SI.METRE)
        m3 = m1 + m2
        self.assertTrue(isinstance(m3, Measure))
        self.assertAlmostEqual(45.6, m3.numericalValue, delta=0.000001)

    def test_addition_2(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        m1 = om(13.5, k)
        m2 = om(32.1, SI.KELVIN)
        m3 = m1 + m2
        self.assertTrue(isinstance(m3, Point))
        self.assertAlmostEqual(45.6, m3.numericalValue, delta=0.000001)

    def test_addition_3(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        m1 = om(13.5, k)
        m2 = om(32.1, k)
        self.assertRaises(ValueError, lambda: m1 + m2)

    def test_addition_3(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        m1 = om(13.5, SI.KELVIN)
        m2 = om(32.1, k)
        self.assertRaises(ValueError, lambda: m1 + m2)

    def test_subtraction_1(self):
        m1 = om(43.5, SI.METRE)
        m2 = om(32.1, SI.METRE)
        m3 = m1 - m2
        self.assertTrue(isinstance(m3, Measure))
        self.assertAlmostEqual(11.4, m3.numericalValue, delta=0.000001)

    def test_subtraction_2(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        m1 = om(43.5, k)
        m2 = om(32.1, SI.KELVIN)
        m3 = m1 - m2
        self.assertTrue(isinstance(m3, Point))
        self.assertAlmostEqual(11.4, m3.numericalValue, delta=0.000001)
        self.assertTrue(k, m3.scale)

    def test_subtraction_3(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        m1 = om(43.5, k)
        m2 = om(32.1, k)
        m3 = m1 - m2
        self.assertTrue(isinstance(m3, Measure))
        self.assertAlmostEqual(11.4, m3.numericalValue, delta=0.000001)
        self.assertTrue(SI.KELVIN, m3.unit)

    def test_subtraction_4(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        m1 = om(43.5, SI.KELVIN)
        m2 = om(32.1, k)
        self.assertRaises(ValueError, lambda: m1 - m2)

    def test_multiplication_1(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        m1 = om(43.5, k)
        m2 = om(3.2, SI.METRE)
        m3 = m1 * m2
        self.assertTrue(isinstance(m3, Measure))
        self.assertAlmostEqual(139.2, m3.numericalValue, delta=0.000001)
        self.assertEqual("K.m", str(m3.unit.symbol()))

    def test_multiplication_2(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        m1 = om(43.5, SI.METRE)
        m2 = om(3.2, k)
        m3 = m1 * m2
        self.assertTrue(isinstance(m3, Measure))
        self.assertAlmostEqual(139.2, m3.numericalValue, delta=0.000001)
        self.assertEqual("m.K", str(m3.unit.symbol()))

    def test_division_1(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        m1 = om(43.5, k)
        m2 = om(3.2, SI.METRE)
        m3 = m1 / m2
        self.assertTrue(isinstance(m3, Measure))
        self.assertAlmostEqual(13.59375, m3.numericalValue, delta=0.00001)
        self.assertEqual("K/m", str(m3.unit.symbol()))

    def test_division_2(self):
        k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
        m1 = om(43.5, SI.METRE)
        m2 = om(3.2, k)
        m3 = m1 / m2
        self.assertTrue(isinstance(m3, Measure))
        self.assertAlmostEqual(13.59375, m3.numericalValue, delta=0.00001)
        self.assertEqual("m/K", str(m3.unit.symbol()))
