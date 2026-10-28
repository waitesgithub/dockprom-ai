---
title: Core Stack
description: Metrics, logs, traces, alerting, persistence, and MCP integration.
---

import CoreArchitecture from '@site/static/img/architecture-core.svg';

# Core observability and AIOps stack

The core stack supplies the services consumed by the GenUI companion: Grafana,
Prometheus, Loki, Tempo, OpenTelemetry Collector, Alertmanager, the Ollama
gateway, MCP servers, and PostgreSQL with pgvector.

<p align="center">
  <CoreArchitecture
    role="img"
    aria-label="Animated Dockprom-AI core observability and AIOps architecture"
    style={{width: '100%', height: 'auto'}}
  />
</p>

## Telemetry flow

1. Exporters and instrumented applications send metrics, logs, and traces.
2. Prometheus stores metrics, Loki stores logs, and Tempo stores traces.
3. Grafana queries those backends for dashboards and investigation.
4. Alertmanager routes Prometheus alerts to incident-management integrations.
5. The Grafana and Prometheus MCP servers expose read-oriented investigation tools to authorized AI clients.

## GenUI dependencies

The companion Compose file expects these DNS names on the external
`monitor-net` network:

| Service name | Purpose |
| --- | --- |
| `ollama-gateway` | OpenAI-compatible generation and Ollama embeddings. |
| `mattermost-db` | PostgreSQL/pgvector database containing `rag_storage`. |
| `mcp-grafana` | Grafana MCP SSE endpoint. |
| `prometheus-mcp` | Prometheus MCP SSE endpoint. |

The current repository does not contain the core Compose definition. Deploy or
attach compatible core services before starting `compose-genui.yaml`.
