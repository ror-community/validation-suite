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
        print(field)
        result = re.search(rf'File is missing field\(s\)\: {field}', out, re.MULTILINE)
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
