import unittest

from omlib.constants import OM, SI
from omlib.dimension import Dimension
from omlib.unit import SingularUnit, PrefixedUnit, UnitMultiple, UnitDivision, UnitMultiplication, UnitExponentiation, \
    Unit


class TestUnits(unittest.TestCase):

    def test__singular_unit(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = SingularUnit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        self.assertEqual('metre', m.label().value)
        self.assertEqual('m', m.symbol().value)
        self.assertEqual('http://www.ontology-of-units-of-measure.org/resource/om-2/metre', str(m.identifier))
        self.assertEqual(m_dim, m.dimensions)

    def test__prefixed_unit(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = SingularUnit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        km = PrefixedUnit(SI.KILO, m, OM.NAMESPACE + 'kilometre')
        self.assertEqual('kilometre', km.label().value)
        self.assertEqual('km', km.symbol().value)
        self.assertEqual('http://www.ontology-of-units-of-measure.org/resource/om-2/kilometre', str(km.identifier))
        self.assertEqual(m_dim, km.dimensions)

    def test__unit_multiple(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = SingularUnit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        km = PrefixedUnit(SI.KILO, m, OM.NAMESPACE + 'kilometre')
        km100 = UnitMultiple(km, 100.0, symbol='100km')
        self.assertEqual('100.0 kilometre', km100.label().value)
        self.assertEqual('100km', km100.symbol().value)
        self.assertEqual(m_dim, km100.dimensions)

    def test__unit_division(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = SingularUnit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        km = PrefixedUnit(SI.KILO, m, OM.NAMESPACE + 'kilometre')
        m_per_km = UnitDivision(m, km)
        m_per_km_dim = Dimension(0, 0, 0, 0, 0, 0, 0)
        self.assertTrue(m_per_km.label() is None)
        self.assertEqual('m/km', m_per_km.symbol().value)
        self.assertEqual(m_per_km_dim, m_per_km.dimensions)

    def test__unit_multiplication(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = SingularUnit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = SingularUnit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        ms = UnitMultiplication(m, s)
        ms_dim = Dimension(1, 1, 0, 0, 0, 0, 0)
        self.assertTrue(ms.label() is None)
        self.assertEqual('m.s', ms.symbol().value)
        self.assertEqual(ms_dim, ms.dimensions)

    def test__unit_exponentiation(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = SingularUnit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        m3 = UnitExponentiation(m, 3)
        m3_dim = Dimension(0, 3, 0, 0, 0, 0, 0)
        self.assertTrue(m3.label() is None)
        self.assertEqual('m3', m3.symbol().value)
        self.assertEqual(m3_dim, m3.dimensions)

    def test__unit_compound_1(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = SingularUnit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = SingularUnit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        ss = UnitMultiplication(s, s)
        ms2 = UnitDivision(m, ss)
        ms2_dim = Dimension(-2, 1, 0, 0, 0, 0, 0)
        self.assertTrue(ms2.label() is None)
        self.assertEqual('m/(s.s)', ms2.symbol().value)
        self.assertEqual(ms2_dim, ms2.dimensions)

    def test__unit_compound_2(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = SingularUnit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = SingularUnit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        ms = UnitDivision(m, s)
        ms2 = UnitDivision(ms, s)
        ms2_dim = Dimension(-2, 1, 0, 0, 0, 0, 0)
        self.assertTrue(ms2.label() is None)
        self.assertEqual('(m/s)/s', ms2.symbol().value)
        self.assertEqual(ms2_dim, ms2.dimensions)

    def test__unit_compound_3(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = SingularUnit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = SingularUnit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        s2 = UnitExponentiation(s, 2)
        ms2 = UnitDivision(m, s2)
        ms2_dim = Dimension(-2, 1, 0, 0, 0, 0, 0)
        self.assertTrue(ms2.label() is None)
        self.assertEqual('m/(s2)', ms2.symbol().value)
        self.assertEqual(ms2_dim, ms2.dimensions)

    def test_unit_get(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = SingularUnit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = SingularUnit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        units = Unit.with_label("metre")
        self.assertEqual(1, len(units))
        self.assertEqual('metre', units[0].label().value)
        self.assertEqual('m', units[0].symbol().value)
        self.assertEqual('http://www.ontology-of-units-of-measure.org/resource/om-2/metre', str(units[0].identifier))
        self.assertEqual(m_dim, units[0].dimensions)

    def test_singular_unit_conversion(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = SingularUnit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        inch = SingularUnit('inch', '\'', base_unit=m, factor=2.54e-2, identifier=OM.NAMESPACE + 'inch')
        m_to_inch_factor = Unit.conversion_factor(m, inch)
        self.assertEqual(2.54e-2, m_to_inch_factor)
        inch_to_m_factor = Unit.conversion_factor(inch, m)
        self.assertEqual(39.3700787, inch_to_m_factor)
