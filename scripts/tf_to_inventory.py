#!/usr/bin/env python3
import json, subprocess, sys, os

print(f"Current working directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

# Get terraform JSON output for 'web_public_ips'
print("Running: terraform output -json")
proc = subprocess.run(["terraform", "output", "-json"], capture_output=True, text=True)

if proc.returncode != 0:
    print(f"Terraform command failed with return code: {proc.returncode}", file=sys.stderr)
    print(f"STDOUT: {proc.stdout}", file=sys.stderr)
    print(f"STDERR: {proc.stderr}", file=sys.stderr)
    sys.exit(1)

print(f"Terraform output: {proc.stdout}")

data = json.loads(proc.stdout)
ips = data.get("web_public_ips", {}).get("value", [])

if not ips:
    print("No IPs found in terraform output 'web_public_ips'", file=sys.stderr)
    print(f"Available keys: {list(data.keys())}", file=sys.stderr)
    sys.exit(2)

print(f"Found IPs: {ips}")

with open("inventory.ini", "w") as f:
    f.write("[web]\n")
    for ip in ips:
        # change ansible_user if needed (ubuntu/ec2-user)
        f.write(f"{ip} ansible_user=admin\n")

print("Wrote inventory.ini")
print("Inventory contents:")
with open("inventory.ini", "r") as f:
    print(f.read())