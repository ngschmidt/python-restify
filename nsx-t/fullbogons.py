#!/usr/bin/python3
# Python NSX-T Fullbogon lists
# Nicholas Schmidt
# 24-Dec-2021

# System Calls
import os
import sys

# HTTP Client
import requests

# Dictionary and list comparisons
from deepdiff import DeepDiff

# NSX-T Client
from restify.RuminatingCogitation import Reliquary

# IP address validation
import ipaddress

# JSON
import json


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


def assemble_nsgroup(input_obj_name, input_obj_list):
    patch_dict = {
        "expression": [
            {
                "ip_addresses": [
                    "1.1.1.1/32"
                ],
                "resource_type": "IPAddressExpression"
            }
        ],
        "group_type": [
            "IPAddress"
        ]
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

# Initialize NSX-T Connections

# Use `Reliquary`` to form API connection
cogitation_interface = Reliquary(
    "settings.json", input_user=os.getenv("APIUSER"), input_pass=os.getenv("APIPASS")
)

# Fetch the Cymru Fullbogon list
# First, let's pick up the current list via HTTP:
fullbogon_text = requests.get(
    "https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt"
).text

# Now, we have to do something with it, like converting it to a `dict`
fullbogon_list = fullbogon_text.splitlines()
print("Found a list of length " + str(len(fullbogon_list)) + ". Validating...")

# Then, let's validate the entries
fullbogon_list_validated = []
for i in fullbogon_list:
    if validate_ip_network(i):
        fullbogon_list_validated.append(i)
print(
    "Found a list of length "
    + str(len(fullbogon_list_validated))
    + " with valid IP Destinations!"
)

# Create NSX-T NSGroup if it doesn't exist
nsgroup_name = "cymru_ipv4_fullbogons"
cogitation_interface.namshub(
    "patch_policy_inventory_group",
    namshub_variables={"domain": "default", "id": nsgroup_name},
    namshub_payload=assemble_nsgroup(nsgroup_name, fullbogon_list_validated),
)

# Validate the PATCH
implemented_object = cogitation_interface.namshub(
    "get_policy_inventory_group",
    namshub_variables={"domain": "default", "id": nsgroup_name},
)
implemented_ip_list = implemented_object["expression"]["ip_addresses"]
print("abc")
print(implemented_ip_list)
print(DeepDiff(fullbogon_list_validated, implemented_ip_list, ignore_order=True))
