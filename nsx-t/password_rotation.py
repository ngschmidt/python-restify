#!/usr/bin/python3
# Python NSX-T Password Rotation with Vault
# Nicholas Schmidt
# 4-Dec-2021

import os

import hvac

print(os.getenv("VAULT_URL"))
print(os.getenv('VAULT_TOKEN'))
