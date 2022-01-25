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
GEONAMES['URL'] = 'http://api.geonames.org/getJSON'

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

def get_relationship_pairing(file):
    relation = []
    rel_dict = {}
    try:
        with open(file, 'r') as rel:
            relationships = DictReader(rel)
            for row in relationships:
                check_record_id = parse_record_id(row['Record ID'])
                check_related_id = parse_record_id(row['Related ID'])
                if (check_record_id and check_related_id): 
                    rel_dict['short_record_id'] = check_record_id
                    rel_dict['short_related_id'] = check_related_id
                    rel_dict['record_name'] = row['Name of org in Record ID']
                    rel_dict['record_id'] = row['Record ID']
                    rel_dict['related_id'] = row['Related ID']
                    rel_dict['related_name'] = row['Name of org in Related ID']
                    rel_dict['record_relationship'] = row['Relationship of Related ID to Record ID']
                    rel_dict['related_location'] = row['Current location of Related ID']
                    relation.append(rel_dict.copy())
    except IOError as e:
        raise RuntimeError(f"Reading file {file}: {e}")
    return relation

def arg_exists(arg):
    check_path = os.path.exists(arg)
    if not(check_path):
        raise Exception(f"{arg} is required and must exist")
