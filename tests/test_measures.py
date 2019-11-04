import unittest

from omlib.constants import OM, SI
from omlib.dimension import Dimension
from omlib.measure import Measure
from omlib.unit import Unit


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
