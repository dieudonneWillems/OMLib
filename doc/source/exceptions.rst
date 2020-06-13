Exceptions
==========

Not all units can be converted between each other. This section discusses the different exceptions that 
can occur when units or scales cannot be converted to each other.

DimensionalException
--------------------

For instance, a measure with unit metre per second cannot be converted to a measure with the hour (time) 
unit as the units have different dimensions. Or a scale cannot be converted to another scale when they 
have different dimensions.

In the following example, the metre per second unit has a dimension of ``{T=-1, L=1}``, and the hour unit 
has a dimension of ``{T=1}``. Only units that have the same dimensions can be converted to each other. 
If the dimensions do not match, you will get a ``DimensionalException``.

::

    m1 = om(14.2, OM.METRE_PER_SECOND)
    m1.convert(OM.HOUR_TIME)

results in:

::

    Traceback (most recent call last):
      File "/path/to/OMlib/run.py", line 78, in <module>
        conversion_exceptions()
      File "/path/to/OMlib/run.py", line 72, in conversion_exceptions
        m1.convert(OM.HOUR_TIME)
      File "/path/to/OMlib/omlib/measure.py", line 180, in convert
        factor = Unit.conversion_factor(self.unit, to_unit)
      File "/path/to/OMlib/omlib/unit.py", line 144, in conversion_factor
        .format(from_unit.dimensions, to_unit.dimensions))
    omlib.exceptions.dimensionexception.DimensionalException: A unit with dimensions (T=-1, L=1, M=0, I=0, θ=0, N=0, J=0) cannot be converted to a unit with dimensions (T=1, L=0, M=0, I=0, θ=0, N=0, J=0).


UnitConversionException
-----------------------


Some times units have the same dimension but cannot be converted to each other because they do 
not have a same ancestor or base unit. This will result in ``UnitConversionException``:

::

    my_unit = Unit.get_singular_unit("my unit", "mu", Dimension(T=-1, L=1))
    m2 = om(311.43, my_unit)
    m2.convert(OM.METRE_PER_SECOND)

results in:

::
    Traceback (most recent call last):
      File "/path/to/OMlib/run.py", line 84, in <module>
        conversion_exceptions()
      File "/path/to/OMlib/run.py", line 78, in conversion_exceptions
        m2.convert(OM.METRE_PER_SECOND)
      File "/path/to/OMlib/omlib/measure.py", line 180, in convert
        factor = Unit.conversion_factor(self.unit, to_unit)
      File "/path/to/OMlib/omlib/unit.py", line 151, in conversion_factor
        .format(from_unit, to_unit))
    omlib.exceptions.unitconversionexception.UnitConversionException: Cannot convert from my unit   mu      <N20dad03f13d44cb09978bae7bd9ad214>  dim: (T=-1, L=1, M=0, I=0, θ=0, N=0, J=0) to None      m/s     <http://www.ontology-of-units-of-measure.org/resource/om-2/metrePerSecond>  dim: (T=-1, L=1, M=0, I=0, θ=0, N=0, J=0) as they do not have a common ancestor unit.

The common ancestor unit is necessary to calculate the conversion factor between the 
two units (see below).


ScaleConversionException
------------------------


Scales that cannot be converted to each other because they do not have the same base scale, also 
raise an exception when they are converted to each other. This is not a ``UnitConversionException`` 
but a ``ScaleConversionException``.

::

    my_scale = Scale.get_ratio_scale(OM.DEGREE_FAHRENHEIT, "my scale")
    p1 = om(354.23, OM.KELVIN_SCALE)
    p1.convert(my_scale)

results in:

::
    Traceback (most recent call last):
      File "/path/to/OMlib/run.py", line 90, in <module>
        conversion_eexceptions()
      File "/path/to/OMlib/run.py", line 84, in conversion_exceptions
        p1.convert(my_scale)
      File "/path/to/OMlib/omlib/measure.py", line 47, in convert
        off_set = Scale.conversion_off_set(self.scale, to_scale)
      File "/path/to/omlib/scale.py", line 108, in conversion_off_set
        .format(from_scale, to_scale))
    omlib.exceptions.unitconversionexception.ScaleConversionException: Cannot convert from Kelvin scale     <http://www.ontology-of-units-of-measure.org/resource/om-2/KelvinScale> unit: kelvinK       <http://www.ontology-of-units-of-measure.org/resource/om-2/kelvin>  dim: (T=0, L=0, M=0, I=0, θ=1, N=0, J=0) dim: (T=0, L=0, M=0, I=0, θ=1, N=0, J=0) to my scale       <Nf49438949cfe454a8a632c316a8924de> unit: degree Fahrenheit °F      <Nfd9d80336e9e4513898c6c770736102a>  dim: (T=0, L=0, M=0, I=0, θ=1, N=0, J=0) dim: (T=0, L=0, M=0, I=0, θ=1, N=0, J=0) as they do not use the same base ratio scale, i.e. they do not have the same known zero point.


ValueError
----------


A ``ValueError`` is raised when the provided parameter of the conversion method is not a unit where 
a unit is expected, or not a scale where a scale is expected.

For instance in the following example a measure (the result of the ``om()`` function when a 
unit ``SI.KELVIN`` is provided) cannot be converted to the Kelvin scale:

::

    m3 = om(66.32, SI.KELVIN)
    m3.convert(OM.KELVIN_SCALE)


results in:


::

    Traceback (most recent call last):
      File "/path/to/OMlib/run.py", line 86, in <module>
        conversion_exceptions()
      File "/path/to/OMlib/run.py", line 80, in conversion_exceptions
        m3.convert(OM.KELVIN_SCALE)
      File "/path/to/OMlib/omlib/measure.py", line 179, in convert
        raise ValueError("The parameter to the convert method is not of the correct type (Unit).")
    ValueError: The parameter to the convert method is not of the correct type (Unit).

This will also happen when the parameter provided to the convert method is, for instance, a string, or a number.
