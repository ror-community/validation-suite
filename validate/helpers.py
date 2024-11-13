import json
import sys
import jsonschema
import pycountry
import requests
import validators
from validate.utilities import *
from copy import deepcopy

File = None
ROR_DISPLAY = "ror_display"
CONTINENT_CODES_NAMES = {
    "AF": "Africa",
    "AN": "Antarctica",
    "AS": "Asia",
    "EU": "Europe",
    "NA": "North America",
    "OC": "Oceania",
    "SA": "South America"
}

def handle_check(name,msg=None):
    # all the validator messages use this pattern
    message = {}
    if msg:
        message[name] = {'status':msg}
    return message

def validate_url(url):
    # validates url format against a library
    msg = None
    validated_url = validators.url(url)
    if not(validated_url):
        msg = "URL validation Error"
    return msg

def check_lang_code(lang):
    msg = None
    pylanguage = pycountry.languages.get(alpha_2=lang)
    if not(pylanguage):
        msg = f'Language value {lang} is not an iso639 standard'
    return msg

def check_duplicates(list_to_check):
    duplicates = []
    unique_items = []
    for item in list_to_check:
        if item not in unique_items:
            unique_items.append(item)
    duplicates = [item for item in unique_items if list_to_check.count(item) > 1]
    return duplicates

def check_substrings(list_to_check):
    substring_matches = []
    for item in list_to_check:
        for i in list_to_check:
            if item in i:
                if i.index(item) > 0:
                    substring_matches.append(i)
    return substring_matches


def check_country(geonames_response):
    # checks country code and country name
    country_check = {}
    geonames_country_code = geonames_response['countryCode']
    record_country_code = File['country']['country_code']
    geonames_country_name = geonames_response['countryName']
    record_country_name = File['country']['country_name']
    if geonames_country_code != record_country_code:
        country_check['country_code'] = {'ror': record_country_code, 'geonames': geonames_country_code}
    if geonames_country_name != record_country_name:
        country_check['country_name'] = {'ror': record_country_name, 'geonames': geonames_country_name}
    return country_check

def check_continent_v2(location):
    continent_check = {}
    if location['geonames_details']['continent_code']:
        geonames_continent_name = CONTINENT_CODES_NAMES[location['geonames_details']['continent_code']]
        record_continent_name = location['geonames_details']['continent_name']
        if  geonames_continent_name != record_continent_name:
            continent_check['continent_name'] = {'ror': record_continent_name, 'geonames':  geonames_continent_name}
    return continent_check

def mapped_geoname_record():
    # mapping of ror v1 fields to geoname response fields
    ror_to_geoname = {
          "lat": "lat",
          "lng": "lng",
          "city": "name",
          "geonames_city": {
            "id": "geonameId",
            "city": "name",
            "geonames_admin1": {
                "name": "adminName1",
                "id": "adminId1",
                "ascii_name": "adminName1",
                "code": ["countryCode","adminCode1"]
            },
            "geonames_admin2": {
                "name": "adminName2",
                "id": "adminId2",
                "ascii_name": "adminName2",
                "code": ["countryCode","adminCode1","adminCode2"]
            },
            "country_geonames_id": "countryId"
        }}
    return ror_to_geoname

def mapped_geoname_record_v2():
    # mapping of ror v2 fields to geoname response fields
    ror_to_geoname = {
        "geonames_id": "geonameId",
        "geonames_details": {
            "continent_code": "continentCode",
            "country_code": "countryCode",
            "country_name": "countryName",
            "country_subdivision_code": ["adminCodes1", "ISO3166_2"],
            "country_subdivision_name": "adminName1",
            "lat": "lat",
            "lng": "lng",
            "name": "name"
        }
    }
    return ror_to_geoname

def get_geonames_response(id):
    # queries geonames api with the city geonames id as a query parameter
    msg = None
    result = None
    query_params = {}
    query_params['geonameId'] = id
    query_params['username'] = GEONAMES['USER']
    url = GEONAMES['URL']
    try:
        response = requests.get(url,params=query_params)
        response.raise_for_status()
        result = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        msg = "Connection Error"
    return result,msg

def get_record_address():
    # returns the address dictionary with the geonames city id
    address = File['addresses'][0]
    id = address['geonames_city']['id']
    return id,address

def get_ror_display_name(names):
    ror_display = None
    for name in names:
        if ROR_DISPLAY in name['types']:
            ror_display = name['value']
            break
    return ror_display


def get_relationship_info():
    # returns relationship dictionary
    return {"id": File['id'], "name": File['name'],"rel": File["relationships"]}


def get_relationship_info_v2():
    # returns relationship dictionary
    name = get_ror_display_name(File['names'])
    return {"id": File['id'], "name": name,"rel": File["relationships"]}


def compare_ror_geoname(mapped_fields,ror_address,geonames_response,msg={}):
    compare = msg
    for key, value in mapped_fields.items():
        # If value is of dict type then print
        # all key-value pairs in the nested dictionary
        if isinstance(value, dict):
            if key in ror_address:
                compare_ror_geoname(value,ror_address[key],geonames_response,compare)
        else:
            _,original_address = get_record_address()
            ror_value = ror_address[key] if key in ror_address else original_address[key]
            geonames_value = None
            if (key == "code"):
                key_exists = True
                for x in value:
                    if not(x in geonames_response):
                        key_exists = False
                if key_exists:
                    geonames_value = ".".join([geonames_response[x] for x in value])
            else:
                if (value in geonames_response) and (geonames_response[value] != ""):
                    geonames_value = geonames_response[value]
            if str(ror_value) != str(geonames_value):
                compare[key] = {"ror": ror_value, "geonames": geonames_value}
    return deepcopy(compare)

def compare_ror_geoname_v2(mapped_fields,ror_address,geonames_response,msg={}):
    compare = msg
    original_address = deepcopy(ror_address)
    for key, value in mapped_fields.items():
        # If value is of dict type then print
        # all key-value pairs in the nested dictionary
        if isinstance(value, dict):
            if key in ror_address:
                compare_ror_geoname_v2(value,ror_address[key],geonames_response,compare)
        else:
            ror_value = ror_address[key] if key in ror_address else original_address[key]
            geonames_value = None
            if key == 'country_subdivision_code':
                if value[0] in geonames_response:
                    if geonames_response[value[0]][value[1]] != "":
                        geonames_value = geonames_response[value[0]][value[1]]
            else:
                if (value in geonames_response) and (geonames_response[value] != ""):
                    geonames_value = geonames_response[value]
            if str(ror_value) != str(geonames_value):
                compare[key] = {"ror": ror_value, "geonames": geonames_value}
    return deepcopy(compare)
