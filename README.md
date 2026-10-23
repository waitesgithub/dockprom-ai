# Dockprom-AI: AI-Powered Observability Stack

[![Unit Tests](https://github.com/grafana/mcp-grafana/actions/workflows/unit.yml/badge.svg)](https://github.com/grafana/mcp-grafana/actions/workflows/unit.yml)
[![Integration Tests](https://github.com/grafana/mcp-grafana/actions/workflows/integration.yml/badge.svg)](https://github.com/grafana/mcp-grafana/actions/workflows/integration.yml)
[![E2E Tests](https://github.com/grafana/mcp-grafana/actions/workflows/e2e.yml/badge.svg)](https://github.com/grafana/mcp-grafana/actions/workflows/e2e.yml)

A comprehensive monitoring solution for Docker hosts and containers with AI-powered observability, combining:
- **Prometheus** - Metrics database
- **Grafana** - Visualization and dashboards
- **Loki** - Log aggregation
- **Tempo** - Distributed tracing
- **OpenTelemetry Collector** - OTLP ingest
- **cAdvisor** - Container metrics
- **NodeExporter** - Host metrics
- **Grafana MCP Server** - AI-powered Grafana integration
- **Ollama Gateway** - LLM inference with observability
- **AlertManager** - Alert management

## Quick Start

### Prerequisites

- Docker Engine >= 1.13
- Docker Compose >= 1.11

### Installation

Clone this repository and start the monitoring stack:

```bash
git clone https://github.com/waitesgithub/dockprom-ai
cd dockprom-ai

ADMIN_USER='admin' ADMIN_PASSWORD='admin' ADMIN_PASSWORD_HASH='$2a$14$1l.IozJx7xQRVmlkEQ32OeEEfP5mRxTpbDTCTcXRqn19gXD8YK1pO' docker-compose up -d
```

**Note:** Caddy v2 requires passwords as hash values. The above hash corresponds to password 'admin'. To generate a new hash:

```bash
docker run --rm caddy caddy hash-password --plaintext 'YOUR_PASSWORD'
```

## Services

The stack includes the following services:

| Service | URL | Description |
|---------|-----|-------------|
| **Grafana** | `http://<host-ip>:3000` | Visualization and dashboards (admin/admin) |
| **Prometheus** | `http://<host-ip>:9090` | Metrics database and queries |
| **Prometheus Pushgateway** | `http://<host-ip>:9091` | Push acceptor for ephemeral/batch jobs |
| **AlertManager** | `http://<host-ip>:9093` | Alert management and routing |
| **Loki** | `http://<host-ip>:3100` | Log aggregation database |
| **Tempo** | `http://<host-ip>:3200` | Distributed tracing database |
| **OpenTelemetry Collector** | `http://<host-ip>:4318` (HTTP) | OTLP metrics, logs, and traces ingest |
| **OpenTelemetry Collector** | `http://<host-ip>:4317` (gRPC) | OTLP ingest |
| **Ollama Gateway** | `http://<host-ip>:11435` | HTTP proxy with tracing/metrics for Ollama |
| **NodeExporter** | - | Host metrics collector |
| **cAdvisor** | - | Container metrics collector |
| **Alloy** | - | Docker logs collector → Loki |
| **Caddy** | - | Reverse proxy with basic auth |

## Pinned Versions

All image tags are pinned to exact versions from official GitHub releases (no `latest` tags), so deployments are reproducible. Each image line in `compose.yml` has a comment linking to its release.

| Service | Image | Version | Released | Releases |
|---------|-------|---------|----------|----------|
| Prometheus | `prom/prometheus` | v3.15.1 | Oct 21, 2026 | [link](https://github.com/prometheus/prometheus/releases) |
| Grafana | `grafana/grafana` | 13.2.4 | Oct 13, 2026 | [link](https://github.com/grafana/grafana/releases) |
| Loki | `grafana/loki` | 3.7.9 | Oct 20, 2026 | [link](https://github.com/grafana/loki/releases) |
| Tempo | `grafana/tempo` | 3.1.1 | - | [link](https://github.com/grafana/tempo/releases) |
| OpenTelemetry Collector Contrib | `otel/opentelemetry-collector-contrib` | 0.163.0 | Oct 14, 2026 | [link](https://github.com/open-telemetry/opentelemetry-collector-releases/releases) |
| AlertManager | `prom/alertmanager` | v0.34.1 | Sep 17, 2026 | [link](https://github.com/prometheus/alertmanager/releases) |
| Node Exporter | `prom/node-exporter` | v1.12.1 | Jul 14, 2026 | [link](https://github.com/prometheus/node_exporter/releases) |
| Pushgateway | `prom/pushgateway` | v1.11.4 | Oct 8, 2026 | [link](https://github.com/prometheus/pushgateway/releases) |
| Logporter | `lifailon/logporter` | v1.2.0 | Jul 31, 2026 | [link](https://github.com/Lifailon/logporter/releases) |
| Ollama | `ollama/ollama` | 0.40.9 | - | [link](https://github.com/ollama/ollama/releases) |
| Caddy | `caddy` | 2.11.7 | Oct 3, 2026 | [link](https://github.com/caddyserver/caddy/releases) |
| mcp-grafana | `grafana/mcp-grafana` | 2.1.1 | - | [link](https://github.com/grafana/mcp-grafana/releases) |

Pushgateway, Logporter, Ollama, Caddy and mcp-grafana are not currently defined in `compose.yml`; use the versions above when adding them.

### Major version upgrades

- **Loki** v2 → v3
- **Tempo** v2 → v3
- **Logporter** v0 → v1

Review the upstream release notes and migrate configs (`loki-config.yaml`, `tempo.yaml`) before upgrading.

### Versioning strategy and updating

Tags follow upstream semantic versioning exactly as published (some images omit the `v` prefix). To update a service:

1. Check the releases page linked above and read the changelog.
2. Edit the `image:` tag and its release comment in `compose.yml`, and update this table.
3. Run `docker-compose pull <service> && docker-compose up -d <service>`.

### Compatibility notes

- Grafana MCP Server requires Grafana 9.0 or later.
- Loki 3.x and Tempo 3.x have configuration changes from 2.x; validate configs before upgrading.
- Upgrade the Grafana stack components together and test dashboards and datasources afterwards.

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

## AI Observability: Ollama + OTEL + Loki + Tempo

Dockprom-AI extends the stack with a **drop-in observability bundle** for AI/LLM applications:

- **Traces** - Apps send OTLP traces → stored in Tempo → viewed in Grafana
- **Logs** - Docker logs collected by Alloy → stored in Loki → viewed in Grafana
- **Metrics** - OTLP metrics sent to OTel Collector → exposed for Prometheus
- **Ollama Gateway** - Envoy proxy with automatic request tracing and metrics

### Make Host Ollama Reachable

The gateway runs in Docker and forwards to `host.docker.internal:11434`. On Linux, ensure Ollama listens on a non-loopback interface:

```bash
export OLLAMA_HOST=0.0.0.0:11434
ollama serve
```

### Use the Ollama Gateway

Point your applications to:

```
http://<host-ip>:11435
```

This automatically provides:
- **Tempo traces** for each request
- **Prometheus metrics** for RPS, latency, and errors
- **Loki logs** for gateway and access logs

### Instrument Your Application

For deeper observability, instrument your app with OpenTelemetry.

**For apps running on the host:**

```bash
export OTEL_SERVICE_NAME="my-app"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://127.0.0.1:4318"
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
```

**For apps in Docker (same `monitor-net` network):**

```bash
OTEL_SERVICE_NAME=my-app
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
```

## Setup Grafana

Navigate to `http://<host-ip>:3000` and login with **admin / admin**. 

**Change credentials by modifying your compose file or config:**

```yaml
grafana:
  image: grafana/grafana:13.2.4
  env_file:
    - config
```

**Config file format:**

```yaml
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=changeme
GF_USERS_ALLOW_SIGN_UP=false
```

### Pre-configured Datasources

Grafana includes a pre-configured Prometheus datasource:

- **Name:** Prometheus
- **Type:** Prometheus
- **URL:** `http://prometheus:9090`
- **Access:** proxy

Additional datasources:
- **Loki** - `http://loki:3100`
- **Tempo** - `http://tempo:3200`

### Pre-configured Dashboards

**Docker Host Dashboard**
- Server uptime, CPU, and memory metrics
- System load, processes, and I/O
- CPU usage by mode
- Memory and storage usage
- Network metrics by device
- Swap usage and activity

**Docker Containers Dashboard**
- Total containers CPU, memory, and storage
- Running containers and system load
- Container CPU usage
- Container memory usage
- Container network I/O

**Monitor Services Dashboard**
- Prometheus uptime and storage metrics
- Prometheus ingestion rate and scrape metrics
- Alert tracking and performance graphs

## Define Alerts

Three alert groups are configured in [prometheus/alert.rules](prometheus/alert.rules):

### Monitoring Services Alerts

Alert if monitoring targets (node-exporter, cAdvisor) are down:

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

Configure receivers in [alertmanager/config.yml](alertmanager/config.yml).

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

Reload alert rules without restarting:

```bash
curl -X POST http://admin:admin@<host-ip>:9090/-/reload
```

## Pushing Metrics to Pushgateway

Push metrics from batch jobs or services:

```bash
echo "some_metric 3.14" | curl --data-binary @- http://user:password@localhost:9091/metrics/job/some_job
```

Replace `user:password` with your admin credentials.

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

# Modify compose.yml to include 'user: root' for grafana service
docker-compose up -d

docker exec -it --user root grafana bash
# Inside container:
chown -R grafana:grafana /var/lib/grafana
chown -R grafana:grafana /usr/share/grafana
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is provided as-is. Grafana components are licensed under their respective licenses.

## Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/)
- [Tempo Documentation](https://grafana.com/docs/tempo/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Grafana MCP Server](https://github.com/grafana/mcp-grafana)
