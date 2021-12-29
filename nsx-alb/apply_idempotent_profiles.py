#!/usr/bin/python3
# Python NSX Advanced Load Balancer Profile Applicator
# Nicholas Schmidt
# 29-Dec-2021

# System Calls
import os
import sys

# REST Client
from restify.RuminatingCogitation import Reliquary

# JSON
import json

# Let the user know if the envs aren't set up properly
for env_mandatory in ["APIUSER", "APIPASS"]:
    if env_mandatory not in os.environ:
        sys.exit(
            "Missing environment variable " + env_mandatory + " not found! Exiting..."
        )

# Initialize NSX ALB Connections
# Find all applicable profiles, then try to apply them idempotently

# Use `Reliquary`` to form API connection
cogitation_interface = Reliquary(
    "settings.json", input_user=os.getenv("APIUSER"), input_pass=os.getenv("APIPASS")
)

# Build a dictionary to help organize what we're about to do
# Schema:
# application_profile_name: { "directory": "", "uuid": "", "profile": "", "result": "" }

work_dict = {"application_profiles": {}, "tls_profiles": {}}

# Find all profiles that we want to apply
# List Application Profiles
# HTTP
for i in os.listdir("profiles/http"):
    profile_temp = cogitation_interface.get_json_file_or_string(
        os.curdir + "/profiles/http/" + i
    )
    work_dict["application_profiles"][profile_temp["name"]] = {
        "directory": os.curdir + "/profiles/http/" + i,
        "uuid": "",
        "profile": profile_temp,
        "result": "",
    }

# TLS
for i in os.listdir("profiles/tls"):
    profile_temp = cogitation_interface.get_json_file_or_string(
        os.curdir + "/profiles/tls/" + i
    )
    work_dict["tls_profiles"][profile_temp["name"]] = {
        "directory": os.curdir + "/profiles/tls/" + i,
        "uuid": "",
        "profile": profile_temp,
        "result": "",
    }

# Attempt to Apply as new profiles first
# Then if that fails, try to find them via the list
# Test to see if there's a difference between what we have in Git and the deployment
# Then try and PUT them based on that UUID if it's different
print(type(work_dict))
print(json.dumps(work_dict, indent=2))
