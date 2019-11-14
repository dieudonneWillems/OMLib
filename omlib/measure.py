import math

from omlib.constants import SI
from omlib.exceptions.dimensionexception import DimensionalException
from omlib.thing import Thing
from omlib.unit import Unit, PrefixedUnit, SingularUnit


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

    @staticmethod
    def create_by_converting_to_base_unit(measure, in_system_of_units=SI):
        if not isinstance(measure, Measure):
            raise ValueError("The parameter to the convert method is not of the correct type (Measure).")
        new_measure = Measure(measure.numerical_value, measure.unit)
        new_measure.convert_to_base_units(in_system_of_units)
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

    def convert_to_base_units(self, in_system_of_units=SI.SYSTEM_OF_UNITS):
        base = Unit.get_base_units(self.unit, in_system_of_units)
        self.convert(base)

    def convert_to_convenient_units(self, system_of_units=None, use_prefixes=True):
        if system_of_units is None:
            system_of_units = self.unit.systemOfUnits
        test_units = self.unit.with_dimensions(self.unit.dimensions, in_system_of_units=system_of_units)
        selected_unit = self.unit
        log_selected_value = Measure.__get_log_value(self.numerical_value, selected_unit)
        for test_unit in test_units:
            if use_prefixes or not isinstance(test_unit, PrefixedUnit):
                factor = Unit.conversion_factor(self.unit, test_unit)
                value = abs(self.numerical_value * factor)
                log_value = Measure.__get_log_value(value, test_unit)
                if log_value < log_selected_value:
                    log_selected_value = log_value
                    selected_unit = test_unit
        self.convert(selected_unit)

    @staticmethod
    def __get_log_value(value, unit):
        log_value = abs(math.log10(value))
        if value < 1:
            log_value = log_value + 2
        if not isinstance(unit, SingularUnit):
            log_value = log_value + 1
        return log_value

    def __str__(self):
        return f'{self.numerical_value} {self.unit.symbol()}'

    def __new_value_for_comparisson(self, other):
        if isinstance(other, Measure):
            factor = Unit.conversion_factor(self.unit, other.unit)
            new_value = self.numerical_value * factor
            return new_value
        return None

    def __eq__(self, other):
        new_value = self.__new_value_for_comparisson(other)
        if new_value is not None:
            return new_value == other.numerical_value
        return False

    def __ne__(self, other):
        new_value = self.__new_value_for_comparisson(other)
        if new_value is not None:
            return new_value != other.numerical_value
        return False

    def __lt__(self, other):
        new_value = self.__new_value_for_comparisson(other)
        if new_value is not None:
            return new_value < other.numerical_value
        return False

    def __le__(self, other):
        new_value = self.__new_value_for_comparisson(other)
        if new_value is not None:
            return new_value <= other.numerical_value
        return False

    def __gt__(self, other):
        new_value = self.__new_value_for_comparisson(other)
        if new_value is not None:
            return new_value > other.numerical_value
        return False

    def __ge__(self, other):
        new_value = self.__new_value_for_comparisson(other)
        if new_value is not None:
            return new_value >= other.numerical_value
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
