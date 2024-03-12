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
from zipfile import ZipFile, ZIP_DEFLATED

ERROR_LOG = "validation_errors.log"
logging.basicConfig(filename=ERROR_LOG,level=logging.WARNING, filemode='w')

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
    parser.add_argument('-d', '--domains', help='Validate domains against prod and release files', action='store_true', default=False)
    args = parser.parse_args()
    return args

def run_validation_tests(record, version, check_address, check_domains, path=None, rel_file=None):
    """Runs validation tests on a json record"""
    if version == '1':
        validate = vt.Validate_Tests(record)
        validation_errors = validate.validate_all(check_address, file_path=path, rel_file=rel_file)
        validation_warnings = []
    if version == '2':
        validate = vt.Validate_Tests_V2(record)
        validation_errors, validation_warnings = validate.validate_all(check_address, check_domains, file_path=path, rel_file=rel_file)
    return validation_errors, validation_warnings

def print_warnings(warnings, validation_warnings):
    """Printing all warnings picked up through the tests"""
    for msg in warnings:
        validation_warnings = True
        for filename, err in msg.items():
            logging.warning(f"FOR FILE: {filename}")
            if isinstance(err, list):
                logging.warning("VALIDATION TEST WARNINGS:")
                for e in err:
                    for loc, message in e.items():
                        logging.warning(f"In {loc}: {message}")
    return validation_warnings

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

def validate_dump(input, version, check_address, check_domains, rel_file = None, path = None, schema = None):
    """Runs the files against the schema validator and the class that checks the usecases"""
    validation_errors = False
    validation_warnings = False
    errors = []
    warnings = []
    '''
    if (rel_file and not(path)):
        raise AttributeError(f"Relationship file: {rel_file} must be passed with a --file-path argument which is a path to the rest of the files for relationship validation")
    elif (rel_file and path):
        u.arg_exists(rel_file)
    '''
    dump_unzipped = None
    records = []
    with ZipFile(input, "r") as zf:
        json_files_count = sum('.json' in s for s in zf.namelist())
        if json_files_count > 0:
            if version == '2':
                filenames = [name for name in zf.namelist() if 'ror-data_schema_v2.json' in name]
                if len(filenames) == 1:
                    dump_unzipped = zf.extract(filenames[0], '.')
                else:
                    print("Dump zip contains multiple schema_v2.json files. Something is wrong.")
            else:
                filenames = [name for name in zf.namelist() if 'ror-data.json' in name]
                if len(filenames) == 1:
                    dump_unzipped = zf.extract(filenames[0], '.')
                else:
                    print("Dump zip contains multiple ror_data.json files. Something is wrong.")
        else:
            print("Dump zip contains no json files. Something is wrong.")

    records = u.get_json(dump_unzipped)

    for r in records:
        messages = {}
        file_errors = {}
        file_warnings = {}
        record_name  = r['id'].split("https://ror.org/")[1]
        valid = True
        valid, msg = vs.validate_record(r,schema,version)
        if valid:
            print("schema valid")
            file_errors[record_name], file_warnings[record_name] = run_validation_tests(r, version, check_address, check_domains, path, rel_file)
            if len(file_errors[record_name]) == 0:
                file_errors[record_name] = None
            if len(file_warnings[record_name]) == 0:
                file_warnings[record_name] = None
        else:
            print("NOT schema valid")
            file_errors[record_name] = msg

        if file_errors[record_name]:
            errors.append(deepcopy(file_errors))
        if file_warnings[record_name]:
            warnings.append(deepcopy(file_warnings))

    if len(errors) > 0:
        validation_errors = print_errors(errors, validation_errors)

    if len(warnings) > 0:
        validation_warnings = print_warnings(warnings)

    if validation_errors:
        with open(ERROR_LOG, 'r') as f:
            print(f.read())
        sys.exit(1)
    else:
        if validation_warnings:
            with open(ERROR_LOG, 'r') as f:
                print(f.read())
        sys.exit(0)


def validate_files(input, version, check_address, check_domains, rel_file = None, path = None, schema = None):
    """Runs the files against the schema validator and the class that checks the usecases"""
    files = get_files(input)
    filename = ""
    validation_errors = False
    validation_warnings = False
    errors = []
    warnings = []

    if (rel_file and not(path)):
        raise AttributeError(f"Relationship file: {rel_file} must be passed with a --file-path argument which is a path to the rest of the files for relationship validation")
    elif (rel_file and path):
        u.arg_exists(rel_file)

    for f in files:
        file_errors = {}
        file_warnings = {}
        filename = os.path.basename(f).split(".")[0]
        u.arg_exists(f)
        record = u.get_json(f)
        valid = True
        valid, schema_val_errors = vs.validate_record(record, schema,version)
        if valid:
            print("schema valid")
            file_errors[filename], file_warnings[filename] = run_validation_tests(record, version, check_address, check_domains, path, rel_file)
            if len(file_errors[filename]) == 0:
                file_errors[filename] = None
            if len(file_warnings[filename]) == 0:
                file_warnings[filename] = None
        else:
            print("NOT schema valid")
            file_errors[filename] = schema_val_errors
            file_warnings[filename] = None

        if file_errors[filename]:
            errors.append(deepcopy(file_errors))
        if file_warnings[filename]:
            warnings.append(deepcopy(file_warnings))

    if len(errors) > 0:
        validation_errors = print_errors(errors, validation_errors)

    if len(warnings) > 0:
        validation_warnings = print_warnings(warnings, validation_warnings)

    if validation_errors:
        with open(ERROR_LOG, 'r') as f:
            print(f.read())
        sys.exit(1)
    else:
        if validation_warnings:
            with open(ERROR_LOG, 'r') as f:
                print(f.read())
        sys.exit(0)

def main():
    args = set_args()
    schema = args.schema if args.schema else None
    rel_file = os.path.normpath(args.rel_file) if args.rel_file else None
    path = os.path.normpath(args.file_path) if args.file_path else None
    version  = args.schema_version
    check_address = True
    check_domains = False
    if args.no_geonames:
        check_address = False
    if args.domains:
        check_domains = True
    if os.path.splitext(args.input)[1] == '.zip':
        # do not attempt to validate relationships or addresses in dump
        check_address = False
        check_domains = False
        rel_file = None
        path = None
        validate_dump(args.input, version, check_address, check_domains, rel_file, path, schema)
    else:
        validate_files(args.input, version, check_address, check_domains, rel_file, path, schema)


if __name__ == "__main__":
    main()
