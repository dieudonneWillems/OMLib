from omlib.exceptions.dimensionexception import DimensionalException
from omlib.constants import OM, SI
from omlib.dimension import Dimension
from omlib.unit import Unit, PrefixedUnit, SingularUnit, UnitMultiple, UnitDivision

if __name__ == '__main__':
    print('This is the Python library for applying the Ontology of Units of Measure (OM).')
    unit = Unit('metre', 'm')
    unit.add_preferred_label('meter', 'nl')
    print('Created unit {} with symbol {}'.format(unit.prefLabels, unit.symbols))
    print('\tDutch name: {}'.format(unit.preferred_label('nl')))

    time_dim = Dimension(1, 0, 0, 0, 0, 0, 0)
    print('Created time dimension: {}'.format(time_dim))

    dim1 = Dimension(1, 0, 3, 0, 2, 1, 0)
    dim2 = Dimension(1, 0, 3, 0, 2, 1, 0)
    print('Compare dimensions: {} =?= {} {}'.format(time_dim, dim2, time_dim == dim2))
    print('Compare dimensions: {} =?= {} {}'.format(dim1, dim2, dim1 == dim2))

    dim3 = dim1 + dim2
    print('Added dimensions: {}'.format(dim3))
    try:
        dim4 = time_dim + dim2
        print('Added dimensions: {}'.format(dim4))
    except DimensionalException as error:
        print(error)
    try:
        dim4 = time_dim - dim2
        print('Subtracted dimensions: {}'.format(dim4))
    except DimensionalException as error:
        print(error)

    dim4 = dim1 * dim2
    print('Multiplied dimensions: {}'.format(dim4))
    dim5 = time_dim / dim2
    print('Divided dimensions: {}'.format(dim5))

    m = SingularUnit('metre', 'm', Dimension(0, 1, 0, 0, 0, 0, 0), identifier=OM.NAMESPACE + 'metre')
    print('Singular Unit: {}'.format(m))
    km = PrefixedUnit(SI.KILO, m, OM.NAMESPACE + 'kilometre')
    print('Prefixed Unit: {}'.format(km))
    km100 = UnitMultiple(km, 100.0, symbol='100km')
    print('Unit Multiple: {}'.format(km100))

    mpkm = UnitDivision(m, km)
    print('Unit Division: {}'.format(mpkm))


