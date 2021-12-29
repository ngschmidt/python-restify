#!/usr/bin/python3
# Python REST CLI Tool
# Nicholas Schmidt
# 13 Feb 2021

# Command line parsing imports
import argparse

# Import Restify Library
from restify.RuminatingCogitation import Reliquary

# Import OS - let's use this for passwords and usernames
# APIUSER = Username
# APIPASS = Password
import os

api_user = os.getenv("APIUSER")
api_pass = os.getenv("APIPASS")

# Arguments Parsing
parser = argparse.ArgumentParser(description="Fetch via API")
parser.add_argument("-f", help="REST Settings File (JSON)")
parser.add_argument(
    "--vars", help="Variables to pass (JSON). For more detail, use list_plays"
)
args = parser.parse_args()

# Set the interface - apply from variables no matter what
cogitation_interface = Reliquary(args.f, input_user=api_user, input_pass=api_pass)

# Iterate thru easy test cases
for i in cogitation_interface.cogitation_bibliotheca:
    if not cogitation_interface.get_play_requiresbody(
        i
    ) and not cogitation_interface.get_play_requiresvariables(i):
        print(cogitation_interface.namshub(i, namshub_variables=args.vars))
# More coverage testing should go here
