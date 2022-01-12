import json
import sys
import os
import requests
from validate.utilities import *

info = {"file_path": None, "record_info": None}
errors = []

def rel_pair_validator(label):
    """Setting up the relationship pairs for relationship types"""

    p = "Parent"
    c = "Child"
    r = "Related"
    pair = {p: c, c: p, r: r}
    return pair.get(label, None)


def rel_values_mapping():
    """Setting up the relationship pairs for institution names"""
    return {"label": "name", "id": "id"}


def validate_relationship(file_rel, related_rel):
    err = {}
    err[related_rel['id']] = []
    org_id = info["record_info"]["id"]
    org_name = info["record_info"]["name"]
    paired_value = rel_pair_validator(file_rel['type'])

    # Relationship type occur in pairs, they must equal the paired controlled vocabulary
    if not (paired_value == related_rel['related_relationship']['type']):
        err[related_rel['id']].append(f"Illegal relationship pairing: relationship type: {related_rel['related_relationship']['type']} should be {paired_value}")

    # Names of related institutions must equal each other
    mappings = rel_values_mapping()
    for k, v in mappings.items():
        if not (file_rel[k] == related_rel[v]) or not (
                related_rel['related_relationship'][k]
                == info['record_info'][v]):
            err[related_rel['id']].append(f"Values are not equal: validating record: {info['record_info'][v]} and relationship: {file_rel} and related record: {related_rel}")
    if err[related_rel['id']]:
        errors.append(err)


def generate_related_relationships(id, name, rel):
    record = {}
    record['id'] = id
    record['name'] = name
    if len(rel) > 0:
        record['related_relationship'] = list(
            filter(lambda d: d['id'] == info["record_info"]["id"], rel))
    if (len(rel) == 0) or (len(record['related_relationship']) == 0):
        record['related_relationship'] = None
    else:
        record['related_relationship'] = record['related_relationship'][0]
    return record


def get_related_records(record_id):
    related_record = {}
    filename = info["file_path"] + "/" + record_id.split(
        "ror.org/")[1] + ".json"
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            related_record = generate_related_relationships(
                data['id'], data['name'], data['relationships'])
        except Exception as e:
            print(f"Couldn't open file {filename}: {e}")
    return related_record


def check_relationships():
    files_exist = []
    for record in info['record_info']['rel']:
        related_relshp = get_related_records(record['id'])
        if related_relshp:
            files_exist.append(record['id'])
            if related_relshp['related_relationship']:
                validate_relationship(record, related_relshp)
            else:
                errors.append(
                    f"Related relationship not found for {related_relshp['id']}")
    if len(files_exist) == 0:
        errors.append(f"Relationships exist for {info['record_info']['id']}. At least one file listed in relationships must exist")    
    return errors
