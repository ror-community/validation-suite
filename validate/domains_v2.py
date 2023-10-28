import json
import os
import requests

API_URL = "http://api.dev.ror.org/v2/organizations"


def get_files(file_path):
    file = []
    if os.path.isdir(file_path):
        path = os.path.normpath(file_path)
        for f in os.listdir(file_path):
            file.append(f)
        files = list(map(lambda x: path+"/"+x, file))
    else:
        raise RuntimeError(f"{file_path} must be a valid file or directory")
    return files

def check_domains_release(record, files):
    errors = []
    for domain in record['domains']:
        records_with_domain = []
        for file in files:
            with open(file) as infile:
                release_record = json.load(infile)
                if domain in release_record['domains']:
                    records_with_domain.append(release_record['id'])
        if records_with_domain > 0:
            errors.append(f"Record {record['id']} has a domain that exists on a production record: {domain}.")
    return errors

def check_domains_prod(record):
    errors = []
    for domain in record['domains']:
        params = {'query.advanced': 'domains:' + domain}
        try:
            rsp = requests.get(API_URL, params=params)
            print(rsp.url)
            rsp.raise_for_status()
            response = rsp.json()
            if response['number_of_results'] > 0:
                ids = [item['id'] for item in response['items']]
                errors.append(f"{domain} exists on {response['number_of_results']} production record(s): {', '.join(ids)}.")
        except requests.exceptions.RequestException as e:
            raise RuntimeError (f"Couldn't complete request {rsp.url}: {e}")
    return errors


def check_domains(current_record, file_path):
    msg = None
    if file_path:
        files = get_files(file_path)
        msg = check_domains_release(current_record, files)
    if len(msg) == 0:
        msg = check_domains_prod(current_record)
    return msg
