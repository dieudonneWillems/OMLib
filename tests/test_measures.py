import unittest

from omlib.constants import OM
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
