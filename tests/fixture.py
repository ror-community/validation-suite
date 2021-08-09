import pytest
import os
import sys
import subprocess

# TODO: invocation becomes its own function that can be used everywhere

# TODO: Invalid types of inputs, i.e. various types of schema invalidations, various types of validation test failures. Cover all use cases

@pytest.fixture(scope = "module")

def invalid_established_date():
    return b"FOR FILE:  01k4yrm29-invalid-estdate\nVALIDATION TEST ERRORS: \n\nIn check_address: {'status': {'lat': {'ror': 36.369595, 'geonames': '36.34913'}, 'lng': {'ror': 127.364025, 'geonames': '127.38493'}}}\n\nIn check_established_year: {'status': 'Year value: 12345 should be an integer between 3 and 4 digits'}\n\n"
