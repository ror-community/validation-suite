import os
import zipfile
import requests
import json
import sys
import validators
from csv import DictReader

DEFAULT_SCHEMA = "https://raw.githubusercontent.com/ror-community/ror-schema/master/ror_schema.json"
API_URL = "https://api.ror.org/organizations"

GEONAMES = {}
GEONAMES['USER'] = "roradmin"
GEONAMES['URL'] = 'https://secure.geonames.net/getJSON'

def url_validation(url):
    return validators.url(url)

def get_file_from_url(url=DEFAULT_SCHEMA):
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
