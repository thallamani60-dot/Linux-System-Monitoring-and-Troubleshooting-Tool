# Memory pressure (bounded simulation)

**Symptom:** available memory falls below the configured percentage threshold. On a disposable host, run a bounded allocator using Python: `python3 -c 'import time; x=bytearray(64*1024*1024); time.sleep(45)' & LOAD_PID=$!`. Adjust the allocation down to fit comfortably in available RAM. Inspect `free -h`, `ps aux --sort=-%mem | head`, and `python monitor.py`; stop the exact child using `kill "$LOAD_PID"` or wait 45 seconds. Verify with `ps -p "$LOAD_PID"` and a fresh `free -h`/report. Never induce OOM on a shared machine.
