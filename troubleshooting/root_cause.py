"""Evidence-based root-cause hints; these are hypotheses, not conclusions."""
def root_cause_hint(component):
    return {"cpu": "Possible causes include a busy workload, runaway process, or repeated service retries; confirm with process and journal evidence.",
            "memory": "Possible causes include workload growth, a leak, or cache pressure; inspect available memory and process RSS.",
            "disk": "Possible causes include logs, temporary files, or application data growth; identify the directory before cleanup.",
            "network": "Check link, address, route, ports, then DNS to isolate the failing layer."}.get(component, "Inspect the service unit and its journal before changing state.")
