#!/usr/bin/python3
# Python NSX-T Password Rotation with Vault
# Nicholas Schmidt
# 4-Dec-2021

# System Calls
import os
import sys

# Hashicorp Client
import hvac


# Let the user know if the envs aren't set up properly
for env_mandatory in ["VAULT_URL", "VAULT_TOKEN"]:
    if env_mandatory not in os.environ:
        sys.exit(
            "Missing environment variable " + env_mandatory + " not found! Exiting..."
        )

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

# Verify we're connected
if (
    vault_client.is_sealed() is False
    and vault_client.is_authenticated() is True
    and vault_client.is_initialized() is True
):
    print("Authentication Status: " + str(vault_client.is_authenticated()))
else:
    sys.exit(
        "Unable to start the Vault client!\r\n Status (Sealed): "
        + str(vault_client.is_sealed())
        + "\r\n Status (Authenticated): "
        + str(vault_client.is_authenticated())
        + "\r\n Status (Initialized): "
        + str(vault_client.is_initialized())
    )
