#!/usr/bin/python3
# Python NSX-T Password Rotation with Vault
# Nicholas Schmidt
# 4-Dec-2021

# System Calls
import os
import sys

# Hashicorp Client
import hvac


# Say which Vault we're hitting, let the user know if the envs aren't set up properly
for env_mandatory in ['VAULT_URL', 'VAULT_TOKEN', 'VAULT_CA']:
    if env_mandatory not in os.environ:
        sys.exit("Missing environment variable " + env_mandatory + " not found! Exiting...")

print("Connecting to Vault instance at " + os.getenv('VAULT_URL'))

vault_client = hvac.Client()
vault_client = hvac.Client(url=os.getenv('VAULT_URL'), token=os.getenv('VAULT_TOKEN'), verify=os.getenv('VAULT_CA'))

print(vault_client.read('nsx/abc'))
