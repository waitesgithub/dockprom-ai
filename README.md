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
- **Logporter** - Container metrics and Docker log shipping to Loki
- **NodeExporter** - Host metrics
- **Grafana MCP Server** - AI-powered Grafana integration
- **AlertManager** - Alert management

## Quick Start

### Prerequisites

- Docker Engine
- Docker Compose v2.20 or later

### Installation

Clone this repository and start the monitoring stack:

```bash
git clone https://github.com/waitesgithub/dockprom-ai
cd dockprom-ai
```

```bash
docker compose up -d
```

Grafana defaults to `admin` / `admin`; set `ADMIN_USER` and `ADMIN_PASSWORD`
to change those credentials. Caddy is optional and disabled by default. To run
it, generate a password hash and start the `proxy` profile:

```bash
docker run --rm caddy:v2.11.7 caddy hash-password --plaintext 'YOUR_PASSWORD'
export ADMIN_PASSWORD_HASH='your-generated-hash'
docker compose --profile proxy up -d
```

To enable the optional Grafana MCP server, create a Grafana service-account
token after Grafana starts, then run:

```bash
export GRAFANA_SERVICE_ACCOUNT_TOKEN='your-service-account-token'
docker compose --profile mcp up -d mcp-grafana
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
| **NodeExporter** | - | Host metrics collector |
| **Logporter** | `http://127.0.0.1:9333` | Container metrics, Docker logs, and dashboard |
| **Grafana MCP Server** | `http://127.0.0.1:8000/sse` | Optional local AI client integration (`--profile mcp`) |
| **Caddy** | `http://<host-ip>` | Optional reverse proxy with basic auth (`--profile proxy`) |

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

## AI Application Observability

- **Traces** - Apps send OTLP traces to the Collector → stored in Tempo → viewed in Grafana
- **Logs** - Docker logs collected by Logporter → stored in Loki → viewed in Grafana
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

### Dashboards

The Logporter dashboard is available at `http://127.0.0.1:9333`. To provision
additional Grafana dashboards, place their exported JSON files in `screens/`;
Grafana watches that directory through its configured dashboard provider.

## Define Alerts

The initial target health alert is configured in [prometheus/alert.rules](prometheus/alert.rules):

### Monitoring Services Alerts

Alert if a Prometheus monitoring target, including node-exporter or Logporter, is down:

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

Container alert expressions should use the metric names and labels exposed by
Logporter at `http://127.0.0.1:9333/metrics`. Existing cAdvisor expressions
such as `container_memory_usage_bytes` may need to be translated before use.

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

The Compose stack starts the official Grafana MCP server in SSE
mode. Create a service account token in Grafana, export it as
`GRAFANA_SERVICE_ACCOUNT_TOKEN`, and configure your MCP client to connect to
`http://localhost:8000/sse`. Keep the token private and grant only the
permissions needed by the client. The service is bound to localhost and is not
published to external interfaces. Start it with
`docker compose --profile mcp up -d mcp-grafana`.

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

## Image versions and upgrade notes

The Compose file pins the requested upstream releases:

| Service | Image |
|---------|-------|
| Prometheus | `prom/prometheus:v3.15.1` |
| Grafana | `grafana/grafana:13.2.4` |
| Caddy | `caddy:v2.11.7` |
| Alertmanager | `prom/alertmanager:0.34.1` |
| Node Exporter | `prom/node-exporter:v1.12.1` |
| Pushgateway | `prom/pushgateway:v1.11.4` |
| Loki | `grafana/loki:2.9.3` |
| Logporter | `lifailon/logporter:latest` |

Grafana 13.2.4 is a major-version upgrade from Grafana 12.4.0. Back up the
`grafana-data` volume before upgrading and test your existing dashboards in a
staging instance. Grafana may migrate dashboard models or panel layouts on
first startup; keep exported dashboard JSON backups and check panels, variables,
and queries after the migration. Restore the volume backup to roll back rather
than downgrading Grafana against an already-migrated database.

Logporter replaces cAdvisor and collects both container metrics and Docker
logs, so a separate container-metrics agent and Docker log collector are not
needed for those functions. Combining these functions can reduce the number
of running services; actual resource use depends on workload, so measure it
before setting resource limits. The Docker socket is mounted read-only, but
access to the Docker API is still highly privileged; only run Logporter on a
trusted host. Its dashboard is available locally at `http://127.0.0.1:9333`;
dashboard JSON can also be provisioned through the `screens/` directory.
Existing cAdvisor dashboards and alert expressions may need updates to use
Logporter's metrics (inspect `http://127.0.0.1:9333/metrics`). Although
cAdvisor's upstream image moved from `gcr.io/cadvisor/cadvisor` to
`ghcr.io/google/cadvisor`, this stack removes cAdvisor instead of upgrading
it.

The Compose stack keeps Loki on 2.9.3 as specified. Tempo, the OpenTelemetry
Collector, and the MCP server use their upstream `latest` tags because no
release tags were specified for them here; review and pin those separately if
you need reproducible upgrades.

The optional Caddy proxy is started with the `proxy` Compose profile and
requires a Caddy password hash. Grafana's credentials and MCP service-account
token should be set through environment variables rather than committed config.

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
