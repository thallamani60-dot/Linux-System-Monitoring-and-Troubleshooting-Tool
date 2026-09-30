"""Memory metrics."""
from pathlib import Path
def memory_metrics(threshold=80.0, proc_root="/proc"):
    values = {}
    for line in (Path(proc_root) / "meminfo").read_text().splitlines():
        k, _, rest = line.partition(":")
        if rest.strip(): values[k] = int(rest.split()[0]) * 1024
    total = values["MemTotal"]; available = values.get("MemAvailable", values.get("MemFree", 0))
    used = total - available; percent = 100 * used / total if total else 0
    return {"total_bytes": total, "used_bytes": used, "available_bytes": available,
            "usage_percent": round(percent, 1), "threshold": threshold,
            "status": "CRITICAL" if percent >= threshold else "OK"}
