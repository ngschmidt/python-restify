#!/usr/bin/python3
# Python NSX-T Password Rotation with Vault
# Nicholas Schmidt
# 4-Dec-2021

# System Calls
import os
import sys
from textwrap import indent

# Hashicorp Client
import hvac

# NSX-T Client
from restify.RuminatingCogitation import Reliquary

# Markup libraries
import json

# Let the user know if the envs aren't set up properly
for env_mandatory in ["VAULT_URL", "VAULT_TOKEN", "APIUSER", "APIPASS"]:
    if env_mandatory not in os.environ:
        sys.exit(
            "Missing environment variable " + env_mandatory + " not found! Exiting..."
        )

# Use `hvac` to initialize Vault API connection

# Say the vault instance we're connecting to
print("Connecting to Vault instance at " + os.getenv("VAULT_URL"))

# Start-up the vault client. We can read the environment variable for a custom CA if it exists
vault_client = hvac.Client()
if "VAULT_CA" in os.environ:
    vault_client = hvac.Client(
        url=os.getenv("VAULT_URL"),
        token=os.getenv("VAULT_TOKEN"),
        verify=os.getenv("VAULT_CA"),
    )
else:
    vault_client = hvac.Client(
        url=os.getenv("VAULT_URL"), token=os.getenv("VAULT_TOKEN")
    )

# Verify we're connected, unsealed, and authenticated
# If not, exit because the rest of the code won't work
if (
    vault_client.is_sealed() is False
    and vault_client.is_authenticated() is True
    and vault_client.is_initialized() is True
):
    print("Vault Status: " + str(vault_client.is_authenticated()))
else:
    sys.exit(
        "Unable to start the Vault client!\r\n Status (Sealed): "
        + str(vault_client.is_sealed())
        + "\r\n Status (Authenticated): "
        + str(vault_client.is_authenticated())
        + "\r\n Status (Initialized): "
        + str(vault_client.is_initialized())
    )

# Initialize NSX-T Connections

# Use `Reliquary`` to form API connection
cogitation_interface = Reliquary(
    "settings.json", input_user=os.getenv("APIUSER"), input_pass=os.getenv("APIPASS")
)

# Fetch NSX Edge Transport Nodes
tn_result = json.loads(cogitation_interface.namshub("get_tns"))["results"]
tn_dict = {}
for i in tn_result:
    # Only add to the list if it's an Edge Transport Node
    if i["node_deployment_info"]["resource_type"] == "EdgeNode":
        tn_dict[i["node_id"]] = {
            "type": i["node_deployment_info"]["resource_type"],
            "name": i["node_deployment_info"]["display_name"],
        }

# Print our list
print("Found the following Edge Transport Nodes: ")
print(json.dumps(tn_dict, indent=4))

# Fetch existing Edge Transport Node Secrets
print(vault_client.secrets.kv.v2.read_secret_version(path="abc", mount_point="nsx"))

# Generate new Edge Transport Node Secrets

# Apply new Edge Transport Node Secrets

# If it fails, rollback the Secret
