---
id: intro
title: Overview & Architecture
slug: /
---

<p align="center">
  <img src="/img/dockprom-ai-logo.png" alt="Dockprom-AI Logo" width="340" />
</p>

# Dockprom-AI

> **Production-Grade AI Observability &amp; AIOps Platform**  
> *Prometheus 3 • Grafana 13 • Loki 3 • Tempo 3 • OpenTelemetry • Host Ollama Gateway • MCP Servers • Chainlit • Open-Intelligent-UI • pgvector*

**Dockprom-AI** is an out-of-the-box monitoring, tracing, log aggregation, and AIOps solution for Docker hosts, containerized microservices, and local LLM workloads. It modernizes the classic Docker Prometheus ecosystem with native **Model Context Protocol (MCP)** tool servers, local GPU-accelerated LLM inferencing via host Ollama, automated incident triage via Keep and Mattermost, and an interactive **Generative UI (GenUI)** control plane powered by Chainlit and OpenUI.

---

## Architecture Overview

Dockprom-AI operates as a coordinated **dual-stack architecture** communicating across a high-isolation bridge network (`monitor-net`):

1. **Core Observability & AIOps Stack (`compose.yml`)**: Telemetry ingest, time-series storage, tracing, log aggregation, alerting pipelines, and native MCP endpoints.
2. **Generative UI & Copilot Stack (`compose-genui.yaml`)**: Conversational SRE workflows, vector similarity search over runbooks, and live React-based interactive remediation interfaces.

### 1. Core Observability Stack

The core pipeline captures metrics, distributed traces, and container logs with deep Linux kernel and host hardware instrumentation:

<p align="center">
  <img src="/dockprom-ai/img/architecture-core.svg" alt="Dockprom-AI Core Architecture" width="100%" />
</p>

### 2. Generative UI & Copilot Pipeline

The GenUI pipeline connects user prompts to real-time telemetry, semantic runbook embeddings, and streaming React components:

<p align="center">
  <img src="/dockprom-ai/img/architecture-genui.svg" alt="Dockprom-AI GenUI Architecture" width="100%" />
</p>

---

## Key Stack Components
### 1. Observability & Telemetry Engine (`compose.yml`)
- **Prometheus v3.15.1**: High-performance time-series database with PromQL evaluation, TSDB compaction, and native OpenTelemetry ingest.
- **Grafana 13.3.0**: Unified telemetry frontend featuring pre-provisioned dashboards, correlation links, and native TraceQL/LogQL exploration.
- **Loki 3.7.9**: High-throughput structured log aggregation engine running TSDB schema v13.
- **Tempo 3.1.1**: Low-footprint distributed tracing backend supporting OTLP over gRPC and HTTP.
- **OpenTelemetry Collector Contrib 0.164.0**: Multi-tenant collector pipeline receiving traces, logs, and metrics and multiplexing them to Tempo, Loki, and Prometheus.
- **Logporter 1.5.0**: High-efficiency, memory-conscious container log collector and resource exporter replacing legacy cAdvisor.
- **Node Exporter v1.12.1**: Hardware and Linux kernel telemetry collector.
- **Caddy 2.11.7**: Edge reverse proxy with built-in TLS and bcrypt HTTP basic authentication.

### 2. AI Intelligence & MCP Servers
- **Grafana MCP Server 2.1.1**: Official Model Context Protocol (MCP) server running in SSE mode on port `8000`, allowing AI agents to query dashboards, panels, and data sources directly.
- **Prometheus MCP Server v0.18.0**: Official Prometheus Model Context Protocol server running in SSE mode on port `8080`, exposing PromQL metric evaluations and instant queries to external models.
- **Host Ollama Gateway (Envoy v1.40.2)**: High-performance reverse proxy on port `11435` bridging internal container workloads directly to host-native GPU Ollama (`:11434`) while emitting full OTLP request latencies and trace headers.

### 3. Incident Management & Vector Memory
- **pgvector (PostgreSQL 17)**: Primary relational database extended with native vector similarity search. Serves Keep, Mattermost, and holds the `rag_storage` database for operational incident runbooks.
- **Keep AIOps v0.54.3**: Alert correlation, deduplication, and automated workflow orchestrator.
- **Mattermost Team Edition 12.0.1**: ChatOps platform and automated incident alerting sink.
- **Postgres Exporter v0.20.1**: Telemetry exporter capturing PostgreSQL query latencies and vector index utilization via `pg_stat_statements`.

### 4. Generative UI & Companion Stack (`compose-genui.yaml`)
- **Chainlit Copilot (Port `8050`)**: Conversational AIOps control plane that performs multi-step diagnostic reasoning, queries `pgvector` for similarity runbook matches, invokes Grafana/Prometheus MCP tools, and streams token responses.
- **Open-Intelligent-UI / OpenUI (Port `3001`)**: Next.js streaming interface running `@openuidev/react` and Thesys OpenUI Lang to compile LLM output into live, dynamic React cards, interactive parameter forms, and incident remediation buttons.

---

## Service Endpoints & Ports

| Service | Port / URL | Network | Purpose |
| :--- | :--- | :--- | :--- |
| **Grafana** | `http://localhost:3000` | Host / `monitor-net` | Visualization and dashboards |
| **Prometheus** | `http://localhost:9090` | Host / `monitor-net` | PromQL metrics database |
| **Alertmanager** | `http://localhost:9093` | Host / `monitor-net` | Alert routing and deduplication |
| **Loki** | `http://localhost:3100` | Internal (`monitor-net`) | LogQL structured log store |
| **Tempo** | `http://localhost:3200` | Internal (`monitor-net`) | Distributed trace store |
| **OTel Collector** | `:4317` (gRPC), `:4318` (HTTP) | Internal (`monitor-net`) | Telemetry pipeline ingest |
| **Grafana MCP Server** | `http://localhost:8000/sse` | Host / `monitor-net` | Grafana tool access for AI models |
| **Prometheus MCP Server**| `http://localhost:8080/sse` | Host / `monitor-net` | PromQL tool access for AI models |
| **Host Ollama Gateway** | `http://localhost:11435` | Host / `monitor-net` | Envoy proxy to host Ollama (`:11434`) |
| **Keep AIOps** | `http://localhost:8082` | Host / `monitor-net` | Incident correlation platform |
| **Mattermost** | `http://localhost:8065` | Host / `monitor-net` | Incident response ChatOps |
| **pgvector (Postgres 17)**| `localhost:5432` | Host / `monitor-net` | Vector storage (`rag_storage`) |
| **Chainlit Copilot** | `http://localhost:8050` | Host / `monitor-net` | Multi-turn AIOps agent UI |
| **Open-Intelligent-UI** | `http://localhost:3001` | Host / `monitor-net` | Live Generative UI React surface |

---

## AI Agent Integration (MCP Configuration)

To connect AI assistants (such as Claude Desktop, Cursor, Continue, Roo Code, or Cline) to your live observability stack, register the SSE endpoints in your client configuration:

```json
{
  "mcpServers": {
    "grafana": {
      "type": "sse",
      "url": "http://localhost:8000/sse"
    },
    "prometheus": {
      "type": "sse",
      "url": "http://localhost:8080/sse"
    }
  }
}
