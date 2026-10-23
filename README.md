# Dockprom-AI: AI-Powered Observability Stack

[![License: MIT](https://img.shields.io/github/license/waitesgithub/dockprom-ai)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/waitesgithub/dockprom-ai)](https://github.com/waitesgithub/dockprom-ai/commits)
[![Repo Size](https://img.shields.io/github/repo-size/waitesgithub/dockprom-ai)](https://github.com/waitesgithub/dockprom-ai)

A Docker Compose based monitoring and observability stack for Docker hosts and containers, with an optional AI integration through the Grafana MCP Server. This is a **configuration/deployment project** (YAML-based, no application code): everything is defined in `docker-compose.yaml` and the accompanying configuration files.

Services deployed by `docker-compose.yaml`:
- **Prometheus** - Metrics database
- **Grafana** - Visualization and dashboards
- **Loki** - Log aggregation
- **Tempo** - Distributed tracing
- **OpenTelemetry Collector** - OTLP ingest
- **Node Exporter** - Host metrics
- **AlertManager** - Alert routing and notifications

## Repository Information

- **Fork of:** [cmakkaya/Observability_3_0_AI-PoweredAPM-AI_Stack-Observability_Stack](https://github.com/cmakkaya/Observability_3_0_AI-PoweredAPM-AI_Stack-Observability_Stack)
- **License:** [MIT](LICENSE)
- **Created:** December 16, 2025
- **Language composition:** YAML / configuration files (no compiled or scripted source code)

## Quick Start

### Prerequisites

- Docker Engine >= 1.13
- Docker Compose >= 1.11

### Installation

Clone this repository and start the monitoring stack:

```bash
git clone https://github.com/waitesgithub/dockprom-ai
cd dockprom-ai

docker-compose up -d
```

The configuration files listed in [Configuration Files](#configuration-files) are mounted into the containers, so they must exist next to `docker-compose.yaml` before starting the stack.

## Services

The stack (network `monitoring`) includes the following services:

| Service | URL / Port | Description |
|---------|-----|-------------|
| **Grafana** | `http://<host-ip>:3000` | Visualization and dashboards |
| **Prometheus** | `http://<host-ip>:9090` | Metrics database and queries (90d retention, lifecycle API enabled) |
| **Node Exporter** | `http://<host-ip>:9100` | Host metrics collector (reads `/proc`, `/sys`, `/`) |
| **AlertManager** | `http://<host-ip>:9093` | Alert routing and email notifications |
| **Loki** | `http://<host-ip>:3100` | Log aggregation database |
| **Tempo** | `http://<host-ip>:3200` | Distributed tracing database (HTTP API) |
| **OpenTelemetry Collector** | `4317` (OTLP gRPC), `4318` (OTLP HTTP) | OTLP traces, metrics, and logs ingest |

### OpenTelemetry Collector ports

| Port | Purpose |
|------|---------|
| 4317 | OTLP gRPC receiver |
| 4318 | OTLP HTTP receiver |
| 8889 / 8890 | Prometheus metrics exposed by the collector |
| 13133 | health_check extension |
| 1888 | pprof extension |
| 55679 | zpages extension |

### Volumes

`prometheus_data`, `grafana-data`, `loki-data`, `tempo-data`, `otel-data`.

## Configuration Files

| File | Used by | Purpose |
|------|---------|---------|
| `docker-compose.yaml` | Docker Compose | Service, network, and volume definitions |
| `prometheus.yml` | Prometheus | Scrape configuration |
| `alert-rules.yml` | Prometheus | Alerting rules |
| `alert-config.yaml` | AlertManager | Routes and receivers |
| `alert-email-template.tmpl` | AlertManager | Email notification template (mounted as `/etc/alertmanager/email-template.tmpl`) |
| `tempo.yaml` | Tempo | Tracing backend configuration |
| `loki-config.yaml` | Loki | Log storage configuration |
| `otel-collector-config.yaml` | OpenTelemetry Collector | Receivers, processors, and exporters |

## AI-Powered Observability with Grafana MCP Server

Dockprom-AI integrates the **Grafana MCP Server**, enabling AI agents (Claude, Cursor, etc.) to interact with your observability stack.

### Features

#### Dashboards
- **Search for dashboards** - Find by title, folder, tags, or starred status
- **Get dashboard details** - Retrieve full dashboard JSON or summaries
- **List dashboard versions** - Access saved snapshots and version history
- **Get dashboard properties** - Extract specific parts using JSONPath
- **Create/Update dashboards** - Programmatic dashboard management
- **Patch dashboards** - Apply targeted modifications
- **Get panel queries** - Extract query information from panels

#### Prometheus Querying
- **Query Prometheus** - Execute PromQL queries (instant and range)
- **Query metadata** - Retrieve metric names, label names, and values
- **Histogram percentiles** - Calculate p50, p90, p95, p99 percentiles

#### Loki Querying
- **Query logs** - Run LogQL queries against Loki datasources
- **Query metadata** - Retrieve available labels and their values
- **Query patterns** - Identify common log structures and anomalies

#### Alerting
- **List alert rules** - View alert rules and their statuses
- **Create/Update alert rules** - Programmatically manage alerts
- **Delete alert rules** - Remove rules by UID
- **Manage routing** - Configure notification policies and contact points

#### Incident Management
- **Search incidents** - Find incidents with filters
- **Create incidents** - Programmatically create incident tickets
- **Update incidents** - Modify status, severity, and custom fields
- **Read incident details** - Get full incident information

#### OnCall Management
- **List schedules** - View on-call schedules
- **Get shift details** - Retrieve specific shift information
- **Get current on-call users** - See who's on-call
- **Manage alert groups** - Acknowledge, resolve, or filter alerts

#### Navigation
- **Generate deeplinks** - Create accurate URLs for Grafana resources
- **Dashboard links** - Direct links to dashboards using UIDs
- **Panel links** - Links to specific panels with viewPanel parameters
- **Explore links** - Pre-configured Grafana Explore links

#### Admin Tools
- **List teams** - View all teams
- **List users** - View organization users
- **List roles** - View all Grafana roles
- **Manage permissions** - View and manage resource permissions
- **Get user/org info** - Current identity and capabilities

## AI Observability: OTEL + Loki + Tempo

The stack provides an observability backend for AI/LLM applications:

- **Traces** - Apps send OTLP traces to the OTel Collector → stored in Tempo → viewed in Grafana
- **Logs** - Logs stored in Loki → viewed in Grafana
- **Metrics** - OTLP metrics sent to the OTel Collector → exposed for Prometheus

### Instrument Your Application

For deeper observability, instrument your app with OpenTelemetry.

**For apps running on the host:**

```bash
export OTEL_SERVICE_NAME="my-app"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://127.0.0.1:4318"
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
```

**For apps in Docker (same `monitoring` network):**

```bash
OTEL_SERVICE_NAME=my-app
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
```

## Setup Grafana

Navigate to `http://<host-ip>:3000` and login with the Grafana defaults (**admin / admin**, you will be prompted to change the password).

To change credentials, add environment variables to the `grafana` service in `docker-compose.yaml`, for example:

```yaml
grafana:
  image: grafana/grafana:latest
  environment:
    - GF_SECURITY_ADMIN_USER=admin
    - GF_SECURITY_ADMIN_PASSWORD=changeme
    - GF_USERS_ALLOW_SIGN_UP=false
```

### Datasources

Datasources are not provisioned automatically. Add them in Grafana (Connections → Data sources) using the container names on the `monitoring` network:

- **Prometheus** - `http://prometheus:9090`
- **Loki** - `http://loki:3100`
- **Tempo** - `http://tempo:3200`

## Define Alerts

Prometheus loads alerting rules from `alert-rules.yml`. Example rule groups:

### Monitoring Services Alerts

Alert if monitoring targets (e.g. node-exporter) are down:

```yaml
- alert: monitor_service_down
  expr: up == 0
  for: 30s
  labels:
    severity: critical
  annotations:
    summary: "Monitor service non-operational"
    description: "Service {{ $labels.instance }} is down."
```

### Docker Host Alerts

High CPU load:

```yaml
- alert: high_cpu_load
  expr: node_load1 > 1.5
  for: 30s
  labels:
    severity: warning
  annotations:
    summary: "Server under high load"
    description: "Docker host is under high load, avg load 1m: {{ $value }}"
```

High memory usage:

```yaml
- alert: high_memory_load
  expr: (sum(node_memory_MemTotal_bytes) - sum(node_memory_MemFree_bytes + node_memory_Buffers_bytes + node_memory_Cached_bytes)) / sum(node_memory_MemTotal_bytes) * 100 > 85
  for: 30s
  labels:
    severity: warning
  annotations:
    summary: "Server memory is almost full"
    description: "Docker host memory usage: {{ humanize $value }}%"
```

High storage usage:

```yaml
- alert: high_storage_load
  expr: (node_filesystem_size_bytes{fstype="aufs"} - node_filesystem_free_bytes{fstype="aufs"}) / node_filesystem_size_bytes{fstype="aufs"} * 100 > 85
  for: 30s
  labels:
    severity: warning
  annotations:
    summary: "Server storage is almost full"
    description: "Docker host storage usage: {{ humanize $value }}%"
```

### Docker Containers Alerts

Container down:

```yaml
- alert: container_down
  expr: absent(container_memory_usage_bytes{name="service-name"})
  for: 30s
  labels:
    severity: critical
  annotations:
    summary: "Container down"
    description: "Container is down for more than 30 seconds."
```

Container high CPU:

```yaml
- alert: container_high_cpu
  expr: sum(rate(container_cpu_usage_seconds_total{name="service"}[1m])) / count(node_cpu_seconds_total{mode="system"}) * 100 > 10
  for: 30s
  labels:
    severity: warning
  annotations:
    summary: "Container high CPU"
    description: "Container CPU usage: {{ humanize $value }}%"
```

Container high memory:

```yaml
- alert: container_high_memory
  expr: sum(container_memory_usage_bytes{name="service"}) > 1200000000
  for: 30s
  labels:
    severity: warning
  annotations:
    summary: "Container high memory"
    description: "Container memory consumption: {{ humanize $value }}"
```

## Setup Alerting

AlertManager handles alerts sent by Prometheus and can route them to:
- Email
- Slack
- PagerDuty
- Webhooks
- And many more

Receivers are configured in `alert-config.yaml`; the email template is `alert-email-template.tmpl`.

### Slack Integration

Create a Slack incoming webhook, then configure AlertManager:

```yaml
route:
  receiver: 'slack'

receivers:
  - name: 'slack'
    slack_configs:
      - send_resolved: true
        text: "{{ .CommonAnnotations.description }}"
        username: 'Prometheus'
        channel: '#alerts'
        api_url: 'https://hooks.slack.com/services/<webhook-id>'
```

### Reload Alert Rules

Prometheus runs with `--web.enable-lifecycle`, so rules can be reloaded without restarting:

```bash
curl -X POST http://<host-ip>:9090/-/reload
```

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

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the [MIT License](LICENSE). Grafana, Prometheus, and other components are licensed under their respective licenses.

## Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/)
- [Tempo Documentation](https://grafana.com/docs/tempo/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Grafana MCP Server](https://github.com/grafana/mcp-grafana)
