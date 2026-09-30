# Incident playbooks

These are controlled training procedures. Run them only on a disposable Ubuntu EC2 instance or another machine you administer. Record the actual observed output and timestamps in your own report; examples here are procedures, not claims of real incidents.

## Safe test workload helpers

Use a temporary directory under `/tmp`, cap memory explicitly, and always stop the background process from the same shell. Do not fill `/` and do not use unbounded stress commands.

