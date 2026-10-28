---
id: intro
title: Overview & Architecture
slug: /
---

import coreArchitecture from '@site/static/img/architecture-core.svg';
import genuiArchitecture from '@site/static/img/architecture-genui.svg';
import dockpromLogo from '@site/static/img/dockprom-ai-logo.png';

<p align="center">
  <img src={dockpromLogo} alt="Dockprom-AI logo" width="340" />
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
  <img src={coreArchitecture} alt="Dockprom-AI core observability and AIOps architecture" width="100%" />
</p>

### 2. Generative UI & Copilot Pipeline

The GenUI pipeline connects user prompts to real-time telemetry, semantic runbook embeddings, and streaming React components:

<p align="center">
  <img src={genuiArchitecture} alt="Dockprom-AI Generative UI and AIOps copilot architecture" width="100%" />
</p>
