#!/usr/bin/env bash
set -u
section() { printf '\n==== %s ====\n' "$1"; }
section SYSTEM
printf 'Hostname: '; hostname
printf 'Uptime: '; uptime -p 2>/dev/null || uptime
section CPU; top -bn1 | head -n 5
section MEMORY; free -h
section DISK; df -h /
section TOP_PROCESSES; ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n 8
section NETWORK; ip -brief address 2>/dev/null || true
section LISTENING_PORTS; ss -tulnp 2>/dev/null || ss -tuln
section FAILED_SERVICES; systemctl --failed --no-legend 2>/dev/null || true
section RECENT_ERRORS; journalctl -p err -n 20 --no-pager 2>/dev/null || echo 'Journal unavailable to this user.'
