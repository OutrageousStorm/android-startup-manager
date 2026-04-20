# ⚡ Android Startup Manager

Disable apps from auto-starting at boot — improve boot time and reduce memory footprint.

## Tools

| Script | What it does |
|--------|-------------|
| `list_startup.py` | Show all apps configured to auto-start |
| `disable_startup.py` | Disable auto-start for specific apps |
| `analyze.py` | Measure boot time impact per app |

## Usage

```bash
# Show all startup apps
python3 list_startup.py

# Disable specific app from starting
python3 disable_startup.py com.facebook.katana

# Measure startup impact
python3 analyze.py
```
