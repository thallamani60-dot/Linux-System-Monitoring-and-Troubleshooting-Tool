"""Return processes ranked by CPU and memory using the Linux ps command."""
import subprocess
from config import COMMAND_TIMEOUT

def top_processes(limit=5):
    try:
        result = subprocess.run(
            ["ps", "-eo", "pid=,comm=,pcpu=,pmem="], capture_output=True,
            text=True, timeout=COMMAND_TIMEOUT, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    rows = []
    for line in result.stdout.splitlines():
        fields = line.split(None, 3)
        if len(fields) != 4:
            continue
        try:
            rows.append({"pid": int(fields[0]), "name": fields[1],
                         "cpu_percent": round(float(fields[2]), 1),
                         "memory_percent": round(float(fields[3]), 1)})
        except ValueError:
            continue
    # Keep the union of CPU and memory leaders so either kind of pressure is visible.
    cpu = sorted(rows, key=lambda item: item["cpu_percent"], reverse=True)[:limit]
    memory = sorted(rows, key=lambda item: item["memory_percent"], reverse=True)[:limit]
    return sorted({item["pid"]: item for item in cpu + memory}.values(),
                  key=lambda item: max(item["cpu_percent"], item["memory_percent"]), reverse=True)
