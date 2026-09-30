#!/usr/bin/env bash
set -u
section() { printf '\n==== %s ====\n' "$1"; }
section ADDRESSES; ip address show 2>/dev/null || echo 'ip command unavailable'
section ROUTES; ip route show 2>/dev/null || true
section DNS; getent hosts example.com || echo 'DNS lookup failed'
section INTERNET; if ping -c 3 -W 2 1.1.1.1; then :; else echo 'ICMP failed or filtered; this alone does not prove TCP connectivity is down.'; fi
section LISTENING_PORTS; ss -tulnp 2>/dev/null || ss -tuln
