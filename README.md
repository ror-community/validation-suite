# Validation Suite

This is a collection of tests that validate the following:

* schema
* Relationship pair checking:
   * Check that the relationship pairs are accurate.
   * If a relationship is established in one file, the corresponding relationship should exist in the file listed in the file that is being validated.
* Checks address against the geonames address
* ISO code for language
* Makes sure links are in the correct format
* Checks established year

## Running the Suite
To run it with docker, please do the following:
* Make sure docker and docker-compose are installed
* For a demo run, do the following:
  * `docker-compose up -d`
  * `docker exec validate python run_validation.py -i ror-files/valid/015m7wh34.json -p ror-files/valid`. This validates one file and checks the path listed for other files that will be listed in relationships of the file being validated, if they exist.
* To see what arguments are needed for the script, do the following:
```
$ docker exec validate python run_validation.py -h
usage: run_validation.py [-h] -i INPUT [-s SCHEMA] [-p FILE_PATH]
Script to validate ROR files
optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to one file or one directory for validation
  -s SCHEMA, --schema SCHEMA
                        Path or URL to schema
  -p FILE_PATH, --file-path FILE_PATH
                        Path to the rest of the files for relationship
                        validation
```
* To run the script against a directory on the local machine, the directory should be mounted in the docker-compose file and can be continued as above
 * For example, to run the script against a directory, mount the directory in the `docker-compose.yml` file here:

   ```
   volumes:
   - .:/usr/src/app
   #- mount additional test files here. Ex:
   #-path/on/local/machine/ror-files:/path/in/container/ror-files
   ```
   * An example of running the script against a directory:`docker exec validate python run_validation.py -i test-files/invalid`
* If a file is invalid, the script will print out the errors to stdout and will have an exit code of 1. If the file passes validation, the exit code will be 0.
