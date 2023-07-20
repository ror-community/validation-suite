import pytest
import re
import os
from ..setup import *

V1_VERSION = '1'
V2_VERSION = '2'

'''
def invalid_files():
    """This is a dictionary of use cases and the corresponding files and expected responses. The value in the rsp key is a function in the responses file"""

    invalid = {
                "invalid_established_date": {"file": "01k4yrm29-invalid-estdate.json","rsp": invalid_established_date_address_mismatch},"invalid_links": {"file": "03yrm5c26-invalid-link.json","rsp": invalid_links}, "invalid_iso_country":{"file": "02baj6749.json","rsp": invalid_iso_country_mismatch},
                "invalid_relationship":{"file": "02baj6743.json","rsp": invalid_relationship}}

    return invalid

def check_pattern(string, text):
    return re.search(rf"{string}", text, re.MULTILINE)
'''

def test_invalid_link_v1():
    filename = "invalid_link.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V1_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V1_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V1_VERSION)
    out, err, exitcode = run_args(required_args, o_args)
    expected_msg = "In check_links: {'status': {'http://www.cdlib.o': 'URL validation Error', 'wikipedia.org/wiki/California_Digital_Library': 'URL validation Error'}}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1

def test_invalid_langcode_v1():
    filename = "invalid_langcode.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V1_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V1_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V1_VERSION)
    out, err, exitcode = run_args(required_args, o_args)
    expected_msg = "In check_language_code: {'status': 'Language value ft is not an iso639 standard'}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1

def test_invalid_estdate_v1():
    filename = "invalid_estdate.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V1_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V1_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V1_VERSION)
    out, err, exitcode = run_args(required_args, o_args)
    expected_msg = "In check_established_year: {'status': 'Year value: 12345 should be an integer between 3 and 4 digits'}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1

def test_invalid_address_v1():
    filename = "invalid_address.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V1_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V1_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V1_VERSION)
    out, err, exitcode = run_args(required_args, o_args, False)
    expected_msg = "In check_address: {'status': {'country_name': {'ror': 'Fradce', 'geonames': 'France'}}}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1

def test_invalid_relationship_v1():
    filename = "02baj6743.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V1_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V1_VERSION)
    o_args = format_optional_args(s = schema, p = dir)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V1_VERSION)
    out, err, exitcode = run_args(required_args, o_args, False)
    expected_msg = "In relationships: \\[{'https://ror.org/05qec5a53': \\['Illegal relationship pairing: relationship type: Child should be Parent'\\]}\\]"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1

'''
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
'''