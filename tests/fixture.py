import pytest
import os
import sys
import subprocess

# TODO: invocation becomes its own function that can be used everywhere

# TODO: Invalid types of inputs, i.e. various types of schema invalidations, various types of validation test failures. Cover all use cases

@pytest.fixture(scope = "module")

def invalid_established_date_address_mismatch():
    return b"FOR FILE:  01k4yrm29-invalid-estdate\nVALIDATION TEST ERRORS: \n\nIn check_address: {'status': {'lat': {'ror': 36.369595, 'geonames': '36.34913'}, 'lng': {'ror': 127.364025, 'geonames': '127.38493'}}}\n\nIn check_established_year: {'status': 'Year value: 12345 should be an integer between 3 and 4 digits'}\n\n"

@pytest.fixture(scope = "module")
def invalid_links():
    return b"FOR FILE:  03yrm5c26-invalid-link\nVALIDATION TEST ERRORS: \n\nIn check_links: {'status': {'http://www.cdlib.o': 'Validation Error', 'wikipedia.org/wiki/California_Digital_Library': 'Validation Error'}}\n\n"

@pytest.fixture(scope = "module")
def invalid_relationship():
    return b"FOR FILE:  02baj6743\nVALIDATION TEST ERRORS: \n\nIn relationships: [{'https://ror.org/05qec5a53': ['Illegal relationship pairing: relationship type: Child should be Parent\']}, \"tests/fixtures/invalid/usecase-issues/015m7wh34.json doesn\'t exist\"]\n\n"

@pytest.fixture(scope = "module")
def invalid_iso_country_mismatch():
    return b'FOR FILE:  02baj6749\nVALIDATION TEST ERRORS: \n\nIn check_address: {\'status\': {\'country_name\': {\'ror\': \'Fradnce\', \'geonames\': \'France\'}}}\n\nIn check_language_code: {\'status\': \'Language value: [{\\\'label\\\': "Centre d\\\'Investigation Clinique de Rennes", \\\'iso639\\\': \\\'ft\\\'}] is not an iso639 standard\'}\n\n'
