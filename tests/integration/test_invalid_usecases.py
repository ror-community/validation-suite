import pytest
import re
import os
from ..setup import *
from ..fixtures import *

def invalid_fixture_path():
    return "tests/fixtures/invalid/usecase-issues/"

def invalid_files():
    """This is a dictionary of use cases and the corresponding files and expected responses. The value in the rsp key is a function in the responses file"""

    invalid = {
                "invalid_established_date": {"file": "01k4yrm29-invalid-estdate.json","rsp": invalid_established_date_address_mismatch},"invalid_links": {"file": "03yrm5c26-invalid-link.json","rsp": invalid_links}, "invalid_iso_country":{"file": "02baj6749.json","rsp": invalid_iso_country_mismatch},
                "invalid_relationship":{"file": "02baj6743.json","rsp": invalid_relationship}}

    return invalid

def check_pattern(string, text):
    return re.search(rf"{string}", text, re.MULTILINE)

def test_all():
    invalid_cases = invalid_files()
    for i, data in invalid_cases.items():
        input = invalid_fixture_path() + data["file"]
        o_args = []
        if i == "invalid_relationship":
            o_args = run_optional_args(p = invalid_fixture_path())
        out, err, exitcode = run_args(input, o_args)
        fixture = data["rsp"]()
        print("\nTesting: ", i)
        for x in fixture:
            err = check_pattern(x, out)
            assert bool(err) is True
