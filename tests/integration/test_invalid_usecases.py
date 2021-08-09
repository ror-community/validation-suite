import pytest
import os
import sys
import subprocess
import copy
from ..setup import *
from ..fixture import *

def invalid_fixture_path():
    return "tests/fixtures/invalid/usecase-issues/"

def invalid_files(key):
    invalid = {"invalid_established_date": "01k4yrm29-invalid-estdate.json", "invalid_links": "03yrm5c26-invalid-link.json", "invalid_relationship": "02baj6743.json", "invalid_iso_country": "02baj6749.json"}

    return invalid[key]


def test_invalid_established_date(invalid_established_date_address_mismatch):
    """This test sends an invalid file which passes the schema but has an invalid established date length."""
    file = invalid_files("invalid_established_date")
    input = invalid_fixture_path()+file
    out, err, exitcode = run_args(input)
    assert exitcode == 1
    assert out == invalid_established_date_address_mismatch

def test_invalid_links(invalid_links):
    """This test sends an invalid file which passes the schema but has an invalid established date length."""
    file = invalid_files("invalid_links")
    input = invalid_fixture_path()+file
    out, err, exitcode = run_args(input)
    assert exitcode == 1
    assert out == invalid_links

def test_invalid_relshp(invalid_relationship):
    """This test sends an invalid file which passes the schema but has an invalid established date length."""
    file = invalid_files("invalid_relationship")
    o_args = run_optional_args(p = "tests/fixtures/invalid/usecase-issues")
    input = invalid_fixture_path()+file
    out, err, exitcode = run_args(input, o_args)
    assert exitcode == 1
    assert out == invalid_relationship

def test_invalid_iso_country(invalid_iso_country_mismatch):
    """This test sends an invalid file which passes the schema but has an invalid established date length."""
    file = invalid_files("invalid_iso_country")
    input = invalid_fixture_path()+file
    out, err, exitcode = run_args(input)
    assert exitcode == 1
    assert out == invalid_iso_country_mismatch
