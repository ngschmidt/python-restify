#!/usr/bin/python3
# Deploy VM From Content Library
# Missing in `vmware_rest` Ansible Modules - deploy a VM from a template
# Nicholas Schmidt
# 02-Jan-2022

# System Calls
import os
import sys

# NSX-T Client
from restify.RuminatingCogitation import Reliquary

# Markup libraries
import json

# Let the user know if the envs aren't set up properly
for env_mandatory in ["API_ENDPOINT", "API_USER", "API_PASS"]:
    if env_mandatory not in os.environ:
        sys.exit(
            "Missing environment variable " + env_mandatory + " not found! Exiting..."
        )

# Initialize vSphere Connection

# Use `Reliquary` to create API object
cogitation_interface = Reliquary(
    "settings.json",
    input_user=os.getenv("API_USER"),
    input_pass=os.getenv("API_PASS"),
    input_endpoint=os.getenv("API_ENDPOINT"),
)

# Get the API key and add it to the API interface object
cogitation_interface.add_http_header(
    "vmware-api-session-id", cogitation_interface.namshub("post_api_key").strip("\"")
)

# Then, let's fetch the vSphere details

print(json.dumps(json.loads(cogitation_interface.namshub("get_clibs")), indent=4))

# Let's check for a configuration. If none exists, dump the vSphere details to help the process along
