from rdflib import URIRef

from omlib.unit import Prefix


class OM:
    NAMESPACE = 'http://www.ontology-of-units-of-measure.org/resource/om-2/'
    LENGTH_DIMENSION = URIRef(NAMESPACE + 'length-Dimension')


class SI:
    YOTTA = Prefix('yotta', 'Y', 1e24, OM.NAMESPACE+'yotta')
    ZETTA = Prefix('zetta', 'Z', 1e21, OM.NAMESPACE+'zetta')
    EXA = Prefix('exa', 'E', 1e18, OM.NAMESPACE+'exa')
    PETA = Prefix('peta', 'P', 1e15, OM.NAMESPACE+'peta')
    TERA = Prefix('tera', 'T', 1e12, OM.NAMESPACE+'tera')
    GIGA = Prefix('giga', 'G', 1e9, OM.NAMESPACE+'giga')
    MEGA = Prefix('mega', 'M', 1e6, OM.NAMESPACE+'mega')
    KILO = Prefix('kilo', 'k', 1e3, OM.NAMESPACE+'kilo')
    HECTO = Prefix('hecto', 'h', 1e2, OM.NAMESPACE+'hecto')
    DECA = Prefix('deca', 'da', 1e1, OM.NAMESPACE+'deca')
    DECI = Prefix('deci', 'd', 1e-1, OM.NAMESPACE+'deci')
    CENTI = Prefix('centi', 'c', 1e-2, OM.NAMESPACE+'centi')
    MILLI = Prefix('milli', 'm', 1e-3, OM.NAMESPACE+'milli')
    MICRO = Prefix('micro', 'μ', 1e-6, OM.NAMESPACE+'micro')
    NANO = Prefix('nano', 'n', 1e-9, OM.NAMESPACE+'nano')
    PICO = Prefix('pico', 'p', 1e-12, OM.NAMESPACE+'pico')
    FEMTO = Prefix('femto', 'f', 1e-15, OM.NAMESPACE+'femto')
    ATTO = Prefix('atto', 'a', 1e-18, OM.NAMESPACE+'atto')
    ZEPTO = Prefix('zepto', 'z', 1e-21, OM.NAMESPACE+'zepto')
    YOCTO = Prefix('yocto', 'y', 1e-24, OM.NAMESPACE+'yocto')


class IEC:
    KIBI = Prefix('kibi', 'Ki', pow(2, 10), OM.NAMESPACE+'kibi')
    MEBI = Prefix('mebi', 'Mi', pow(2, 20), OM.NAMESPACE+'mebi')
    GIBI = Prefix('gibi', 'Gi', pow(2, 30), OM.NAMESPACE+'gibi')
    TEBI = Prefix('tebi', 'Ti', pow(2, 40), OM.NAMESPACE+'tebi')
    PEBI = Prefix('pebi', 'Pi', pow(2, 50), OM.NAMESPACE+'pebi')
    EXBI = Prefix('exbi', 'Ei', pow(2, 60), OM.NAMESPACE+'exbi')
    ZEBI = Prefix('zebi', 'Zi', pow(2, 70), OM.NAMESPACE+'zebi')
    YOBI = Prefix('yobi', 'Yi', pow(2, 80), OM.NAMESPACE+'yobi')


class JEDEC:
    KILO = Prefix('kilo', 'k', pow(2, 10), OM.NAMESPACE+'jedec-kilo')
    MEGA = Prefix('mega', 'M', pow(2, 20), OM.NAMESPACE+'jedec-mega')
    GIGA = Prefix('giga', 'G', pow(2, 30), OM.NAMESPACE+'jedec-giga')