# Unit and Scale Conversion

One of the main functionalities of OM is the conversion between units and between scales, and by extension the conversion of a measure to another unit or a point to another scale. Examples would be the conversion from centimetres to inches, and from the Celsius scale to the Fahrenheit scale.

The API includes support for easily convert to the base units in a specific system, e.g. kilometres to metres, and to convert easily to the most convenient unit, e.g. 0.0000134 m to 13.4 μm.

## How to convert a measure to a different unit

There are two ways to convert a measure to a different unit. The first converts the receiver measure itself by using the `convert(to_unit)` method in the `Measure` class as follows:

```python
m1 = om(175, OM.CENTIMETRE)
print("before conversion: m1 = {}".format(m1))
m1.convert(IMPERIAL.INCH)
print("after conversion: m1 = {}".format(m1))
```

The result:

```
before conversion: m1 = 175 cm
after conversion: m1 = 68.8976377952756 in
```

The second way creates a new measure which is the converted instance of the first measure. The static function `Measure.create_by_converting(measure, to_unit)` can be used to do so:

```python
m2 = om(1.82, SI.METRE)
m3 = Measure.create_by_converting(m2, OM.CENTIMETRE)
print("Converted {} to {}".format(m2, m3))
```

which results is:

```
Converted 1.82 m to 182.0 cm
```

### Conversion to base units

Sometimes you want to convert to the base unit of the system of units you are working with. For length (or distance), this would be in the International System of Units (SI), the metre, while in the imperial system it would be the yard. Two convenience methods exist to do just that. These are (equivalent to the convert function), a class method and a static function:

- `convert_to_base_units(in_system_of_units=None)` - This class method takes one optional argument, the system of units of the base unit to which you want to convert.
- `create_by_converting_to_base_units(measure, in_system_of_units=SI)` - This static method takes two arguments, the first is required and is the measure that needs to be converted, the second in optional and is the system of units of the base unit to which you want to convert.

The unit to which the measure is converted will be the base unit in that specific system of units. If the system is not defined, the base unit of the system of units of the initial unit is used. *Usually you will probably need to convert to the base unit in the current system, e.g. kilometres to metres (SI system), and inches to yards (imperial system). The optional `in_system_of_units` argument should then not be used.* 

```python
m4 = om(4.34, IMPERIAL.FOOT)
print("before conversion: m4 = {}".format(m4))
m4.convert_to_base_units()
print("after conversion: m4 = {}".format(m4))

m5 = om(1.54, IMPERIAL.FOOT)
print("before conversion: m5 = {}".format(m5))
m5.convert_to_base_units(SI.SYSTEM_OF_UNITS)
print("after conversion: m5 = {}".format(m5))
```

which results in:

```
before conversion: m4 = 4.34 ft
after conversion: m4 = 1.4466666666666665 yd

before conversion: m5 = 1.54 ft
after conversion: m5 = 0.469392 m
```

Conversion to the base units in a specific system of units can, off course, also be done with more complex units:

```python
m6 = om(63, OM.KILOMETRE_PER_HOUR)
print("before conversion: m6 = {}".format(m6))
m6.convert_to_base_units()
print("after conversion: m6 = {}".format(m6))
```

resulting in:

```
before conversion: m6 = 63 km/h
after conversion: m6 = 17.5 m/s
```

### Conversion to convenient units

The most convenient unit for a measure is the unit for which the log of the numerical value is closer to 1.0. So 12.3e6 m  would be converted to 12.3 Mm (megametre) and 0.000000004543 m would be converted to 4.543 nm (nanometre). 

#### Conversion rules:

Which unit the measure is converted to is determined by the absolute log value of the numerical value converted to the new unit. This value is adjusted according to the following rules:

* The log value is appended with 2.0 if the log value is smaller than 1 (i.e the value is between 0 and 1.0)
* The log value is appended with 1.0 if the unit to be converted into is not a singular unit.

These adjustments mean that numerical values larger than 1.0 have preference above values just below 1.0. So, for instance, the preferred conversion unit for 0.098 m is cm (i.e. 9.8 cm) instead of dm (i.e. 0.98 dm). And singular units have a preference over other units such as prefixed units or unit divisions. For example, the convenient unit for 1 kg/(m.s2​) is Pa (Pascal), the result being ​1 Pa​. 

#### Methods and functions:

There are both a class method `convert_to_convenient_units(system_of_units=None, use_prefixes=True)` and a static function `create_by_converting_to_convenient_units(measure, in_system_of_units=None, use_prefixes=True)` to convert measures to convenient units. The `use_prefixes` parameter determines whether prefixed units (e.g. millimetre, hectometre, kiloKelvin) should also be allowed as the resulting unit (default is `True`).

For example if we have a measure of 1200 seconds, it would be converted by the following code: 

```python
m7 = om(1200, SI.SECOND)
print("before conversion: m7 = {}".format(m7))
m7.convert_to_convenient_units(use_prefixes=False)
print("after conversion: m7 = {}".format(m7))
```

 to 20.0 minutes:

```
before conversion: m7 = 1200 s
after conversion: m7 = 20.0 m
```

If we allow the use of prefixes, 1200 seconds would be converted to 1.2 ks (kilo seconds):

```python
m8 = om(1200, SI.SECOND)
print("before conversion: m8 = {}".format(m8))
m8.convert_to_convenient_units()
print("after conversion: m8 = {}".format(m8))
```

with result:

```
before conversion: m8 = 1200 s
after conversion: m8 = 1.2 ks
```

You can also covert to more convenient units in another system of units, such as converting 0.083 m to 3.268 in:

```python
m9 = om(0.083, SI.METRE)
print("before conversion: m9 = {}".format(m9))
m9.convert_to_convenient_units(system_of_units=IMPERIAL.SYSTEM_OF_UNITS)
print("after conversion: m9 = {}".format(m9))
```

```
before conversion: m9 = 0.083 m
after conversion: m9 = 3.2677165354330713 in
```



## How to convert points on a measurement scale to a different scale

## How conversion works

