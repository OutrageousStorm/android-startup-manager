#!/usr/bin/env python3
"""
startup_scan.py -- Find all apps registered to start at boot
Usage: python3 startup_scan.py [--filter keyword]
"""
import subprocess, re

def adb(cmd):
    return subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True).stdout

BOOT_RECEIVERS = [
    "android.intent.action.BOOT_COMPLETED",
    "android.intent.action.QUICKBOOT_POWERON",
    "com.htc.intent.action.QUICKBOOT_POWERON",
]

def find_boot_receivers():
    manifest_dump = adb("pm dump | grep -A2 -B2 'BOOT_COMPLETED'")
    receivers = set()
    
    # Also check dumpsys receiver info
    for pkg in adb("pm list packages -3").splitlines():
        if pkg.startswith("package:"):
            pkg = pkg.split(":")[1]
            dump = adb(f"pm dump {pkg}")
            for line in dump.splitlines():
                if "BOOT_COMPLETED" in line or "QUICKBOOT" in line:
                    # Extract package name
                    receivers.add(pkg)
    
    return receivers

def main():
    print("\n🚀 Boot Receiver Scanner")
    print("=" * 45)
    
    receivers = find_boot_receivers()
    
    if not receivers:
        print("No apps registered for boot startup found.")
        return
    
    print(f"\nFound {len(receivers)} apps that start at boot:\n")
    for pkg in sorted(receivers):
        label = pkg.split('.')[-1]
        print(f"  • {label:<30} {pkg}")
    
    print(f"\nTo disable startup for an app:")
    print(f"  adb shell pm disable-user <package.name>")

if __name__ == "__main__":
    main()
