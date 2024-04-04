import os
import zipfile
import requests
import json
import sys
import validators
from csv import DictReader

DEFAULT_SCHEMA_V1_0 = "https://raw.githubusercontent.com/ror-community/ror-schema/master/ror_schema.json"
DEFAULT_SCHEMA_V2_0 = "https://raw.githubusercontent.com/ror-community/ror-schema/master/ror_schema_v2_0.json"
API_URL = "https://api.ror.org/organizations"

GEONAMES = {}
GEONAMES['USER'] = "roradmin"
GEONAMES['URL'] = 'https://secure.geonames.net/getJSON'

def url_validation(url):
    return validators.url(url)

def get_schema_from_url(version):
    url = ''
    if version == '1':
        print("getting v1 schema")
        url = DEFAULT_SCHEMA_V1_0
    if version == '2':
        print("getting v2 schema")
        url = DEFAULT_SCHEMA_V2_0
    rsp = requests.get(url)
    rsp.raise_for_status()
    return rsp.json()

def get_json(arg,type="file"):
    if (type == "file"):
        try:
            with open(arg, 'r') as f:
                data = json.load(f)
        except Exception as e:
            raise(e)
    elif (type == "url"):
        data = get_file_from_url(arg)
    return data

def arg_exists(arg):
    check_path = os.path.exists(arg)
    if not(check_path):
        raise Exception(f"{arg} is required and must exist")
