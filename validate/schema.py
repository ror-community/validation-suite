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

def validate_file(file,schema):
    """ checks if schema is sent and if so, retrieving the schema depending on its type and validating the file against it"""
    
    if schema:
        stype = schema_type(schema)
    arg_exists(file)
    valid = False
    schema = get_file_from_url() if schema is None else get_json(schema,stype)
    msg = None
    json = get_json(file)
    try:
        validate(instance = json, schema = schema)
    except jsonschema.exceptions.ValidationError as err:
        msg = err
    valid = False if msg else True
    return valid, msg
