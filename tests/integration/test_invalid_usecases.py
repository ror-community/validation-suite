import pytest
import os
import sys
import subprocess
import copy
from ..setup import *
from ..fixture import *

def invalid_files(key):
    invalid = {"invalid_established_date": "tests/fixtures/invalid/01k4yrm29-invalid-estdate.json"}

    return invalid[key]


def test_invalid_estdate_length(invalid_estdate_length):
    """This test sends an invalid file which passes the schema but has an invalid established date length."""
    file = invalid_files("invalid_established_date")
    out, err, exitcode = run_args(file)
    assert exitcode == 1
    assert out == invalid_estdate_length
