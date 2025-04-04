import pytest
import os
from ..setup import *
import re


V2_VERSION = '2'

def test_invalid_link_v2():
    filename = "invalid_link.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V2_VERSION)
    out, err, exitcode = run_args(required_args, o_args)
    expected_msg = "In check_links: {'status': {'http://www.universityofcalifornia.e': 'URL validation Error'}}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1


def test_invalid_langcode_v2():
    filename = "invalid_langcode.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V2_VERSION)
    out, err, exitcode = run_args(required_args, o_args)
    expected_msg = "In check_names: {'status': {'NAMES_LANG_ERROR': \['Language value ft is not an iso639 standard']}}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1


def test_invalid_estdate_v2():
    filename = "invalid_estdate.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V2_VERSION)
    out, err, exitcode = run_args(required_args, o_args)
    expected_msg = "In check_established_year: {'status': 'Year value: 12345 should be an integer between 3 and 4 digits'}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1


def test_invalid_location_v2():
    filename = "invalid_location.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V2_VERSION)
    out, err, exitcode = run_args(required_args, o_args, False)
    expected_msg = "In check_locations: {'status': {'LOCATION_ERROR_GEONAMES_ID_5378538': {'country_name': {'ror': 'United Stats', 'geonames': 'United States'}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1


def test_invalid_names_duplicate_values_v2():
    filename = "invalid_names_duplicate_values.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V2_VERSION)
    out, err, exitcode = run_args(required_args, o_args, False)
    expected_msg = "In check_names: {'status': {'NAMES_DUPLICATES_WARNING': 'Multiple names have the same value\(s\): UC System'}}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1


def test_invalid_names_no_ror_display_v2():
    filename = "invalid_names_no_ror_display.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V2_VERSION)
    out, err, exitcode = run_args(required_args, o_args, False)
    expected_msg = "In check_names: {'status': {'NAMES_TYPES_ERROR': 'Exactly 1 name must have type ror_display. 0 names have ror_display in their name types.'}}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1


def test_invalid_external_ids_duplicate_type_v2():
    filename = "invalid_external_ids_duplicate_type.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V2_VERSION)
    out, err, exitcode = run_args(required_args, o_args, False)
    expected_msg = "In check_external_ids: {'status': {'EXT_IDS_DUPLICATE_TYPES_ERROR': 'Multiple external ID items have the same type\(s\): fundref'}}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1


def test_invalid_external_ids_preferred_not_in_all_v2():
    filename = "invalid_external_ids_preferred_not_in_all.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V2_VERSION)
    out, err, exitcode = run_args(required_args, o_args, False)
    expected_msg = "In check_external_ids: {'status': {'EXT_IDS_PREFERRED_ERROR': \"1 or more external ID items have a value in preferred that is not included in all: \[{'grid': 'grid.30389.31'}\]\"}}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1


def test_invalid_domains_v2():
    filename = "invalid_domains.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V2_VERSION)
    out, err, exitcode = run_args(required_args, o_args, False)
    expected_msg = "In check_domains: {'status': {'DOMAINS_ERROR': 'Domains contains subdomains of other domains: foo.universityofcalifornia.edu, foo.bar.universityofcalifornia.edu'}}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1


def test_invalid_continent_name_code_pair_v2():
    filename = "invalid_continent_name_code_pair.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V2_VERSION)
    out, err, exitcode = run_args(required_args, o_args, False)
    expected_msg = "'continent_name': {'ror': 'Europe', 'geonames': 'North America'}"
    result = re.search(rf"{expected_msg}", out, re.MULTILINE)
    assert bool(result) is True
    assert exitcode == 1