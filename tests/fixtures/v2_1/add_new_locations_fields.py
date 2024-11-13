import argparse
import copy
import json
import os
import sys
import re

V2_1_LOCATIONS = [
        {
            "geonames_id": 5378538,
            "geonames_details": {
                "continent_code": "NA",
                "continent_name": "North America",
                "country_code": "US",
                "country_name": "United States",
                "country_subdivision_code": "CA",
                "country_subdivision_name": "California",
                "lat": 37.802168,
                "lng": -122.271281,
                "name": "Oakland"
            }
        }
    ]

def update_file(file):
    with open(file, "r+") as infile:
        data = json.load(infile)
        data["locations"] = V2_1_LOCATIONS
        infile.seek(0)  # rewind
        json.dump(data, infile)
        infile.truncate()

def get_files(input):
    files = []
    if os.path.isfile(input):
        files.append(input)
    elif os.path.isdir(input):
        file = []
        path = os.path.normpath(input)
        for f in os.listdir(input):
            file.append(f)
        files = list(map(lambda x: path+"/"+x, file))
    else:
        raise RuntimeError(f"{input} must be a valid file or directory")
    return files


def main():
    parser = argparse.ArgumentParser(description="Script to generate v1 ROR record from v2 record")
    parser.add_argument('-i', '--inputpath', type=str, required=True)

    args = parser.parse_args()

    files = get_files(args.inputpath)

    if files:
        print(f"Converting files in {args.inputpath}")
        for file in files:
            print(f"Processing {file}")
            update_file(file)
    else:
        print("No files exist in " + args.inputpath)

if __name__ == "__main__":
    main()

