"""Filesystem usage metrics."""
import shutil

def disk_metrics(path="/", threshold=85.0):
    total, used, free = shutil.disk_usage(path); percent = 100 * used / total if total else 0
    return {"path": path, "total_bytes": total, "used_bytes": used, "free_bytes": free,
            "usage_percent": round(percent, 1), "threshold": threshold,
            "status": "CRITICAL" if percent >= threshold else "OK"}
