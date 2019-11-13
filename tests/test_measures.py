import unittest

from omlib.constants import OM, SI
from omlib.dimension import Dimension
from omlib.measure import Measure
from omlib.unit import Unit, UnitMultiplication, UnitDivision


class TestUnits(unittest.TestCase):

    def test_singular_unit_measure_conversion(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        inch = Unit.get_singular_unit('inch', '\'', base_unit=m, factor=2.54e-2, identifier=OM.NAMESPACE + 'inch')
        feet = Unit.get_singular_unit('feet', 'ft', base_unit=inch, factor=12, identifier=OM.NAMESPACE + 'feet')
        measure = Measure(1.75, m)
        measure.convert(feet)
        self.assertAlmostEqual(float(5.74147), float(measure.numerical_value), delta=0.0001)
        self.assertEqual(str(OM.NAMESPACE + 'feet'), str(measure.unit.identifier))

    def test_singular_unit_measure_conversion_by_creation(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        inch = Unit.get_singular_unit('inch', '\'', base_unit=m, factor=2.54e-2, identifier=OM.NAMESPACE + 'inch')
        feet = Unit.get_singular_unit('feet', 'ft', base_unit=inch, factor=12, identifier=OM.NAMESPACE + 'feet')
        measure = Measure(1.75, m)
        new_measure = Measure.create_by_converting(measure, feet)
        self.assertAlmostEqual(float(5.74147), float(new_measure.numerical_value), delta=0.0001)
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
        self.assertAlmostEqual(12.2, measure.numerical_value, delta=0.1)
        self.assertEqual(str(OM.NAMESPACE + 'psi'), str(measure.unit.identifier))
        measure.convert(pa)
        self.assertAlmostEqual(84116, measure.numerical_value, delta=1)
        self.assertEqual(str(OM.NAMESPACE + 'Pascal'), str(measure.unit.identifier))

    def test_add_measures(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        cm = Unit.get_prefixed_unit(SI.CENTI, m, identifier=OM.NAMESPACE + 'centimetre')
        value_1 = Measure(2, m)
        value_2 = Measure(50, cm)
        result_value_1 = value_1 + value_2
        self.assertAlmostEqual(2.5, result_value_1.numerical_value, delta=0.01)
        self.assertEqual(str(OM.NAMESPACE + 'metre'), str(result_value_1.unit.identifier))
        result_value_2 = value_2 + value_1
        self.assertAlmostEqual(250, result_value_2.numerical_value, delta=0.01)
        self.assertEqual(str(OM.NAMESPACE + 'centimetre'), str(result_value_2.unit.identifier))

    def test_subtract_measures(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        cm = Unit.get_prefixed_unit(SI.CENTI, m, identifier=OM.NAMESPACE + 'centimetre')
        value_1 = Measure(2, m)
        value_2 = Measure(50, cm)
        result_value_1 = value_1 - value_2
        self.assertAlmostEqual(1.5, result_value_1.numerical_value, delta=0.01)
        self.assertEqual(str(OM.NAMESPACE + 'metre'), str(result_value_1.unit.identifier))
        result_value_2 = value_2 - value_1
        self.assertAlmostEqual(-150, result_value_2.numerical_value, delta=0.01)
        self.assertEqual(str(OM.NAMESPACE + 'centimetre'), str(result_value_2.unit.identifier))

    def test_multiply_measures(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        value_1 = Measure(2, m)
        value_2 = Measure(50, s)
        result_value_1 = value_1 * value_2
        self.assertAlmostEqual(100, result_value_1.numerical_value, delta=0.01)
        self.assertTrue(isinstance(result_value_1.unit, UnitMultiplication))
        self.assertEqual(str(OM.NAMESPACE + 'metre'), str(result_value_1.unit.multiplier.identifier))
        self.assertEqual(str(OM.NAMESPACE + 'second'), str(result_value_1.unit.multiplicand.identifier))
        result_value_2 = value_2 * value_1
        self.assertAlmostEqual(100, result_value_2.numerical_value, delta=0.01)
        self.assertTrue(isinstance(result_value_2.unit, UnitMultiplication))
        self.assertEqual(str(OM.NAMESPACE + 'metre'), str(result_value_2.unit.multiplicand.identifier))
        self.assertEqual(str(OM.NAMESPACE + 'second'), str(result_value_2.unit.multiplier.identifier))
        m_s = Unit.get_unit_multiplication(m, s, identifier=OM.NAMESPACE + 'metreSecond')
        self.assertEqual(str(OM.NAMESPACE + 'metreSecond'), str(result_value_1.unit.identifier))

    def test_divide_measures(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        value_1 = Measure(2, m)
        value_2 = Measure(50, s)
        result_value_1 = value_1 / value_2
        self.assertAlmostEqual(0.04, result_value_1.numerical_value, delta=0.01)
        self.assertTrue(isinstance(result_value_1.unit, UnitDivision))
        self.assertEqual(str(OM.NAMESPACE + 'metre'), str(result_value_1.unit.numerator.identifier))
        self.assertEqual(str(OM.NAMESPACE + 'second'), str(result_value_1.unit.denominator.identifier))
        result_value_2 = value_2 / value_1
        self.assertAlmostEqual(25, result_value_2.numerical_value, delta=0.01)
        self.assertTrue(isinstance(result_value_2.unit, UnitDivision))
        self.assertEqual(str(OM.NAMESPACE + 'second'), str(result_value_2.unit.numerator.identifier))
        self.assertEqual(str(OM.NAMESPACE + 'metre'), str(result_value_2.unit.denominator.identifier))
        m_s = Unit.get_unit_division(m, s, identifier=OM.NAMESPACE + 'metrePerSecond')
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
        measure = Measure(2.4,hm_hour)
        measure.convert_to_base_units()
        self.assertEqual(m_s, measure.unit)
        self.assertAlmostEqual(0.0667, measure.numerical_value, delta=0.0001)

