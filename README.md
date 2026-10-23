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
- **Logporter** - Container metrics and Docker log collection
- **NodeExporter** - Host metrics
- **Grafana MCP Server** - AI-powered Grafana integration
- **Caddy** - HTTPS reverse proxy for Grafana
- **AlertManager** - Alert management

## Quick Start

### Prerequisites

- Docker Engine with the Docker Compose v2 plugin

### Installation

Clone this repository and start the monitoring stack:

```bash
git clone https://github.com/waitesgithub/dockprom-ai
cd dockprom-ai

export GF_SECURITY_ADMIN_PASSWORD='choose-a-strong-password'
docker compose up -d
```

Grafana's admin password is required at startup and is not stored in the repository. Grafana is available on port `3000`; Caddy serves it at `https://localhost` using its local certificate.

The MCP server is optional. Create a Grafana service-account token, then start it with:

```bash
export GRAFANA_SERVICE_ACCOUNT_TOKEN='your-service-account-token'
docker compose --profile mcp up -d --build mcp-grafana
```

The MCP endpoint is bound to `127.0.0.1:8000` and uses the Go-based Grafana MCP server.

## Services

The stack includes the following services:

| Service | URL | Description |
|---------|-----|-------------|
| **Grafana** | `http://<host-ip>:3000` | Visualization and dashboards |
| **Prometheus** | `http://<host-ip>:9090` | Metrics database and queries |
| **Prometheus Pushgateway** | `http://<host-ip>:9091` | Push acceptor for ephemeral/batch jobs |
| **AlertManager** | `http://<host-ip>:9093` | Alert management and routing |
| **Loki** | `http://<host-ip>:3100` | Log aggregation database |
| **Tempo** | `http://<host-ip>:3200` | Distributed tracing database |
| **OpenTelemetry Collector** | `http://<host-ip>:4318` (HTTP) | OTLP metrics and traces ingest |
| **OpenTelemetry Collector** | `http://<host-ip>:4317` (gRPC) | OTLP ingest |
| **NodeExporter** | - | Host metrics collector |
| **Logporter** | `http://<host-ip>:9333` | Container metrics and Docker log collection |
| **Caddy** | `https://localhost` | HTTPS reverse proxy to Grafana |
| **Grafana MCP Server** | `http://127.0.0.1:8000` | Optional AI integration (MCP profile) |

## Image versions

The main stack pins the requested upstream releases:

| Service | Image |
|---------|-------|
| Prometheus | `prom/prometheus:v3.15.1` |
| Grafana | `grafana/grafana:13.2.4` |
| Caddy | `caddy:v2.11.7` |
| AlertManager | `prom/alertmanager:0.34.1` |
| NodeExporter | `prom/node-exporter:v1.12.1` |
| Pushgateway | `prom/pushgateway:v1.11.4` |
| Logporter | `lifailon/logporter:latest` |
| Loki | `grafana/loki:2.9.3` |

Tempo and the OpenTelemetry Collector retain their existing `latest` tags because no replacement versions were specified.

`docker-compose.exporters.yml` is an optional exporters-only deployment and expects an existing `monitoring` Docker network. Do not run it alongside the main Compose stack, which already includes the same exporters and publishes those ports.

## Why Logporter instead of cAdvisor?

Dockprom uses Logporter instead of cAdvisor. cAdvisor v0.60.6 is published from `ghcr.io/google/cadvisor`, rather than the older `gcr.io/cadvisor/cadvisor` repository; replacing cAdvisor avoids coupling this stack to that image-host migration. Logporter exposes Docker container and volume metrics on port `9333`, provides a built-in dashboard, and can forward Docker logs to Loki using `LOKI_URL=http://loki:3100`.

The Logporter exporter gathers container data through the Docker API and reports metrics such as container CPU time, memory usage, network and block I/O, process count, image size, and volume size. It requires access to the Docker socket; the Compose mount is read-only, but Docker socket access should still be treated as privileged. For more restricted deployments, use a separately secured Docker socket proxy. See the [Logporter performance comparison](https://github.com/Lifailon/logporter#performance) for upstream measurements; this repository does not claim a fixed resource reduction.

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

## OpenTelemetry, Loki, and Tempo

The stack accepts OpenTelemetry metrics and traces and collects Docker container logs:

- **Traces** - Apps send OTLP traces → stored in Tempo → viewed in Grafana
- **Logs** - Logporter collects Docker logs → stored in Loki → viewed in Grafana
- **Metrics** - OTLP metrics sent to OTel Collector → exposed for Prometheus

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

Navigate to `http://<host-ip>:3000` and sign in with the admin user and password provided at startup. The root `config` file contains non-secret Grafana settings; set `GF_SECURITY_ADMIN_PASSWORD` in your shell or an untracked environment file.

`config` uses Docker environment-file syntax:

```text
GF_SECURITY_ADMIN_USER=admin
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

Dashboards in `grafana/dashboards/` are provisioned on startup and use Grafana's current `timeseries` and `stat` visualizations, Prometheus datasource UIDs, and `fieldConfig.defaults`/`fieldConfig.overrides`.

**Docker Host Dashboard**
- Host CPU usage and available memory

**Docker Containers Dashboard**
- Per-container CPU and memory from Logporter metrics

**Monitor Services Dashboard**
- Prometheus scrape target availability

### Grafana 13 dashboard migration

There were no dashboard JSON templates in the previous repository snapshot, despite the README describing dashboards. The three provisioned dashboards therefore use Grafana's standard dashboard JSON model with modern panel types and field configuration; they do not contain the deprecated `graph` visualization. Grafana upgrades/imports older dashboards by migrating the dashboard model, but custom dashboards should be exported from Grafana 13 after review and checked with:

```bash
python3 helpers/validate-dashboards.py
```

The validator checks dashboard JSON structure, panel types, field configuration, and panel layout. It is a structural check, not a Grafana renderer; verify query results in Grafana after the Prometheus targets are healthy.

## Define Alerts

Alerts are defined in [prometheus/alert-rules.yml](prometheus/alert-rules.yml) and sent to AlertManager at `alertmanager:9093`.

`MonitorServiceDown` fires when any configured Prometheus scrape target is unreachable. `HostHighMemoryUsage` detects host memory usage above 85%.

## Setup Alerting

AlertManager handles alerts sent by Prometheus and can route them to:
- Email
- Slack
- PagerDuty
- Webhooks
- And many more

Configure routes and receivers in [alertmanager/alertmanager.yml](alertmanager/alertmanager.yml).

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
