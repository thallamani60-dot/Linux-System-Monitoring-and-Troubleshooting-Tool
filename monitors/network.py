"""Read-only interface, listening socket, and connectivity checks."""
import socket
import subprocess
from config import COMMAND_TIMEOUT

def _run(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=COMMAND_TIMEOUT, check=False)
        return p.stdout.strip() if p.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired): return ""

def network_metrics():
    interfaces = []
    for line in _run(["ip", "-brief", "address"]).splitlines():
        parts = line.split()
        if parts: interfaces.append({"name": parts[0], "up": "UP" in parts, "addresses": parts[2:]})
    internet = False
    try:
        with socket.create_connection(("1.1.1.1", 443), timeout=2): internet = True
    except OSError: pass
    return {"interfaces": interfaces, "listening_ports": _run(["ss", "-H", "-lntup"]).splitlines(),
            "tcp_connections": _run(["ss", "-H", "-tan"]).splitlines(), "internet_reachable": internet}
