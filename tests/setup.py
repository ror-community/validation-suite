import pytest
import os
import sys
import subprocess

def valid_input(version):
    if version == '1':
        return ["tests/fixtures/v1/valid/015m7wh34.json","tests/fixtures/valid/v1"]
    if version == '2':
        return ["tests/fixtures/v2/valid/015m7wh34.json","tests/fixtures/valid/v2"]

def valid_file_path(version):
    if version == '1':
        return "tests/fixtures/v1/valid"
    if version == '2':
        return "tests/fixtures/v2/valid"

def schema_fixture(version):
    if version == '1':
        return "tests/fixtures/v1/schema/ror_schema.json"
    if version == '2':
        return "tests/fixtures/v2/schema/ror_schema.json"

def fixture_file_schema():
    if version == '1':
        return "tests/fixtures/v1/invalid/schema-issues/skeleton.json"
    if version == '2':
        return "tests/fixtures/v2/invalid/schema-issues/skeleton.json"

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

def run_args(required_args, optional_args = []):
    print("REQUIRED ARGS")
    print(required_args)
    print("OPTIONAL ARGS")
    print(optional_args)
    command = [*invocation(), *required_args, *optional_args]
    out, err, exitcode = capture(command)
    print(out)
    print(err)
    return out, err, exitcode
