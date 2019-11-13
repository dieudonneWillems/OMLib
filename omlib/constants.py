from rdflib import URIRef

from omlib.dimension import Dimension
from omlib.unit import Prefix, Unit


class OM:
    NAMESPACE = 'http://www.ontology-of-units-of-measure.org/resource/om-2/'
    LENGTH_DIMENSION = URIRef(NAMESPACE + 'length-Dimension')


class SI:
    SYSTEM_OF_UNITS = "SI" # WARNING If you change "SI" also change in constants.py

    # SI Prefixes
    YOTTA = Prefix('yotta', 'Y', 1e24, OM.NAMESPACE + 'yotta')
    ZETTA = Prefix('zetta', 'Z', 1e21, OM.NAMESPACE + 'zetta')
    EXA = Prefix('exa', 'E', 1e18, OM.NAMESPACE + 'exa')
    PETA = Prefix('peta', 'P', 1e15, OM.NAMESPACE + 'peta')
    TERA = Prefix('tera', 'T', 1e12, OM.NAMESPACE + 'tera')
    GIGA = Prefix('giga', 'G', 1e9, OM.NAMESPACE + 'giga')
    MEGA = Prefix('mega', 'M', 1e6, OM.NAMESPACE + 'mega')
    KILO = Prefix('kilo', 'k', 1e3, OM.NAMESPACE + 'kilo')
    HECTO = Prefix('hecto', 'h', 1e2, OM.NAMESPACE + 'hecto')
    DECA = Prefix('deca', 'da', 1e1, OM.NAMESPACE + 'deca')
    DECI = Prefix('deci', 'd', 1e-1, OM.NAMESPACE + 'deci')
    CENTI = Prefix('centi', 'c', 1e-2, OM.NAMESPACE + 'centi')
    MILLI = Prefix('milli', 'm', 1e-3, OM.NAMESPACE + 'milli')
    MICRO = Prefix('micro', 'μ', 1e-6, OM.NAMESPACE + 'micro')
    NANO = Prefix('nano', 'n', 1e-9, OM.NAMESPACE + 'nano')
    PICO = Prefix('pico', 'p', 1e-12, OM.NAMESPACE + 'pico')
    FEMTO = Prefix('femto', 'f', 1e-15, OM.NAMESPACE + 'femto')
    ATTO = Prefix('atto', 'a', 1e-18, OM.NAMESPACE + 'atto')
    ZEPTO = Prefix('zepto', 'z', 1e-21, OM.NAMESPACE + 'zepto')
    YOCTO = Prefix('yocto', 'y', 1e-24, OM.NAMESPACE + 'yocto')

    # SI Base Units
    SECOND = Unit.get_singular_unit('second', 's', Dimension(1, 0, 0, 0, 0, 0, 0), identifier=OM.NAMESPACE + 'second',
                                    system_of_Units=SYSTEM_OF_UNITS, is_base_unit=True)
    METRE = Unit.get_singular_unit('metre', 'm', Dimension(0, 1, 0, 0, 0, 0, 0), identifier=OM.NAMESPACE + 'metre',
                                   system_of_Units=SYSTEM_OF_UNITS, is_base_unit=True)
    GRAM = Unit.get_singular_unit('gram', 'g', Dimension(0, 0, 1, 0, 0, 0, 0), identifier=OM.NAMESPACE + 'gram')
    KILOGRAM = Unit.get_prefixed_unit(KILO, GRAM, identifier=OM.NAMESPACE + 'kilogram', system_of_Units=SYSTEM_OF_UNITS,
                                      is_base_unit=True)
    AMPERE = Unit.get_singular_unit('ampere', 'A', Dimension(0, 0, 0, 1, 0, 0, 0), identifier=OM.NAMESPACE + 'ampere',
                                    system_of_Units=SYSTEM_OF_UNITS, is_base_unit=True)
    KELVIN = Unit.get_singular_unit('kelvin', 'K', Dimension(0, 0, 0, 0, 1, 0, 0), identifier=OM.NAMESPACE + 'kelvin',
                                    system_of_Units=SYSTEM_OF_UNITS, is_base_unit=True)
    MOLE = Unit.get_singular_unit('mole', 'mol', Dimension(0, 0, 0, 0, 0, 1, 0), identifier=OM.NAMESPACE + 'mole',
                                  system_of_Units=SYSTEM_OF_UNITS, is_base_unit=True)
    CANDELA = Unit.get_singular_unit('candela', 'cd', Dimension(0, 0, 0, 0, 0, 0, 1),
                                     identifier=OM.NAMESPACE + 'candela', system_of_Units=SYSTEM_OF_UNITS,
                                     is_base_unit=True)


class IEC:
    KIBI = Prefix('kibi', 'Ki', pow(2, 10), OM.NAMESPACE + 'kibi')
    MEBI = Prefix('mebi', 'Mi', pow(2, 20), OM.NAMESPACE + 'mebi')
    GIBI = Prefix('gibi', 'Gi', pow(2, 30), OM.NAMESPACE + 'gibi')
    TEBI = Prefix('tebi', 'Ti', pow(2, 40), OM.NAMESPACE + 'tebi')
    PEBI = Prefix('pebi', 'Pi', pow(2, 50), OM.NAMESPACE + 'pebi')
    EXBI = Prefix('exbi', 'Ei', pow(2, 60), OM.NAMESPACE + 'exbi')
    ZEBI = Prefix('zebi', 'Zi', pow(2, 70), OM.NAMESPACE + 'zebi')
    YOBI = Prefix('yobi', 'Yi', pow(2, 80), OM.NAMESPACE + 'yobi')


class JEDEC:
    KILO = Prefix('kilo', 'k', pow(2, 10), OM.NAMESPACE + 'jedec-kilo')
    MEGA = Prefix('mega', 'M', pow(2, 20), OM.NAMESPACE + 'jedec-mega')
    GIGA = Prefix('giga', 'G', pow(2, 30), OM.NAMESPACE + 'jedec-giga')


class IMPERIAL:
    SYSTEM_OF_UNITS = "IMPERIAL"

    # Imperial Base uits
    YARD = Unit.get_singular_unit('yard', 'yd', base_unit=SI.METRE, factor=0.9144, identifier=OM.NAMESPACE + 'yard',
                                  system_of_Units=SYSTEM_OF_UNITS, is_base_unit=True)
    POUND = Unit.get_singular_unit('pound', 'lb', base_unit=SI.KILOGRAM, factor=0.45359237,
                                   identifier=OM.NAMESPACE + 'pound', system_of_Units=SYSTEM_OF_UNITS,
                                   is_base_unit=True)


