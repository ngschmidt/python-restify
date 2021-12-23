#!/usr/bin/python3
# Python NSX-T Advanced Load Balancer Cleanup
# Nicholas Schmidt
# 22-Dec-2021

# System Calls
import os
import sys

# NSX-T Client
from restify.RuminatingCogitation import Reliquary

# Markup libraries
import json

# Let the user know if the envs aren't set up properly
for env_mandatory in ["APIUSER", "APIPASS"]:
    if env_mandatory not in os.environ:
        sys.exit(
            "Missing environment variable " + env_mandatory + " not found! Exiting..."
        )

# Initialize NSX-T Connections
# The issue here is that NSX-T ALB Deployments may become stale or orphaned, and can only be cleaned up from the API.

# Use `Reliquary`` to form API connection
cogitation_interface = Reliquary(
    "settings.json", input_user=os.getenv("APIUSER"), input_pass=os.getenv("APIPASS")
)

# Fetch NSX ALB Deployments
alb_result = json.loads(cogitation_interface.namshub("get_nsxalb_controller"))[
    "results"
]

# Check to see if any NSX ALB Controllers are deployed
if (len(alb_result)) == 0:
    sys.exit("No NSX ALB Controllers detected!")

for i in alb_result:
    # Print, then ask if we should delete each one. Discard any input that isn't what we want.
    controller_uuid = i["vm_id"]
    controller_hostname = i["deployment_config"]["hostname"]
    controller_yesno = input(
        "Would you like to delete AVI Deployed controller "
        + controller_hostname
        + "? (y/n)"
    ).lower()
    if controller_yesno in ["yes", "y"]:
        # API Delete ALB Controller
        print("Executing API DELETE on " + controller_uuid)
        cogitation_interface.namshub(
            "delete_nsxalb_controller",
            namshub_variables='{"id": "' + controller_uuid + '"}',
        )
        # Let's check to see what controllers are left
        for i in json.loads(cogitation_interface.namshub("get_nsxalb_controller"))[
            "results"
        ]:
            print("Found remaining controller " + i["vm_id"] + "!")
            if i["vm_id"] == controller_hostname:
                sys.exit("We found the old controller we tried to delete!")
    else:
        print("Passing on " + controller_uuid + "!")
