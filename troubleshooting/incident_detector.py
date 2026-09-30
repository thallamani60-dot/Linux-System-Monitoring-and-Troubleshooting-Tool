"""Convert metric threshold failures into stable incident descriptions."""
from datetime import datetime, timezone
from uuid import uuid4
from troubleshooting.recommendations import recommendations
from troubleshooting.root_cause import root_cause_hint

def detect_incidents(snapshot):
    incidents = []
    for component in ("cpu", "memory", "disk"):
        item = snapshot.get(component, {})
        if item.get("status") == "CRITICAL":
            steps = recommendations(component)
            incidents.append({"incident_id": "INC-" + uuid4().hex[:8].upper(), "timestamp": datetime.now(timezone.utc).isoformat(),
                "component": component, "severity": "CRITICAL", "symptom": f"{component.title()} usage exceeded threshold.",
                "detected_metric": item.get("usage_percent"), "threshold": item.get("threshold"),
                "investigation_commands": [x[0] for x in steps], "root_cause": root_cause_hint(component),
                "resolution": "Investigate evidence and apply an approved, component-specific fix; Sentinel takes no corrective action.",
                "verification": "Rerun the health report and confirm the metric is below threshold.", "status": "OPEN"})
    for svc in snapshot.get("services", []):
        if svc.get("status") in ("FAILED", "INACTIVE"):
            steps = recommendations("service")
            incidents.append({"incident_id": "INC-" + uuid4().hex[:8].upper(), "timestamp": datetime.now(timezone.utc).isoformat(),
                "component": svc["name"], "severity": "CRITICAL", "symptom": f"Service {svc['name']} is {svc['status']}.",
                "detected_metric": svc["status"], "threshold": "ACTIVE", "investigation_commands": [x[0].replace("SERVICE", svc["name"]) for x in steps],
                "root_cause": root_cause_hint(svc["name"]), "resolution": "Investigate first; start or restart only after a human approves an appropriate action.",
                "verification": f"Confirm systemctl is-active {svc['name']} reports active and rerun the health report.", "status": "OPEN"})
    return incidents
