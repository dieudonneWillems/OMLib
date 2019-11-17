import unittest

from omlib.constants import SI
from omlib.exceptions.unitidentityexception import ScaleIdentityException
from omlib.scale import Scale


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
