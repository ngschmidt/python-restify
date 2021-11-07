#!/usr/bin/python3
# Python REST CLI Tool, supporting classes
# Nicholas Schmidt
# 06 Mar 2021

# API Processing imports
import requests

# Command line validating imports
from django.core.validators import URLValidator

# JSON is how we import/export just about everything here...
import json

# Method Overloading via decorator
from multipledispatch import dispatch


# Begin Supporting Classes
class Settings:
    # Initial Variable Settings
    #
    settings_file = {
        "settings": {
            "authentication": {
                "username": "admin",
                "password": "password",
                "method": "basic",
                "certificate": "",
                "key": "",
            },
            "tls": {"validation": False},
            "verbosity": 1,
            "endpoint": "https://nsx.lab.engyak.net",
        },
        "plays": {},
        "errors": {
            "200": ["OK", "Request fulfilled, document follows"],
            "201": ["Created", "Document created, URL follows"],
            "202": ["Accepted", "Request accepted, processing continues off-line"],
            "203": ["Non-Authoritative Information", "Request fulfilled from cache"],
            "204": ["No Content", "Request fulfilled, nothing follows"],
            "205": ["Reset Content", "Clear input form for further input."],
            "206": ["Partial Content", "Partial content follows."],
            "300": ["Multiple Choices", "Object has several resources -- see URI list"],
            "301": ["Moved Permanently", "Object moved permanently -- see URI list"],
            "302": ["Found", "Object moved temporarily -- see URI list"],
            "303": ["See Other", "Object moved -- see Method and URL list"],
            "304": ["Not Modified", "Document has not changed since given time"],
            "305": [
                "Use Proxy",
                "You must use proxy specified in Location to access this resource.",
            ],
            "307": ["Temporary Redirect", "Object moved temporarily -- see URI list"],
            "400": ["Bad Request", "Bad request syntax or unsupported method"],
            "401": ["Unauthorized", "No permission -- see authorization schemes"],
            "402": ["Payment Required", "No payment -- see charging schemes"],
            "403": ["Forbidden", "Request forbidden -- authorization will not help"],
            "404": ["Not Found", "Nothing matches the given URI"],
            "405": [
                "Method Not Allowed",
                "Specified method is invalid for this server.",
            ],
            "406": ["Not Acceptable", "URI not available in preferred format."],
            "407": [
                "Proxy Authentication Required",
                "You must authenticate with this proxy before proceeding.",
            ],
            "408": ["Request Timeout", "Request timed out; try again later."],
            "409": ["Conflict", "Request conflict."],
            "410": ["Gone", "URI no longer exists and has been permanently removed."],
            "411": ["Length Required", "Client must specify Content-Length."],
            "412": ["Precondition Failed", "Precondition in headers is false."],
            "413": ["Request Entity Too Large", "Entity is too large."],
            "414": ["Request-URI Too Long", "URI is too long."],
            "415": ["Unsupported Media Type", "Entity body in unsupported format."],
            "416": ["Requested Range Not Satisfiable", "Cannot satisfy request range."],
            "417": ["Expectation Failed", "Expect condition could not be satisfied."],
            "500": ["Internal Server Error", "Server got itself in trouble"],
            "501": ["Not Implemented", "Server does not support this operation"],
            "502": ["Bad Gateway", "Invalid responses from another server/proxy."],
            "503": [
                "Service Unavailable",
                "The server cannot process the request due to a high load",
            ],
            "504": [
                "Gateway Timeout",
                "The gateway server did not receive a timely response",
            ],
            "505": ["HTTP Version Not Supported", "Cannot fulfill request."],
        },
    }

    # Return as JSON
    def get_settings_json(self):
        return json.dumps(self.settings_file, indent=4)


class Reliquary:

    # Initial Variable Settings
    #
    cogitation_verbosity = 0
    cogitation_certvalidation = True
    cogitation_username = ""
    cogitation_password = ""
    cogitation_authkey = ""
    cogitation_authcert = ""
    cogitation_endpoint = ""
    cogitation_bibliotheca = {}
    cogitation_errors = {}

    # We're pretty much picking up our configuration data
    def __init__(self, input_settings):

        # Load Settings from JSON
        try:
            with open(input_settings, "r") as json_filehandle:
                json_settings = json.load(json_filehandle)
        except Exception as e:
            print("E0000: Error Loading Settings File: " + str(e))
            exit()

        try:
            # Let's start with basic global settings
            self.cogitation_verbosity = json_settings["settings"]["verbosity"]
            self.cogitation_endpoint = json_settings["settings"]["endpoint"]
            # TLS Tuning
            self.cogitation_certvalidation = json_settings["settings"]["tls"][
                "validation"
            ]
            # Authentication Settings
            self.cogitation_username = json_settings["settings"]["authentication"][
                "username"
            ]
            self.cogitation_password = json_settings["settings"]["authentication"][
                "password"
            ]
            self.cogitation_authcert = json_settings["settings"]["authentication"][
                "certificate"
            ]
            self.cogitation_authkey = json_settings["settings"]["authentication"]["key"]
            # Load Known API Actions
            self.cogitation_bibliotheca = json_settings["plays"]
            # Load HTTP Errors
            self.cogitation_errors = json_settings["errors"]
        except Exception as e:
            print("E0002: Error Loading Settings! Settings Dictionary:")
            print(json.dumps(json_settings, indent=4))
            exit(str(e))

        # 99% solution here is to validate that a URL provided is valid. This doesn't test it or anything
        validate = URLValidator()
        try:
            validate(self.cogitation_endpoint)
        except Exception as e:
            print('E0001: Invalid URL Formatting. Example: "https://www.abc.com/"')
            exit(str(e))

    # Functions

    # Do API DELETE, using basic credentials
    def do_api_delete(self, do_api_uri, do_api_object):
        # Perform API Processing - conditional basic authentication
        try:
            do_api_get_headers = {
                "content-type": "application/json",
                "X-Allow-Overwrite": "true",
            }
            do_api_get_url = (
                self.cogitation_endpoint
                + self.cogitation_bibliotheca[do_api_uri][0]
                + do_api_object
                + self.cogitation_bibliotheca[do_api_uri][1]
            )
            do_api_get_r = requests.delete(
                do_api_get_url,
                headers=do_api_get_headers,
                verify=self.cogitation_certvalidation,
                auth=(self.cogitation_username, self.cogitation_password),
            )
            # We'll be discarding the actual `Response` object after this, but we do want to get HTTP status for erro handling
            response_code = do_api_get_r.status_code
            print(response_code)
            do_api_get_r.raise_for_status()  # trigger an exception before trying to convert or read data. This should allow us to get good error info
            return do_api_get_r.text  # if HTTP status is good, save response
        except requests.Timeout:
            print("E1000: API Connection timeout!")
        except requests.ConnectionError as connection_error:
            print(connection_error)
        except requests.HTTPError:
            if self.get_http_error_code(response_code):
                print(
                    "EA"
                    + str(response_code)
                    + ": HTTP Status Error "
                    + str(response_code)
                    + " "
                    + self.get_http_error_code(response_code)
                )
                return do_api_get_r.text
            else:
                print("EA999: Unhandled HTTP Error " + str(response_code) + "!")
                exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
        except requests.RequestException as requests_exception:
            print(requests_exception)
        except Exception as e:
            print("E1002: Unhandled Requests exception! " + str(e))
            exit()

    # Do API GET, using basic credentials
    def do_api_get(self, do_api_uri, do_api_object):
        # Perform API Processing - conditional basic authentication
        try:
            do_api_get_headers = {
                "content-type": "application/json",
                "X-Allow-Overwrite": "true",
            }
            do_api_get_url = (
                self.cogitation_endpoint
                + self.cogitation_bibliotheca[do_api_uri][0]
                + do_api_object
            )
            do_api_get_r = requests.get(
                do_api_get_url,
                headers=do_api_get_headers,
                verify=self.cogitation_certvalidation,
                auth=(self.cogitation_username, self.cogitation_password),
            )
            # We'll be discarding the actual `Response` object after this, but we do want to get HTTP status for erro handling
            response_code = do_api_get_r.status_code
            print(response_code)
            do_api_get_r.raise_for_status()  # trigger an exception before trying to convert or read data. This should allow us to get good error info
            return do_api_get_r.text  # if HTTP status is good, save response
        except requests.Timeout:
            print("E1000: API Connection timeout!")
        except requests.ConnectionError as connection_error:
            print(connection_error)
        except requests.HTTPError:
            if self.get_http_error_code(response_code):
                print(
                    "EA"
                    + str(response_code)
                    + ": HTTP Status Error "
                    + str(response_code)
                    + " "
                    + self.get_http_error_code(response_code)
                )
                return do_api_get_r.text
            else:
                print("EA999: Unhandled HTTP Error " + str(response_code) + "!")
                exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
        except requests.RequestException as requests_exception:
            print(requests_exception)
        except Exception as e:
            print("E1002: Unhandled Requests exception! " + str(e))
            exit()

    @dispatch(str, str)
    def namshub(self, namshub_string, namshub_object):
        namshub_verb = self.get_play_verb(namshub_string)
        namshub_resource = self.get_play_uri(namshub_string)
        if namshub_verb == "DELETE":
            print(self.do_api_delete(self.get_play_uri(namshub_resource), namshub_object))
        elif namshub_verb == "GET":
            print(self.do_api_get(self.get_play_uri(namshub_resource), namshub_object))

    @dispatch(str, str, str)
    def namshub(self, namshub_string, namshub_object, namshub_body):
        namshub_verb = self.get_play_verb(namshub_string)
        namshub_resource = self.get_play_uri(namshub_string)
        if self.get_play_requiresbody(namshub_resource) is True:
            if namshub_verb == "POST":
                print(self.do_api_post(self.get_play_uri(namshub_resource), namshub_object))
            elif namshub_verb == "PATCH":
                print(self.do_api_post(self.get_play_uri(namshub_resource), namshub_object))
        else:
            exit("Function doesn't require a body, but the method used does!")

    def get_http_error_code(self, get_http_error_code_code):
        return json.dumps(self.cogitation_errors[get_http_error_code_code], indent=4)

    def get_play_uri(self, get_play_name):
        try:
            return self.cogitation_bibliotheca[get_play_name]['uri']
        except Exception as e:
            exit('Exception fetching play URI: ' + str(get_play_name) + str(e))

    def get_play_verb(self, get_play_name):
        try:
            return self.cogitation_bibliotheca[get_play_name]['method']
        except Exception as e:
            exit('Exception fetching play method: ' + str(get_play_name) + str(e))

    def get_play_requiresbody(self, get_play_name):
        try:
            return self.cogitation_bibliotheca[get_play_name]['requiresbody']
        except Exception as e:
            exit('Exception fetching play requirement: ' + str(get_play_name) + str(e))
