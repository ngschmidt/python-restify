#!/usr/bin/python3
# Python NSX-T Certificate Change
# Nicholas Schmidt
# 21-Nov-2021

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
stack = {
    "old_cluster_certificate_id": False,
    "old_certificate_list": [],
    "upload_result": False,
    "new_certificate_id": False,
    "new_certificate_list": [],
    "new_cluster_certificate_id": False,
}

# GET current cluster certificate ID
stack["old_cluster_certificate_id"] = json.loads(
    cogitation_interface.namshub("get_cluster_certificate_id")
)["certificate_id"]

# GET certificate store
for i in json.loads(cogitation_interface.namshub("get_cluster_certificates"))[
    "results"
]:
    stack["old_certificate_list"].append(i["id"])
# We need to compare lists, so let's sort it first
stack["old_certificate_list"].sort()

# PUT a replacement certificate with a new name
print(cogitation_interface.namshub("put_certificate", namshub_variables="cert.json"))

# GET certificate store (validate PUT)
for i in json.loads(cogitation_interface.namshub("get_cluster_certificates"))[
    "results"
]:
    stack["new_certificate_list"].append(i["id"])
# We need to compare lists, so let's sort it first, then make it the difference between new and old
stack["old_certificate_list"].sort()
stack["new_certificate_list"] = list(
    set(stack["new_certificate_list"]) - set(stack["old_certificate_list"])
)

# Be Idempotent - this may be run multiple times, and should handle it accordingly.
if len(stack["new_certificate_list"]) == 0:
    stack["new_certificate_id"] = input(
        "Change not detected! Please select a certificate to replace with: "
    )
else:
    stack["new_certificate_id"] = stack["new_certificate_list"][0]

# GET certificate ID (to further validate PUT)
print(
    cogitation_interface.namshub(
        "get_cluster_certificate",
        namshub_variables=json.dumps({"id": stack["new_certificate_id"]}),
    )
)
# POST update cluster certificate
print(
    cogitation_interface.namshub(
        "post_cluster_certificate",
        namshub_variables=json.dumps({"id": stack["new_certificate_id"]}),
    )
)
print(
    cogitation_interface.namshub(
        "post_webui_certificate",
        namshub_variables=json.dumps({"id": stack["new_certificate_id"]}),
    )
)

# GET current cluster certificate ID
stack["new_cluster_certificate_id"] = json.loads(
    cogitation_interface.namshub("get_cluster_certificate_id")
)["certificate_id"]

# Show the results
print(json.dumps(stack, indent=4))
