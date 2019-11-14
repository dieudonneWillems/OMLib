from rdflib import Literal, XSD, URIRef

from exceptions.dimensionexception import DimensionalException
from exceptions.unitconversionexception import UnitConversionException
from exceptions.unitidentityexception import UnitIdentityException
from omlib.dimension import Dimension
from omlib.thing import Thing, SymbolThing


class Unit(SymbolThing):
    _units = []

    @staticmethod
    def with_label(label):
        get_units = []
        for unit in Unit._units:
            for u_label in unit.all_labels():
                if str(u_label) == label:
                    get_units.append(unit)
        return get_units

    @staticmethod
    def with_symbol(symbol):
        get_units = []
        for unit in Unit._units:
            for u_symbol in unit.all_symbols():
                if str(u_symbol) == symbol:
                    get_units.append(unit)
        return get_units

    @staticmethod
    def with_identifier(identifier):
        for unit in Unit._units:
            if str(unit.identifier) == str(identifier):
                return unit
        return None

    @staticmethod
    def with_prefix(prefix, base):
        for unit in Unit._units:
            if isinstance(unit, PrefixedUnit):
                if unit.baseUnit == base and unit.prefix == prefix:
                    return unit
        return None

    @staticmethod
    def with_multiplication(multiplier, multiplicand):
        for unit in Unit._units:
            if isinstance(unit, UnitMultiplication):
                if unit.multiplier == multiplier and unit.multiplicand == multiplicand:
                    return unit
        return None

    @staticmethod
    def with_division(numerator, denominator):
        for unit in Unit._units:
            if isinstance(unit, UnitDivision):
                if unit.numerator == numerator and unit.denominator == denominator:
                    return unit
        return None

    @staticmethod
    def with_exponentiation(base, exponent):
        for unit in Unit._units:
            if isinstance(unit, UnitExponentiation):
                if unit.base == base and unit.exponent == exponent:
                    return unit
        return None

    @staticmethod
    def with_dimensions(dimensions, in_system_of_units=None):
        if isinstance(dimensions, Dimension):
            get_units = []
            for test_unit in Unit._units:
                if test_unit.dimensions == dimensions:
                    if in_system_of_units is None or test_unit.systemOfUnits == in_system_of_units:
                        get_units.append(test_unit)
            return get_units
        return None

    @staticmethod
    def get_base_units(for_unit, in_system_of_units="SI"):  # WARNING If you change "SI" also change in constants.py
        if isinstance(for_unit, SingularUnit) or isinstance(for_unit, PrefixedUnit) \
                or isinstance(for_unit, UnitMultiple):
            units = Unit.with_dimensions(for_unit.dimensions)
            for unit in units:
                if unit.isBaseUnit and unit.systemOfUnits == in_system_of_units:
                    return unit
        if isinstance(for_unit, UnitMultiplication):
            base_multiplier = Unit.get_base_units(for_unit.multiplier, in_system_of_units)
            base_multiplicand = Unit.get_base_units(for_unit.multiplicand, in_system_of_units)
            if base_multiplier is not None and base_multiplicand is not None:
                unit = Unit.get_unit_multiplication(base_multiplier, base_multiplicand,
                                                    system_of_units=in_system_of_units)
                return unit
        if isinstance(for_unit, UnitDivision):
            base_numerator = Unit.get_base_units(for_unit.numerator, in_system_of_units)
            base_denominator = Unit.get_base_units(for_unit.denominator, in_system_of_units)
            if base_numerator is not None and base_denominator is not None:
                unit = Unit.get_unit_division(base_numerator, base_denominator, system_of_units=in_system_of_units)
                return unit
        if isinstance(for_unit, UnitExponentiation):
            base_base = Unit.get_base_units(for_unit.base, in_system_of_units)
            if base_base is not None:
                unit = Unit.get_unit_exponentiation(base_base, for_unit.exponent, system_of_units=in_system_of_units)
                return unit
        raise UnitIdentityException("Cannot find a base unit for {} in the system of units: {}"
                                    .format(for_unit, in_system_of_units))

    @staticmethod
    def __add_when_not_duplicate(unit):
        result_unit = Unit.with_identifier(unit.identifier)
        dim_units = Unit.with_dimensions(unit.dimensions)
        if result_unit is None:
            for test_unit in dim_units:
                try:
                    conversion_factor = abs(Unit.conversion_factor(unit, test_unit) - 1.0)
                    if conversion_factor < 0.0000001:
                        result_unit = test_unit
                        break
                except UnitConversionException as error:
                    pass
        if result_unit is not None:
            if unit.label() is not None or unit.symbol() is not None:
                all_labels = result_unit.all_labels()
                found = False
                str_unit_label = str(unit.label())
                for label in all_labels:
                    if str(label) == str_unit_label:
                        found = True
                        break
                if not found:
                    result_unit = None
        if result_unit is None:
            result_unit = unit
            Unit._units.append(unit)
        return result_unit

    @staticmethod
    def conversion_factor(from_unit, to_unit):
        can_convert = Unit.can_convert(from_unit, to_unit)
        if not can_convert:
            raise DimensionalException("A unit with dimensions {} cannot be converted to a unit with dimensions {}."
                                       .format(from_unit.dimensions, to_unit.dimensions))
        from_base_units_exponents = from_unit.get_base_units_exponents()
        to_base_units_exponents = to_unit.get_base_units_exponents()
        from_norm = Unit.__normalise_base_units_exponents(from_base_units_exponents)
        to_norm = Unit.__normalise_base_units_exponents(to_base_units_exponents)
        if not Unit.__check_same_units_from_normalised(from_norm, to_norm):
            raise UnitConversionException("Cannot convert from {} to {} as they do not have a common ancestor unit."
                                            .format(from_unit, to_unit))
        from_factor = Unit.__factor_from_normalised(from_norm)
        to_factor = Unit.__factor_from_normalised(to_norm)
        factor = from_factor / to_factor
        return factor

    @staticmethod
    def __normalise_base_units_exponents(base_unit_exponents):
        unit_dict = {}
        for exponent in base_unit_exponents:
            entry = [0, 1.0]
            if exponent[0].identifier in unit_dict:
                entry = unit_dict[exponent[0].identifier]
            entry[0] = entry[0] + exponent[1]
            entry[1] = entry[1] * pow(exponent[2], exponent[1])
            unit_dict[exponent[0].identifier] = entry
        return unit_dict

    @staticmethod
    def __factor_from_normalised(normalised):
        factor = 1.0
        for entry in normalised:
            factor = factor * normalised.get(entry)[1]
        return factor

    @staticmethod
    def __check_same_units_from_normalised(normalised_unit1, normalised_unit2):
        keys1 = normalised_unit1.keys()
        for ident in keys1:
            exp_1 = normalised_unit1.get(ident)
            exp_2 = normalised_unit2.get(ident)
            if exp_2 is None or exp_1[0] != exp_2[0]:
                return False
        keys2 = normalised_unit2.keys()
        for ident in keys2:
            exp_1 = normalised_unit1.get(ident)
            exp_2 = normalised_unit2.get(ident)
            if exp_1 is None or exp_1[0] != exp_2[0]:
                return False
        return True

    @staticmethod
    def print_base_units_exponents(unit):
        base_units_exponents = unit.get_base_units_exponents()
        bue_string = ""
        i = 0
        for exponent in base_units_exponents:
            bue_string += f'[{str(exponent[0].symbol()), exponent[1], exponent[2]}]'
            i = i + 1
            if i < len(base_units_exponents):
                bue_string += ', '

        print('BASE UNIT EXPONENTS: {}: [{}]'.format(unit.symbol(), bue_string))

    @staticmethod
    def can_convert(from_unit, to_unit):
        if isinstance(from_unit, Unit) and isinstance(to_unit, Unit):
            if from_unit.dimensions == to_unit.dimensions:
                return True
            return False
        if not isinstance(from_unit, Unit) and not isinstance(to_unit, Unit):
            raise ValueError("Both arguments of can_convert are required to be of type Unit.")
        if not isinstance(from_unit, Unit):
            raise ValueError("The first argument of can_convert is required to be of type Unit.")
        if not isinstance(to_unit, Unit):
            raise ValueError("The second argument of can_convert is required to be of type Unit.")

    @staticmethod
    def get_singular_unit(label, symbol, dimensions=Dimension(), base_unit=None, factor=1.0, identifier=None,
                          cache=True, system_of_units=None, is_base_unit=False):
        unit = None
        if identifier is not None:
            test_unit = Unit.with_identifier(identifier)
            if test_unit is not None:
                if not isinstance(test_unit, SingularUnit):
                    raise UnitIdentityException("The identifier for a SingularUnit has been used earlier"
                                                " for another type of unit")
                else:
                    if base_unit is not None:
                        base_identifier = str(base_unit.identifier)
                        test_identifier = str(test_unit.baseUnit.identifier)
                        if base_identifier != test_identifier:
                            raise UnitIdentityException("The requested SingularUnit uses a different base unit"
                                                        " as the earlier defined unit with the same identifier.")
                        if factor != test_unit.factor:
                            raise UnitIdentityException("The requested SingularUnit uses a different conversion factor"
                                                        " as the earlier defined unit with the same identifier.")
                return test_unit
        if unit is None:
            unit = SingularUnit(label, symbol, dimensions, base_unit, factor, identifier, system_of_units, is_base_unit)
            if cache:
                unit = Unit.__add_when_not_duplicate(unit)
        return unit

    @staticmethod
    def get_prefixed_unit(prefix, base_unit, identifier=None, cache=True, system_of_units=None, is_base_unit=False):
        unit = None
        if identifier is not None:
            test_unit = Unit.with_identifier(identifier)
            if test_unit is not None:
                if not isinstance(test_unit, PrefixedUnit):
                    raise UnitIdentityException("The identifier for a PrefixedUnit has been used earlier"
                                                " for another type of unit")
                else:
                    base_identifier = str(base_unit.identifier)
                    test_identifier = str(test_unit.baseUnit.identifier)
                    if base_identifier != test_identifier:
                        raise UnitIdentityException("The requested PrefixedUnit uses a different base unit"
                                                    " as the earlier defined unit with the same identifier.")
                    if str(prefix.identifier) != str(test_unit.prefix.identifier):
                        raise UnitIdentityException("The requested PrefixedUnit uses a different prefix"
                                                    " as the earlier defined unit with the same identifier.")
                return test_unit
        if unit is None:
            test_unit = Unit.with_prefix(prefix, base_unit)
            if test_unit is not None:
                if identifier is not None and not isinstance(test_unit.identifier, URIRef):
                    test_unit.identifier = URIRef(identifier)
                if system_of_units is not None and test_unit.systemOfUnits is None:
                    test_unit.systemOfUnits = system_of_units
                if is_base_unit and not test_unit.isBaseUnit:
                    test_unit.isBaseUnit = is_base_unit
                return test_unit
        if unit is None:
            if system_of_units is None:
                system_of_units = base_unit.systemOfUnits
            unit = PrefixedUnit(prefix, base_unit, identifier, system_of_units=system_of_units,
                                is_base_unit=is_base_unit)
            if cache:
                unit = Unit.__add_when_not_duplicate(unit)
        return unit

    @staticmethod
    def get_unit_multiple(base_unit, factor=1.0, identifier=None, label=None, symbol=None, cache=True,
                          system_of_units=None):
        unit = None
        if identifier is not None:
            test_unit = Unit.with_identifier(identifier)
            if test_unit is not None:
                if not isinstance(test_unit, UnitMultiple):
                    raise UnitIdentityException("The identifier for a UnitMultiple has been used earlier"
                                                " for another type of unit")
                else:
                    base_identifier = str(base_unit.identifier)
                    test_identifier = str(test_unit.baseUnit.identifier)
                    if base_identifier != test_identifier:
                        raise UnitIdentityException("The requested UnitMultiple uses a different base unit"
                                                    " as the earlier defined unit with the same identifier.")
                if system_of_units is not None:
                    test_unit.systemOfUnits = system_of_units
                return test_unit
        if unit is None:
            unit = UnitMultiple(base_unit, factor, identifier, label, symbol, system_of_units)
            if cache:
                unit = Unit.__add_when_not_duplicate(unit)
        return unit

    @staticmethod
    def get_unit_multiplication(multiplier, multiplicand, symbol=None, identifier=None, cache=True,
                                system_of_units=None):
        if identifier is not None:
            for test_unit in Unit._units:
                if str(test_unit.identifier) == str(identifier):
                    if not isinstance(test_unit, UnitMultiplication):
                        raise UnitIdentityException("The identifier for a UnitMultiplication has been used earlier"
                                                    " for another type of unit")
                    else:
                        if str(multiplier.identifier) != str(test_unit.multiplier.identifier) or \
                                str(multiplicand.identifier) != str(test_unit.multiplicand.identifier):
                            raise UnitIdentityException("The requested UnitMultiplication uses a different pair of"
                                                        " units as multiplier and multiplicand as the earlier defined"
                                                        " unit with the same identifier.")
                    if system_of_units is not None:
                        test_unit.systemOfUnits = system_of_units
                    return test_unit
        unit = Unit.with_multiplication(multiplier, multiplicand)
        if unit is not None:
            if identifier is not None:
                unit.identifier = identifier
            if symbol is not None:
                unit.add_symbol(symbol)
            if system_of_units is not None:
                unit.systemOfUnits = system_of_units
        if unit is None:
            for unit in Unit._units:
                if isinstance(unit, UnitMultiplication):
                    if str(multiplier.identifier) == str(unit.multiplier.identifier) and \
                            str(multiplicand.identifier) == str(unit.multiplicand.identifier):
                        if system_of_units is not None:
                            unit.systemOfUnits = system_of_units
                        return unit
            if system_of_units is None and multiplier.systemOfUnits is not None and \
                    multiplicand.systemOfUnits is not None and multiplicand.systemOfUnits == multiplier.systemOfUnits:
                system_of_units = multiplier.systemOfUnits
            unit = UnitMultiplication(multiplier, multiplicand, symbol, identifier, system_of_units)
            if cache:
                unit = Unit.__add_when_not_duplicate(unit)
        return unit

    @staticmethod
    def get_unit_division(numerator, denominator, symbol=None, identifier=None, cache=True, system_of_units=None):
        if identifier is not None:
            for test_unit in Unit._units:
                if str(test_unit.identifier) == str(identifier):
                    if not isinstance(test_unit, UnitDivision):
                        raise UnitIdentityException("The identifier for a UnitDivision has been used earlier"
                                                    " for another type of unit")
                    else:
                        if str(numerator.identifier) != str(test_unit.numerator.identifier) or \
                                str(denominator.identifier) != str(test_unit.denominator.identifier):
                            raise UnitIdentityException("The requested UnitDivision uses a different pair of"
                                                        " units as numerator and denominator as the earlier "
                                                        "defined unit with the same identifier.")
                    if system_of_units is not None:
                        test_unit.systemOfUnits = system_of_units
                    return test_unit
        unit = Unit.with_division(numerator, denominator)
        if unit is not None:
            if identifier is not None:
                unit.identifier = identifier
            if symbol is not None:
                unit.add_symbol(symbol)
            if system_of_units is not None:
                unit.systemOfUnits = system_of_units
        if unit is None:
            for unit in Unit._units:
                if isinstance(unit, UnitDivision):
                    if str(numerator.identifier) == str(unit.numerator.identifier) and \
                            str(denominator.identifier) == str(unit.denominator.identifier):
                        if system_of_units is not None:
                            unit.systemOfUnits = system_of_units
                        return unit
            if system_of_units is None and denominator.systemOfUnits is not None and \
                    numerator.systemOfUnits is not None and numerator.systemOfUnits == denominator.systemOfUnits:
                system_of_units = numerator.systemOfUnits
            unit = UnitDivision(numerator, denominator, symbol, identifier, system_of_units)
            if cache:
                unit = Unit.__add_when_not_duplicate(unit)
        return unit

    @staticmethod
    def get_unit_exponentiation(base, exponent, symbol=None, identifier=None, cache=True, system_of_units=None):
        unit = None
        if identifier is not None:
            for test_unit in Unit._units:
                if str(test_unit.identifier) == str(identifier):
                    if not isinstance(test_unit, UnitExponentiation):
                        raise UnitIdentityException("The identifier for a UnitExponentiation has been used earlier"
                                                    " for another type of unit")
                    else:
                        if str(base.identifier) != str(test_unit.base.identifier):
                            raise UnitIdentityException("The requested UnitExponentiation uses a different unit "
                                                        "as base as the earlier defined unit with the same identifier.")
                        if exponent != test_unit.exponent:
                            raise UnitIdentityException("The requested UnitExponentiation uses a different exponent as"
                                                        " the earlier defined unit with the same identifier.")
                    if system_of_units is not None:
                        unit.systemOfUnits = system_of_units
                    return test_unit
        unit = Unit.with_exponentiation(base, exponent)
        if unit is not None:
            if identifier is not None:
                unit.identifier = identifier
            if symbol is not None:
                unit.add_symbol(symbol)
            if system_of_units is not None:
                unit.systemOfUnits = system_of_units
        if unit is None:
            for unit in Unit._units:
                if isinstance(unit, UnitExponentiation):
                    if str(base.identifier) == str(unit.base.identifier) and \
                            exponent == unit.exponent:
                        if system_of_units is not None:
                            unit.systemOfUnits = system_of_units
                        return unit
            if system_of_units is None and base.systemOfUnits is not None:
                system_of_units = base.systemOfUnits
            unit = UnitExponentiation(base, exponent, symbol, identifier, system_of_units)
            if cache:
                unit = Unit.__add_when_not_duplicate(unit)
        return unit

    def __init__(self, label=None, symbol=None, dimensions=Dimension(), identifier=None, system_of_units=None,
                 is_base_unit=False):
        super().__init__(label, symbol, identifier)
        self.isBaseUnit = is_base_unit
        self.systemOfUnits = system_of_units
        self.dimensions = dimensions

    def __str__(self):
        return f'{self.label()}\t{self.symbol()}\t<{self.identifier}>  dim: {self.dimensions}'

    def __eq__(self, other):
        if isinstance(other, Unit):
            return str(self.identifier) == str(other.identifier)
        return False

    def __ne__(self, other):
        return not (self == other)


class Prefix(object):

    def __init__(self, name, symbol, factor, identifier):
        self.name = name
        self.symbol = symbol
        self.factor = factor
        self.identifier = identifier

    def __eq__(self, other):
        if isinstance(other, Prefix):
            return str(self.identifier) == str(other.identifier)
        return False

    def __ne__(self, other):
        return not (self == other)


class SingularUnit(Unit):

    def __init__(self, label, symbol, dimensions=Dimension(), base_unit=None, factor=1.0, identifier=None,
                 system_of_units=None, is_base_unit=False):
        if base_unit is not None:
            dimensions = base_unit.dimensions
        super().__init__(label, symbol, dimensions, identifier, system_of_units=system_of_units,
                         is_base_unit=is_base_unit)
        self.factor = factor
        self.baseUnit = base_unit

    def __eq__(self, other):
        if isinstance(other, SingularUnit):
            if not isinstance(self.identifier, URIRef) or not isinstance(other.identifier, URIRef):
                if self.baseUnit is None and other.baseUnit == self and other.factor == self.factor:
                    return True
                if other.baseUnit is None and self.baseUnit == other and other.factor == self.factor:
                    return True
                if other.baseUnit == self.baseUnit and other.factor == self.factor:
                    return True
            else:
                return str(self.identifier) == str(other.identifier)
        return False

    def get_base_units_exponents(self):
        if self.baseUnit is None:
            return [[self, 1, 1.0]]
        base_base = self.baseUnit.get_base_units_exponents()
        result = []
        factor_added = False
        for exponents in base_base:
            if not factor_added:
                corrected_factor = pow(self.factor, 1/(exponents[1]))
                converted = [exponents[0], exponents[1], exponents[2] * corrected_factor]
                factor_added = True
            else:
                converted = exponents
            result.append(converted)
        return result


class PrefixedUnit(Unit):

    def __init__(self, prefix, base_unit, identifier=None, system_of_units=None, is_base_unit=False):
        label = f'{prefix.name}{base_unit.label()}'
        symbol = f'{prefix.symbol}{base_unit.symbol()}'
        self.prefix = prefix
        self.baseUnit = base_unit
        super().__init__(label, symbol, dimensions=self.baseUnit.dimensions, identifier=identifier,
                         system_of_units=system_of_units, is_base_unit=is_base_unit)

    def __eq__(self, other):
        if isinstance(other, PrefixedUnit):
            if not isinstance(self.identifier, URIRef) or not isinstance(other.identifier, URIRef):
                if other.baseUnit == self.baseUnit and other.prefix == self.prefix:
                    return True
            else:
                return str(self.identifier) == str(other.identifier)
        return False

    def get_base_units_exponents(self):
        base_base = self.baseUnit.get_base_units_exponents()
        result = []
        for exponents in base_base:
            converted = [exponents[0], exponents[1], exponents[2] * self.prefix.factor]
            result.append(converted)
        return result


class UnitMultiple(SingularUnit):

    def __init__(self, base_unit, factor=1.0, identifier=None, label=None, symbol=None, system_of_units=None,
                 is_base_unit=False):
        if label is None:
            label = f'{factor} {base_unit.label()}'
        if symbol is None:
            symbol = f'{factor}{base_unit.symbol()}'
        super().__init__(label, symbol, base_unit.dimensions, base_unit, factor, identifier,
                         system_of_units=system_of_units, is_base_unit=is_base_unit)


class CompoundUnit(Unit):

    def __init__(self, symbol, dimensions, identifier=None, system_of_units=None, is_base_unit=False):
        super().__init__(None, symbol, dimensions, identifier, system_of_units=system_of_units,
                         is_base_unit=is_base_unit)


class UnitMultiplication(CompoundUnit):

    def __init__(self, multiplier, multiplicand, symbol=None, identifier=None, system_of_units=None,
                 is_base_unit=False):
        dimensions = multiplier.dimensions * multiplicand.dimensions
        if symbol is None:
            multiplier_str = str(multiplier.symbol())
            if isinstance(multiplier, CompoundUnit):
                multiplier_str = f'({multiplier_str})'
            multiplicand_str = str(multiplicand.symbol())
            if isinstance(multiplicand, CompoundUnit):
                multiplicand_str = f'({multiplicand_str})'
            symbol = f'{multiplier_str}.{multiplicand_str}'
        super().__init__(symbol, dimensions, identifier, system_of_units=system_of_units, is_base_unit=is_base_unit)
        self.multiplier = multiplier
        self.multiplicand = multiplicand

    def __eq__(self, other):
        if isinstance(other, UnitMultiplication):
            if not isinstance(self.identifier, URIRef) or not isinstance(other.identifier, URIRef):
                if other.multiplier == self.multiplier and other.multiplicand == self.multiplicand:
                    return True
                if other.multiplier == self.multiplicand and other.multiplicand == self.multiplier:
                    return True
            else:
                return str(self.identifier) == str(other.identifier)
        return False

    def get_base_units_exponents(self):
        multiplier_base = self.multiplier.get_base_units_exponents()
        multiplicand_base = self.multiplicand.get_base_units_exponents()
        result = []
        result.extend(multiplier_base)
        result.extend(multiplicand_base)
        return result


class UnitDivision(CompoundUnit):

    def __init__(self, numerator, denominator, symbol=None, identifier=None, system_of_units=None, is_base_unit=False):
        dimensions = numerator.dimensions / denominator.dimensions
        if symbol is None:
            numerator_str = str(numerator.symbol())
            if isinstance(numerator, CompoundUnit):
                numerator_str = f'({numerator_str})'
            denominator_str = str(denominator.symbol())
            if isinstance(denominator, CompoundUnit):
                denominator_str = f'({denominator_str})'
            symbol = f'{numerator_str}/{denominator_str}'
        super().__init__(symbol, dimensions, identifier, system_of_units=system_of_units, is_base_unit=is_base_unit)
        self.numerator = numerator
        self.denominator = denominator

    def __eq__(self, other):
        if isinstance(other, UnitDivision):
            if not isinstance(self.identifier, URIRef) or not isinstance(other.identifier, URIRef):
                if other.numerator == self.numerator and other.denominator == self.denominator:
                    return True
            else:
                return str(self.identifier) == str(other.identifier)
        return False

    def get_base_units_exponents(self):
        numerator_base = self.numerator.get_base_units_exponents()
        denominator_base = self.denominator.get_base_units_exponents()
        result = []
        result.extend(numerator_base)
        for exponents in denominator_base:
            result.append([exponents[0], -exponents[1], exponents[2]])
        return result


class UnitExponentiation(CompoundUnit):

    def __init__(self, base, exponent, symbol=None, identifier=None, system_of_units=None, is_base_unit=False):
        dimensions = Dimension.pow(base.dimensions, exponent)
        if symbol is None:
            base_str = str(base.symbol())
            if isinstance(base, CompoundUnit):
                base_str = f'({base_str})'
            symbol = f'{base_str}{exponent}'
        super().__init__(symbol, dimensions, identifier, system_of_units=system_of_units, is_base_unit=is_base_unit)
        self.base = base
        self.exponent = exponent

    def __eq__(self, other):
        if isinstance(other, UnitExponentiation):
            if not isinstance(self.identifier, URIRef) or not isinstance(other.identifier, URIRef):
                if other.base == self.base and other.exponent == self.exponent:
                    return True
            else:
                return str(self.identifier) == str(other.identifier)
        return False

    def get_base_units_exponents(self):
        base_base = self.base.get_base_units_exponents()
        result = []
        for exponents in base_base:
            result.append([exponents[0], exponents[1] * self.exponent, exponents[2]])
        return result
