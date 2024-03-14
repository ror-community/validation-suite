import json
import os
import re
import requests
from csv import DictReader
from validate.utilities import *
import validate.helpers as vh

API_URL = "http://api.ror.org/v2/organizations/"
INVERSE_TYPES = ('parent', 'child', 'related')
INFO = {"file_path": '', "record_info": {}, "errors": []}

def rel_pair_validator(label):
    """Setting up the relationship pairs for relationship types"""

    p = "parent"
    c = "child"
    r = "related"
    pr = "predecessor"
    s = "successor"
    pair = {p: c, c: p, r: r, pr: None, s: None}
    return pair.get(label, None)


def rel_values_mapping():
    """Setting up the relationship pairs for institution names"""
    return {"label": "name", "id": "id"}

def validate_relationship(file_rel, related_rel):
    err = {}
    err[related_rel['id']] = []
    paired_value = rel_pair_validator(file_rel['type'])

    if paired_value is not None:
        # Some relationship types occur in pairs, they must equal the paired controlled vocabulary
        if not (paired_value == related_rel['related_relationship']['type']):
            err[related_rel['id']].append(f"Illegal relationship pairing: relationship type: {related_rel['related_relationship']['type']} should be {paired_value}")

    # Names of related institutions must equal each other
    mappings = rel_values_mapping()
    for k, v in mappings.items():
        if not (file_rel[k] == related_rel[v]) or (related_rel['related_relationship'] is not None and not (
                related_rel['related_relationship'][k]
                == INFO['record_info'][v])):
            err[related_rel['id']].append(f"Values are not equal: validating record: {INFO['record_info'][v]} and relationship: {file_rel} and related record: {related_rel}")
    if err[related_rel['id']]:
        INFO["errors"].append(err)


def generate_related_relationships(id, names, status, rel):
    record = {}
    record['id'] = id
    record['names'] = vh.get_ror_display_name(names)
    record['status'] = status
    if len(rel) > 0:
        record['related_relationship'] = list(
            filter(lambda d: d['id'] == INFO["record_info"]["id"], rel))
    if (len(rel) == 0) or (len(record['related_relationship']) == 0):
        record['related_relationship'] = None
    else:
        record['related_relationship'] = record['related_relationship'][0]
    return record

def get_related_record(record_id):
    related_record = {}
    filename = INFO["file_path"] + "/" + record_id.split(
        "ror.org/")[1] + ".json"
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            related_record = generate_related_relationships(
                data['id'], data['names'], data['status'], data['relationships'])
        except Exception as e:
            raise RuntimeError (f"Couldn't open file {filename}: {e}")
    return related_record

def get_related_record_api(record_id):
    related_record = {}
    download_url = API_URL + record_id
    try:
        rsp = requests.get(download_url)
        rsp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError (f"Couldn't download record {download_url}: {e}")
    try:
        response = rsp.json()
        related_record = generate_related_relationships(
                response['id'], response['names'], response['status'], response['relationships'])
    except Exception as e:
        raise RuntimeError (f"Couldn't generate related record data for {download_url}: {e}")

    return related_record

def get_related_name_api(related_id):
    name = None
    download_url=API_URL + related_id
    try:
        rsp = requests.get(download_url)
        rsp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request for {download_url}: {e}")
    try:
        response = rsp.json()
        name = vh.get_ror_display_name(response['names'])
    except Exception as e:
        raise RuntimeError(f"Getting name for {related_id}: {e}")
    return name

def parse_record_id(id):
    parsed_id = None
    pattern = '^https:\/\/ror.org\/(0[a-z|0-9]{8})$'
    ror_id = re.search(pattern, id)
    if ror_id:
        parsed_id = ror_id.group(1)
    else:
        INFO["errors"].append(f"ROR ID: {id} does not match format: {pattern}. Record will not be validated")
    return parsed_id

def read_relationship_from_file(rel_file):
    relationships = []
    rel_dict = {}
    try:
        with open(rel_file, 'r') as rel:
            rel_file_dict = DictReader(rel)
            for row in rel_file_dict:
                check_record_id = parse_record_id(row['Record ID'])
                check_related_id = parse_record_id(row['Related ID'])
                if (check_record_id and check_related_id):
                    rel_dict['short_record_id'] = check_record_id
                    rel_dict['short_related_id'] = check_related_id
                    rel_dict['record_id'] = row['Record ID']
                    rel_dict['related_id'] = row['Related ID']
                    rel_dict['record_relationship'] = row['Relationship of Related ID to Record ID']
                    relationships.append(rel_dict.copy())
    except IOError as e:
        raise RuntimeError(f"Reading file {rel_file}: {e}")
    return relationships

def get_single_related_relationship(related_id):
    return get_related_record(related_id)

def check_relationships_from_file(rel_file):
    files_exist = []
    relationships = read_relationship_from_file(rel_file)
    get_file_ids = list(i['record_id'] for i in relationships)
    if INFO["record_info"]['id'] in get_file_ids:
        if INFO["record_info"]['rel']:
            all_current_id_relationships = list(i for i in relationships if i['record_id'] == INFO["record_info"]['id'])
            for r in all_current_id_relationships:
                file_rel = list(rel for rel in INFO["record_info"]['rel'] if rel['id'] == r['related_id'])
                if len(file_rel)==0:
                    INFO["errors"].append(f"Relationship to {r['related_id']} is missing from file for {INFO['record_info']['id']}")
                else:
                    file_rel = file_rel[0]
                    related_relshp = get_related_record(r['related_id'])
                    if not related_relshp and r['record_relationship'] not in INVERSE_TYPES:
                        related_relshp = get_related_record_api(r['related_id'])
                    if related_relshp:
                        files_exist.append(r['related_id'])
                        if related_relshp['related_relationship'] or r['record_relationship'] not in INVERSE_TYPES:
                            validate_relationship(file_rel, related_relshp)
                        else:
                            INFO["errors"].append(
                            f"Relationship is a type that must have inverse in related record but related relationship not found for {related_relshp['id']}")
            if len(files_exist) == 0:
                INFO["errors"].append(f"According to {rel_file}, relationships exist for {INFO['record_info']['id']}. At least one file listed in relationships must exist")
        else:
            INFO["errors"].append(f"According to {rel_file}, relationships exist for {INFO['record_info']['id']}. However, no relationships exist in the file")
    return INFO["errors"]

def check_relationships():
    files_exist = []
    for relationship in INFO['record_info']['rel']:
        related_relshp = get_related_record(relationship['id'])
        if related_relshp:
            files_exist.append(relationship['id'])
            if related_relshp['related_relationship']:
                validate_relationship(relationship, related_relshp)
            else:
                INFO["errors"].append(
                    f"Related relationship not found for {related_relshp['id']}")
    if len(files_exist) == 0:
        INFO["errors"].append(f"Relationships exist for {INFO['record_info']['id']}. At least one file listed in relationships must exist")
    return INFO["errors"]

def check_file_exists(record_id):
    filename = INFO["file_path"] + "/" + record_id.split(
        "ror.org/")[1] + ".json"
    return os.path.exists(filename)

def check_relationships_removed():
    related_active_records = []
    for relationship in INFO['record_info']['rel']:
        if check_file_exists(relationship['id']):
            print("File exists for " + relationship['id'])
            related_relshp = get_related_record(relationship['id'])
        else:
            print("File does not exist. Fetching relationships from API for " + relationship['id'])
            related_relshp = get_related_record_api(relationship['id'])
        if related_relshp['related_relationship'] and related_relshp['status'] == 'active':
            related_active_records.append(related_relshp['related_relationship'])
    related_active_records_not_predecessor = [r for r in related_active_records if r['type'] != 'predecessor']
    if len(related_active_records_not_predecessor) > 0:
        INFO["errors"].append(f"Inactive record {INFO['record_info']['id']} has {str(len(related_active_records_not_predecessor))} relationshps to active records. These relationships must be removed.")
    return INFO["errors"]

def check_duplicate_relationships():
    duplicates = []
    duplicate_types = []
    rel_types = [r['type'] for r in INFO["record_info"]['rel']]
    rels_grouped_by_type = {}
    for type in rel_types:
        current_type_ids = []
        for rel in INFO["record_info"]['rel']:
            if rel['type'] == type:
                current_type_ids.append(rel['id'])
        rels_grouped_by_type[type] = current_type_ids
    for type, ids in rels_grouped_by_type.items():
        current_duplicates = [i for i in ids if ids.count(i) > 1]
        if len(current_duplicates) > 0:
            duplicate_types.append(type)
        duplicates.extend(current_duplicates)
    if len(duplicates) > 0:
        INFO["errors"].append(f"Record {INFO['record_info']['id']} has duplicate relationships in type(s): {duplicate_types}. Please check and remove duplicates.")
    return INFO["errors"]


def process_relationships(current_record, file_path, rel_file=None):
    msg = None
    INFO["errors"] = []
    INFO["file_path"] = file_path
    INFO["record_info"] = vh.get_relationship_info_v2()

    msg = check_duplicate_relationships()
    if len(msg) == 0:
        if rel_file and current_record['status'] == 'active':
            msg = check_relationships_from_file(rel_file)
        else:
            if INFO["record_info"]['rel']:
                if current_record['status'] == 'active':
                    msg = check_relationships()
                else:
                    msg = check_relationships_removed()
    return msg
