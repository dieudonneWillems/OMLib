# How to create measures and points

The easiest way to create a measure or point in OMlib is by use of the global function `om()`. To be able to use this function you will need to import the function using:

```python
from omlib.measure import om
```

The `om()` function is located in the `omlib.measure` file of OMlib.

The function takes a maximum of three parameters, the first two of which are required and the third is optional.

1. The numerical value of the measure or point.
2. The unit if you need to create a measure, or the scale if you need to create a point.
3. An optional identifier for the measure or point. This identifier should be unique and will be used when creating an RDF representation of the measure or point.

To create a distance measure of 12m, for example, you can use the following code:

```python
from omlib.constants import SI
from omlib.measure import om

m1 = om(12.0, SI.METRE)
```

`SI.METRE` is the unit as defined in the `SI` class in `omlib.constants`. The resulting value `m1` will be of type `Measure` and will have a numerical value of `12.0`.

To create a point on a the Celsius temperature scale, you can use the following:

```python
from omlib.constants import SI
from omlib.measure import om
from omlib.scale import Scale

k = Scale.get_ratio_scale(SI.KELVIN, "Kelvin scale", "http://example.org/KelvinScale")
c_unit = Unit.get_singular_unit("degree Celsius", "°C", base_unit=SI.KELVIN, factor=1.0)
c = Scale.get_interval_scale(k, c_unit, -273.15, "Celsius scale")

m1 = om(23.2, c)
```

In this case we will need to create the Celsius scale first (as it is not defined as a SI constant). 