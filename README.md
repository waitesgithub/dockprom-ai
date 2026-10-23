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
- **Logporter** - Docker metrics, container logs, and image update checks
- **Node Exporter** - Host metrics
- **Grafana MCP Server** - AI-powered Grafana integration
- **AlertManager** - Alert management

## Quick Start

### Prerequisites

- Docker Engine with Docker Compose v2

### Installation

Clone this repository and start the monitoring stack:

```bash
git clone https://github.com/waitesgithub/dockprom-ai
cd dockprom-ai

export MCP_GRAFANA_SERVER_TOKEN="$(openssl rand -hex 32)"
docker compose --env-file config up -d
```

The committed `config` file is for local evaluation. Change the default Grafana
and Logporter passwords before exposing the stack beyond localhost. Create a
Grafana service account after the first start, then provide its token through
the `GRAFANA_SERVICE_ACCOUNT_TOKEN` environment variable and restart
`mcp-grafana`. Keep credentials out of the tracked `config` file and keep the
stack on localhost unless you configure appropriate network controls.

## Services

The stack includes the following services:

| Service | URL | Description |
|---------|-----|-------------|
| **Grafana** | `http://localhost:3000` | Visualization and dashboards (admin/admin by default) |
| **Prometheus** | `http://localhost:9090` | Metrics database and queries |
| **Prometheus Pushgateway** | `http://localhost:9091` | Push acceptor for ephemeral/batch jobs |
| **AlertManager** | `http://localhost:9093` | Alert management and routing |
| **Loki** | `http://localhost:3100` | Log aggregation database |
| **Tempo** | `http://localhost:3200` | Distributed tracing database |
| **Logporter** | `http://localhost:9333` | Docker metrics, container log dashboard, and image update checks (admin/admin by default) |
| **Grafana MCP** | `http://localhost:8000` | Grafana MCP HTTP endpoint |
| **OpenTelemetry Collector** | `http://localhost:4318` (HTTP) | OTLP metrics, logs, and traces ingest |
| **OpenTelemetry Collector** | `http://localhost:4317` (gRPC) | OTLP ingest |
| **NodeExporter** | - | Host metrics collector |
| **Caddy** | `http://localhost:8080` | Reverse proxy to Grafana |

The stack's published ports bind to localhost. `docker-compose.exporters.yml`
provides a separate host-networked exporter setup; adjust Prometheus scrape
targets to the host addresses when using it instead of the default services.

## Logporter

Logporter replaces cAdvisor for container metrics and also collects Docker logs
for Loki, reports image-update status, and serves its own dashboard at
`http://localhost:9333`. Its Docker dashboard can be imported into Grafana with
dashboard ID **23848**; the Logporter web dashboard is available directly.

The Compose setup enables Docker volume metrics (30-minute cache), checks for
image updates every 30 minutes, and pushes logs to Loki every 5 seconds or
after 1,000 lines. The Logporter UI defaults to `admin` / `admin`; change
`LOGPORTER_DASHBOARD_USERNAME` and `LOGPORTER_DASHBOARD_PASSWORD` in `config`
before exposing it to other hosts.

Logporter accesses the Docker API through a network-isolated socket proxy
configured for read operations. Mounting the Docker socket still grants access
to sensitive host metadata, so keep the proxy and monitoring network private.
Logporter is designed as a lightweight alternative to cAdvisor; the resource
difference depends on host and container workload rather than being a fixed
performance guarantee.

| Capability | cAdvisor | Logporter |
|------------|----------|-----------|
| Container metrics | Yes | Yes |
| Docker log forwarding to Loki | No | Yes |
| Image update status | No | Yes |
| Dashboard | External Grafana dashboard | Web UI on port 9333 and Grafana dashboard 23848 |
| Resource comparison | Baseline | The upstream publishes a 24-hour comparison for 25 containers; results vary by workload ([benchmark](https://github.com/Lifailon/logporter#performance)) |

## Image versions

| Component | Image |
|-----------|-------|
| Prometheus | `prom/prometheus:v2.47.0` |
| Grafana | `grafana/grafana:13.2.4` |
| AlertManager | `prom/alertmanager:v0.34.1` |
| Node Exporter | `prom/node-exporter:v1.6.1` |
| Logporter | `lifailon/logporter:latest` |
| Loki | `grafana/loki:latest` |
| Grafana MCP | Built locally from `grafana/mcp-grafana` at upstream `v2.1.1` |

## AI-Powered Observability with Grafana MCP Server

Dockprom-AI builds and runs the Go-based **Grafana MCP Server** from the
upstream `v2.1.1` release, enabling MCP clients (Claude, Cursor, etc.) to
interact with Grafana. The service listens on `http://localhost:8000`; provide
a Grafana service-account token through the environment before using it.

Create a service account in Grafana and grant only the permissions needed by
your MCP client. Set `GRAFANA_SERVICE_ACCOUNT_TOKEN` in the environment.
The separate `MCP_GRAFANA_SERVER_TOKEN` protects the HTTP endpoint; MCP clients
must send it as a bearer token. The server only accepts localhost Host headers.
After setting the service-account token, restart the MCP service with
`docker compose --env-file config up -d mcp-grafana`.

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

## AI Observability: OpenTelemetry + Loki + Tempo

Applications can send telemetry to the OpenTelemetry Collector and view it in
Grafana:

- **Traces** - Apps send OTLP traces → stored in Tempo → viewed in Grafana
- **Logs** - Apps send OTLP logs → stored in Loki → viewed in Grafana; Logporter also sends Docker logs
- **Metrics** - OTLP metrics sent to OTel Collector → exposed for Prometheus

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
  image: grafana/grafana:latest
  env_file:
    - config
```

**Config file format** (`config`):

```dotenv
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

### Dashboards

The `Dockprom AI` dashboard is provisioned from
`grafana/dashboards/dockprom-ai.json`. Import Logporter's Grafana dashboard
with dashboard ID **23848** to view its Docker metrics.

## Define Alerts

Alert groups are configured in [prometheus/alert.rules](prometheus/alert.rules):

### Monitoring Services Alerts

Alert if monitoring targets (node-exporter, Logporter) are down:

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

Container memory alert:

```yaml
- alert: container_high_memory
  expr: docker_memory_usage > 1200000000
  for: 30s
  labels:
    severity: warning
  annotations:
    summary: "Container high memory"
    description: "Container memory consumption: {{ humanize $value }} bytes."
```

Container high CPU:

```yaml
- alert: container_high_cpu
  expr: sum(rate(docker_cpu_usage_total[1m])) * 100 > 10
  for: 30s
  labels:
    severity: warning
  annotations:
    summary: "Container CPU usage is high"
    description: "Container CPU usage: {{ humanize $value }}%"
```

Container image update check:

```yaml
- alert: container_image_update
  expr: docker_image_update == 1
  for: 30s
  labels:
    severity: warning
  annotations:
    summary: "Docker image update available"
    description: "An update is available for {{ $labels.image }}."
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

# Modify docker-compose.yml to include 'user: root' for grafana service
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
