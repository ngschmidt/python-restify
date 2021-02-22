#!/usr/bin/python3
# Python REST CLI Class
# Nicholas Schmidt
# 13 Feb 2021

# API Processing imports
import requests

# Command line validating imports
from django.core.validators import URLValidator

# JSON is the storage method leveraged for play storage, settings, etc.
import json

class Reliquary:

    # Initial Variable Settings
    #
    cogitation_verbosity = 0
    cogitation_certvalidation = True
    cogitation_username = ''
    cogitation_password = ''
    cogitation_authkey = ''
    cogitation_authcert = ''
    cogitation_endpoint = ''
    cogitation_bibliotheca = {}
    cogitation_errors = {}

    # We're pretty much picking up our configuration data
    def __init__(self, input_settings):

        # Load Settings from JSON
        try: 
            json_filehandle = open(input_settings, 'r')
            json_settings = json.load(json_filehandle)
        except:
            print('E0000: Error Loading Settings File!')
            exit()

        try:
            # Let's start with basic global settings
            self.cogitation_verbosity =         json_settings['settings']['verbosity']
            self.cogitation_endpoint =          json_settings['settings']['endpoint']
            # TLS Tuning
            self.cogitation_certvalidation =    json_settings['settings']['tls']['validation']
            # Authentication Settings
            self.cogitation_username =          json_settings['settings']['authentication']['username']
            self.cogitation_password =          json_settings['settings']['authentication']['password']
            self.cogitation_authcert =          json_settings['settings']['authentication']['certificate']
            self.cogitation_authkey =           json_settings['settings']['authentication']['key']
            # Load Known API Actions
            self.cogitation_bibliotheca =       json_settings['plays']
            # Load HTTP Errors
            self.cogitation_errors =            json_settings['errors']
        except:
            print('E0002: Error Loading Settings! Settings Dictionary:')
            print(json.dumps(json_settings, indent=4))
            exit()

        # 99% solution here is to validate that a URL provided is valid. This doesn't test it or anything
        validate = URLValidator()
        try:
            validate(self.cogitation_endpoint)
        except:
            print('E0001: Invalid URL Formatting. Example: "https://www.abc.com/"')
            exit()

    # Functions

    # Do API DELETE, using basic credentials
    def do_api_delete(self, do_api_thing, do_api_object):
        # Perform API Processing - conditional basic authentication
        try:
            do_api_get_headers = {
                'content-type': 'application/json',
                'X-Allow-Overwrite': 'true'
            }
            do_api_get_url = self.cogitation_endpoint + self.cogitation_bibliotheca[do_api_thing][0] +
                                do_api_object + self.cogitation_bibliotheca[do_api_thing][1]
            do_api_get_r = requests.delete(do_api_get_url, headers=do_api_get_headers, verify=self.cogitation_certvalidation, auth=(self.cogitation_username, self.cogitation_password))
            # We'll be discarding the actual `Response` object after this, but we do want to get HTTP status for erro handling
            response_code = do_api_get_r.status_code
            print(response_code)
            do_api_get_r.raise_for_status()  # trigger an exception before trying to convert or read data. This should allow us to get good error info
            return do_api_get_r.text  # if HTTP status is good, save response
        except requests.Timeout:
            print('E1000: API Connection timeout!')
        except requests.ConnectionError as connection_error:
            print(connection_error)
        except requests.HTTPError:
            if self.get_http_error_code(response_code):
                print('EA' + str(response_code) + ': HTTP Status Error ' + str(response_code) + ' ' + self.get_http_error_code(response_code))
                return do_api_get_r.text
            else:
                print('EA999: Unhandled HTTP Error ' + str(response_code) + '!')
                exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
        except requests.RequestException as requests_exception:
            print(requests_exception)
        except Exception as e:
            print('E1002: Unhandled Requests exception! ' + str(e))
            exit()

    # Do API GET, using basic credentials
    def do_api_get(self, do_api_thing, do_api_object):
        # Perform API Processing - conditional basic authentication
        try:
            do_api_get_headers = {
                'content-type': 'application/json',
                'X-Allow-Overwrite': 'true'
            }
            do_api_get_url = self.cogitation_endpoint + self.cogitation_bibliotheca[do_api_thing][0] + do_api_object
            do_api_get_r = requests.get(do_api_get_url, headers=do_api_get_headers, verify=self.cogitation_certvalidation,
                                        auth=(self.cogitation_username, self.cogitation_password))
            # We'll be discarding the actual `Response` object after this, but we do want to get HTTP status for erro handling
            response_code = do_api_get_r.status_code
            print(response_code)
            do_api_get_r.raise_for_status()  # trigger an exception before trying to convert or read data. This should allow us to get good error info
            return do_api_get_r.text  # if HTTP status is good, save response
        except requests.Timeout:
            print('E1000: API Connection timeout!')
        except requests.ConnectionError as connection_error:
            print(connection_error)
        except requests.HTTPError:
            if self.get_http_error_code(response_code):
                print('EA' + str(response_code) + ': HTTP Status Error ' + str(response_code) + ' ' + self.get_http_error_code(response_code))
                return do_api_get_r.text
            else:
                print('EA999: Unhandled HTTP Error ' + str(response_code) + '!')
                exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
        except requests.RequestException as requests_exception:
            print(requests_exception)
        except Exception as e:
            print('E1002: Unhandled Requests exception! ' + str(e))
            exit()

    def get_http_error_code(self, get_http_error_code_code):
        return json.dumps(self.cogitation_errors[get_http_error_code_code], indent=4)
