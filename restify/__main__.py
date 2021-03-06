#!/usr/bin/python3
# Python REST CLI Tool
# Nicholas Schmidt
# 13 Feb 2021

# Command line parsing imports
import argparse

# JSON Parsing tool
import json

# Import Restify Library
from restify.RuminatingCogitation import Settings
from restify.RuminatingCogitation import Reliquary

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
    template = Settings()
    print(template.get_settings_json())
    exit()

cogitation_interface = Reliquary(args.f)

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
