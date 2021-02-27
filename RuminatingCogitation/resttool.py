#!/usr/bin/python3
# Python REST CLI Tool
# Nicholas Schmidt
# 13 Feb 2021

# Command line parsing imports
import argparse

# JSON Parsing tool
import json

# API Processing imports
import requests

# Command line validating imports
from django.core.validators import URLValidator


# Begin Supporting Classes
class RuminatingCogitationSettings:
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


class RuminatingCogitationReliquary:

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
            json_filehandle = open(input_settings, "r")
            json_settings = json.load(json_filehandle)
        except:
            print("E0000: Error Loading Settings File!")
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
        except:
            print("E0002: Error Loading Settings! Settings Dictionary:")
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
                "content-type": "application/json",
                "X-Allow-Overwrite": "true",
            }
            do_api_get_url = (
                self.cogitation_endpoint
                + self.cogitation_bibliotheca[do_api_thing][0]
                + do_api_object
                + self.cogitation_bibliotheca[do_api_thing][1]
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
    def do_api_get(self, do_api_thing, do_api_object):
        # Perform API Processing - conditional basic authentication
        try:
            do_api_get_headers = {
                "content-type": "application/json",
                "X-Allow-Overwrite": "true",
            }
            do_api_get_url = (
                self.cogitation_endpoint
                + self.cogitation_bibliotheca[do_api_thing][0]
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

    def get_http_error_code(self, get_http_error_code_code):
        return json.dumps(self.cogitation_errors[get_http_error_code_code], indent=4)


play_help = (
    "Play to execute, Example: delete_do-things_<uuid>. \r\n"
    + "Other options: `list_plays`, or `create_settings` to build a settings file."
)
# Arguments Parsing
parser = argparse.ArgumentParser(description="Fetch via API")
parser.add_argument("-f", help="REST Settings File")
parser.add_argument("play", help=play_help)
args = parser.parse_args()

if args.play == "create_settings":
    template = RuminatingCogitationSettings()
    print(template.get_settings_json())
    exit()

cogitation_interface = RuminatingCogitationReliquary(args.f)

if args.play == "list_plays":
    print(json.dumps(cogitation_interface.cogitation_bibliotheca, indent=4))
    exit()

# The play construct demonstrated above is a nam-shub, or `<verb>_<endpoint>_<object>` format. We'll use this to decide what to do, split by a dash
namshub = args.play.split("_")
if len(namshub) == 3:
    namshub_verb = namshub[0]
    namshub_endpoint = namshub[1]
    namshub_object = namshub[2]
    if namshub_verb == "delete":
        print(cogitation_interface.do_api_delete(namshub_endpoint, namshub_object))
    elif namshub_verb == "get":
        print(cogitation_interface.do_api_get(namshub_endpoint, namshub_object))
    else:
        print("E2001: Invalid nam-shub verb!")
else:
    print("Malformatted play: " + json.dumps(namshub, indent=4))
