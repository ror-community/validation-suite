import argparse
import validate.validation as vt
import validate.schema as vs
import validate.utilities as u
from copy import deepcopy
import os
import sys
import json
import pathlib

def set_args():
    parser = argparse.ArgumentParser(
                    description="Script to validate ROR files")
    parser.add_argument('-i', '--input', help='Path to one file or one directory for validation', required=True)
    parser.add_argument('-s', '--schema', help='Path or URL to schema')
    parser.add_argument('-p', '--file-path', help='Path to the rest of the files for relationship validation')
    args = parser.parse_args()
    return args

def run_validation_tests(file, path=None):
    try:
        with open(file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(e)
    validate = vt.Validate_Tests(data)
    validation_errors = validate.validate_all(file_path=path)
    return validation_errors

def print_errors(errors,validation_errors):
    for msg in errors:
        validation_errors = True
        for filename, err in msg.items():
            print("FOR FILE: ", filename)
            if isinstance(err, list):
                print("VALIDATION TEST ERRORS: \n")
                for e in err:
                    for loc, message in e.items():
                        print(f"In {loc}: {message}\n")
            else:
                print(f"SCHEMA ERROR:\n {err}")
    return validation_errors

def get_files(input):
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

def validate(input, path = None, schema = None):
    files = get_files(input)
    filename = ""
    validation_errors = False
    errors = []
    for f in files:
        messages = {}
        filename = os.path.basename(f).split(".")[0]
        valid = True
        valid, msg = vs.validate_file(f,schema)
        if valid:
            messages[filename] = run_validation_tests(f,path)
            if len(messages[filename]) == 0:
                messages[filename] = None
        else:
            messages[filename] = msg

        if messages[filename]:
            errors.append(deepcopy(messages))

    if len(errors) > 0:
        validation_errors = print_errors(errors, validation_errors)

    if validation_errors:
        exit(1)
    else:
        print("VALID")
        exit(0)

def validate2(input, path = None, schema = None):
    files = get_files(input)
    filename = ""
    validation_errors = False
    errors = []
    for f in files:
        messages = {}
        filename = os.path.basename(f).split(".")[0]
        valid, msg = vs.validate_file(f,schema)
        if valid:
            messages[filename] = run_validation_tests(f,path)
            if len(messages[filename]) == 0:
                messages[filename] = None
        else:
            messages[filename] = msg

        if messages[filename]:
            errors.append(deepcopy(messages))

    if len(errors) > 0:
        validation_errors = print_errors(errors, validation_errors)

    if validation_errors:
        exit(1)
    else:
        print("VALID")
        exit(0)

def main():
    args = set_args()
    schema = args.schema if args.schema else None
    path = os.path.normpath(args.file_path) if args.file_path else None
    validate(args.input, path, schema)


if __name__ == "__main__":
    main()
