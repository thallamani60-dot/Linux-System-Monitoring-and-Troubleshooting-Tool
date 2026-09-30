# High CPU (controlled simulation)

**Symptom:** CPU exceeds configured threshold. On a disposable Linux host, run a bounded worker: `timeout 45s bash -c 'while :; do :; done' & LOAD_PID=$!`. Observe with `top` and `ps aux --sort=-%cpu | head`, and run `python monitor.py`. Stop only the process you started with `kill "$LOAD_PID"` (or let `timeout` expire), then verify with `ps -p "$LOAD_PID"` and a fresh report. The shell variable is scoped to the shell where the command was run. A high reading alone does not prove root cause.
