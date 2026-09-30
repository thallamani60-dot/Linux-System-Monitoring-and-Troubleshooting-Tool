# Linux Sentinel

A beginner-friendly, read-only Linux health checker built with Python's standard library, Bash, and Linux commands. It checks CPU, memory, disk, processes, network, systemd services, and recent journal messages, then prints and saves a troubleshooting report.

It requires no third-party Python packages, cloud services, database, Docker, or framework.

## Requirements

- Linux with Python 3
- `ps`, `ip`, `ss`, `systemctl`, and `journalctl` commands (some are included in the `procps`, `iproute2`, and `systemd` packages)

On Ubuntu or Debian, install the basic tools if needed:

```bash
sudo apt update
sudo apt install -y python3 procps iproute2 systemd
```

## Run

From this project directory, run the whole health check with one command:

```bash
bash scripts/run.sh
```

The report appears in the terminal and is saved as `reports/health-<timestamp>.md`. A nonzero exit code means an incident was detected. To print JSON without saving a report:

```bash
python3 monitor.py --json --no-report
```

## Checks and thresholds

CPU, RAM, and disk warnings default to 80%. Process output includes the top CPU and memory users. Network details use `ip` and `ss`; a short TCP connection to `1.1.1.1:443` is shown as a basic reachability check. Services are checked with `systemctl`; recent messages are read with `journalctl`.

You can override thresholds, disk path, and services with environment variables:

```bash
SENTINEL_CPU_THRESHOLD=80 \
SENTINEL_MEMORY_THRESHOLD=80 \
SENTINEL_DISK_THRESHOLD=80 \
SENTINEL_DISK_PATH=/ \
SENTINEL_SERVICES=ssh,nginx \
bash scripts/run.sh
```

Set `SENTINEL_SERVICES=ssh` if Nginx is not installed. Some Linux distributions call the SSH unit `sshd`. The tool does not stop processes, restart services, or delete files. It reports likely causes as hypotheses for a person to investigate. Service and journal visibility depends on the current user's permissions.

## Project files

- `monitor.py` — command-line entry point and report writer
- `monitors/` — CPU, memory, disk, process, network, and service checks
- `troubleshooting/` — incident descriptions, log analysis, and investigation guidance
- `scripts/` — one-command launcher and Bash helper scripts
- `reports/sample-health-report.md` — clearly marked illustrative report
- `incidents/` — extra troubleshooting examples

## Bash helpers

Run a quick shell summary with `bash scripts/system_health.sh`, network commands with `bash scripts/network_check.sh`, or inspect one service with `bash scripts/service_check.sh nginx`.

## Example troubleshooting report

The generated report states each detected problem, a possible cause, commands to investigate, and a suggested next step. See [the sample report](reports/sample-health-report.md). The sample uses fictional values and is not actual system output.
