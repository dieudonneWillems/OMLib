
from omlib.constants import OM, SI
from omlib.measure import om, Point, Measure

if __name__ == '__main__':
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


