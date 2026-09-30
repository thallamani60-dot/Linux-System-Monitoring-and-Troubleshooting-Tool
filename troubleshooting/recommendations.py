"""Safe, read-only first-line diagnostic commands with their purpose."""
GUIDES = {
 "cpu": [("top", "See live CPU use and whether load is sustained."), ("ps aux --sort=-%cpu | head", "Rank processes by CPU use."), ("systemctl --failed", "Find failed units that may be retrying."), ("journalctl -p err -n 100", "Review recent system errors.")],
 "memory": [("free -h", "Compare available memory and swap."), ("ps aux --sort=-%mem | head", "Find processes using the most resident memory."), ("journalctl -p err -n 100", "Look for allocation failures or OOM events.")],
 "disk": [("df -h /", "Check filesystem capacity."), ("du -xhd1 / 2>/dev/null | sort -h", "Locate large top-level directories without crossing filesystems."), ("journalctl -p err -n 100", "Check for filesystem or write errors.")],
 "network": [("ip address", "Check link state and assigned addresses."), ("ip route", "Check the default route and routing table."), ("ss -tulnp", "Inspect listening TCP/UDP sockets."), ("ping -c 3 1.1.1.1", "Test IP reachability (ICMP may be filtered)."), ("getent hosts example.com", "Test system name resolution.")],
 "service": [("systemctl status SERVICE", "Inspect unit state and recent messages."), ("journalctl -u SERVICE -n 100", "Review unit-specific logs."), ("systemctl is-enabled SERVICE", "Check whether the unit starts at boot.")]
}
def recommendations(component): return GUIDES.get(component.lower(), [])
