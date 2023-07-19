import pytest
import os
from ..setup import *
import re

V1_VERSION = '1'

def test_missing_fields_v1():
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V1_VERSION) + sub_folders["missing_fields"]
    files = os.listdir(dir)
    schema = schema_fixture(V1_VERSION)
    o_args = format_optional_args(s = schema)
    for f in files:
        full_path = os.path.join(dir, f)
        required_args = format_required_args(full_path, V1_VERSION)
        out, err, exitcode = run_args(required_args, o_args)
        field = os.path.splitext(f)[0]
        result = re.search(r'File is missing field\(s\)\: {0}'.format(field), out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 1


def test_enum_values_v1():
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V1_VERSION) + sub_folders["enum_values"]
    files = os.listdir(dir)
    schema = schema_fixture(V1_VERSION)
    o_args = format_optional_args(s = schema)
    for f in files:
        full_path = os.path.join(dir, f)
        required_args = format_required_args(full_path, V1_VERSION)
        out, err, exitcode = run_args(required_args, o_args)
        result = re.search(r"SCHEMA ERROR", out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 1

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


def test_valid_no_rels_v1():
    dir = valid_file_path(V1_VERSION)
    files = os.listdir(dir)
    schema = schema_fixture(V1_VERSION)
    o_args = format_optional_args(s = schema)
    for f in files:
        full_path = os.path.join(dir, f)
        required_args = format_required_args(full_path, V1_VERSION)
        out, err, exitcode = run_args(required_args, o_args)
        result = re.search(r"schema valid", out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 0

def test_valid_rels_v1():
    dir = valid_file_path(V1_VERSION)
    files = os.listdir(dir)
    schema = schema_fixture(V1_VERSION)
    o_args = format_optional_args(s = schema, p = dir)
    for f in files:
        full_path = os.path.join(dir, f)
        required_args = format_required_args(full_path, V1_VERSION)
        out, err, exitcode = run_args(required_args, o_args)
        result = re.search(r"schema valid", out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 0