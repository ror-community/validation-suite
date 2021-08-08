import pytest
import os
import sys
import subprocess
import copy

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..')
sys.path.append( mymodule_dir )

import run_validations as rv

def capture(command):
    print(command)
    proc = subprocess.Popen(command,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
    )
    out,err = proc.communicate()
    return out, err, proc.returncode

def valid_input():
    return ["tests/fixtures/valid/015m7wh34.json","tests/fixtures/valid"]

def schema_fixture():
    return "tests/fixtures/schema/v1/ror_schema.json"

def flatten(nested_list):
    return [final_list for t in nested_list for final_list in t]

def run_optional_args(**optional_args):
    if optional_args:
        altered_keys = ["-" + k for k in optional_args.keys()]
        fixed_args = dict(zip(altered_keys, list(optional_args.values())))
        return flatten(list(fixed_args.items()))

def run_args(input, optional_args = []):
    invocation = ["python", "run_validations.py","-i"]
    command = [*invocation, input, *optional_args]
    out, err, exitcode = capture(command)
    return out, err, exitcode


def test_valid_input_only():
    """This test in only for valid inputs"""
    for i in valid_input():
        out, err, exitcode = run_args(i)
        assert exitcode == 0
        assert out == b'VALID\n'
        assert err == b''

def test_valid_input_rels():
    o_args = run_optional_args(p = "tests/fixtures/valid")
    for i in valid_input():
        out, err, exitcode = run_args(i, o_args)
        assert exitcode == 0
        assert out == b'VALID\n'
        assert err == b''

def test_valid_input_schema():
    schema = schema_fixture()
    o_args = run_optional_args(s = schema)
    for i in valid_input():
        out, err, exitcode = run_args(i, o_args)
        assert exitcode == 0
        assert out == b'VALID\n'
        assert err == b''

#def test_file_validation():
    #file = "tests/fixtures/valid/015m7wh34.json"
    #with pytest.raises(SystemExit):
        #rv.validate(file)
    #out, err = capsys.readouterr()
    #assert out == "VALID\n"
    #print(out, err)
