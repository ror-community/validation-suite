import pytest
import os
import sys
import subprocess
import copy
from ..setup import *
from ..fixture import *

def invalid_files(key):
    invalid = {"invalid_established_date": "tests/fixtures/invalid/usecase-issues/01k4yrm29-invalid-estdate.json", "invalid_links": "tests/fixtures/invalid/usecase-issues/03yrm5c26-invalid-link.json", "invalid_relationship": "tests/fixtures/invalid/usecase-issues/02baj6743.json"}

    return invalid[key]


def test_invalid_established_date(invalid_established_date_address_mismatch):
    """This test sends an invalid file which passes the schema but has an invalid established date length."""
    file = invalid_files("invalid_established_date")
    out, err, exitcode = run_args(file)
    assert exitcode == 1
    assert out == invalid_established_date_address_mismatch

def test_invalid_links(invalid_links):
    """This test sends an invalid file which passes the schema but has an invalid established date length."""
    file = invalid_files("invalid_links")
    out, err, exitcode = run_args(file)
    assert exitcode == 1
    assert out == invalid_links

def test_invalid_relshp(invalid_relationship):
    """This test sends an invalid file which passes the schema but has an invalid established date length."""
    file = invalid_files("invalid_relationship")
    o_args = run_optional_args(p = "tests/fixtures/invalid/usecase-issues")
    out, err, exitcode = run_args(file, o_args)
    assert exitcode == 1
    assert out == invalid_relationship
