import pytest
import os
import sys
import subprocess
import copy
from ..setup import *

V1_VERSION = '1'
V2_VERSION = '2'

def run_valid_args(version, optional_args = []):
    for input_file in valid_input(version):
        required_args = format_required_args(input_file, version)
        out, err, exitcode = run_args(required_args, optional_args)
        assert "Validating" in out

def test_valid_input_only_v1():
    """This test is only for valid inputs"""
    run_valid_args(V1_VERSION)

def test_valid_input_rels_v1():
    """This test is for valid inputs and checking relationships"""
    path = valid_file_path(V1_VERSION)
    o_args = format_optional_args(p = path)
    run_valid_args(V1_VERSION, o_args)

def test_valid_input_schema_v1():
    """This test is for valid inputs and sending a schema file instead of using the default"""
    schema = schema_fixture(V1_VERSION)
    o_args = format_optional_args(s = schema)
    run_valid_args(V1_VERSION, o_args)

def test_valid_all_args_v1():
    """This test is for valid inputs where a schema file is sent instead of the default and check for relationships"""
    schema = schema_fixture(V1_VERSION)
    path = valid_file_path(V1_VERSION)
    o_args = format_optional_args(s = schema, p = path)
    run_valid_args(V1_VERSION, o_args)

def test_invalid_args_v1():
    """This test sends an invalid argument"""
    bad_command = [*invocation(), "-r", "test", "-v", V1_VERSION]
    out, err, exitcode = capture(bad_command)
    assert exitcode == 2
    assert out == ''
    assert 'error: the following arguments are required: -i/--input' in err
