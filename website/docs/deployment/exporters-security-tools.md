---
id: exporters-security-tools
title: Exporters and Security CLI Tools
---

# Exporters and security CLI tools

Dockprom-AI uses open-source exporters and CLI tools. Enable only the tools
needed for the host and keep optional scrape targets disabled or expected to be
down until their service is installed.

## Exporter reference

| Domain | Open-source integration | Default endpoint | Project |
| --- | --- | --- | --- |
| Host | Node Exporter | `:9100/metrics` | [prometheus/node_exporter](https://github.com/prometheus/node_exporter) |
| PostgreSQL | PostgreSQL Exporter | `:9187/metrics` | [prometheus-community/postgres_exporter](https://github.com/prometheus-community/postgres_exporter) |
| Ollama | Ollama Exporter | Implementation-specific | [maravexa/ollama-exporter](https://github.com/maravexa/ollama-exporter) |
| NVIDIA GPU | DCGM Exporter | `:9400/metrics` | [NVIDIA/dcgm-exporter](https://github.com/NVIDIA/dcgm-exporter) |
| AMD GPU | AMD SMI Exporter | Implementation-specific | [amd/amd_smi_exporter](https://github.com/amd/amd_smi_exporter) |
| Intel GPU | Device Plugins / GPU telemetry | Implementation-specific | [intel/intel-device-plugins-for-kubernetes](https://github.com/intel/intel-device-plugins-for-kubernetes) |
| OpenTelemetry Collector | Collector internal telemetry | `:8888/metrics` | [open-telemetry/opentelemetry-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) |
| Caddy | Built-in Prometheus metrics | `:2019/metrics` when enabled | [caddyserver/caddy](https://github.com/caddyserver/caddy) |
| Falco | Falco metrics / Falcosidekick | `:8765/metrics` when configured | [falcosecurity/falco](https://github.com/falcosecurity/falco) |

Exporter metric names can change between releases. Pin exporter versions and
validate the dashboard queries against `/metrics` before production rollout.

## NVIDIA DCGM Exporter

The `nvidia` Compose profile provides a placeholder service:

```bash
docker compose --profile nvidia up -d dcgm-exporter
curl --fail http://localhost:9400/metrics
```

This requires a supported NVIDIA driver and NVIDIA Container Toolkit. Do not
enable the profile on non-NVIDIA hosts.

## AMD and Intel GPU alternatives

Do not run DCGM Exporter for AMD or Intel hardware. Use the vendor's open-source
telemetry tool and either expose Prometheus metrics directly or write bounded
metrics into the Node Exporter textfile collector.

## Install Falco

Follow the official Falco package-repository instructions for the host
distribution. After adding the official repository, a Debian/Ubuntu host can
install the CLI and service with:

```bash
sudo apt-get update
sudo apt-get install --yes falco
sudo systemctl enable --now falco
sudo falco --version
```

Configure Falco JSON output for structured Loki ingestion. Enable its metrics
endpoint or deploy the open-source Falcosidekick component when Prometheus event
counters are required. Keep custom rules in version control and validate them:

```bash
sudo falco --validate /etc/falco/falco.yaml
sudo falco --list
```

Falco requires elevated kernel visibility. Review the driver choice and host
security policy before installation.

## Install Trivy CLI

Use the official Aqua Security repository or download a checksummed release.
After configuring the official repository on Debian/Ubuntu:

```bash
sudo apt-get update
sudo apt-get install --yes trivy
trivy --version
```

Run CLI scans without committing reports containing secrets:

```bash
trivy repository --scanners vuln,secret,misconfig .
trivy config compose.yaml
trivy image --severity HIGH,CRITICAL --exit-code 1 grafana/grafana-oss:latest
trivy fs --format json --output /tmp/trivy-results.json .
```

Trivy does not expose a Prometheus endpoint by itself. For dashboards, convert a
small non-sensitive scan summary to Node Exporter textfile metrics, or ship a
redacted JSON summary to Loki. Never publish discovered secret values.

## Operational safety

- Use read-only database roles for Grafana.
- Bind local dashboards and exporters to loopback or the internal Docker
  network unless an authenticated proxy is present.
- Keep source IPs and user identifiers out of metric labels.
- Pin container images by digest for production.
- Validate downloads with upstream checksums or package signatures.
- Review exporter licenses and metric compatibility during upgrades.
