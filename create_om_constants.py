import os

from rdflib import Graph, URIRef

from omlib.constants import OM_IDS


def load_OM():
    app_path = os.path.dirname(os.path.abspath(__file__))
    om_path = os.path.join(app_path, "omlib/rdf/om-2.0.rdf")
    om = Graph()
    om.parse(om_path)
    return om


def __add_property_to_dict(dict, propertyKey, value):
    if value is not None:
        if propertyKey in dict:
            existing_value = dict[propertyKey]
            if isinstance(existing_value, list):
                if value not in existing_value:
                    existing_value.append(value)
            else:
                if existing_value != value:
                    existing_value = [existing_value, value]
            dict[propertyKey] = existing_value
        else:
            dict[propertyKey] = value
    return dict


def define_units(om_graph):
    sparql = """
        PREFIX :<http://www.ontology-of-units-of-measure.org/resource/om-2/>
        PREFIX owl:<http://www.w3.org/2002/07/owl#>
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
        PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX om:<http://www.ontology-of-units-of-measure.org/resource/om-2/>

        SELECT * WHERE {
            ?instance a ?class.
            ?class rdfs:subClassOf* om:Unit.
            OPTIONAL { ?instance rdfs:label ?label. }
            OPTIONAL { ?instance om:alternativeLabel ?altLabel. }
            OPTIONAL { ?instance om:symbol ?symbol. }
            OPTIONAL { ?instance om:alternativeSymbol ?altSymbol. }
            OPTIONAL { ?instance om:hasPrefix ?prefix. }
            OPTIONAL { ?instance om:hasFactor ?factor. }
            OPTIONAL { ?instance om:hasUnit ?baseUnit. }
            OPTIONAL { ?instance om:hasTerm1 ?multiplier. }
            OPTIONAL { ?instance om:hasTerm2 ?multiplicand. }
            OPTIONAL { ?instance om:hasNumerator ?numerator. }
            OPTIONAL { ?instance om:hasDenominator ?denominator. }
            OPTIONAL { ?instance om:hasBase ?exponentBase. }
            OPTIONAL { ?instance om:hasExponent ?exponent. }
            OPTIONAL { 
                ?instance om:hasDimension ?dimension. 
                ?dimension om:hasSITimeDimensionExponent ?timeDimExp.
                ?dimension om:hasSILengthDimensionExponent ?lengthDimExp.
                ?dimension om:hasSIMassDimensionExponent ?massDimExp.
                ?dimension om:hasSIElectricCurrentDimensionExponent ?electricCurrentDimExp.
                ?dimension om:hasSIThermodynamicTemperatureDimensionExponent ?thermodynamicTemperatureDimExp.
                ?dimension om:hasSIAmountOfSubstanceDimensionExponent ?amountOfSubstanceDimExp.
                ?dimension om:hasSILuminousIntensityDimensionExponent ?luminousIntensityDimExp.
            }
        }"""
    results = om_graph.query(sparql)
    all_units_dict = dict()
    for row in results:
        unit_dict = None
        if row.instance in all_units_dict:
            unit_dict = all_units_dict[row.instance]
        else:
            unit_dict = dict()
        unit_dict = __add_property_to_dict(unit_dict, "class", row['class'])
        unit_dict = __add_property_to_dict(unit_dict, "label", row.label)
        unit_dict = __add_property_to_dict(unit_dict, "altLabel", row.altLabel)
        unit_dict = __add_property_to_dict(unit_dict, "symbol", row.symbol)
        unit_dict = __add_property_to_dict(unit_dict, "altSymbol", row.altSymbol)
        unit_dict = __add_property_to_dict(unit_dict, "prefix", row.prefix)
        unit_dict = __add_property_to_dict(unit_dict, "factor", row.factor)
        unit_dict = __add_property_to_dict(unit_dict, "baseUnit", row.baseUnit)
        unit_dict = __add_property_to_dict(unit_dict, "multiplier", row.multiplier)
        unit_dict = __add_property_to_dict(unit_dict, "multiplicand", row.multiplicand)
        unit_dict = __add_property_to_dict(unit_dict, "multiplier", row.multiplier)
        unit_dict = __add_property_to_dict(unit_dict, "numerator", row.numerator)
        unit_dict = __add_property_to_dict(unit_dict, "denominator", row.denominator)
        unit_dict = __add_property_to_dict(unit_dict, "exponentBase", row.exponentBase)
        unit_dict = __add_property_to_dict(unit_dict, "exponent", row.exponent)
        unit_dict = __add_property_to_dict(unit_dict, "timeDimExp", row.timeDimExp)
        unit_dict = __add_property_to_dict(unit_dict, "lengthDimExp", row.lengthDimExp)
        unit_dict = __add_property_to_dict(unit_dict, "massDimExp", row.massDimExp)
        unit_dict = __add_property_to_dict(unit_dict, "electricCurrentDimExp", row.electricCurrentDimExp)
        unit_dict = __add_property_to_dict(unit_dict, "thermodynamicTemperatureDimExp",
                                           row.thermodynamicTemperatureDimExp)
        unit_dict = __add_property_to_dict(unit_dict, "amountOfSubstanceDimExp", row.amountOfSubstanceDimExp)
        unit_dict = __add_property_to_dict(unit_dict, "luminousIntensityDimExp", row.luminousIntensityDimExp)
        all_units_dict[row.instance] = unit_dict
    return all_units_dict


def __determine_order(all_units_dict):
    # Units may depend on each other, the dependants should be defined later.
    order = []
    todo = []
    keys = all_units_dict.keys()
    gram = str(OM_IDS.NAMESPACE + 'gram')
    for ident in keys:
        todo.append(ident)
    while len(todo) > 0:
        for ident in todo:
            ident_str = str(ident)
            unit_dict = all_units_dict[ident]
            all_parents = True
            if 'baseUnit' in unit_dict:
                base_unit = unit_dict['baseUnit']
                if base_unit not in order:
                    all_parents = False
            if 'multiplier' in unit_dict:
                multiplier = unit_dict['multiplier']
                if multiplier not in order:
                    all_parents = False
            if ident_str == gram:
                all_parents = True
            if all_parents:
                order.append(ident)
                todo.remove(ident)
    return order


def __get_preferred_label(label_list):
    label = None
    if isinstance(label_list, list):
        for temp in label_list:
            if temp.language == 'en':
                label = temp
                break
            if temp.language is None and label is None:
                label = temp
    else:
        label = label_list
    label = label.value
    return label


def __remove_quotes(object):
    if object is None:
        return None
    result = None
    if isinstance(object, list):
        result = "["
        for item in object:
            string = None
            if isinstance(item, URIRef):
                string = item.value
            else:
                string = str(item)
            string = str.replace("'", "\\'")
            string = str.replace('"', '\\"')
            if len(result) > 1:
                result += ', '
            result += "'" + string + "'"
        result += "]"
    else:
        string = None
        if isinstance(object, URIRef):
            string = object.value
        else:
            string = str(object)
            string = str.replace("'", "\\'")
            string = str.replace('"', '\\"')
        result = "'" + string + "'"
    return result


def create_singular_unit_in_file(identifier, unit_dict, file_contents):
    label = None
    if 'label' in unit_dict:
        label = unit_dict['label']
    symbol = None
    if 'symbol' in unit_dict:
        symbol = unit_dict['symbol']
    if label is not None and not isinstance(label, list):
        label = "'" + label + "'"
    if symbol is not None and not isinstance(symbol, list):
        symbol = "'" + symbol + "'"
    py_name = os.path.basename(os.path.normpath(identifier))
    py_name = py_name.replace('-', '')
    label = __remove_quotes(label)
    symbol = __remove_quotes(symbol)
    if 'baseUnit' in unit_dict:
        base_unit = unit_dict['baseUnit']
        factor = 1.0
        if 'factor' in unit_dict:
            factor = unit_dict['factor'].value
        else:
            pass
        line = "    {} = Unit.get_singular_unit({}, {}, base_unit='{}', factor={}, identifier='{}')\n".format(py_name,
                                                                                                              label,
                                                                                                              symbol,
                                                                                                              base_unit,
                                                                                                              factor,
                                                                                                              identifier)
        file_contents = file_contents + line
    else:
        pass
    return file_contents


def create_prefixed_unit_in_file(identifier, unit_dict, file_contents):
    return file_contents


def create_all_units_in_file(all_units_dict, file_contents):
    ids = __determine_order(all_units_dict)
    for ident in ids:
        unit_dict = all_units_dict[ident]
        unit_classes = unit_dict['class']
        singular_unit = URIRef(OM_IDS.NAMESPACE + 'SingularUnit')
        prefixed_unit = URIRef(OM_IDS.NAMESPACE + 'PrefixedUnit')
        unit_multiple = URIRef(OM_IDS.NAMESPACE + 'UnitMultiple')
        unit_multiplication = URIRef(OM_IDS.NAMESPACE + 'UnitMultiplication')
        unit_division = URIRef(OM_IDS.NAMESPACE + 'UnitDivision')
        unit_exponentiation = URIRef(OM_IDS.NAMESPACE + 'UnitExponentiation')
        if prefixed_unit in unit_classes:
            file_contents = create_prefixed_unit_in_file(ident, unit_dict, file_contents)
        else:
            if unit_multiple in unit_classes:
                file_contents = create_prefixed_unit_in_file(ident, unit_dict, file_contents)
            else:
                if unit_multiplication in unit_classes:
                    file_contents = create_prefixed_unit_in_file(ident, unit_dict, file_contents)
                else:
                    if unit_division in unit_classes:
                        file_contents = create_prefixed_unit_in_file(ident, unit_dict, file_contents)
                    else:
                        if unit_exponentiation in unit_classes:
                            file_contents = create_prefixed_unit_in_file(ident, unit_dict, file_contents)
                        else:
                            file_contents = create_singular_unit_in_file(ident, unit_dict, file_contents)
    return file_contents


if __name__ == '__main__':
    graph = load_OM()
    all_units_dict = define_units(graph)
    file_contents = """
import rdflib
from omlib.constants import OM_IDS
from rdflib import URIRef
from omlib.dimension import Dimension
from omlib.scale import Scale
from omlib.unit import Prefix, Unit

class OM:
    NAMESPACE = OM_IDS.NAMESPACE
    
"""
    file_contents = create_all_units_in_file(all_units_dict, file_contents)
    print(file_contents)
    app_path = os.path.dirname(os.path.abspath(__file__))
    om_path = os.path.join(app_path, "omlib/om-constants.py")
    file = open(om_path, 'w')
    file.write(file_contents)
    file.close()
    pass
