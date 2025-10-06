#!/usr/bin/env python3
import json
import sys
import os

print(f"Current working directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

# Read from tf_output.json instead of running terraform command
tf_output_file = "tf_output.json"

if not os.path.exists(tf_output_file):
    print(f"Error: {tf_output_file} not found!", file=sys.stderr)
    sys.exit(1)

print(f"Reading from {tf_output_file}")

try:
    with open(tf_output_file, 'r') as f:
        data = json.load(f)
    print(f"Successfully loaded {tf_output_file}")
    print(f"Content: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"Error reading {tf_output_file}: {e}", file=sys.stderr)
    sys.exit(1)

# Extract IPs - handle the structure from tf_output.json
ips = data.get("web_public_ips", {}).get("value", [])

if not ips:
    print("No IPs found in terraform output 'web_public_ips'", file=sys.stderr)
    print(f"Available keys: {list(data.keys())}", file=sys.stderr)
    sys.exit(2)

print(f"Found IPs: {ips}")

# Generate inventory file
with open("inventory.ini", "w") as f:
    f.write("[web]\n")
    for ip in ips:
        # Using 'admin' for Debian instances
        f.write(f"{ip} ansible_user=admin ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'\n")

print("Successfully wrote inventory.ini")
print("Inventory contents:")
with open("inventory.ini", "r") as f:
    print(f.read())