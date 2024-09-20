# Validation Suite

Checks whether ROR records are schema valid against a specified JSON schema doc and performs additional tests depending on the specified schema version.

## Pre-requisites
- [Docker](https://www.docker.com/)
- [Docker compose](https://docs.docker.com/compose/install/)

## Running the Suite

### Basic usage
1. Inside the validation-suite directory, start the Docker container using Docker compose

        cd validation-suite
        docker-compose up -d

2. To validate a single ROR record WITHOUT relationship validation, specify the path to the record as the `-i` argument and the schema version as the `-v` argument.

        docker exec validate python run_validations.py -i tests/fixtures/v1/valid/015m7wh34.json -v 1

3. To validate multiple ROR records WITHOUT relationship validation, specify the path to the directory the records are located as the `-i` argument and the schema version as the `-v` argument.

        docker exec validate python run_validations.py -i tests/fixtures/v1/valid/ -v 1

4. To validate an entire ROR dump WITHOUT relationship validation, specify the path to the dump zip file in the `-i` argument and the schema version as the `-v` argument. When validating an entire dump, also specify a local schema file using the `-s` argument so that the code does not hit the Github API rate limit.

        docker exec validate python run_validations.py -i tests/fixtures/v1/valid/v1.29-2023-07-27-ror-data.zip -v 1 -s tests/fixtures/v1/schema/ror_schema.json

### Mounting a local directory

Examples above use files that are needed in order to run tests in the `tests/` directory. You can add files to these directories locally, but please do not commit additional files, as they could causes problems running tests. Alternately, to run the script against a directory on your local machine, mount the directory in the `volumes` section of the docker-compose file:

        volumes:
        - .:/usr/src/app
        #- mount additional test files here. Ex:
        #-path/on/local/machine/ror-files:/path/in/container/ror-files

### Validating relationships

Relationship pairings are not validated by default. To check that correct relationship pairings exist (ex: if a record being validated has a parent relationship, the corresponding record has a child relationship with the correct name in the label field), specify the path to a directory that contains the related ROR record files using the `-p` argument.

        docker exec validate python run_validations.py -i tests/fixtures/v1/valid/ -v 1 -p tests/fixtures/v1/valid/

- Directory path can be the same as the input path as specified in `-i`
- If a record file is not found in the specified directory, the record will be downloaded from the production API
- Directoy can be empty, if you would like to validate relationships against production (will fail if related records don't exist in production, ex if you are validating files during the release process)
- If the `-p` argument is not included, relationship pairing validation is skipped, but schema validation of the relationhips field is still performed

During the release process, relationships are added/updated using a script that references a relationships.csv that is included in every release that includes relationship changes. Relationships can be validated against this CSV using the `-r` argument to specify the path to the CSV.

        docker exec validate python run_validations.py -i files/ -p files/ -f relationships.csv

### Skipping Geonames validation

By default, Geonames information in the v1 `addresses` and v2 `locations` fields is validated against the Geonames API. Validating a large number of files or an entire data dump with Geonames validation enabled takes a long time and can result in Geonames API rate limiting. For quicker validation, use the `-n` flag to disable validation against the Geonames API. **Always use this flag when validating an entire data dump.**

        docker exec validate python run_validations.py -i tests/fixtures/v1/valid/v1.29-2023-07-27-ror-data.zip -v 1 -s tests/fixtures/v1/schema/ror_schema.json -n

### Specifying a schema file

By default, the schema file to validate against is retrieved from https://github.com/ror-community/ror-schema . Validating a large number of files or an entire data dump takes a long time and can result in Github rate limiting. For quicker validation, use the `-s` argument to point to a local copy of the schema file (such as the copy in the tests/fixtures/ directory). Make sure this file corresponds to the version specified in the `-v` argument. Always use this flag when validating an entire data dump.

        docker exec validate python run_validations.py -i tests/fixtures/v1/valid/v1.29-2023-07-27-ror-data.zip -v 1 -s tests/fixtures/v1/schema/ror_schema.json -n

`-s` can also be used when testing schema changes.

## Argument reference

- `-i` (required) Path to a JSON file, a directory containing JSON files or a data dump zip file
- `-v` (required) ROR schema version to validate against (1 or 2)
- `-s` Path or URL to schema file. If not specified, schema will be retrieved from https://github.com/ror-community/ror-schema .
- `-p` Path to the rest of the ROR record files for relationship pairing validation. Relationship pairing validation is skipped if this argument is not included.
- `-r` Path to the CSV file containing relationship mappings. Used during release process.
- `-n` Skip Geonames API validation for address fields

## Invalid files
- An example of running the script against a directory that has invalid files:`docker exec validate python run_validations.py -i tests/fixtures/v1/invalid/usecase-issues`
- If a file is invalid, the script will print out the errors to stdout and will have an exit code of 1. If the file passes validation, the exit code will be 0.
- To look at the output of a file that is validates incorrectly against the schema, run this as an example: `docker exec validate python run_validations.py -i tests/fixtures/v1/invalid/schema-issues/enum_values/bad-relationship-type.json`

## Running tests
1. Inside the validation-suite directory, start the Docker container using Docker compose

        cd validation-suite
        docker-compose up -d

2. Run the tests

        docker exec validate pytest tests/integration/
