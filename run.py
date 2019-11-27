
from omlib.constants import OM, SI, IMPERIAL
from omlib.measure import om, Point, Measure

def creating_measures_and_points():
    m1 = om(12.0, SI.METRE)
    print(m1)
    print(type(m1))
    m2 = om(23.2, OM.CELSIUS_SCALE)
    print(m2)
    print(type(m2))

    m3 = Measure(1.75, SI.METRE)
    print(m3)
    print(type(m3))
    m4 = Point(-45.33, OM.CELSIUS_SCALE)
    print(m4)
    print(type(m4))

def unit_and_scale_conversion():
    m1 = om(175, OM.CENTIMETRE)
    print("before conversion: m1 = {}".format(m1))
    m1.convert(IMPERIAL.INCH)
    print("after conversion: m1 = {}".format(m1))

    m2 = om(1.82, SI.METRE)
    m3 = Measure.create_by_converting(m2, OM.CENTIMETRE)
    print("Converted {} to {}".format(m2, m3))

    m4 = om(4.34, IMPERIAL.FOOT)
    print("before conversion: m4 = {}".format(m4))
    m4.convert_to_base_units()
    print("after conversion: m4 = {}".format(m4))

    m5 = om(1.54, IMPERIAL.FOOT)
    print("before conversion: m5 = {}".format(m5))
    m5.convert_to_base_units(SI.SYSTEM_OF_UNITS)
    print("after conversion: m5 = {}".format(m5))

    m6 = om(63, OM.KILOMETRE_PER_HOUR)
    print("before conversion: m6 = {}".format(m6))
    m6.convert_to_base_units()
    print("after conversion: m6 = {}".format(m6))

    m7 = om(1200, SI.SECOND)
    print("before conversion: m7 = {}".format(m7))
    m7.convert_to_convenient_units(use_prefixes=False)
    print("after conversion: m7 = {}".format(m7))

    m8 = om(1200, SI.SECOND)
    print("before conversion: m8 = {}".format(m8))
    m8.convert_to_convenient_units()
    print("after conversion: m8 = {}".format(m8))

    m9 = om(0.083, SI.METRE)
    print("before conversion: m9 = {}".format(m9))
    m9.convert_to_convenient_units(system_of_units=IMPERIAL.SYSTEM_OF_UNITS)
    print("after conversion: m9 = {}".format(m9))


if __name__ == '__main__':
    creating_measures_and_points()
    unit_and_scale_conversion()

