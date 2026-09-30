"""Classify journal entries without assuming elevated permissions."""
import subprocess
from config import COMMAND_TIMEOUT

def analyze_journal(lines=100, unit=None):
    cmd = ["journalctl", "--no-pager", "-n", str(lines), "-o", "short-iso"]
    if unit: cmd += ["-u", unit]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=COMMAND_TIMEOUT)
        entries = p.stdout.splitlines()
    except (OSError, subprocess.TimeoutExpired): entries = []
    findings = []
    for line in entries:
        low = line.lower()
        if any(x in low for x in ("critical", "panic", "emerg")): level = "CRITICAL"
        elif any(x in low for x in ("error", "failed", "denied")): level = "ERROR"
        elif any(x in low for x in ("warning", "timeout", "timed out")): level = "WARNING"
        else: level = "INFO"
        findings.append({"level": level, "message": line})
    return findings
