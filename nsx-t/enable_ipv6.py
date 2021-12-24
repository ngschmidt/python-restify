#!/usr/bin/python3
# Python NSX-T IPv6 Enabler
# For some reason, IPv6 is disabled by default, let's fix that
# Nicholas Schmidt
# 24-Dec-2021

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

# Use `Reliquary`` to form API connection
cogitation_interface = Reliquary(
    "settings.json", input_user=os.getenv("APIUSER"), input_pass=os.getenv("APIPASS")
)

# Fetch NSX Global Settings
settings_result = json.loads(cogitation_interface.namshub("get_globalconfig"))[
    "l3_forwarding_mode"
]

# Check to see if IPv6 is already enabled
if settings_result not in ["IPV4_ONLY", "IPV4_AND_IPV6"]:
    # Die if it isn't returning normal output
    sys.exit("Anomalous output found: " + settings_result)
# If IPv4 is the only Layer3 enabled, do the work
elif settings_result in ["IPV4_ONLY"]:
    cogitation_interface.namshub("set_globalconfig_ipv6_on")
    # Check to see if anything changed
    settings_after = json.loads(cogitation_interface.namshub("get_globalconfig"))[
        "l3_forwarding_mode"
    ]
    if settings_after not in ["IPV4_AND_IPV6"]:
        sys.exit(
            "Anomalous output found after attempting to change IPv6: " + settings_after
        )
# Don't do anything if the setting is already set
else:
    print("IPv6 is already enabled: " + settings_result + "!")
