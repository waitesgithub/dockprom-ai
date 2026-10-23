# Dockprom-AI: AI-Powered Observability Stack

[![License: MIT](https://img.shields.io/github/license/waitesgithub/dockprom-ai)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/waitesgithub/dockprom-ai)](https://github.com/waitesgithub/dockprom-ai/commits)

A Docker Compose based monitoring and observability stack for Docker hosts and containers. This is a **configuration/deployment project** (YAML and JSON, no application code): everything is defined in `docker-compose.yaml` and the accompanying configuration files.

- **Fork of:** [cmakkaya/Observability_3_0_AI-PoweredAPM-AI_Stack-Observability_Stack](https://github.com/cmakkaya/Observability_3_0_AI-PoweredAPM-AI_Stack-Observability_Stack)
- **License:** [MIT](LICENSE)
- **Created:** December 16, 2025
- **Container dashboards:** from [Lifailon/logporter](https://github.com/Lifailon/logporter) (MIT)

## Quick Start

Prerequisites: Docker Engine and Docker Compose.

```bash
git clone https://github.com/waitesgithub/dockprom-ai
cd dockprom-ai
docker-compose up -d
```

The files listed under [Configuration Files](#configuration-files) are mounted into the containers and must exist next to `docker-compose.yaml`.

## Services

All services run on the `monitoring` Docker network.

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| **Prometheus** | `prom/prometheus:v3.15.1` | 9090 | Metrics database (90d retention, lifecycle API enabled) |
| **Grafana** | `grafana/grafana:13.2.4` | 3000 | Dashboards; datasources and dashboards are provisioned |
| **Node Exporter** | `prom/node-exporter:v1.12.1` | 9100 | Host metrics |
| **AlertManager** | `prom/alertmanager:v0.34.1` | 9093 | Alert routing and email notifications |
| **Loki** | `grafana/loki:latest` | 3100 | Log aggregation |
| **Tempo** | `grafana/tempo:latest` | 3200 | Distributed tracing (HTTP API) |
| **OpenTelemetry Collector** | `otel/opentelemetry-collector-contrib:0.163.0` | 4317 (gRPC), 4318 (HTTP) | OTLP ingest |
| **logporter** | `lifailon/logporter:latest` | 9333 | Docker container metrics for Prometheus; ships container logs to Loki |

OpenTelemetry Collector also exposes 8889/8890 (Prometheus metrics), 13133 (health check), 1888 (pprof) and 55679 (zpages).

Volumes: `prometheus_data`, `grafana-data`, `loki-data`, `tempo-data`, `otel-data`.

## Configuration Files

| File | Used by | Purpose |
|------|---------|---------|
| `docker-compose.yaml` | Docker Compose | Services, network and volumes |
| `prometheus.yml` | Prometheus | Scrape jobs (prometheus, node-exporter, otel-collector, logporter) and AlertManager target |
| `alert-rules.yml` | Prometheus | Docker container alert rules (from logporter) |
| `grafana/provider.yaml` | Grafana | Dashboard provisioning (folder "Docker") |
| `grafana/datasources.yaml` | Grafana | Prometheus and Loki datasources |
| `grafana/dashboards/logs.json` | Grafana | Container logs dashboard (Loki) |
| `grafana/dashboards/metrics.json` | Grafana | Container metrics dashboard (Prometheus) |
| `alert-config.yaml` | AlertManager | Routes and receivers |
| `alert-email-template.tmpl` | AlertManager | Email template (mounted as `/etc/alertmanager/email-template.tmpl`) |
| `tempo.yaml` | Tempo | Tracing backend configuration |
| `loki-config.yaml` | Loki | Log storage configuration |
| `otel-collector-config.yaml` | OpenTelemetry Collector | Receivers, processors and exporters |

> **Note:** `alert-config.yaml`, `alert-email-template.tmpl`, `tempo.yaml`, `loki-config.yaml` and `otel-collector-config.yaml` are referenced by `docker-compose.yaml` but are not yet included in this repository.

## Grafana

Open `http://<host-ip>:3000` (default login `admin` / `admin`; change it by adding `GF_SECURITY_ADMIN_USER` / `GF_SECURITY_ADMIN_PASSWORD` to the `grafana` service environment).

Provisioned datasources: **prometheus** (`http://prometheus:9090`, default) and **loki** (`http://loki:3100`). Dashboards in the **Docker** folder:

- **metrics** - per-container CPU, memory, network, disk I/O, volumes and image update status (via logporter metrics)
- **logs** - container logs from Loki

## Alerting

Prometheus loads the rules in `alert-rules.yml` (container CPU, memory, network, disk I/O, volume and image size, and container down/restart alerts) and sends them to AlertManager at `alertmanager:9093`. Configure receivers in `alert-config.yaml`.

Reload Prometheus configuration and rules without a restart:

```bash
curl -X POST http://<host-ip>:9090/-/reload
```

## Sending OpenTelemetry Data

Apps on the host:

```bash
export OTEL_SERVICE_NAME="my-app"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://127.0.0.1:4318"
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
```

Apps in Docker (same `monitoring` network): use `OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318`.

## Grafana MCP Server Configuration

### Quick Start with Claude Desktop

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "grafana": {
      "command": "uvx",
      "args": ["mcp-grafana"],
      "env": {
        "GRAFANA_URL": "http://localhost:3000",
        "GRAFANA_SERVICE_ACCOUNT_TOKEN": "<your service account token>"
      }
    }
  }
}
```

For Grafana Cloud, replace `GRAFANA_URL` with your instance URL.

### Requirements

- **Grafana version 9.0 or later**
- Valid Grafana API token or service account

### Tools Reference

The MCP server provides 100+ tools across multiple categories:

| Category | Tools | Example |
|----------|-------|---------|
| **Dashboard** | search, get, update, patch, create | Manage dashboards programmatically |
| **Prometheus** | query, metadata, histogram percentiles | PromQL queries and exploration |
| **Loki** | query logs, metadata, patterns | LogQL queries and log analysis |
| **Alerting** | read/write rules, manage routing | Alert rule management |
| **Incident** | search, create, update, read | Incident management |
| **OnCall** | schedules, shifts, teams, alerts | On-call management |
| **Navigation** | deeplinks | Generate accurate Grafana links |
| **Admin** | teams, users, roles, permissions | Administration tools |

See the full tools list in the [Grafana MCP Server documentation](https://github.com/grafana/mcp-grafana#tools).

## RBAC Permissions

Each tool requires specific RBAC permissions. When creating a service account, ensure it has the necessary permissions for your use case.

**Common Scope Patterns:**

- **Broad access:** `datasources:*`, `dashboards:*`, `folders:*`
- **Limited access:** `datasources:uid:prometheus-uid`, `dashboards:uid:abc123`

**Example full MCP access:**

```
datasources:* (datasources:read, datasources:query)
dashboards:* (dashboards:read, dashboards:create, dashboards:write)
folders:* (for dashboard creation and alert rules)
teams:* (teams:read)
global.users:* (users:read)
```

For more details, see the [Grafana RBAC documentation](https://grafana.com/docs/grafana/latest/administration/roles-and-permissions/access-control/).

## Troubleshooting

### Storage and Filesystem Issues

For storage metrics and free storage graphs, specify the correct filesystem type in your queries. Find your system's filesystem type:

```bash
# In Prometheus
node_filesystem_free_bytes

# Or in your dashboard JSON
"expr": "sum(node_filesystem_free_bytes{fstype=\"btrfs\"})"
```

### Grafana File Permissions

If upgrading Grafana to v5.2.2+, the user ID changed from 104 to 472.

**Solution:** Change ownership in the container:

```bash
docker-compose down

# Modify docker-compose.yaml to include 'user: root' for grafana service
docker-compose up -d

docker exec -it --user root grafana bash
# Inside container:
chown -R grafana:grafana /var/lib/grafana
chown -R grafana:grafana /usr/share/grafana
```

## Contributing

Contributions are welcome! Please submit pull requests or open issues.

## License

This project is licensed under the [MIT License](LICENSE). Bundled components (Grafana, Prometheus, logporter dashboards, etc.) are licensed under their respective licenses.

## Resources

- [Prometheus](https://prometheus.io/docs/) · [Grafana](https://grafana.com/docs/) · [Loki](https://grafana.com/docs/loki/) · [Tempo](https://grafana.com/docs/tempo/) · [OpenTelemetry](https://opentelemetry.io/docs/)
- [logporter](https://github.com/Lifailon/logporter)
- [Grafana MCP Server](https://github.com/grafana/mcp-grafana)
