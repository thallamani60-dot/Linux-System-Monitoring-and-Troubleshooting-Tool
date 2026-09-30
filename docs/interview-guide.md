# Interview preparation

1. Why EC2? It provides a familiar, controllable Linux host for demonstrating OS operations; production choice depends on workload and managed-service tradeoffs.
2. Why Python? It supports structured collection, classification, and report generation with a small standard-library footprint.
3. Why Bash? It is effective for concise operator workflows and native Linux command composition.
4. Why systemd instead of cron? systemd provides unit dependencies, service state, centralized journal output, and timer scheduling.
5. How does journalctl work? It queries systemd's journal, filterable by unit, priority, and time; access depends on host policy.
6. How is high CPU detected? A sampled CPU percentage is compared with a configurable threshold; process sampling helps investigation but is not a causal proof.
7. How would you troubleshoot Nginx? Check `systemctl status`, unit journal, config/test output, listener, and access/error logs before making a change.
8. What if disk reaches 100%? Writes, logs, package operations, and services can fail; identify large paths and expand/clean only with a verified plan.
9. How does CloudWatch differ? CloudWatch provides centralized AWS metrics, dashboards, and alarms; guest memory/disk need the agent and custom metrics need explicit configuration. Sentinel adds local process, service, journal, and diagnostic context.
10. How to scale? Add stable metric export and centralized transport, explicit identity/retention, alert deduplication, and fleet configuration management; do not silently assume local reports are centralized.
