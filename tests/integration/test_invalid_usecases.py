import pytest
import re
import os
from ..setup import *
from ..fixture import *

def invalid_fixture_path():
    return "tests/fixtures/invalid/usecase-issues/"

def invalid_files(key):
    invalid = {
                "invalid_established_date": "01k4yrm29-invalid-estdate.json",
                "invalid_links": "03yrm5c26-invalid-link.json",
                "invalid_relationship": "02baj6743.json", "invalid_iso_country": "02baj6749.json"}

    return invalid[key]

def check_pattern(string, text):
    return re.search(rf"{string}", text, re.MULTILINE)

def test_invalid_established_date_address():
    """This test sends an invalid file which passes the schema but has an invalid established date length and incorrect address values."""
    file = invalid_files("invalid_established_date")
    input = invalid_fixture_path()+file
    out, err, exitcode = run_args(input)
    address = "In check_address: {'status': {'lat': {'ror': 36.369595, 'geonames': '36.34913'}, 'lng': {'ror': 127.364025, 'geonames': '127.38493'}}}"
    year = "In check_established_year: {'status': 'Year value: 12345 should be an integer between 3 and 4 digits'}"
    chk_address_err = check_pattern(address, out)
    chk_year_err = check_pattern(year, out)
    assert exitcode == 1
    assert bool(chk_address_err) is True
    assert bool(chk_year_err) is True

def test_invalid_links():
    """This test sends an invalid file which passes the schema but has invalid links."""
    file = invalid_files("invalid_links")
    input = invalid_fixture_path()+file
    out, err, exitcode = run_args(input)
    links = "In check_links: {'status': {'http://www.cdlib.o': 'Validation Error', 'wikipedia.org/wiki/California_Digital_Library': 'Validation Error'}}"
    links_err = check_pattern(links, out)
    assert exitcode == 1
    assert bool(links_err) is True

def test_invalid_relshp():
    """This test sends an invalid file which passes the schema but has invalid relationships."""
    file = invalid_files("invalid_relationship")
    o_args = run_optional_args(p = "tests/fixtures/invalid/usecase-issues")
    input = invalid_fixture_path()+file
    out, err, exitcode = run_args(input, o_args)
    relshp1 = "Illegal relationship pairing: relationship type: Child should be Parent"
    relshp1_err = check_pattern(relshp1, out)
    relshp2 = "tests/fixtures/invalid/usecase-issues/015m7wh34.json doesn't exist"
    relshp2_err = check_pattern(relshp2, out)
    assert exitcode == 1
    assert bool(relshp1_err) is True
    assert bool(relshp2_err) is True

def test_invalid_iso_country():
    """This test sends an invalid file which passes the schema but has an incorrect country mismatch."""
    file = invalid_files("invalid_iso_country")
    input = invalid_fixture_path()+file
    out, err, exitcode = run_args(input)
    country = "In check_address: {'status': {'country_name': {'ror': 'Fradnce', 'geonames': 'France'}}}"
    country_err = check_pattern(country, out)
    assert exitcode == 1
    assert bool(country_err) is True
