#!/usr/bin/python3
# Python NSX Advanced Load Balancer Profile Applicator
# Nicholas Schmidt
# 29-Dec-2021

# System Calls
import os
import sys

# JSON
import json

# Impot DeepDiff. We need this to compare dictionaries
import deepdiff

# REST Client
from restify.RuminatingCogitation import Reliquary


# Find Element in list (based on name)
def find_element_in_list(find_list, find_element):
    for i in find_list:
        if type(i) is dict and i["name"] == find_element:
            return i
    return None


# Recursively converge application profiles
def converge_app_profile(app_profile_dict):
    # First, grab a copy of the existing application profile
    before_app_profile = json.loads(
        cogitation_interface.namshub(
            "get_app_profile", namshub_variables={"id": app_profile_dict["uuid"]}
        )
    )

    # Fastest and cheapest compare operation first
    if not app_profile_dict["profile"] == before_app_profile:
        # Build a deep difference of the two dictionaries, removing attributes that are not part of the profile, but the API generates
        diff_app_profile = deepdiff.DeepDiff(
            before_app_profile,
            app_profile_dict["profile"],
            exclude_paths=[
                "root['uuid']",
                "root['url']",
                "root['uuid']",
                "root['_last_modified']",
                "root['tenant_ref']",
            ],
        )

        # If there are differences, try to fix them at least 3 times
        if len(diff_app_profile) > 0 and app_profile_dict["retries"] < 3:
            print("Difference between dictionaries found: " + str(diff_app_profile))
            print(
                "Converging "
                + app_profile_dict["profile"]["name"]
                + " attempt # "
                + str(app_profile_dict["retries"] + 1)
            )
            # Increment retry counter
            app_profile_dict["retries"] += 1
            # Then perform Update verb on profile
            cogitation_interface.namshub(
                "update_app_profile",
                namshub_payload=app_profile_dict["profile"],
                namshub_variables={"id": app_profile_dict["uuid"]},
            )
            # Perform recursion
            converge_app_profile(app_profile_dict)
        else:
            return before_app_profile


# Recursively converge TLS profiles
def converge_tls_profile(tls_profile_dict):
    # First, grab a copy of the existing tls profile
    before_tls_profile = json.loads(
        cogitation_interface.namshub(
            "get_tls_profile", namshub_variables={"id": tls_profile_dict["uuid"]}
        )
    )

    # Fastest and cheapest compare operation first
    if not tls_profile_dict["profile"] == before_tls_profile:
        # Build a deep difference of the two dictionaries, removing attributes that are not part of the profile, but the API generates

        diff_tls_profile = deepdiff.DeepDiff(
            before_tls_profile,
            tls_profile_dict["profile"],
            exclude_paths=[
                "root['uuid']",
                "root['url']",
                "root['uuid']",
                "root['_last_modified']",
                "root['tenant_ref']",
                "root['display_name']",
                "root['ec_named_curve']",
                "root['signature_algorithm']",
                "root['ssl_rating']",
                "root['send_close_notify']",
                "root['dhparam']",
                "root['type']",
                "root['resource_type']",
            ],
        )

        # If there are differences, try to fix them at least 3 times
        if len(diff_tls_profile) > 0 and tls_profile_dict["retries"] < 3:
            print("Difference between dictionaries found: " + str(diff_tls_profile))
            print(
                "Converging "
                + tls_profile_dict["profile"]["name"]
                + " attempt # "
                + str(tls_profile_dict["retries"] + 1)
            )
            # Increment retry counter
            tls_profile_dict["retries"] += 1
            # Then Perform Update verb on profile
            cogitation_interface.namshub(
                "update_tls_profile",
                namshub_payload=tls_profile_dict["profile"],
                namshub_variables={"id": tls_profile_dict["uuid"]},
            )
            # Perform recursion
            converge_tls_profile(tls_profile_dict)
        else:
            return before_tls_profile


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
        "retries": 0,
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
        "retries": 0,
    }

# Collect Remote Configurations
apps_dict = json.loads(cogitation_interface.namshub("get_app_profiles"))["results"]
tls_dict = json.loads(cogitation_interface.namshub("get_tls_profiles"))["results"]

# Attempt to Apply as new profiles first. Save the results under 'result' for processing later
# Apps
for i in work_dict["application_profiles"]:
    # Try to find an existing profile
    existing_profile = find_element_in_list(apps_dict, i)

    # If one doesn't exist, try and create it
    if existing_profile is None:
        work_dict["application_profiles"][i]["result"] = cogitation_interface.namshub(
            "create_app_profile",
            namshub_payload=work_dict["application_profiles"][i]["profile"],
        )
    # If one does exist, converge it
    else:
        work_dict["application_profiles"][i]["uuid"] = existing_profile["uuid"]
        converge_app_profile(work_dict["application_profiles"][i])
        work_dict["application_profiles"][i]["result"] = converge_app_profile(
            work_dict["application_profiles"][i]
        )

# TLS
for i in work_dict["tls_profiles"]:
    # Try to find an existing profile
    existing_profile = find_element_in_list(tls_dict, i)

    # If one doesn't exist, try and create it
    if existing_profile is None:
        work_dict["tls_profiles"][i]["result"] = cogitation_interface.namshub(
            "create_tls_profile",
            namshub_payload=work_dict["tls_profiles"][i]["profile"],
        )

    # If one does exist, converge it
    else:
        work_dict["tls_profiles"][i]["uuid"] = existing_profile["uuid"]
        converge_tls_profile(work_dict["tls_profiles"][i])
        work_dict["tls_profiles"][i]["result"] = converge_tls_profile(
            work_dict["tls_profiles"][i]
        )

print("Profile convergence report:")
print(cogitation_interface.json_prettyprint(work_dict))
