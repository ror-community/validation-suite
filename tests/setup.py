import pytest
import os
import sys
import subprocess

# TODO: invocation becomes its own function that can be used everywhere

# TODO: Invalid types of inputs, i.e. various types of schema invalidations, various types of validation test failures. Cover all use cases

def valid_input():
    return ["tests/fixtures/valid/015m7wh34.json","tests/fixtures/valid"]

def valid_file_path():
    return "tests/fixtures/valid"

def schema_fixture():
    return "tests/fixtures/schema/v1/ror_schema.json"

def capture(command):
    proc = subprocess.Popen(command,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
    )
    out,err = proc.communicate()
    return out, err, proc.returncode

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
    invocation = ["python", "run_validations.py","-i"]
    command = [*invocation, input, *optional_args]
    out, err, exitcode = capture(command)
    return out, err, exitcode

def valid_input():
    return ["tests/fixtures/valid/015m7wh34.json","tests/fixtures/valid"]

def valid_file_path():
    return "tests/fixtures/valid"

def schema_fixture():
    return "tests/fixtures/schema/v1/ror_schema.json"

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
    invocation = ["python", "run_validations.py","-i"]
    command = [*invocation, input, *optional_args]
    out, err, exitcode = capture(command)
    return out, err, exitcode

def run_valid_args(optional_args = []):
    for i in valid_input():
        out, err, exitcode = run_args(i, optional_args)
        assert exitcode == 0
        assert out == b'VALID\n'
        assert err == b''
