"""Sample CPU and load metrics from Linux's /proc filesystem."""
from pathlib import Path
import time


def cpu_metrics(threshold=80.0, interval=0.15, proc_root="/proc"):
    root = Path(proc_root)
    def read():
        parts = (root / "stat").read_text().splitlines()[0].split()[1:]
        nums = list(map(int, parts)); idle = nums[3] + (nums[4] if len(nums) > 4 else 0)
        return sum(nums), idle
    a, ia = read(); time.sleep(max(0, interval)); b, ib = read()
    usage = 0.0 if b == a else 100 * (1 - (ib - ia) / (b - a))
    count = sum(1 for p in (root / "stat").read_text().splitlines() if p.startswith("cpu") and p[3:4].isdigit()) or 1
    loads = None
    try:
        loads = tuple(map(float, (root / "loadavg").read_text().split()[:3]))
    except OSError:
        pass
    return {"usage_percent": round(usage, 1), "cpu_count": count, "load_average": loads,
            "threshold": threshold, "status": "CRITICAL" if usage >= threshold else "OK"}
