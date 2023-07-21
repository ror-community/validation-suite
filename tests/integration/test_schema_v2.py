import pytest
import os
from ..setup import *
import re


V2_VERSION = '2'


def test_missing_fields_v2():
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["missing_fields"]
    files = os.listdir(dir)
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    for f in files:
        full_path = os.path.join(dir, f)
        required_args = format_required_args(full_path, V2_VERSION)
        out, err, exitcode = run_args(required_args, o_args)
        field = os.path.splitext(f)[0]
        result = re.search(r'File is missing field\(s\)\: {0}'.format(field), out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 1


def test_missing_properties_v2():
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["missing_properties"]
    files = os.listdir(dir)
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    for f in files:
        full_path = os.path.join(dir, f)
        required_args = format_required_args(full_path, V2_VERSION)
        out, err, exitcode = run_args(required_args, o_args)
        expected_msg = "is a required property"
        result = re.search(rf"{expected_msg}", out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 1


def test_bad_enum_values_v2():
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["enum_values"]
    files = os.listdir(dir)
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    for f in files:
        full_path = os.path.join(dir, f)
        required_args = format_required_args(full_path, V2_VERSION)
        out, err, exitcode = run_args(required_args, o_args)
        expected_msg = "Failed validating 'enum' in schema"
        result = re.search(rf"{expected_msg}", out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 1


def test_bad_formats_v2():
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["value_formats"] + "formats/"
    files = os.listdir(dir)
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    for f in files:
        full_path = os.path.join(dir, f)
        required_args = format_required_args(full_path, V2_VERSION)
        out, err, exitcode = run_args(required_args, o_args)
        expected_msg = "is not a"
        result = re.search(rf"{expected_msg}", out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 1


def test_bad_patterns_v2():
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["value_formats"] + "patterns/"
    files = os.listdir(dir)
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    for f in files:
        full_path = os.path.join(dir, f)
        required_args = format_required_args(full_path, V2_VERSION)
        out, err, exitcode = run_args(required_args, o_args)
        expected_msg = "does not match"
        result = re.search(rf"{expected_msg}", out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 1


def test_bad_unique_items_v2():
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["value_formats"] + "unique_items/"
    files = os.listdir(dir)
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    for f in files:
        full_path = os.path.join(dir, f)
        required_args = format_required_args(full_path, V2_VERSION)
        out, err, exitcode = run_args(required_args, o_args)
        expected_msg = "has non-unique elements"
        result = re.search(rf"{expected_msg}", out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 1


def test_bad_non_empty_strings_v2():
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["value_formats"] + "non_empty_strings/"
    files = os.listdir(dir)
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    for f in files:
        full_path = os.path.join(dir, f)
        required_args = format_required_args(full_path, V2_VERSION)
        out, err, exitcode = run_args(required_args, o_args)
        expected_msg = "is too short"
        result = re.search(rf"{expected_msg}", out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 1


def test_bad_types_v2():
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["value_formats"] + "types/"
    files = os.listdir(dir)
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    for f in files:
        full_path = os.path.join(dir, f)
        required_args = format_required_args(full_path, V2_VERSION)
        out, err, exitcode = run_args(required_args, o_args)
        expected_msg = "is not of type"
        result = re.search(rf"{expected_msg}", out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 1


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


def test_invalid_langcode_v1():
    filename = "invalid_langcode.json"
    sub_folders = invalid_sub_folders()
    dir = invalid_file_path(V2_VERSION) + sub_folders["usecase_issues"]
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    full_path = os.path.join(dir, filename)
    required_args = format_required_args(full_path, V2_VERSION)
    out, err, exitcode = run_args(required_args, o_args)
    expected_msg = "In check_names: {'status': {'NAMES_LANG_ERROR': ['Language value ft is not an iso639 standard']}}"
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
    expected_msg = "In check_names: {'status': {'NAMES_DUPLICATES_ERROR': 'Multiple names have the same value(s): UC System'}}"
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
    expected_msg = "In check_external_ids: {'status': {'EXT_IDS_DUPLICATE_TYPES_ERROR': 'Multiple external ID items have the same type(s): fundref'}}"
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
    expected_msg = "In check_external_ids: {'status': {'EXT_IDS_PREFERRED_ERROR': \"1 or more external ID items have a value in preferred that is not included in all: [{'grid': 'grid.30389.31'}]\"}}"
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


def test_valid_no_rels_v2():
    dir = valid_file_path(V2_VERSION)
    files = os.listdir(dir)
    schema = schema_fixture(V2_VERSION)
    o_args = format_optional_args(s = schema)
    for f in files:
        full_path = os.path.join(dir, f)
        required_args = format_required_args(full_path, V2_VERSION)
        out, err, exitcode = run_args(required_args, o_args)
        result = re.search(r"schema valid", out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 0