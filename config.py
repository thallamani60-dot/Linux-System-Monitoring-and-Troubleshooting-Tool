"""Runtime configuration. Override values with environment variables."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CPU_THRESHOLD = float(os.getenv("SENTINEL_CPU_THRESHOLD", "80"))
MEMORY_THRESHOLD = float(os.getenv("SENTINEL_MEMORY_THRESHOLD", "80"))
DISK_THRESHOLD = float(os.getenv("SENTINEL_DISK_THRESHOLD", "80"))
DISK_PATH = os.getenv("SENTINEL_DISK_PATH", "/")
SERVICES = tuple(s.strip() for s in os.getenv("SENTINEL_SERVICES", "ssh,nginx").split(",") if s.strip())
REPORT_DIR = Path(os.getenv("SENTINEL_REPORT_DIR", ROOT / "reports"))
LOG_DIR = Path(os.getenv("SENTINEL_LOG_DIR", ROOT / "logs"))
INCIDENT_DIR = Path(os.getenv("SENTINEL_INCIDENT_DIR", ROOT / "incidents" / "records"))
LOG_LINES = int(os.getenv("SENTINEL_LOG_LINES", "100"))
COMMAND_TIMEOUT = float(os.getenv("SENTINEL_COMMAND_TIMEOUT", "5"))
