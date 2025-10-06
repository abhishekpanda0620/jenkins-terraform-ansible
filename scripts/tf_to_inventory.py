#!/usr/bin/env python3
import json, subprocess, sys

# Get terraform JSON output for 'web_public_ips'
proc = subprocess.run(["terraform", "output", "-json"], capture_output=True, text=True)
if proc.returncode != 0:
    print(proc.stderr, file=sys.stderr); sys.exit(1)

data = json.loads(proc.stdout)
ips = data.get("web_public_ips", {}).get("value", [])

if not ips:
    print("No IPs found in terraform output 'web_public_ips'", file=sys.stderr); sys.exit(2)

with open("inventory.ini", "w") as f:
    f.write("[web]\n")
    for ip in ips:
        # change ansible_user if needed (ubuntu/ec2-user)
        f.write(f"{ip} ansible_user=ubuntu\n")
print("Wrote inventory.ini")
