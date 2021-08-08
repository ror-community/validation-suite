import pytest
import os
import sys
import subprocess
import copy
from setup import *

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..')
sys.path.append( mymodule_dir )

import run_validations as rv

def test_valid_input_only():
    """This test in only for valid inputs"""
    run_valid_args()

def test_valid_input_rels():
    """This test in for valid inputs and checking relationships"""
    path = valid_file_path()
    o_args = run_optional_args(p = path)
    run_valid_args(o_args)

def test_valid_input_schema():
    """This test in for valid inputs and sending a schema file instead of using the default"""
    schema = schema_fixture()
    o_args = run_optional_args(s = schema)
    run_valid_args(o_args)

def test_valid_all_args():
    """This test in for valid inputs where a schema file is sent instead of the default and check for relationships"""
    schema = schema_fixture()
    path = valid_file_path()
    o_args = run_optional_args(s = schema, p = path)
    run_valid_args(o_args)

def test_invalid_args():
    """This test sends an invalid argument"""
    bad_command = ["python", "run_validations.py", "-r", "test"]
    out, err, exitcode = capture(bad_command)
    assert exitcode == 2
    assert out == b''
    assert err == b'usage: run_validations.py [-h] -i INPUT [-s SCHEMA] [-p FILE_PATH]\nrun_validations.py: error: the following arguments are required: -i/--input\n'
