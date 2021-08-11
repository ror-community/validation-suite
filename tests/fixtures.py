import pytest
import os
import sys
import subprocess

def invalid_established_date_address_mismatch():
    address = "In check_address: {'status': {'lat': {'ror': .*?, 'geonames': '.*?'}, 'lng': {'ror': .*?, 'geonames': '.*?'}}}"
    year = "In check_established_year: {'status': 'Year value: 12345 should be an integer between 3 and 4 digits'}"
    return address, year

def invalid_links():
    rsp = "In check_links: {'status': {'http://www.cdlib.o': 'Validation Error', 'wikipedia.org/wiki/California_Digital_Library': 'Validation Error'}}"
    return rsp

def invalid_relationship():
    bad_pairing = "Illegal relationship pairing: relationship type: Child should be Parent"

    no_pairing = ".*? doesn't exist"
    return bad_pairing, no_pairing

def invalid_iso_country_mismatch():
    return "In check_address: {'status': {'country_name': {'ror': 'Fradnce', 'geonames': 'France'}}}"
