import argparse
import validate.validation as vt
import validate.schema as vs
import validate.utilities as u
from copy import deepcopy
import os
import sys
import json
import pathlib
import logging

ERROR_LOG = "validation_errors.log"
logging.basicConfig(filename=ERROR_LOG,level=logging.ERROR, filemode='w')

def set_args():
    """CLI"""
    parser = argparse.ArgumentParser(
                    description="Script to validate ROR files")
    parser.add_argument('-i', '--input', help='Path to one file or one directory for validation', required=True)
    parser.add_argument('-s', '--schema', help='Path or URL to schema')
    parser.add_argument('-p', '--file-path', help='Path to the rest of the files for relationship validation')
    parser.add_argument('-f', '--rel-file', help='Path to the file containing relationship mappings')
    parser.add_argument('-v', '--schema-version', help='ROR schema version to validate against (1 or 2)', required=True, choices=['1', '2'])
    parser.add_argument('-n', '--no-geonames', help='Skip Geonames API validation for address fields', action='store_true')
    args = parser.parse_args()
    return args

def run_validation_tests(file, version, check_address, path=None, rel_file=None):
    """Runs validation tests on a file"""
    try:
        with open(file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        raise(e)
    if version == '1':
        validate = vt.Validate_Tests(data)
    if version == '2':
        validate = vt.Validate_Tests_V2(data)
    validation_errors = validate.validate_all(check_address, file_path=path, rel_file=rel_file)
    return validation_errors

def print_errors(errors,validation_errors):
    """Printing all errors picked up through the tests"""
    for msg in errors:
        validation_errors = True
        for filename, err in msg.items():
            logging.error(f"FOR FILE: {filename}")
            if isinstance(err, list):
                logging.error("VALIDATION TEST ERRORS:")
                for e in err:
                    for loc, message in e.items():
                        logging.error(f"In {loc}: {message}")
            else:
                logging.error("SCHEMA ERROR:")
                logging.error(err)
    return validation_errors

def get_files(input):
    """Gathers files or files in a directory for processing"""
    files = []
    if os.path.isfile(input):
        files.append(input)
    elif os.path.isdir(input):
        file = []
        path = os.path.normpath(input)
        for f in os.listdir(input):
            file.append(f)
        files = list(map(lambda x: path+"/"+x, file))
    else:
        raise RuntimeError(f"{input} must be a valid file or directory")
    return files

def validate(input, version, check_address, rel_file = None, path = None, schema = None):
    """Runs the files against the schema validator and the class that checks the usecases"""
    files = get_files(input)
    filename = ""
    validation_errors = False
    errors = []

    if (rel_file and not(path)):
        raise AttributeError(f"Relationship file: {rel_file} must be passed with a --file-path argument which is a path to the rest of the files for relationship validation")
    elif (rel_file and path):
        u.arg_exists(rel_file)

    for f in files:
        messages = {}
        filename = os.path.basename(f).split(".")[0]
        valid = True
        valid, msg = vs.validate_file(f,schema,version)
        if valid:
            print("schema valid")
            messages[filename] = run_validation_tests(f, version, check_address, path, rel_file)
            if len(messages[filename]) == 0:
                messages[filename] = None
        else:
            print("NOT schema valid")
            messages[filename] = msg

        if messages[filename]:
            errors.append(deepcopy(messages))

    if len(errors) > 0:
        validation_errors = print_errors(errors, validation_errors)

    if validation_errors:
        with open(ERROR_LOG, 'r') as f:
            print(f.read())
        sys.exit(1)
    else:
        sys.exit(0)

def main():
    args = set_args()
    schema = args.schema if args.schema else None
    rel_file = os.path.normpath(args.rel_file) if args.rel_file else None
    path = os.path.normpath(args.file_path) if args.file_path else None
    version  = args.schema_version
    check_address = True
    if args.no_geonames:
        check_address = False

    validate(args.input, version, check_address, rel_file, path, schema)

if __name__ == "__main__":
    main()
