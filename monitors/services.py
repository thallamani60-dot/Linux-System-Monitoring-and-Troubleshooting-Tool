"""systemd unit health checks."""
import subprocess
from config import COMMAND_TIMEOUT

def service_status(name):
    try:
        p = subprocess.run(["systemctl", "is-active", name], capture_output=True, text=True, timeout=COMMAND_TIMEOUT)
        raw = (p.stdout or p.stderr).strip().lower()
    except (OSError, subprocess.TimeoutExpired): raw = "unknown"
    status = "ACTIVE" if raw == "active" else "FAILED" if raw == "failed" else "INACTIVE" if raw == "inactive" else "UNKNOWN" if raw in ("unknown", "") else raw.upper()
    return {"name": name, "status": status}
