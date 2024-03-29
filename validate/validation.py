import json
import sys
import requests
import validators
import pycountry
import validate.utilities as u
import validate.helpers as vh
import validate.relationships as vr
import datetime as dt

class Validate_Tests:
    def __init__(self,file):
        #instantiate validate class with json record
        vh.File = file

    def _validator_functions(self):
        # getting public methods for the class.
        #Do not have to hardcode functions that will be checked as all validator functions should be public
        m = [attribute for attribute in dir(self) if callable(getattr(self, attribute)) and attribute.startswith('_') is False]
        return m

    def check_links(self):
        # public method for url format validation
        name = str(self.check_links.__name__)
        msg = {}
        links = vh.File['links']
        links.append(vh.File['wikipedia_url'])
        # removing empty strings
        links = list(filter(None, links))
        if len(links) > 0:
            for l in links:
                result = vh.validate_url(l)
                if result:
                    msg[l] = result
        if len(msg) == 0:
            msg = None
        return vh.handle_check(name,msg)

    def check_address(self):
        # compares ror and geonames address values
        name = str(self.check_address.__name__)
        id, address = vh.get_record_address()
        result = None
        compare = {}
        geonames_response,msg = vh.get_geonames_response(id)
        if geonames_response:
            mapped_fields = vh.mapped_geoname_record()
            compare = vh.compare_ror_geoname(mapped_fields,address,geonames_response,{})
            #compares the country in the record against the response
            country_test = vh.check_country(geonames_response)
            if country_test:
                compare.update(country_test)
        else:
            compare["ERROR"] = msg
        return vh.handle_check(name,compare)

    def check_language_code(self):
        # checks language code
        name = str(self.check_language_code.__name__)
        language = vh.File['labels']
        msg = None
        if len(language) > 0:
            pylanguage = pycountry.languages.get(alpha_2=language[0]['iso639'])
            if not(pylanguage):
                msg = f'Language value: {language} is not an iso639 standard'
        return vh.handle_check(name,msg)

    def check_established_year(self):
        # checks established year
        name = str(self.check_established_year.__name__)
        yr = vh.File['established']
        msg = None
        if isinstance(yr, int) and (yr <= 99 or yr > dt.date.today().year):
            msg = f'Year value: {yr} should be an integer between 3 and 4 digits'
        return vh.handle_check(name,msg)

    def validate_all(self, check_address, file_path=None, rel_file=None):
        print("Validating " + vh.File['id'])
        # calling all public methods in this class and removing the current method name.
        # This enables future public methods to be called automatically as well
        method_name = str(self.validate_all.__name__)
        validator_functions = self._validator_functions()
        validator_functions.remove(method_name)
        if not check_address:
            method_name = str(self.check_address.__name__)
            validator_functions.remove(method_name)

        results = []
        for methods in validator_functions:
            validate = getattr(self, methods)
            results.append(validate())
        if file_path:
             # if relationship is being checked
            msg = vr.process_relationships(current_record = vh.File, file_path=file_path, rel_file=rel_file)
            if msg:
                results.append({'relationships':msg})
        results = list(filter(None,results))
        return results
