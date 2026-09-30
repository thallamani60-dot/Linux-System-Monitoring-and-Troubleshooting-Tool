# Troubleshooting guide

Start with `python monitor.py` and read the timestamped report. CPU: `top` and `ps aux --sort=-%cpu | head` show load and likely process contributors. Memory: `free -h` distinguishes available memory from total; `ps aux --sort=-%mem | head` ranks processes. Disk: `df -h /` shows filesystem capacity; `du -xhd1 /` finds large directories on the same filesystem. Network: `ip address` checks addresses/link, `ip route` checks routing, `ss -tulnp` lists sockets, `ping` tests ICMP reachability, and `getent hosts` checks configured name resolution. Services: `systemctl status NAME` gives state and context; `journalctl -u NAME` shows unit logs. Permission restrictions can hide process names and journal entries; run read-only diagnostics with sudo only when needed and authorized.

Thresholds are configurable with `SENTINEL_CPU_THRESHOLD`, `SENTINEL_MEMORY_THRESHOLD`, `SENTINEL_DISK_THRESHOLD`, `SENTINEL_DISK_PATH`, and comma-separated `SENTINEL_SERVICES`.
