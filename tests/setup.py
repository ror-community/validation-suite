import pytest
import os
import sys
import subprocess

def valid_input():
    return ["tests/fixtures/valid/015m7wh34.json","tests/fixtures/valid"]

def valid_file_path():
    return "tests/fixtures/valid"

def schema_fixture():
    return "tests/fixtures/schema/v1/ror_schema.json"

def fixture_file_schema():
    return "tests/fixtures/invalid/schema-issues/skeleton.json"

def invocation(arg = "-i"):
    return ["python", "run_validations.py", "--no-geonames", arg]

def capture(command):
    process = subprocess.run(command, capture_output=True, encoding="utf-8")
    return process.stdout, process.stderr, process.returncode

def flatten(nested_list):
    return [final_list for t in nested_list for final_list in t]

def run_optional_args(**optional_args):
    # returns a list of optional arguments
    # concatenates the hyphen before the argument
    # to mimic the actual invocation
    if optional_args:
        altered_keys = ["-" + k for k in optional_args.keys()]
        fixed_args = dict(zip(altered_keys, list(optional_args.values())))
        return flatten(list(fixed_args.items()))

def run_args(input, optional_args = []):
    command = [*invocation(), input, *optional_args]
    out, err, exitcode = capture(command)
    return out, err, exitcode
