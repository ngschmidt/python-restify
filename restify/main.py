#!/usr/bin/python3
# Python REST CLI Tool
# Nicholas Schmidt
# 13 Feb 2021

# Command line parsing imports
import argparse

# JSON Parsing tool
import json

# Import Restify Library
from RuminatingCogitation import Settings
from RuminatingCogitation import Reliquary

# Import OS - let's use this for passwords and usernames
# APIUSER = Username
# APIPASS = Password
import os

api_user = os.getenv("APIUSER")
api_pass = os.getenv("APIPASS")

play_help = (
    "Play to execute, Example: delete_do-things_<uuid>. \r\n"
    + "Other options: `list_plays`, or `create_settings` to build a settings file."
)
# Arguments Parsing
parser = argparse.ArgumentParser(description="Fetch via API")
parser.add_argument("play", help=play_help)
parser.add_argument("-f", help="REST Settings File (JSON)")
parser.add_argument(
    "--vars", help="Variables to pass (JSON). For more detail, use list_plays"
)
parser.add_argument(
    "--getplay",
    help="Instead of running the command, print it out",
    action="store_true",
)
parser.add_argument(
    "--dryrun",
    help="Instead of running the command, print out the payload",
    action="store_true",
)
args = parser.parse_args()

# Dump a settings file on demand
if args.play == "create_settings":
    template = Settings()
    print(template.get_settings_json())
    exit()

# Set the interface - apply from variables no matter what
cogitation_interface = Reliquary(args.f, input_user=api_user, input_pass=api_pass)

# Once the library is fired up and settings are loaded, offer the option to list any plays in the settings file
if args.play == "list_plays":
    print(json.dumps(cogitation_interface.cogitation_bibliotheca, indent=4))
elif args.getplay or args.dryrun:
    if args.getplay:
        print(
            json.dumps(cogitation_interface.cogitation_bibliotheca[args.play], indent=4)
        )
    if args.dryrun:
        if not args.vars:
            cogitation_interface.namshub(args.play, namshub_dryrun=True)
        else:
            cogitation_interface.namshub(args.play, namshub_variables=json.loads(args.vars), namshub_dryrun=True)
else:
    # Provide an "overloading interface"
    if not args.vars:
        cogitation_interface.namshub(args.play)
    else:
        cogitation_interface.namshub(args.play, namshub_variables=args.vars)
