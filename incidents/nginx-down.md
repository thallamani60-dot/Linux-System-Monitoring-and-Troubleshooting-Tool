# Nginx stopped (controlled simulation)

**Symptom:** configured `nginx` service reports INACTIVE. **Detection:** the service collector compares systemd state with ACTIVE and creates a CRITICAL incident.

On a disposable host with Nginx installed, simulate with `sudo systemctl stop nginx`. Investigate with `systemctl status nginx --no-pager` and `journalctl -u nginx -n 100 --no-pager`. A training root-cause hypothesis is an intentional stop; real cases require evidence from the journal and change history. Resolve with `sudo systemctl start nginx`, then verify `systemctl is-active nginx` and rerun `python monitor.py`. The tool never starts or restarts services automatically.
