# AWS EC2 Ubuntu 24.04 deployment

These instructions describe a deployment procedure; this repository has not been deployed to AWS. Use an account you administer.

## Instance and access

1. In the EC2 console, launch Ubuntu Server 24.04 LTS. Pick an instance size and encrypted EBS volume appropriate for a lab; enable IMDSv2.
2. Create or select an SSH key pair and store the downloaded private key securely outside Git. Set local permissions to owner-only (`chmod 400 key.pem`).
3. Create a security group with inbound TCP 22 restricted to **My IP**. Add application ports only when needed, restricted to expected source CIDRs. Do not expose SSH to `0.0.0.0/0`.
4. Connect: `ssh -i key.pem ubuntu@EC2_PUBLIC_DNS`.

## Install and configure Sentinel

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip
git clone YOUR_GITHUB_REPOSITORY_URL linux-sentinel
cd linux-sentinel
bash scripts/install.sh
./.venv/bin/python monitor.py
```

For a service account deployment, install at a fixed path and create a restricted account:

```bash
sudo install -d -o root -g root /opt/linux-sentinel
sudo cp -a . /opt/linux-sentinel/
sudo useradd --system --home /nonexistent --shell /usr/sbin/nologin linux-sentinel
sudo chown -R linux-sentinel:linux-sentinel /opt/linux-sentinel
sudo -u linux-sentinel bash /opt/linux-sentinel/scripts/install.sh
```

The restricted account owns its virtual environment and report output. The systemd sandbox grants writes only to the project tree's designated output paths; protect the source tree from changes through host access controls if your threat model requires stronger separation.

Configure optional overrides in `/etc/linux-sentinel.conf` (systemd EnvironmentFile format, no shell code), e.g. `SENTINEL_SERVICES=ssh,nginx`. Keep it readable only by root and the service group if it contains sensitive settings; never put AWS keys there.

Install and start the timer:

```bash
sudo cp systemd/linux-sentinel.service /etc/systemd/system/
sudo cp systemd/linux-sentinel.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now linux-sentinel.timer
systemctl status linux-sentinel.timer
systemctl list-timers linux-sentinel.timer
sudo journalctl -u linux-sentinel.service -n 100 --no-pager
```

Run once immediately with `sudo systemctl start linux-sentinel.service`. Review local reports in `/opt/linux-sentinel/reports/`.

## CloudWatch Agent and alarms

Attach an EC2 instance profile with least-privilege CloudWatch Agent permissions (commonly AWS managed `CloudWatchAgentServerPolicy`, reviewed against your account policy) and Systems Manager access only if using SSM. Never place access keys on the instance. Install the CloudWatch Agent package following the AWS documentation for the instance architecture and Ubuntu package method. Create an agent config that explicitly enables memory and disk plugins and selects the desired filesystem/device and dimensions, then start/enable the agent. Validate its service and the appearance of metrics in the selected CloudWatch namespace before creating alarms.

EC2 publishes basic instance metrics such as CPU and network at the configured monitoring granularity. Memory and filesystem utilization are guest metrics and require the CloudWatch Agent. Configure CloudWatch alarms for EC2 CPU utilization and, after verifying agent publication, memory and disk metrics; choose thresholds, periods, missing-data behavior, and SNS notification targets suitable for the workload. Custom Linux Sentinel metrics are not sent to CloudWatch by this application.

Use the official [CloudWatch Agent installation guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Agent.html), [agent configuration reference](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html), and [EC2 monitoring guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-cloudwatch.html) for current package and metric details.

## Simulate, inspect, clean up

Use the five playbooks in `incidents/` on a disposable instance. These are simulations, never production incident claims. Verify Sentinel timer/service logs and report files.

To stop monitoring: `sudo systemctl disable --now linux-sentinel.timer` and optionally `sudo systemctl stop linux-sentinel.service`. To remove the installation after preserving wanted reports: remove its unit files, `sudo systemctl daemon-reload`, then remove `/opt/linux-sentinel` only after checking the path and data. In AWS, terminate the lab instance when finished and separately review/delete unattached EBS volumes, snapshots, Elastic IPs, alarms, log groups, and SNS resources that you created; billing can continue for retained resources.
