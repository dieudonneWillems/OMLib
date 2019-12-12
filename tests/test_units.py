import unittest

from omlib.exceptions.dimensionexception import DimensionalException
from omlib.exceptions.unitconversionexception import UnitConversionException
from omlib.constants import SI, IMPERIAL
from omlib.dimension import Dimension
from omlib.omconstants import OM
from omlib.unit import UnitDivision, UnitExponentiation, \
    Unit


class TestUnits(unittest.TestCase):

    def test__singular_unit(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        self.assertEqual('metre', m.label().value)
        self.assertEqual('m', m.symbol().value)
        self.assertEqual('http://www.ontology-of-units-of-measure.org/resource/om-2/metre', str(m.identifier))
        self.assertEqual(m_dim, m.dimensions)

    def test__prefixed_unit(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        km = Unit.get_prefixed_unit(SI.KILO, m, OM.NAMESPACE + 'kilometre')
        self.assertEqual('kilometre', km.label().value)
        self.assertEqual('km', km.symbol().value)
        self.assertEqual('http://www.ontology-of-units-of-measure.org/resource/om-2/kilometre', str(km.identifier))
        self.assertEqual(m_dim, km.dimensions)

    def test__unit_multiple(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        km = Unit.get_prefixed_unit(SI.KILO, m, OM.NAMESPACE + 'kilometre')
        km100 = Unit.get_unit_multiple(km, 100.0, symbol='100km')
        self.assertEqual('100.0 kilometre', km100.label().value)
        self.assertEqual('100km', km100.symbol().value)
        self.assertEqual(m_dim, km100.dimensions)

    def test__unit_division(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        km = Unit.get_prefixed_unit(SI.KILO, m, OM.NAMESPACE + 'kilometre')
        m_per_km = UnitDivision(m, km)
        m_per_km_dim = Dimension(0, 0, 0, 0, 0, 0, 0)
        self.assertTrue(m_per_km.label() is None)
        self.assertEqual('m/km', m_per_km.symbol().value)
        self.assertEqual(m_per_km_dim, m_per_km.dimensions)

    def test__unit_multiplication(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        ms = Unit.get_unit_multiplication(m, s)
        ms_dim = Dimension(1, 1, 0, 0, 0, 0, 0)
        self.assertTrue(ms.label() is None)
        self.assertEqual('m·s', ms.symbol().value)
        self.assertEqual(ms_dim, ms.dimensions)

    def test__unit_exponentiation(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        m3 = UnitExponentiation(m, 3)
        m3_dim = Dimension(0, 3, 0, 0, 0, 0, 0)
        self.assertTrue(m3.label() is None)
        self.assertEqual('m3', m3.symbol().value)
        self.assertEqual(m3_dim, m3.dimensions)

    def test__unit_compound_1(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        ss = Unit.get_unit_multiplication(s, s)
        ms2 = UnitDivision(m, ss)
        ms2_dim = Dimension(-2, 1, 0, 0, 0, 0, 0)
        self.assertTrue(ms2.label() is None)
        self.assertEqual('m/s2', ms2.symbol().value)
        self.assertEqual(ms2_dim, ms2.dimensions)

    def test__unit_compound_2(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        ms = UnitDivision(m, s)
        ms2 = UnitDivision(ms, s)
        ms2_dim = Dimension(-2, 1, 0, 0, 0, 0, 0)
        self.assertTrue(ms2.label() is None)
        self.assertEqual('(m/s)/s', ms2.symbol().value)
        self.assertEqual(ms2_dim, ms2.dimensions)

    def test__unit_compound_3(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        s2 = UnitExponentiation(s, 2)
        ms2 = UnitDivision(m, s2)
        ms2_dim = Dimension(-2, 1, 0, 0, 0, 0, 0)
        self.assertTrue(ms2.label() is None)
        self.assertEqual('m/s2', ms2.symbol().value)
        self.assertEqual(ms2_dim, ms2.dimensions)

    def test_unit_get(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        units = Unit.with_label("metre")
        self.assertEqual(1, len(units))
        self.assertEqual('metre', units[0].label().value)
        self.assertEqual('m', units[0].symbol().value)
        self.assertEqual('http://www.ontology-of-units-of-measure.org/resource/om-2/metre', str(units[0].identifier))
        self.assertEqual(m_dim, units[0].dimensions)

    def test_singular_unit_conversion_1(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        inch = IMPERIAL.INCH
        m_to_inch_factor = Unit.conversion_factor(m, inch)
        self.assertAlmostEqual(39.3700787, m_to_inch_factor, delta=0.00001)
        inch_to_m_factor = Unit.conversion_factor(inch, m)
        self.assertAlmostEqual(2.54e-2, inch_to_m_factor, delta=0.00001)

    def test_singular_unit_conversion_2(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        feet = IMPERIAL.FOOT
        m_to_feet_factor = Unit.conversion_factor(m, feet)
        self.assertAlmostEqual(3.280839895, m_to_feet_factor, delta=0.0001)
        feet_to_m_factor = Unit.conversion_factor(feet, m)
        self.assertAlmostEqual(0.3048, feet_to_m_factor, delta=0.0001)

    def test_singular_unit_conversion_3(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        myl = Unit.get_singular_unit('my length unit', 'myl', m_dim, identifier=OM.NAMESPACE + 'myl')
        try:
            Unit.conversion_factor(m, myl)
            self.fail("Singular units that do not have a common base should not be converted between each other")
        except UnitConversionException as error:
            self.assertTrue(True)
        km = Unit.get_prefixed_unit(SI.KILO, m, OM.NAMESPACE + 'kilometre')
        myl67 = Unit.get_unit_multiple(myl, 67.0, symbol='67myl')
        try:
            Unit.conversion_factor(km, myl67)
            self.fail("Singular units that do not have a common base should not be converted between each other")
        except UnitConversionException as error:
            self.assertTrue(True)
        myl67_to_myl_factor = Unit.conversion_factor(myl67, myl)
        self.assertAlmostEqual(67, myl67_to_myl_factor, delta=0.0001)

    def test_singular_unit_conversion_4(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        try:
            Unit.conversion_factor(m, s)
            self.fail("Singular units that have different dimension cannot be converted between each other.")
        except DimensionalException as error:
            self.assertTrue(True)
        try:
            Unit.conversion_factor(s, m)
            self.fail("Singular units that have different dimension cannot be converted between each other.")
        except DimensionalException as error:
            self.assertTrue(True)

    def test_prefixed_unit_conversion_1(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        km = Unit.get_prefixed_unit(SI.KILO, m, OM.NAMESPACE + 'kilometre')
        m_to_km_factor = Unit.conversion_factor(m, km)
        self.assertAlmostEqual(0.001, m_to_km_factor, delta=0.0001)
        km_to_m_factor = Unit.conversion_factor(km, m)
        self.assertAlmostEqual(1000.0, km_to_m_factor, delta=0.0001)

    def test_prefixed_unit_conversion_2(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        km = Unit.get_prefixed_unit(SI.KILO, m, OM.NAMESPACE + 'kilometre')
        feet = IMPERIAL.FOOT
        feet_to_km_factor = Unit.conversion_factor(feet, km)
        self.assertAlmostEqual(0.0003048, feet_to_km_factor, delta=0.0001)
        km_to_feet_factor = Unit.conversion_factor(km, feet)
        self.assertAlmostEqual(3280.8399, km_to_feet_factor, delta=0.0001)

    def test_unit_multiple_conversion(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        km = Unit.get_prefixed_unit(SI.KILO, m, OM.NAMESPACE + 'kilometre')
        km100 = Unit.get_unit_multiple(km, 100.0, symbol='100km')
        m_to_km100_factor = Unit.conversion_factor(m, km100)
        self.assertAlmostEqual(0.000001, m_to_km100_factor, delta=0.0001)
        km100_to_m_factor = Unit.conversion_factor(km100, m)
        self.assertAlmostEqual(100000, km100_to_m_factor, delta=0.0001)

    def test_unit_multiplication_conversion_1(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        m2 = Unit.get_unit_multiplication(m, m)
        km = Unit.get_prefixed_unit(SI.KILO, m, OM.NAMESPACE + 'kilometre')
        km2 = Unit.get_unit_multiplication(km, km)
        m2_to_km2 = Unit.conversion_factor(m2, km2)
        self.assertAlmostEqual(1e-6, m2_to_km2, delta=0.0001)
        km2_to_m2 = Unit.conversion_factor(km2, m2)
        self.assertAlmostEqual(1e6, km2_to_m2, delta=0.0001)

    def test_unit_division_conversion_1(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        mps = Unit.get_unit_division(m, s)
        km = Unit.get_prefixed_unit(SI.KILO, m, OM.NAMESPACE + 'kilometre')
        kmps = Unit.get_unit_division(km, s)
        mps_to_kmps = Unit.conversion_factor(mps, kmps)
        self.assertAlmostEqual(1e-3, mps_to_kmps, delta=0.0001)
        kmps_to_mps = Unit.conversion_factor(kmps, mps)
        self.assertAlmostEqual(1e3, kmps_to_mps, delta=0.0001)

    def test_unit_expansion_conversion_1(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        m3 = Unit.get_unit_exponentiation(m, 3)
        cm = Unit.get_prefixed_unit(SI.CENTI, m, OM.NAMESPACE + 'centimetre')
        cm3 = Unit.get_unit_exponentiation(cm, 3)
        m3_to_cm3 = Unit.conversion_factor(m3, cm3)
        self.assertAlmostEqual(1e6, m3_to_cm3, delta=0.0001)
        cm3_to_m3 = Unit.conversion_factor(cm3, m3)
        self.assertAlmostEqual(1e-6, cm3_to_m3, delta=0.0001)

    def test_unit_expansion_conversion_2(self):
        m_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', m_dim, identifier=OM.NAMESPACE + 'metre')
        m3 = Unit.get_unit_exponentiation(m, 3)
        dm = Unit.get_prefixed_unit(SI.DECI, m, OM.NAMESPACE + 'decimetre')
        dm3 = Unit.get_unit_exponentiation(dm, 3)
        litre = Unit.get_singular_unit("litre", "l", base_unit=dm3, factor=1.0, identifier=OM.NAMESPACE + 'litre')
        m3_to_dm3 = Unit.conversion_factor(m3, dm3)
        self.assertAlmostEqual(1e3, m3_to_dm3, delta=0.0001)
        dm3_to_m3 = Unit.conversion_factor(dm3, m3)
        self.assertAlmostEqual(1e-3, dm3_to_m3, delta=0.0001)
        m3_to_l = Unit.conversion_factor(m3, litre)
        self.assertAlmostEqual(1e3, m3_to_l, delta=0.0001)
        l_to_m3 = Unit.conversion_factor(litre, m3)
        self.assertAlmostEqual(1e-3, l_to_m3, delta=0.0001)

    def test_unit_conversion_1(self):
        l_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m_dim = Dimension(0, 0, 1, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', l_dim, identifier=OM.NAMESPACE + 'metre')
        inch = IMPERIAL.INCH
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
        lbf_inch2 = Unit.get_unit_division(lbf, inch2)
        psi = Unit.get_singular_unit("Psi", "psi", base_unit=lbf_inch2, identifier=OM.NAMESPACE + 'psi')
        n_to_lbf = Unit.conversion_factor(n, lbf)
        self.assertAlmostEqual(0.22481, n_to_lbf, delta=0.0001)
        lbf_to_n = Unit.conversion_factor(lbf, n)
        self.assertAlmostEqual(4.448222, lbf_to_n, delta=0.0001)
        pa_to_psi = Unit.conversion_factor(pa, psi)
        self.assertAlmostEqual(0.000145033, pa_to_psi, delta=0.0000001)
        psi_to_pa = Unit.conversion_factor(psi, pa)
        self.assertAlmostEqual(6895, psi_to_pa, delta=1)

    def test_exponentiation_multiplication_conversion(self):
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        s2_1 = Unit.get_unit_exponentiation(s, 2)
        s2_2 = Unit.get_unit_multiplication(s, s)
        s2_1_to_s2_2 = Unit.conversion_factor(s2_1, s2_2)
        self.assertAlmostEqual(1.0, s2_1_to_s2_2, delta=0.00001)
        s2_2_to_s2_1 = Unit.conversion_factor(s2_1, s2_2)
        self.assertAlmostEqual(1.0, s2_2_to_s2_1, delta=0.00001)

    def test_exponentiation_multiplication_conversion_2(self):
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        ms = Unit.get_prefixed_unit(SI.MILLI, s)
        us = Unit.get_prefixed_unit(SI.MICRO, s)
        ms2_1 = Unit.get_unit_exponentiation(ms, 2)
        ms2_2 = Unit.get_unit_multiplication(s, us)
        ms2_1_to_ms2_2 = Unit.conversion_factor(ms2_1, ms2_2)
        self.assertAlmostEqual(1.0, ms2_1_to_ms2_2, delta=0.00001)
        ms2_2_to_ms2_1 = Unit.conversion_factor(ms2_1, ms2_2)
        self.assertAlmostEqual(1.0, ms2_2_to_ms2_1, delta=0.00001)

    def test_exponentiation_multiplication_conversion_3(self):
        l_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        t_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', l_dim, identifier=OM.NAMESPACE + 'metre')
        s = Unit.get_singular_unit('second', 's', t_dim, identifier=OM.NAMESPACE + 'second')
        km = Unit.get_prefixed_unit(SI.KILO, m)
        km_s = Unit.get_unit_division(km, s)
        km_s2 = Unit.get_unit_division(km_s, s)
        s2 = Unit.get_unit_exponentiation(s, 2)
        m_s2 = Unit.get_unit_division(m, s2)
        km_s2_to_m_s2 = Unit.conversion_factor(km_s2, m_s2)
        self.assertAlmostEqual(1000.0, km_s2_to_m_s2, delta=0.001)
        m_s2_to_km_s2 = Unit.conversion_factor(m_s2, km_s2)
        self.assertAlmostEqual(0.001, m_s2_to_km_s2, delta=0.00001)

    def test_exponentiation_multiplication_conversion_4(self):
        l_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', l_dim, identifier=OM.NAMESPACE + 'metre')
        m2 = Unit.get_unit_exponentiation(m, 2)
        m2_10 = Unit.get_singular_unit('10m2', '10m2', base_unit=m2, factor=10.0)
        m2_10_to_m2 = Unit.conversion_factor(m2_10, m2)
        self.assertAlmostEqual(10.0, m2_10_to_m2, delta=0.001)
        m2_to_m2_10 = Unit.conversion_factor(m2, m2_10)
        self.assertAlmostEqual(0.1, m2_to_m2_10, delta=0.00001)

    def test_exponentiation_multiplication_conversion_5(self):
        l_dim = Dimension(0, 1, 0, 0, 0, 0, 0)
        m = Unit.get_singular_unit('metre', 'm', l_dim, identifier=OM.NAMESPACE + 'metre')
        m2 = Unit.get_unit_exponentiation(m, -2)
        m2_10 = Unit.get_singular_unit('10m-2', '10m-2', base_unit=m2, factor=10.0)
        m2_10_to_m2 = Unit.conversion_factor(m2_10, m2)
        self.assertAlmostEqual(10.0, m2_10_to_m2, delta=0.001)
        m2_to_m2_10 = Unit.conversion_factor(m2, m2_10)
        self.assertAlmostEqual(0.1, m2_to_m2_10, delta=0.00001)

    def test_base_units_1(self):
        m = SI.METRE
        km = Unit.get_prefixed_unit(SI.KILO, m)
        base = Unit.get_base_units(km, SI.SYSTEM_OF_UNITS)
        self.assertEqual(m.identifier, base.identifier)
        self.assertNotEqual(km.identifier, base.identifier)

    def test_base_units_2(self):
        m = SI.METRE
        inch = IMPERIAL.INCH
        base = Unit.get_base_units(inch, SI.SYSTEM_OF_UNITS)
        self.assertEqual(m.identifier, base.identifier)
        self.assertNotEqual(inch.identifier, base.identifier)

    def test_base_units_3(self):
        m = SI.METRE
        km = Unit.get_prefixed_unit(SI.KILO, m)
        km100 = Unit.get_unit_multiple(km, 100, label="100 kilometre", symbol="100km")
        base = Unit.get_base_units(km100, SI.SYSTEM_OF_UNITS)
        self.assertEqual(m.identifier, base.identifier)
        self.assertNotEqual(km100.identifier, base.identifier)

    def test_base_units_4(self):
        km = Unit.get_prefixed_unit(SI.KILO, SI.METRE)
        hour = Unit.get_singular_unit("hour", "h", base_unit=SI.SECOND, factor=3600)
        m_s = Unit.get_unit_division(SI.METRE, SI.SECOND)
        km_h = Unit.get_unit_division(km, hour)
        base = Unit.get_base_units(km_h, SI.SYSTEM_OF_UNITS)
        self.assertEqual(m_s.identifier, base.identifier)
        self.assertNotEqual(km_h.identifier, base.identifier)

    def test_base_units_imperial_1(self):
        m = SI.METRE
        yd = IMPERIAL.YARD
        base = Unit.get_base_units(m, IMPERIAL.SYSTEM_OF_UNITS)
        self.assertEqual(yd.identifier, base.identifier)
        self.assertNotEqual(m.identifier, base.identifier)

    def test_base_units_imperial_2(self):
        kg = SI.KILOGRAM
        lb = IMPERIAL.POUND
        base = Unit.get_base_units(kg, IMPERIAL.SYSTEM_OF_UNITS)
        self.assertEqual(lb.identifier, base.identifier)
        self.assertNotEqual(kg.identifier, base.identifier)

    def test_base_units_imperial_3(self):
        m = SI.METRE
        yd = IMPERIAL.YARD
        base = Unit.get_base_units(yd, SI.SYSTEM_OF_UNITS)
        self.assertEqual(m.identifier, base.identifier)
        self.assertNotEqual(yd.identifier, base.identifier)

    def test_base_units_imperial_4(self):
        kg = SI.KILOGRAM
        lb = IMPERIAL.POUND
        base = Unit.get_base_units(lb, SI.SYSTEM_OF_UNITS)
        self.assertEqual(kg.identifier, base.identifier)
        self.assertNotEqual(lb.identifier, base.identifier)

    def test_base_units_imperial_5(self):
        kg = SI.KILOGRAM
        lb = IMPERIAL.POUND
        m = SI.METRE
        yd = IMPERIAL.YARD
        kg_m = Unit.get_unit_division(kg, m)
        lb_yd = Unit.get_unit_division(lb, yd)
        base = Unit.get_base_units(lb_yd, SI.SYSTEM_OF_UNITS)
        self.assertEqual(kg_m, base)
        self.assertNotEqual(lb_yd, base)
        base2 = Unit.get_base_units(kg_m, IMPERIAL.SYSTEM_OF_UNITS)
        self.assertEqual(lb_yd, base2)
        self.assertNotEqual(kg_m, base2)

    def test_unit_simplification(self):
        m_s = Unit.get_unit_division(SI.METRE, SI.SECOND)
        m_s2 = Unit.get_unit_division(m_s, SI.SECOND)
        self.assertEqual('m/s2', str(m_s2.symbol()))
        kgm_s2 = Unit.get_unit_multiplication(SI.KILOGRAM, m_s2)
        self.assertEqual('(kg·m)/s2', str(kgm_s2.symbol()))
        m2 = Unit.get_unit_exponentiation(SI.METRE, 2)
        kg_ms2 = Unit.get_unit_division(kgm_s2, m2)
        self.assertEqual('kg/(m·s2)', str(kg_ms2.symbol()))

    def test_unit_simplification_2(self):
        yard_s = Unit.get_unit_division(IMPERIAL.YARD, SI.SECOND)
        yard_s2 = Unit.get_unit_division(yard_s, SI.SECOND)
        self.assertEqual('yd/s2', str(yard_s2.symbol()))
        kgyard_s2 = Unit.get_unit_multiplication(SI.KILOGRAM, yard_s2)
        self.assertEqual('(kg·yd)/s2', str(kgyard_s2.symbol()))
        m2 = Unit.get_unit_exponentiation(SI.METRE, 2)
        kgyard_m2s2 = Unit.get_unit_division(kgyard_s2, m2)
        self.assertEqual('(kg·yd)/(s2·m2)', str(kgyard_m2s2.symbol()))
