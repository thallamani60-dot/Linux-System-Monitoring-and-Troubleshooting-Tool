#!/usr/bin/env bash
set -u
if [[ $# -ne 1 || ! $1 =~ ^[A-Za-z0-9_.@:-]+$ ]]; then echo "Usage: $0 SERVICE" >&2; exit 2; fi
service=$1
raw=$(systemctl is-active "$service" 2>/dev/null || true)
enabled=$(systemctl is-enabled "$service" 2>/dev/null || true)
[[ $raw == active ]] && status=ACTIVE || { [[ $raw == failed ]] && status=FAILED || status=INACTIVE; }
[[ $enabled == enabled ]] && boot=YES || boot=NO
printf 'Service: %s\nStatus: %s\nEnabled: %s\n' "$service" "$status" "$boot"
echo 'Recent errors:'
journalctl -u "$service" -p err -n 20 --no-pager 2>/dev/null || echo 'Journal unavailable to this user.'
