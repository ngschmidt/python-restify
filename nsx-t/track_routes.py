#!/usr/bin/python3
# Python NSX-T Route Tracker
# Nicholas Schmidt
# 24-Nov-2021

# JSON Parsing tool
import json

# Import Restify Library
from restify.RuminatingCogitation import Reliquary

# Import OS - let's use this for passwords and usernames
# APIUSER = Username
# APIPASS = Password
import os

api_user = os.getenv("APIUSER")
api_pass = os.getenv("APIPASS")

# Set the interface - apply from variables no matter what
cogitation_interface = Reliquary(
    "settings.json", input_user=api_user, input_pass=api_pass
)

# Build Results Dictionary
stack = {}

# Get all router IDs
router_list = json.loads(cogitation_interface.namshub("get_tier0s"))["results"]

# For each router ID, populate the list
for i in router_list:
    # Each logical router has a UUID, and is structured to provide a `dict` per `edge_node`
    stack[i['unique_id']] = {}
    # Embed the friendly name as part of the JSON dictionary
    stack[i['unique_id']]['name'] = i['id']
    stack[i['unique_id']]['contents'] = {}
    # Execute another API call per logical router, this will be mapped into the stack
    stack[i['unique_id']]['contents'] = json.loads(cogitation_interface.namshub("get_tier0_routes", namshub_variables=json.dumps({"id": i['id']})))['results']
    # Recursive sort everything

# Compare to latest json file
try:
    previous_dict = cogitation_interface.get_json_file('trackroute_latest.json')
except:
    previous_dict = {}

# Show the results
print(json.dumps(stack, indent=4))
