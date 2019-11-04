from exceptions.dimensionexception import DimensionalException
from omlib.thing import Thing
from omlib.unit import Unit


class Measure(Thing):

    @staticmethod
    def create_by_converting(measure, to_unit):
        if not isinstance(measure, Measure):
            raise ValueError("The parameter to the convert method is not of the correct type (Measure).")
        if not isinstance(to_unit, Unit):
            raise ValueError("The parameter to the convert method is not of the correct type (Unit).")
        new_measure = Measure(measure.numerical_value, measure.unit)
        new_measure.convert(to_unit)
        return new_measure

    def __init__(self, numerical_value, unit, identifier=None):
        super().__init__(identifier=identifier)
        self.numerical_value = numerical_value
        self.unit = unit

    def convert(self, to_unit):
        if not isinstance(to_unit, Unit):
            raise ValueError("The parameter to the convert method is not of the correct type (Unit).")
        factor = Unit.conversion_factor(self.unit, to_unit)
        self.numerical_value = self.numerical_value * factor
        self.unit = to_unit

    def __str__(self):
        return f'{self.numerical_value} {self.unit.symbol()}'

    def __eq__(self, other):
        if isinstance(other, Measure):
            factor = Unit.conversion_factor(self.unit, other.unit)
            new_value = self.numerical_value * factor
            return new_value == other.numerical_value
        return False

    def __add__(self, other):
        if not isinstance(other, Measure):
            raise ValueError('The value to be added is not a measure.')
        if not self.unit.dimensions == other.unit.dimensions:
            raise DimensionalException("Measures with units of different dimensions cannot be added together. {} != {}"
                                       .format(self.unit, other.unit))
        new_measure = Measure.create_by_converting(other, self.unit)
        return_measure = Measure(self.numerical_value + new_measure.numerical_value, self.unit)
        return return_measure

    def __sub__(self, other):
        if not isinstance(other, Measure):
            raise ValueError('The value to be subtracted is not a measure.')
        if not self.unit.dimensions == other.unit.dimensions:
            raise DimensionalException("Measures with units of different dimensions cannot be subtracted from each "
                                       "other. {} != {}".format(self.unit, other.unit))
        new_measure = Measure.create_by_converting(other, self.unit)
        return_measure = Measure(self.numerical_value - new_measure.numerical_value, self.unit)
        return return_measure

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            new_measure = Measure(self.numerical_value * other, self.unit)
            return new_measure
        if not isinstance(other, Measure):
            raise ValueError('The multiplicand is not a measure, a float, or an int.')
        new_value = self.numerical_value * other.numerical_value
        new_unit = Unit.get_unit_multiplication(self.unit, other.unit)
        new_measure = Measure(new_value, new_unit)
        return new_measure

    def __truediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            new_measure = Measure(self.numerical_value / other, self.unit)
            return new_measure
        if not isinstance(other, Measure):
            raise ValueError('The denominator is not a measure, a float, or an int.')
        new_value = self.numerical_value / other.numerical_value
        new_unit = Unit.get_unit_division(self.unit, other.unit)
        new_measure = Measure(new_value, new_unit)
        return new_measure
