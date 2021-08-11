import pytest
import os
import sys
import subprocess
import copy
from ..setup import *
from ..fixture import *
import json
import re

def invalid_fixture_path():
    return "tests/fixtures/invalid/schema-issues/"

def invalid_sub_folders():
    dirs = {"missing_fields": "missing_fields/",
            "incorrect_enum_values": "enum_values/"}
    return dirs

def required_fields():
    return [
    "acronyms",
    "addresses",
    "aliases",
    "country",
    "established",
    "external_ids",
    "id",
    "labels",
    "links",
    "name",
    "relationships",
    "status",
    "types",
    "wikipedia_url"
  ]

def read_file():
    file = fixture_file_schema()
    try:
        with open(file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(e)
    return data

def write_file(name, data):
    path = invalid_fixture_path() + name
    try:
        with open(path, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(e)

def missing_field(field, data):
    data.pop(field)
    return data

def add_random_value(field, value, data):
    data[field] = value
    return data

def run_command(fname, d):
    input = invalid_fixture_path() + fname
    write_file(fname, d)
    schema = schema_fixture()
    o_args = run_optional_args(s = schema)
    out, err, exitcode = run_args(input, o_args)
    return out, err, exitcode

def test_missing_fields():
    data = read_file()
    path = invalid_sub_folders()
    for rf in required_fields():
        new_data = {**data}
        d = missing_field(rf, new_data)
        fname = f"{path['missing_fields']}/{rf}.json"
        out, err, exitcode = run_command(fname, d)
        result = re.search(rf"\'{rf}.*?property", out, re.MULTILINE)
        assert result.group() == f"'{rf}' is a required property"
        assert exitcode == 1

def test_enum_values():
    sub_folders = invalid_sub_folders()
    dir = invalid_fixture_path() + sub_folders["incorrect_enum_values"]
    files = os.listdir(dir)
    schema = schema_fixture()
    o_args = run_optional_args(s = schema)
    for f in files:
        full_path = os.path.join(dir, f)
        out, err, exitcode = run_args(full_path, o_args)
        result = re.search(r"SCHEMA ERROR", out, re.MULTILINE)
        assert bool(result) is True
        assert exitcode == 1
