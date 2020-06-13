How to create measures and points
=================================

Using the ``om()`` function
---------------------------

The easiest and preferred way to create a measure or point in OMlib is by use of the 
global function ``om()``. To be able to use this function you will need to import 
the function using:

::

    from omlib.constants import OM, SI
    from omlib.measure import om, Point, Measure

The ``om()`` function is located in the ``omlib.measure`` file of ``OMlib``.

The function takes a maximum of three parameters, the first two of which are required and the third is optional.

1. The numerical value of the measure or point.
2. The unit if you need to create a measure, or the scale if you need to create a point.
3. An optional identifier for the measure or point. This identifier should be unique and will 
   be used when creating an RDF representation of the measure or point.

First we need to import the correct modules:

::

    from omlib.constants import SI, OM
    from omlib.measure import om

To create a distance measure of 12m, for example, you can use the following code:


::

    m1 = om(12.0, SI.METRE)
    print(m1)
    print(type(m1))

``SI.METRE`` is the unit as defined in the ``SI`` class in ``omlib.constants``. The resulting 
value ``m1`` will be of type ``Measure`` and will have a numerical value of ``12.0``. The 
output will be:

::

    12.0 m
    <class 'omlib.measure.Measure'>

To create a point on a the Celsius temperature scale, you can use the following:

::

    m2 = om(23.2, OM.CELSIUS_SCALE)
    print(m2)
    print(type(m1))


In this case the second argument is not a unit but a scale; the ``OM.CELSIUS_SCALE`` 
which itself has a unit (``OM.CELSIUS``). The result will, therefore, not be a 
measure but a point on a measurement scale. The output will be:

::

    23.2 °C
    <class 'omlib.measure.Point'>


Directly by initialising Measure or Point
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A measure or point can also be directly created by using the initialising function for 
either the ``Measure`` or ``Point`` classes:

::

    m3 = Measure(1.75, SI.METRE)
    print(m3)
    print(type(m3))

    m4 = Point(-45.33, OM.CELSIUS_SCALE)
    print(m4)
    print(type(m4))

The output will be:

::

    1.75 m
    <class 'omlib.measure.Measure'>

    -45.33 °C
    <class 'omlib.measure.Point'>

