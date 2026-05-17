#!/usr/bin/env python3
"""
startup_disable.py -- Disable apps from starting at boot
Usage: python3 startup_disable.py --app com.example.app
       python3 startup_disable.py --interactive
"""
import subprocess, argparse, sys

def adb(cmd):
    return subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True).stdout

COMMON_SLOW_STARTERS = [
    "com.facebook.katana", "com.facebook.system",
    "com.google.android.apps.maps",
    "com.spotify.music",
    "com.instagram.android",
]

def disable_startup(pkg):
    """Disable a package from auto-starting"""
    result = adb(f"pm disable-user {pkg}")
    if "Exception" in result or "Error" in result:
        print(f"  ✗ Failed to disable {pkg}")
        return False
    print(f"  ✓ Disabled {pkg}")
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", help="Disable specific app")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--common", action="store_true", help="Disable common slow starters")
    args = parser.parse_args()

    print("\n🚀 Boot Startup Disabler")
    print("=" * 45)

    if args.app:
        disable_startup(args.app)
    elif args.common:
        print(f"\nDisabling {len(COMMON_SLOW_STARTERS)} common slow starters...\n")
        for pkg in COMMON_SLOW_STARTERS:
            if "package:" + pkg in adb("pm list packages"):
                disable_startup(pkg)
    elif args.interactive:
        print("\nEnter package names (one per line, 'q' to quit):\n")
        while True:
            pkg = input("> ").strip()
            if pkg == 'q': break
            disable_startup(pkg)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
