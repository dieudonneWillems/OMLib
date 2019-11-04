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
