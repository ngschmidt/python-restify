#!/usr/bin/python3
# Python REST CLI Tool
# Nicholas Schmidt
# 13 Feb 2021

# Command line parsing imports
import argparse

# Import Python Classes
from RuminatingCogitationReliquary import RuminatingCogitationReliquary

# JSON Parsing tool
import json

play_help = 'Play to execute, Example: delete_do-things_<uuid>. \r\n' + \
    'Other options: `list_plays`, or `create_settings` to build a settings file.'  
# Arguments Parsing
parser = argparse.ArgumentParser(description='Fetch via API')
parser.add_argument('-f', help='REST Settings File')
parser.add_argument('play', help=play_help)
args = parser.parse_args()

if args.play == 'create_settings':
    settings_file = {
        "settings": {
            "authentication": {
                "username": "admin",
                "password": "password",
                "method": "basic",
                "certificate": "",
                "key": ""
            },
            "tls": {
                "validation": False
            },
            "verbosity": 1,
            "endpoint": "https://nsx.lab.engyak.net"
        },
        "plays": {},
        "errors": {
            "200": [
                "OK",
                "Request fulfilled, document follows"
            ],
            "201": [
                "Created",
                "Document created, URL follows"
            ],
            "202": [
                "Accepted",
                "Request accepted, processing continues off-line"
            ],
            "203": [
                "Non-Authoritative Information",
                "Request fulfilled from cache"
            ],
            "204": [
                "No Content",
                "Request fulfilled, nothing follows"
            ],
            "205": [
                "Reset Content",
                "Clear input form for further input."
            ],
            "206": [
                "Partial Content",
                "Partial content follows."
            ],
            "300": [
                "Multiple Choices",
                "Object has several resources -- see URI list"
            ],
            "301": [
                "Moved Permanently",
                "Object moved permanently -- see URI list"
            ],
            "302": [
                "Found",
                "Object moved temporarily -- see URI list"
            ],
            "303": [
                "See Other",
                "Object moved -- see Method and URL list"
            ],
            "304": [
                "Not Modified",
                "Document has not changed since given time"
            ],
            "305": [
                "Use Proxy",
                "You must use proxy specified in Location to access this resource."
            ],
            "307": [
                "Temporary Redirect",
                "Object moved temporarily -- see URI list"
            ],
            "400": [
                "Bad Request",
                "Bad request syntax or unsupported method"
            ],
            "401": [
                "Unauthorized",
                "No permission -- see authorization schemes"
            ],
            "402": [
                "Payment Required",
                "No payment -- see charging schemes"
            ],
            "403": [
                "Forbidden",
                "Request forbidden -- authorization will not help"
            ],
            "404": [
                "Not Found",
                "Nothing matches the given URI"
            ],
            "405": [
                "Method Not Allowed",
                "Specified method is invalid for this server."
            ],
            "406": [
                "Not Acceptable",
                "URI not available in preferred format."
            ],
            "407": [
                "Proxy Authentication Required",
                "You must authenticate with this proxy before proceeding."
            ],
            "408": [
                "Request Timeout",
                "Request timed out; try again later."
            ],
            "409": [
                "Conflict",
                "Request conflict."
            ],
            "410": [
                "Gone",
                "URI no longer exists and has been permanently removed."
            ],
            "411": [
                "Length Required",
                "Client must specify Content-Length."
            ],
            "412": [
                "Precondition Failed",
                "Precondition in headers is false."
            ],
            "413": [
                "Request Entity Too Large",
                "Entity is too large."
            ],
            "414": [
                "Request-URI Too Long",
                "URI is too long."
            ],
            "415": [
                "Unsupported Media Type",
                "Entity body in unsupported format."
            ],
            "416": [
                "Requested Range Not Satisfiable",
                "Cannot satisfy request range."
            ],
            "417": [
                "Expectation Failed",
                "Expect condition could not be satisfied."
            ],
            "500": [
                "Internal Server Error",
                "Server got itself in trouble"
            ],
            "501": [
                "Not Implemented",
                "Server does not support this operation"
            ],
            "502": [
                "Bad Gateway",
                "Invalid responses from another server/proxy."
            ],
            "503": [
                "Service Unavailable",
                "The server cannot process the request due to a high load"
            ],
            "504": [
                "Gateway Timeout",
                "The gateway server did not receive a timely response"
            ],
            "505": [
                "HTTP Version Not Supported",
                "Cannot fulfill request."
            ]
        }
    }
    print(json.dumps(settings_file, indent=4))
    exit()

cogitation_interface = RuminatingCogitationReliquary(args.f)

if args.play == 'list_plays':
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