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
    """This test is only for valid inputs"""
    run_valid_args()

def test_valid_input_rels():
    """This test is for valid inputs and checking relationships"""
    path = valid_file_path()
    o_args = run_optional_args(p = path)
    run_valid_args(o_args)

def test_valid_input_schema():
    """This test is for valid inputs and sending a schema file instead of using the default"""
    schema = schema_fixture()
    o_args = run_optional_args(s = schema)
    run_valid_args(o_args)

def test_valid_all_args():
    """This test is for valid inputs where a schema file is sent instead of the default and check for relationships"""
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

def test_invalid_estdate_length():
    """This test sends an invalid file which passes the schema but does not pass a validation test. """
    bad_command = ["python", "run_validations.py", "-i", "tests/fixtures/invalid/01k4yrm29-invalid-estdate.json"]
    out, err, exitcode = capture(bad_command)
    assert exitcode == 1
    assert out == b"FOR FILE:  01k4yrm29-invalid-estdate\nVALIDATION TEST ERRORS: \n\nIn check_address: {'status': {'lat': {'ror': 36.369595, 'geonames': '36.34913'}, 'lng': {'ror': 127.364025, 'geonames': '127.38493'}}}\n\nIn check_established_year: {'status': 'Year value: 12345 should be an integer between 3 and 4 digits'}\n\n"
