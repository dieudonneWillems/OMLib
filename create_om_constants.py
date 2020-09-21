import os
from datetime import datetime

from rdflib import Graph, URIRef, Literal


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
            ?class rdfs:subClassOf* ?superClass.
            OPTIONAL {
                ?system om:hasBaseUnit ?instance.
                BIND (true AS ?isBaseUnit)
            }
            OPTIONAL {
                ?system om:hasDerivedUnit ?instance.
                BIND (false AS ?isBaseUnit)
            }
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
        unit_dict = __add_property_to_dict(unit_dict, "class", row['superClass'])
        unit_dict = __add_property_to_dict(unit_dict, "system", row.system)
        unit_dict = __add_property_to_dict(unit_dict, "isBaseUnit", row.isBaseUnit)
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
    gram = str('http://www.ontology-of-units-of-measure.org/resource/om-2/gram')
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
            if 'multiplicand' in unit_dict:
                multiplicand = unit_dict['multiplicand']
                if multiplicand not in order:
                    all_parents = False
            if 'numerator' in unit_dict:
                numerator = unit_dict['numerator']
                if numerator not in order:
                    all_parents = False
            if 'denominator' in unit_dict:
                denominator = unit_dict['denominator']
                if denominator not in order:
                    all_parents = False
            if 'exponentBase' in unit_dict:
                exponent_base = unit_dict['exponentBase']
                if exponent_base not in order:
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
            string = "" + str(item)
            string = string.replace("'", "\\'")
            string = string.replace('"', '\\"')
            if isinstance(item, Literal):
                string = "Literal('" + string + "'"
                if item.language is not None:
                    string = string + ", lang='" + item.language + "')"
                else:
                    string = string + ")"
            else:
                string = "Literal('" + string + "')"
            if len(result) > 1:
                result += ', '
            result += string
        result += "]"
    else:
        string = str(object)
        string = string.replace("'", "\\'")
        string = string.replace('"', '\\"')
        if isinstance(object, Literal):
            string = "Literal('" + string + "'"
            if object.language is not None:
                string = string + ", lang='" + object.language + "')"
            else:
                string = string + ")"
        else:
            string = str(object)
            print(string)
            string = string.replace("'", "\\'")
            print(string)
            string = string.replace('"', '\\"')
            print(string)
            string = "Literal(" + string + ")"
            print(string)
        result = string
    return result


def __get_python_name(identifier):
    py_name = os.path.basename(os.path.normpath(identifier))
    py_name = py_name.replace('-', '')
    return py_name


def create_singular_unit_in_file(identifier, unit_dict, file_contents):
    label = None
    if 'label' in unit_dict:
        label = unit_dict['label']
    symbol = None
    if 'symbol' in unit_dict:
        symbol = unit_dict['symbol']
    py_name = __get_python_name(identifier)
    label = __remove_quotes(label)
    symbol = __remove_quotes(symbol)
    system = None
    is_base_unit = False
    if 'system' in unit_dict:
        system = unit_dict['system']
        if not isinstance(system, list):
            system = "'"+str(system)+"'"
        else:
            system = str(system)
    if 'isBaseUnit' in unit_dict:
        is_base_unit = unit_dict['isBaseUnit'].value
    if 'baseUnit' in unit_dict and not str(identifier) == str('http://www.ontology-of-units-of-measure.org/resource/om-2/gram'):
        base_unit = unit_dict['baseUnit']
        base_py_name = __get_python_name(base_unit)
        factor = 1.0
        if 'factor' in unit_dict:
            factor = unit_dict['factor'].value
        else:
            pass
        line = "    {} = Unit.get_singular_unit({}, {}, base_unit={}, factor={}, identifier='{}', system_of_units={}, is_base_unit={})\n".format(py_name, label, symbol, base_py_name, factor, identifier, system, is_base_unit)
        file_contents = file_contents + line
    else:
        dimension = "Dimension("
        if 'timeDimExp' in unit_dict:
            dimension += "" + str(unit_dict['timeDimExp'].value) + ", "
        else:
            dimension += "0, "
        if 'lengthDimExp' in unit_dict:
            dimension += "" + str(unit_dict['lengthDimExp'].value) + ", "
        else:
            dimension += "0, "
        if 'massDimExp' in unit_dict:
            dimension += "" + str(unit_dict['massDimExp'].value) + ", "
        else:
            dimension += "0, "
        if 'electricCurrentDimExp' in unit_dict:
            dimension += "" + str(unit_dict['electricCurrentDimExp'].value) + ", "
        else:
            dimension += "0, "
        if 'thermodynamicTemperatureDimExp' in unit_dict:
            dimension += "" + str(unit_dict['thermodynamicTemperatureDimExp'].value) + ", "
        else:
            dimension += "0, "
        if 'amountOfSubstanceDimExp' in unit_dict:
            dimension += "" + str(unit_dict['amountOfSubstanceDimExp'].value) + ", "
        else:
            dimension += "0, "
        if 'luminousIntensityDimExp' in unit_dict:
            dimension += "" + str(unit_dict['luminousIntensityDimExp'].value)
        else:
            dimension += "0"
        dimension += ")"
        line = "    {} = Unit.get_singular_unit({}, {}, {}, identifier='{}', system_of_units={}, is_base_unit={})\n".format(py_name, label, symbol, dimension,  identifier, system, is_base_unit)
        file_contents = file_contents + line
    return file_contents


def create_prefixed_unit_in_file(identifier, unit_dict, file_contents):
    if 'prefix' in unit_dict:
        prefix = unit_dict['prefix']
        system = None
        is_base_unit = False
        if isinstance(prefix, URIRef):
            prefix = str(prefix)
        if 'system' in unit_dict:
            system = unit_dict['system']
            if not isinstance(system, list):
                system = "'"+str(system)+"'"
            else:
                system = str(system)
        if 'isBaseUnit' in unit_dict:
            is_base_unit = unit_dict['isBaseUnit'].value
        py_name = __get_python_name(identifier)
        base_unit = unit_dict['baseUnit']
        base_py_name = __get_python_name(base_unit)
        line = "    {} = Unit.get_prefixed_unit('{}', base_unit={}, identifier='{}', system_of_units={}, is_base_unit={})\n".format(py_name, prefix, base_py_name, identifier, system, is_base_unit)
        file_contents = file_contents + line
    return file_contents


def create_unit_multiple_in_file(identifier, unit_dict, file_contents):
    py_name = __get_python_name(identifier)
    base_unit = unit_dict['baseUnit']
    base_py_name = __get_python_name(base_unit)
    label = None
    if 'label' in unit_dict:
        label = unit_dict['label']
    symbol = None
    if 'symbol' in unit_dict:
        symbol = unit_dict['symbol']
    label = __remove_quotes(label)
    symbol = __remove_quotes(symbol)
    factor = 1.0
    if 'factor' in unit_dict:
        factor = unit_dict['factor'].value
    else:
        pass
    system = None
    if 'system' in unit_dict:
        system = unit_dict['system']
        if not isinstance(system, list):
            system = "'"+str(system)+"'"
        else:
            system = str(system)
    line = "    {} = Unit.get_unit_multiple({}, factor={}, identifier='{}', label={}, symbol={}, system_of_units={})\n".format(py_name, base_py_name, factor, identifier, label, symbol, system)
    file_contents = file_contents + line
    return file_contents


def create_unit_multiplication_in_file(identifier, unit_dict, file_contents):
    py_name = __get_python_name(identifier)
    multiplier = unit_dict['multiplier']
    multiplier_py_name = __get_python_name(multiplier)
    multiplicand = unit_dict['multiplicand']
    multiplicand_py_name = __get_python_name(multiplicand)
    system = None
    if 'system' in unit_dict:
        system = unit_dict['system']
        if not isinstance(system, list):
            system = "'"+str(system)+"'"
        else:
            system = str(system)
    line = "    {} = Unit.get_unit_multiplication({}, {}, identifier='{}', system_of_units={})\n".format(py_name, multiplier_py_name, multiplicand_py_name, identifier, system)
    file_contents = file_contents + line
    return file_contents


def create_unit_division_in_file(identifier, unit_dict, file_contents):
    py_name = __get_python_name(identifier)
    numerator = unit_dict['numerator']
    numerator_py_name = __get_python_name(numerator)
    denominator = unit_dict['denominator']
    denominator_py_name = __get_python_name(denominator)
    system = None
    if 'system' in unit_dict:
        system = unit_dict['system']
        if not isinstance(system, list):
            system = "'"+str(system)+"'"
        else:
            system = str(system)
    line = "    {} = Unit.get_unit_division({}, {}, identifier='{}', system_of_units={})\n".format(py_name, numerator_py_name, denominator_py_name, identifier, system)
    file_contents = file_contents + line
    return file_contents


def create_unit_exponentiation_in_file(identifier, unit_dict, file_contents):
    py_name = __get_python_name(identifier)
    base_unit = unit_dict['exponentBase']
    base_unit_py_name = __get_python_name(base_unit)
    exponent = unit_dict['exponent'].value
    system = None
    if 'system' in unit_dict:
        system = unit_dict['system']
        if not isinstance(system, list):
            system = "'"+str(system)+"'"
        else:
            system = str(system)
    line = "    {} = Unit.get_unit_exponentiation({}, {}, identifier='{}', system_of_units={})\n".format(py_name, base_unit_py_name, exponent, identifier, system)
    file_contents = file_contents + line
    return file_contents


def create_all_units_in_file(all_units_dict, file_contents):
    ids = __determine_order(all_units_dict)
    for ident in ids:
        unit_dict = all_units_dict[ident]
        unit_classes = unit_dict['class']
        singular_unit = URIRef('http://www.ontology-of-units-of-measure.org/resource/om-2/SingularUnit')
        prefixed_unit = URIRef('http://www.ontology-of-units-of-measure.org/resource/om-2/PrefixedUnit')
        unit_multiple = URIRef('http://www.ontology-of-units-of-measure.org/resource/om-2/UnitMultiple')
        unit_multiplication = URIRef('http://www.ontology-of-units-of-measure.org/resource/om-2/UnitMultiplication')
        unit_division = URIRef('http://www.ontology-of-units-of-measure.org/resource/om-2/UnitDivision')
        unit_exponentiation = URIRef('http://www.ontology-of-units-of-measure.org/resource/om-2/UnitExponentiation')
        if prefixed_unit in unit_classes:
            file_contents = create_prefixed_unit_in_file(ident, unit_dict, file_contents)
        else:
            if unit_multiple in unit_classes:
                file_contents = create_unit_multiple_in_file(ident, unit_dict, file_contents)
            else:
                if unit_multiplication in unit_classes:
                    file_contents = create_unit_multiplication_in_file(ident, unit_dict, file_contents)
                else:
                    if unit_division in unit_classes:
                        file_contents = create_unit_division_in_file(ident, unit_dict, file_contents)
                    else:
                        if unit_exponentiation in unit_classes:
                            file_contents = create_unit_exponentiation_in_file(ident, unit_dict, file_contents)
                        else:
                            file_contents = create_singular_unit_in_file(ident, unit_dict, file_contents)
    return file_contents


if __name__ == '__main__':
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    graph = load_OM()
    all_units_dict = define_units(graph)
    file_contents = """
import rdflib
from rdflib import URIRef, Literal
from omlib.dimension import Dimension
from omlib.scale import Scale
from omlib.unit import Prefix, Unit


class OM:

    NAMESPACE = 'http://www.ontology-of-units-of-measure.org/resource/om-2/'
    
"""
    file_contents = "# This file was automatically generated on " + date_time + ".\n" + file_contents
    file_contents = create_all_units_in_file(all_units_dict, file_contents)
    print(file_contents)
    app_path = os.path.dirname(os.path.abspath(__file__))
    om_path = os.path.join(app_path, "omlib/omconstants.py")
    file = open(om_path, 'w')
    file.write(file_contents)
    file.close()
    pass
