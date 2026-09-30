# Architecture

```mermaid
flowchart LR
  Timer[systemd timer, every 5 minutes] --> Service[oneshot service, least-privilege user]
  Service --> App[Python monitor.py]
  App --> Collectors[CPU, memory, disk, process, network, systemd]
  App --> Journal[journalctl, read-only]
  Collectors --> Detect[Threshold and service incident detection]
  Journal --> Detect
  Detect --> Reports[Markdown health reports and JSON incident records]
  EC2[Ubuntu EC2] --> CW[CloudWatch Agent and alarms]
  App -. OS diagnostic reports .-> Reports
```

Linux Sentinel collects OS-level diagnostic context. CloudWatch separately collects configured AWS and guest metrics; the agent and IAM permissions must be installed/configured explicitly.
