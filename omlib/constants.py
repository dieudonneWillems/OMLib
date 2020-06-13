from rdflib import URIRef

from .unit import Prefix


class OM:
    NAMESPACE = 'http://www.ontology-of-units-of-measure.org/resource/om-2/'
    LENGTH_DIMENSION = URIRef(NAMESPACE + 'length-Dimension')


class SI:
    YOTTA = Prefix('yotta', 'Y', 1e24)
    ZETTA = Prefix('zetta', 'Z', 1e21)
    EXA = Prefix('exa', 'E', 1e18)
    PETA = Prefix('peta', 'P', 1e15)
    TERA = Prefix('tera', 'T', 1e12)
    GIGA = Prefix('giga', 'G', 1e9)
    MEGA = Prefix('mega', 'M', 1e6)
    KILO = Prefix('kilo', 'k', 1e3)
    HECTO = Prefix('hecto', 'h', 1e2)
    DECA = Prefix('deca', 'da', 1e1)
    DECI = Prefix('deci', 'd', 1e-1)
    CENTI = Prefix('centi', 'c', 1e-2)
    MILLI = Prefix('milli', 'm', 1e-3)
    MICRO = Prefix('micro', 'μ', 1e-6)
    NANO = Prefix('nano', 'n', 1e-9)
    PICO = Prefix('pico', 'p', 1e-12)
    FEMTO = Prefix('femto', 'f', 1e-15)
    ATTO = Prefix('atto', 'a', 1e-18)
    ZEPTO = Prefix('zepto', 'z', 1e-21)
    YOCTO = Prefix('yocto', 'y', 1e-24)


class IEC:
    KIBI = Prefix('kibi', 'Ki', pow(2, 10))
    MEBI = Prefix('mebi', 'Mi', pow(2, 20))
    GIBI = Prefix('gibi', 'Gi', pow(2, 30))
    TEBI = Prefix('tebi', 'Ti', pow(2, 40))
    PEBI = Prefix('pebi', 'Pi', pow(2, 50))
    EXBI = Prefix('exbi', 'Ei', pow(2, 60))
    ZEBI = Prefix('zebi', 'Zi', pow(2, 70))
    YOBI = Prefix('yobi', 'Yi', pow(2, 80))


class JEDEC:
    KILO = Prefix('kilo', 'k', pow(2, 10))
    MEGA = Prefix('mega', 'M', pow(2, 20))
    GIGA = Prefix('giga', 'G', pow(2, 30))
