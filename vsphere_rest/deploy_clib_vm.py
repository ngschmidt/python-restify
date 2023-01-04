#!/usr/bin/python3
# Deploy VM From Content Library
# Missing in `vmware_rest` Ansible Modules - deploy a VM from a template
# Nicholas Schmidt
# 02-Jan-2022

# System Calls
import os
import sys

# Arguments Parsing
import argparse

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

# Process User Inputs

play_help = (
    "Deploy VM from Content Library \r\n"
    + "Run without options to fetch an example based on the environment\r\n"
    + "Use environment variable `$API_ENDPOINT` to define the HTTP endpoint."
)
# Arguments Parsing
parser = argparse.ArgumentParser(description="Fetch via API")
parser.add_argument("-f", help="REST Settings File (JSON)")
parser.add_argument("-p", help="RESTful Payload")
parser.add_argument("-v", action="store_true")
args = parser.parse_args()

# Initialize vSphere Connection

# Use `Reliquary` to create API object
if args.f:
    cogitation_interface = Reliquary(
        args.f,
        input_user=os.getenv("API_USER"),
        input_pass=os.getenv("API_PASS"),
        input_endpoint=os.getenv("API_ENDPOINT"),
    )
else:
    cogitation_interface = Reliquary(
        "settings.json",
        input_user=os.getenv("API_USER"),
        input_pass=os.getenv("API_PASS"),
        input_endpoint=os.getenv("API_ENDPOINT"),
    )

# Define the JSON Payload as a schema. It'll be overwritten if a file is provided later
json_payload = {
    "id": False,
    "name": False,
    "datastore": False,
    "folder": False,
    "cluster": False,
}

if args.p:
    # Load Settings from JSON
    try:
        with open(args.p, "r") as json_filehandle:
            json_payload = json.load(json_filehandle)
    except Exception as e:
        exit("Error Loading Payload File " + args.p + ": " + str(e))
    for i in ["id", "name", "datastore", "folder", "cluster"]:
        if json_payload[i] is False:
            exit("Missing Key in payload: " + i)

# Get the API key and add it to the API interface object
cogitation_interface.add_http_header(
    "vmware-api-session-id", cogitation_interface.namshub("post_api_key").strip('"')
)

# Format the work dictionary. This will also function as the JSON schema

work_dict = {
    "content_libraries": {
        "content_libraries": [],
        "content_libraries_contents": {},
        "content_library_selected": False,
        "content_library_items": [],
        "content_library_item_selected": False,
    },
    "vsphere": {
        "vcenter_library_selected": False,
        "vcenter_folders": [],
        "vcenter_folder_selected": False,
        "vcenter_datastores": [],
        "vcenter_datastore_selected": False,
        "vcenter_clusters": [],
        "vcenter_cluster_selected": False,
    },
    "deployed": {"vm_id": False},
}

# Then, let's fetch the vSphere details

print("Fetching vSphere Details...")

# Fetch Content Library IDs
work_dict["content_libraries"]["content_libraries"] = json.loads(
    cogitation_interface.namshub("get_clibs")
)
for i in work_dict["content_libraries"]["content_libraries"]:
    # Create a temporary variable, because the overwriting-in-place will end the loop after the first iteration
    nested_loop_list = json.loads(
        cogitation_interface.namshub(
            "get_clib_library_items", namshub_variables={"id": i}
        )
    )
    # Check on each template ID
    for ii in nested_loop_list:
        # Grab info on the content library object
        work_dict["content_libraries"]["content_libraries_contents"][ii] = json.loads(
            cogitation_interface.namshub(
                "get_clib_library_item", namshub_variables={"id": ii}
            )
        )
        # Then, check and see if it's in vCenter
        work_dict["content_libraries"]["content_libraries_contents"][ii][
            "vcenter_obj"
        ] = json.loads(
            cogitation_interface.namshub(
                "get_vcenter_library_item", namshub_variables={"id": ii}
            )
        )
# Fetch vCenter Folders
work_dict["vsphere"]["vcenter_folders"] = json.loads(
    cogitation_interface.namshub("get_vcenter_folders")
)
# Fetch vCenter Datastores
work_dict["vsphere"]["vcenter_datastores"] = json.loads(
    cogitation_interface.namshub("get_vcenter_datastores")
)
# Fetch vCenter Clusters
work_dict["vsphere"]["vcenter_clusters"] = json.loads(
    cogitation_interface.namshub("get_vcenter_clusters")
)

# If no entries were provided, generate suggestions
if not args.p:
    json_payload = {
        "id": {"description": "The Content Library object to clone", "suggestions": {}},
        "name": "Example",
        "datastore": {
            "description": "The vSphere datastore to put virtual disks on",
            "suggestions": {},
        },
        "folder": {
            "description": "The vCenter folder to place the VM into",
            "suggestions": {},
        },
        "cluster": {
            "description": "The vSphere compute cluster to put the VM into",
            "suggestions": {},
        },
    }
    # Loop through and validate templates before suggesting them
    for i in work_dict["content_libraries"]["content_libraries_contents"]:
        if (
            work_dict["content_libraries"]["content_libraries_contents"][i]["vcenter_obj"].get("error_type", True)
            != "INTERNAL_SERVER_ERROR"
        ):
            json_payload["id"]["suggestions"][i] = {
                "name": work_dict["content_libraries"][
                    "content_libraries_contents"
                ][i]["name"],
                "guest_OS": work_dict["content_libraries"][
                    "content_libraries_contents"
                ][i]["vcenter_obj"].get("guest_OS", "UNKNOWN"),
            }
    # Looping datastore suggestions is easy for now. If we knew more data, this would be more refined
    for i in work_dict["vsphere"]["vcenter_datastores"]:
        json_payload["datastore"]["suggestions"][i["datastore"]] = {}
        json_payload["datastore"]["suggestions"][i["datastore"]]["name"] = i["name"]
    # Then, only VM folders
    for i in work_dict["vsphere"]["vcenter_folders"]:
        if i["type"] == "VIRTUAL_MACHINE":
            json_payload["folder"]["suggestions"][i["folder"]] = i["name"]
    # Then, Clusters
    for i in work_dict["vsphere"]["vcenter_clusters"]:
        json_payload["cluster"]["suggestions"][i["cluster"]] = i["name"]
else:
    # Let's start by validating inputs. Schema as reference:
    """
    json_payload = {
        "id": False,
        "name": False,
        "datastore": False,
        "folder": False,
        "cluster": False,
    }
    """
    # Check Template ID first against the collected data, and with a final API call
    if json_payload["id"] not in work_dict["content_libraries"]["content_libraries_contents"]:
        exit("VM Template UUID " + json_payload["id"] + " was not found in cached data!")
    if json.loads(cogitation_interface.namshub("get_vcenter_library_item", namshub_variables={"id": json_payload["id"]})).get("error_type", False):
        exit("VM Template UUID " + json_payload["id"] + " was not found on the remote vCenter Server!")
    # Do the same for the datastore
    if not any(d.get("datastore", False) == json_payload["datastore"] for d in work_dict["vsphere"]["vcenter_datastores"]):
        exit("vSphere Data Store ID " + json_payload["datastore"] + " was not found in cached data!")
    if json.loads(cogitation_interface.namshub("get_vcenter_datastore", namshub_variables={"id": json_payload["datastore"]})).get("error_type", False):
        exit("vSphere Data Store ID " + json_payload["datastore"] + " was not found on the remote vCenter Server!")
    # vCenter REST API does not currently support querying the folder, so let's just check against the cache
    if not any(d.get("folder", False) == json_payload["folder"] for d in work_dict["vsphere"]["vcenter_folders"]):
        exit("vSphere Folder ID " + json_payload["folder"] + " was not found in cached data!")
    # Next, check for a valid cluster
    if not any(d.get("cluster", False) == json_payload["cluster"] for d in work_dict["vsphere"]["vcenter_clusters"]):
        exit("vSphere Cluster ID " + json_payload["cluster"] + " was not found in cached data!")
    if json.loads(cogitation_interface.namshub("get_vcenter_cluster", namshub_variables={"id": json_payload["cluster"]})).get("error_type", False):
        exit("vSphere Cluster ID " + json_payload["cluster"] + " was not found on the remote vCenter Server!")

    # In the words of Darth Sidious, Do it!
    deployed_vm = cogitation_interface.namshub("post_deploy_vm", namshub_variables=json_payload)
    print(json.dumps(deployed_vm), indent=4)
    # TODO: Don't trust the output, validate it

# Dump the work
if args.v:
    print("Work Dictionary:")
    print(json.dumps(work_dict, indent=4))
    print("Payload:")
    print(json.dumps(json_payload, indent=4))
    print("Operation Complete!")
