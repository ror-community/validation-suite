import pytest
import os
from ..setup import *
import re

V2_VERSION = '2'

def test_valid_no_rels_v1():
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