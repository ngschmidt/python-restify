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
import os
import sys

# Try to load from the OS Environment
api_user = os.getenv("APIUSER")
api_pass = os.getenv("APIPASS")
api_endpoint = os.getenv("APIENDPOINT")

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

# Set the interface - apply from variables
if api_endpoint and api_endpoint is str:
    cogitation_interface = Reliquary(
        args.f, input_user=api_user, input_pass=api_pass, input_endpoint=api_endpoint
    )
else:
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
            cogitation_interface.namshub(
                args.play, namshub_variables=args.vars, namshub_dryrun=True
            )
else:
    # Let the user know if the envs aren't set up properly
    for env_mandatory in ["APIUSER", "APIPASS"]:
        if env_mandatory not in os.environ:
            sys.exit(
                "Missing environment variable " + env_mandatory + " not found! Exiting..."
            )

    # Provide an "overloading interface"
    if not args.vars:
        print(cogitation_interface.namshub(args.play))
    elif args.p:
        print(cogitation_interface.namshub(args.play, namshub_variables=args.vars, namshub_payload=args.p))
    else:
        print(cogitation_interface.namshub(args.play, namshub_variables=args.vars))
