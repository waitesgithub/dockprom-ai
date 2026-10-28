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

**Dockprom-AI** is an out-of-the-box monitoring, tracing, log aggregation, and AIOps solution for Docker hosts, containerized microservices, and local LLM workloads. It modernizes the classic Dockprom architecture into a composable observability + AI operations platform with native Model Context Protocol (MCP) integration.

---

## Architecture Overview

Dockprom-AI operates as a coordinated **dual-stack architecture** communicating across a high-isolation bridge network (`monitor-net`):

1. **Core Observability & AIOps Stack (`compose.yml`)**: Telemetry ingest, time-series storage, tracing, log aggregation, alerting pipelines, and native MCP endpoints.
2. **Generative UI & Copilot Stack (`compose-genui.yaml`)**: Conversational SRE workflows, vector similarity search over runbooks, and live React-based interactive remediation interfaces.

### 1. Core Observability Stack

The core pipeline captures metrics, distributed traces, and container logs with deep Linux kernel and host hardware instrumentation:

<p align="center">
  <img src="https://raw.githubusercontent.com/waitesgithub/dockprom-ai/main/img/architecture-core.svg" alt="Dockprom-AI Core Architecture" width="100%" />
</p>

### 2. Generative UI & Copilot Pipeline

The GenUI pipeline connects user prompts to real-time telemetry, semantic runbook embeddings, and streaming React components:

<p align="center">
  <img src="https://raw.githubusercontent.com/waitesgithub/dockprom-ai/main/img/architecture-genui.svg" alt="Dockprom-AI GenUI Architecture" width="100%" />
</p>
