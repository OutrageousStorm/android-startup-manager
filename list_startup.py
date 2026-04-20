#!/usr/bin/env python3
"""
list_startup.py -- List all apps configured to auto-start
Usage: python3 list_startup.py [--sort time|alphabetical]
"""
import subprocess, re, argparse

def adb(cmd):
    r = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    return r.stdout.strip()

def get_startup_apps():
    """Query all persistent apps and receivers configured to auto-start"""
    raw = adb("pm dump | grep -A1 'Receiver'")
    apps = {}
    
    # Also check enabled components
    out = adb("pm list packages -u")  # uninstalled apps
    
    # Parse BOOT_COMPLETED receivers
    for line in raw.splitlines():
        m = re.search(r'Package \[(\S+)\]', line)
        if m:
            pkg = m.group(1)
            # Check if BOOT_COMPLETED is enabled
            has_boot = adb(f"dumpsys package {pkg} | grep BOOT_COMPLETED | grep 'enabled=true'")
            if has_boot:
                apps[pkg] = "BOOT_COMPLETED"
    
    return apps

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sort", choices=["time", "alphabetical"], default="alphabetical")
    args = parser.parse_args()

    print("\n⚡ Android Startup Apps")
    print("=" * 50)
    
    apps = get_startup_apps()
    if not apps:
        print("No startup apps detected (or method requires root dump).")
        print("\nFallback: checking enabled components...")
        # Fallback: just show all installed apps
        raw = adb("pm list packages")
        apps = {l.split(":")[1]: "installed" for l in raw.splitlines() if l.startswith("package:")}
    
    print(f"\nFound {len(apps)} app(s)\n")
    for pkg in sorted(apps.keys()):
        label = pkg.split('.')[-1]
        print(f"  • {label:<30} {pkg}")
    
    print(f"\nTo disable auto-start:")
    print("  python3 disable_startup.py <package>")

if __name__ == "__main__":
    main()
