import json
import sys
import jsonschema
from jsonschema import validate
import validators
from validate.utilities import *

def schema_type(schema):
    if url_validation(schema):
        return "url"
    elif os.path.exists(schema):
        return "file"
    else:
        raise Exception(f"{schema} must either be a file or a url")

def get_fields(json):
    for key , value in json.items():
        yield key

def compare_fields(schema_fields, record_fields):
    missing_fields = []
    for schema_field in schema_fields:
        if schema_field not in record_fields:
            missing_fields.append(schema_field)
    return missing_fields

def check_missing_fields_v1(record, schema):
    missing_fields = []
    schema_fields = list(get_fields(schema.get('properties')))
    record_fields = list(get_fields(record))
    missing_fields.extend(compare_fields(schema_fields, record_fields))

    if "addresses" not in missing_fields:
        schema_address_fields = list(get_fields(schema['properties']['addresses']['items']['properties']))
        record_address_fields = list(get_fields(record['addresses'][0]))
        missing_fields.extend(compare_fields(schema_address_fields, record_address_fields))

        if "addresses" not in missing_fields and "geonames_city" not in missing_fields:
            schema_geonames_fields = list(get_fields(schema['properties']['addresses']['items']['properties']['geonames_city']['properties']))
            record_geonames_fields = list(get_fields(record['addresses'][0]['geonames_city']))
            missing_fields.extend(compare_fields(schema_geonames_fields, record_geonames_fields))

    return missing_fields

def check_missing_fields_v2(record, schema):
    missing_fields = []
    schema_fields = list(get_fields(schema.get('properties')))
    record_fields = list(get_fields(record))
    missing_fields.extend(compare_fields(schema_fields, record_fields))

    if "locations" not in missing_fields:
        schema_address_fields = list(get_fields(schema['properties']['locations']['items']['properties']))
        record_address_fields = list(get_fields(record['locations'][0]))
        missing_fields.extend(compare_fields(schema_address_fields, record_address_fields))

        if "geonames_details" not in missing_fields:
            schema_geonames_fields = list(get_fields(schema['properties']['locations']['items']['properties']['geonames_details']['properties']))
            record_geonames_fields = list(get_fields(record['locations'][0]['geonames_details']))
            missing_fields.extend(compare_fields(schema_geonames_fields, record_geonames_fields))

    return missing_fields

def validate_record(record,schema,version):
    """ checks if schema is sent and if so, retrieving the schema depending on its type and validating the file against it"""

    if schema:
        stype = schema_type(schema)
    valid = False
    schema = get_schema_from_url(version) if schema is None else get_json(schema,stype)
    msg = None
    if version == '1':
        missing_fields = check_missing_fields_v1(record, schema)
    if version == '2':
        missing_fields = check_missing_fields_v2(record, schema)
    if len(missing_fields) == 0:
        try:
            validate(instance = record, schema = schema, format_checker=jsonschema.FormatChecker())
        except jsonschema.exceptions.ValidationError as err:
            msg = err
    else:
        msg = "File is missing field(s): " + ", ".join(missing_fields)
    valid = False if msg else True
    return valid, msg