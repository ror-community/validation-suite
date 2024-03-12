import json
import sys
import requests
import validators

import validate.utilities as u
import validate.helpers as vh
import validate.relationships as vr
import validate.relationships_v2 as vr2
import validate.domains_v2 as vd2
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
        labels = vh.File['labels']
        msg = {}
        if len(labels) > 0:
            for label in labels:
                result = vh.check_lang_code(label['iso639'])
                if result:
                    msg = result
        if len(msg) == 0:
            msg = None
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

class Validate_Tests_V2:
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
        links = [link['value'] for link in vh.File['links']]
        # removing empty strings
        links = list(filter(None, links))
        duplicates = []
        if len(links) > 0:
            duplicates = vh.check_duplicates(links)
        if len(duplicates) > 0:
            msg['LINKS_DUPLICATES_ERROR'] = "Multiple links have the same value(s): " + ", ".join(duplicates)
            for l in links:
                result = vh.validate_url(l)
                if result:
                    msg[l] = result
        if len(msg) == 0:
            msg = None
        return vh.handle_check(name,msg), None

    def check_names(self):
        name = str(self.check_names.__name__)
        error_msg = {}
        warn_msg = {}
        name_types = []
        for record_name in vh.File['names']:
            for name_type in record_name['types']:
                name_types.append(name_type)
        ror_display_count = [name_type for name_type in name_types if name_type == 'ror_display']
        if len(ror_display_count) != 1:
            error_msg['NAMES_TYPES_ERROR'] = f'Exactly 1 name must have type ror_display. {len(ror_display_count)} names have ror_display in their name types.'

        names = [record_name['value'] for record_name in vh.File['names']]
        duplicates = vh.check_duplicates(names)
        if len(duplicates) > 0:
            warn_msg['NAMES_DUPLICATES_WARNING'] = "Multiple names have the same value(s): " + ", ".join(duplicates)
        lang_errors = []
        for record_name in vh.File['names']:
            if record_name['lang'] and record_name['lang'] != "":
                result = vh.check_lang_code(record_name['lang'])
                if result:
                    lang_errors.append(result)
        if len(lang_errors) > 0:
            error_msg['NAMES_LANG_ERROR'] = lang_errors
        if len(error_msg) == 0:
            error_msg = None
        if len(warn_msg) == 0:
            warn_msg = None
        return vh.handle_check(name,error_msg), vh.handle_check(name,warn_msg)

    def check_locations(self):
        # compares ror and geonames address values
        print("checking locations")
        name = str(self.check_locations.__name__)
        msg = {}
        for location in vh.File['locations']:
            location_errors = {}
            geonames_id = location['geonames_id']
            geonames_response,geonames_error = vh.get_geonames_response(geonames_id)
            result = None
            compare = {}
            if geonames_response:
                mapped_fields = vh.mapped_geoname_record_v2()
                #compares the country in the record against the response
                location_errors = vh.compare_ror_geoname_v2(mapped_fields,location,geonames_response,{})
            else:
                location_errors = geonames_error
            if location_errors:
                msg['LOCATION_ERROR_GEONAMES_ID_' + str(geonames_id)] = location_errors
        return vh.handle_check(name,msg), None

    def check_external_ids(self):
        name = str(self.check_external_ids.__name__)
        msg = {}
        # check that only 1 item exists for each external ID type
        id_types = [external_id['type'] for external_id in vh.File['external_ids']]
        duplicate_types = vh.check_duplicates(id_types)
        if len(duplicate_types) > 0:
            msg['EXT_IDS_DUPLICATE_TYPES_ERROR'] = "Multiple external ID items have the same type(s): " + ", ".join(duplicate_types)
        # if 'preferred' has a value, check that the value also exists in 'preferred' list
        preferred_not_in_all = []
        for external_id in vh.File['external_ids']:
            if external_id['preferred']:
                if external_id['preferred'] not in external_id['all']:
                    preferred_not_in_all.append({external_id['type']: external_id['preferred']})
        if len(preferred_not_in_all) > 0:
            msg['EXT_IDS_PREFERRED_ERROR'] = "1 or more external ID items have a value in preferred that is not included in all: " + str(preferred_not_in_all)
        return vh.handle_check(name,msg), None


    def check_domains(self):
        name = str(self.check_domains.__name__)
        msg = {}
        domains = vh.File['domains']
        domains = list(filter(None, domains))
        # check whether subdomains of other domains listed in the same ROR record exist
        substring_matches = vh.check_substrings(domains)
        if len(substring_matches) > 0:
            msg['DOMAINS_ERROR'] = "Domains contains subdomains of other domains: " + ", ".join(substring_matches)
        return vh.handle_check(name,msg), None


    def check_established_year(self):
        # checks established year
        name = str(self.check_established_year.__name__)
        yr = vh.File['established']
        msg = None
        if isinstance(yr, int) and (yr <= 99 or yr > dt.date.today().year):
            msg = f'Year value: {yr} should be an integer between 3 and 4 digits'
        return vh.handle_check(name,msg), None

    def validate_all(self, check_address, check_domains, file_path=None, rel_file=None):
        print("Validating " + vh.File['id'])
        # calling all public methods in this class and removing the current method name.
        # This enables future public methods to be called automatically as well
        method_name = str(self.validate_all.__name__)
        validator_functions = self._validator_functions()
        validator_functions.remove(method_name)
        if not check_address:
            method_name = str(self.check_locations.__name__)
            validator_functions.remove(method_name)

        errors = []
        warnings = []
        for methods in validator_functions:
            validate = getattr(self, methods)
            error_msg, warn_msg = validate()
            errors.append(error_msg)
            warnings.append(warn_msg)
            #results.append(validate())
        if check_domains and len(vh.File['domains']) > 0:
            print("checking domains")
            msg = vd2.check_domains(current_record = vh.File, file_path=file_path)
            if msg:
                errors.append({'domains':msg})
        if file_path:
             # if relationship is being checked
            msg = vr2.process_relationships(current_record = vh.File, file_path=file_path, rel_file=rel_file)
            if msg:
                errors.append({'relationships':msg})
        errors = list(filter(None,errors))
        warnings = list(filter(None,warnings))
        return errors, warnings

