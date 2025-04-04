import pytest
import os
import sys
import subprocess

def valid_input(version):
    if version == '1':
        return ["tests/fixtures/v1/valid/015m7wh34.json","tests/fixtures/v1/valid"]
    if version == '2':
        return ["tests/fixtures/v2_1/valid/example_record_v2_1.json","tests/fixtures/v2_1/valid"]

def valid_file_path(version):
    if version == '1':
        return "tests/fixtures/v1/valid/"
    if version == '2':
        return "tests/fixtures/v2_1/valid/"

def invalid_file_path(version):
    if version == '1':
        return "tests/fixtures/v1/invalid/"
    if version == '2':
        return "tests/fixtures/v2_1/invalid/"

def invalid_sub_folders():
    dirs = {"missing_fields": "missing_fields/",
            "enum_values": "enum_values/",
            "usecase_issues": "usecase_issues/",
            "missing_properties": "missing_properties/",
            "value_formats": "value_formats/"}
    return dirs

def schema_fixture(version):
    if version == '1':
        return "tests/fixtures/v1/schema/ror_schema.json"
    if version == '2':
        return "tests/fixtures/v2_1/schema/ror_schema_v2_1.json"

def invocation():
    return ["python", "run_validations.py"]

def capture(command):
    process = subprocess.run(command, capture_output=True, encoding="utf-8")
    return process.stdout, process.stderr, process.returncode

def flatten(nested_list):
    return [final_list for t in nested_list for final_list in t]

def format_required_args(input_file, version):
    # returns a list of required arguments
    # concatenates the hyphen before the argument
    # to mimic the actual invocation
    return ["-i", input_file, "-v", version]

def format_optional_args(**optional_args):
    # returns a list of optional arguments
    # concatenates the hyphen before the argument
    # to mimic the actual invocation
    if optional_args:
        altered_keys = ["-" + k for k in optional_args.keys()]
        fixed_args = dict(zip(altered_keys, list(optional_args.values())))
        return flatten(list(fixed_args.items()))

def run_args(required_args, optional_args = [], nogeonames=True):
    command = [*invocation(), *required_args, *optional_args]
    if nogeonames:
        command.append("--no-geonames")
    out, err, exitcode = capture(command)
    print(out)
    print(err)
    return out, err, exitcode
