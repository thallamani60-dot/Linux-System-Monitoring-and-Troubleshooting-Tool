#!/usr/bin/env python3
"""Linux Sentinel: safe, read-only system monitoring and report generation."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import subprocess
import sys
import config
from monitors.cpu import cpu_metrics
from monitors.memory import memory_metrics
from monitors.disk import disk_metrics
from monitors.processes import top_processes
from monitors.network import network_metrics
from monitors.services import service_status
from troubleshooting.incident_detector import detect_incidents
from troubleshooting.log_analyzer import analyze_journal
from troubleshooting.recommendations import recommendations

def collect():
    try: uptime = Path('/proc/uptime').read_text().split()[0] + ' seconds'
    except OSError: uptime = 'unknown'
    s = {'timestamp': datetime.now(timezone.utc).isoformat(), 'system': {'hostname': platform.node(), 'os': platform.platform(), 'kernel': platform.release(), 'uptime': uptime}, 'cpu': cpu_metrics(config.CPU_THRESHOLD), 'memory': memory_metrics(config.MEMORY_THRESHOLD), 'disk': disk_metrics(config.DISK_PATH, config.DISK_THRESHOLD), 'processes': top_processes(), 'network': network_metrics(), 'services': [service_status(x) for x in config.SERVICES], 'logs': analyze_journal(config.LOG_LINES)}
    s['incidents'] = detect_incidents(s); s['overall_status'] = 'CRITICAL' if s['incidents'] else 'OK'
    return s

def human_bytes(n):
    for unit in ('B','KiB','MiB','GiB','TiB'):
        if n < 1024 or unit == 'TiB': return f'{n:.1f} {unit}'
        n /= 1024

def render(s):
    c,m,d=s['cpu'],s['memory'],s['disk']
    lines=['='*52,'LINUX SENTINEL HEALTH REPORT','='*52,'',f"Timestamp: {s['timestamp']}",'','SYSTEM',f"Hostname: {s['system']['hostname']}",f"OS: {s['system']['os']}",f"Kernel: {s['system']['kernel']}",f"Uptime: {s['system']['uptime']}",'','CPU',f"Usage: {c['usage_percent']}% (threshold {c['threshold']}%)",f"Cores: {c['cpu_count']}; load: {c['load_average']}",f"Status: {c['status']}",'','MEMORY',f"Usage: {m['usage_percent']}% (threshold {m['threshold']}%)",f"Available: {human_bytes(m['available_bytes'])} / {human_bytes(m['total_bytes'])}",f"Status: {m['status']}",'','DISK',f"Usage: {d['usage_percent']}% on {d['path']} (threshold {d['threshold']}%)",f"Free: {human_bytes(d['free_bytes'])} / {human_bytes(d['total_bytes'])}",f"Status: {d['status']}",'','NETWORK',f"Internet TCP reachability (1.1.1.1:443): {'YES' if s['network']['internet_reachable'] else 'NO'}",'Interfaces: '+(', '.join(f"{i['name']}={'UP' if i['up'] else 'DOWN'}" for i in s['network']['interfaces']) or 'unavailable'),f"Active TCP connections: {len(s['network']['tcp_connections'])}",f"Listening sockets: {len(s['network']['listening_ports'])}",'','SERVICES']
    lines += [f"{x['name']}: {x['status']}" for x in s['services']] or ['No services configured.']
    lines += ['', 'TOP PROCESSES','PID     PROCESS          CPU       MEMORY']
    lines += [f"{p['pid']:<7} {p['name']:<16} {p['cpu_percent']:>5.1f}%    {p['memory_percent']:>5.1f}%" for p in s['processes']] or ['Process list unavailable (check that ps is installed).']
    heavy = [p for p in s['processes'] if p['cpu_percent'] >= 80 or p['memory_percent'] >= 20]
    lines += ['High-use processes: ' + ', '.join(f"{p['name']} (CPU {p['cpu_percent']}%, RAM {p['memory_percent']}%)" for p in heavy)] if heavy else ['No process in the displayed leaders exceeds 80% CPU or 20% RAM.']
    lines += ['', 'INCIDENTS']
    for i in s['incidents']:
        lines += [f"[{i['severity']}] {i['incident_id']} {i['component']}: {i['symptom']}",f"  Metric: {i['detected_metric']} (threshold {i['threshold']})"]
        kind=i['component'] if i['component'] in ('cpu','memory','disk','network') else 'service'
        lines += [f"  Possible cause: {i['root_cause']}", f"  Suggested solution: {i['resolution']}", "  Investigate with:"]
        lines += [f"  {cmd.replace('SERVICE', i['component'])} — {why}" for cmd,why in recommendations(kind)]
    if not s['incidents']: lines.append('No threshold incidents detected.')
    lines += ['', 'LOG ANALYSIS']+[f"[{x['level']}] {x['message']}" for x in s['logs'][:20]]
    if not s['logs']: lines.append('No matching journal entries available.')
    lines += ['',f"OVERALL STATUS: {s['overall_status']}",'='*52,'']
    return '\n'.join(lines)

def save(s, output=None):
    config.REPORT_DIR.mkdir(parents=True,exist_ok=True)
    path=Path(output) if output else config.REPORT_DIR/('health-'+datetime.now().strftime('%Y%m%d-%H%M%S')+'.md')
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(render(s),encoding='utf-8')
    for i in s['incidents']:
        config.INCIDENT_DIR.mkdir(parents=True,exist_ok=True)
        (config.INCIDENT_DIR/(i['incident_id']+'.json')).write_text(json.dumps({**i,'report':str(path)},indent=2),encoding='utf-8')
    return path

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--json',action='store_true'); p.add_argument('--no-report',action='store_true'); p.add_argument('--output')
    a=p.parse_args(argv)
    try: s=collect()
    except (OSError,ValueError,subprocess.SubprocessError) as e: print(f'Collection failed: {e}',file=sys.stderr); return 2
    print(json.dumps(s,indent=2,default=str) if a.json else render(s))
    if not a.no_report: print(f'Report saved: {save(s,a.output)}')
    return 1 if s['overall_status']=='CRITICAL' else 0
if __name__=='__main__': raise SystemExit(main())
