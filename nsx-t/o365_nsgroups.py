#!/usr/bin/python3
# Python NSX-T Microsoft 365 Address Group Collector
# This implementation has a maximum of 4,000 entries
# Nicholas Schmidt
# 23 Jan 2022

# System Calls
import os
import sys

# HTTP Client
import requests
import uuid

# NSX-T Client
from restify.RuminatingCogitation import Reliquary

# IP address validation
import ipaddress

# JSON
import json

# Regex
import re


def validate_ip_network(input_to_validate):
    try:
        ipaddress.ip_network(input_to_validate)
        return True
    except ValueError as e:
        print("Invalid entry found! " + str(e))
        return False
    except Exception as e:
        sys.exit(
            "Unexpected error when validating IP " + input_to_validate + ": " + str(e)
        )


def validate_ip_list(ip_list_to_validate):
    validated_list = []
    for i in ip_list_to_validate:
        if validate_ip_network(i):
            validated_list.append(i)
    return validated_list


def assemble_nsgroup(input_obj_list):
    patch_dict = {
        "expression": [
            {"ip_addresses": input_obj_list, "resource_type": "IPAddressExpression"}
        ],
        "group_type": ["IPAddress"],
    }
    print("Generated the following `dict`: ")
    print(json.dumps(patch_dict, indent=2))
    return patch_dict


# Let the user know if the envs aren't set up properly
for env_mandatory in ["APIUSER", "APIPASS"]:
    if env_mandatory not in os.environ:
        sys.exit(
            "Missing environment variable " + env_mandatory + " not found! Exiting..."
        )

"""
Schema for work `list` members (`dict`)
    "name": (composite of {{ serviceArea }} + {{ serviceAreaDisplayName }} + {{ id }}) lowered
    "ips": `list`
"""
work_list = []

# Fetch m365 data. This needs a UUID to mark the client
office365_endpoint_data = json.loads(
    requests.get(
        "https://endpoints.office.com/endpoints/worldwide?clientrequestid="
        + str(uuid.uuid4())
    ).text
)

# Iterate through published endpoints
for i in office365_endpoint_data:
    # Only act on entries with IP lists
    if "ips" in i.keys():
        output_dict = {}
        # Create a composite name We're removing redundant character words (like Microsoft!) to shorten named strings
        # Alphanumeric strips will make sure that we have no invalid characters
        i_name = re.sub(
            r"\W+",
            "",
            i["serviceArea"] + "_" + i["serviceAreaDisplayName"] + "_" + str(i["id"]),
        ).replace("Microsoft365", "")
        # Name the object
        output_dict["name"] = "m365." + i_name
        # Add the IP list, after validating it of course
        output_dict["ips"] = validate_ip_list(i["ips"])
        # Add the formatted object to the work list
        work_list.append(output_dict)

# We now have a formatted work list to send to NSX-T

# Initialize NSX-T Connections

# Use `Reliquary` to form API connection
cogitation_interface = Reliquary(
    "settings.json", input_user=os.getenv("APIUSER"), input_pass=os.getenv("APIPASS")
)

# Iterate through each object and `PATCH` it to NSX-T

for i in work_list:
    cogitation_interface.namshub(
        "patch_policy_inventory_group",
        namshub_variables={"domain": "default", "id": i["name"]},
        namshub_payload=assemble_nsgroup(i["ips"]),
    )
