# 🚀 Android Startup Manager

Control which apps start at boot — disable slow startups, improve boot time.

## Tools

| Tool | What it does |
|------|-------------|
| `startup_scan.py` | Find all apps registered to start at boot |
| `startup_disable.py` | Batch disable startup for apps |
| `boot_time_monitor.py` | Measure actual boot time before/after optimizations |

## Quick start

```bash
# See what's starting at boot
python3 startup_scan.py

# Disable slow starters (interactive)
python3 startup_disable.py --interactive

# Measure boot time impact
python3 boot_time_monitor.py
```
