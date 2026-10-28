---
id: intro
title: Overview and Quickstart
slug: /
hide_title: true
hide_table_of_contents: true
---

import CoreArchitecture from '@site/static/img/architecture-core.svg';
import GenuiArchitecture from '@site/static/img/architecture-genui.svg';
import dockpromLogo from '@site/static/img/dockprom-ai-logo.png';

<header className="dockpromHero">
  <div className="dockpromHero__glow" aria-hidden="true"></div>
  <div className="dockpromHero__copy">
    <div className="dockpromHero__badges" aria-label="Platform capabilities">
      <span>Open source</span>
      <span>Docker Compose</span>
      <span>Local AI</span>
    </div>
    <img className="dockpromHero__logo" src={dockpromLogo} alt="Dockprom-AI" />
    <h1>Observe every signal. <span>Investigate with AI.</span></h1>
    <p>
      A composable observability and AIOps platform for Docker hosts,
      microservices, and local LLM workloads—with metrics, logs, traces,
      MCP endpoints, runbook retrieval, and Generative UI in one stack.
    </p>
    <div className="dockpromHero__actions">
      <a className="button button--primary button--lg" href="#quickstart">Get started</a>
      <a className="button button--secondary button--lg" href="https://github.com/waitesgithub/dockprom-ai">View on GitHub</a>
    </div>
  </div>
  <div className="dockpromTerminal" aria-label="Dockprom-AI quickstart command">
    <div className="dockpromTerminal__chrome" aria-hidden="true">
      <span></span><span></span><span></span><b>terminal</b>
    </div>
    <pre><code><span>$</span> docker compose up -d{`\n`}<span>$</span> docker compose ps{`\n\n`}prometheus   running{`\n`}grafana      running{`\n`}loki         running{`\n`}tempo        running</code></pre>
  </div>
</header>

<div className="dockpromCapabilityGrid">
  <article><strong>Unified telemetry</strong><span>Prometheus, Grafana, Loki, Tempo, and OpenTelemetry.</span></article>
  <article><strong>AIOps interfaces</strong><span>Grafana and Prometheus MCP endpoints for operational tooling.</span></article>
  <article><strong>Local-first copilot</strong><span>Ollama, Chainlit, OpenUI, and pgvector remain on your network.</span></article>
</div>

## Architecture overview

Dockprom-AI operates as a coordinated **dual-stack architecture** communicating across a high-isolation bridge network (`monitor-net`):

1. **Core observability and AIOps stack:** telemetry ingest, time-series storage, tracing, log aggregation, alerting pipelines, and MCP endpoints.
2. **Generative UI and copilot stack (`compose-genui.yaml`):** conversational workflows, vector search over runbooks, and interactive remediation interfaces.

### Core observability stack

The core pipeline captures metrics, distributed traces, and container logs with deep Linux kernel and host hardware instrumentation:

<p align="center">
  <CoreArchitecture
    role="img"
    aria-label="Animated Dockprom-AI core observability and AIOps architecture"
    style={{width: '100%', height: 'auto'}}
  />
</p>

### Generative UI and copilot pipeline

The GenUI pipeline connects user prompts to real-time telemetry, semantic runbook embeddings, and streaming React components:

<p align="center">
  <GenuiArchitecture
    role="img"
    aria-label="Animated Dockprom-AI Generative UI and AIOps copilot architecture"
    style={{width: '100%', height: 'auto'}}
  />
</p>

## Quickstart

The GenUI stack assumes the core services and external `monitor-net` network
already exist.

```bash
export PGVECTOR_URL='postgresql://<user>:<password>@mattermost-db:5432/rag_storage'
docker compose -f compose-genui.yaml config --quiet
docker compose -f compose-genui.yaml up -d --build
```

Open Chainlit at `http://localhost:8050` and Open-Intelligent-UI at
`http://localhost:3001`.

Continue with the [host prerequisites](deployment/host-prereqs.md),
[environment reference](deployment/configuration-env.md), and
[GenUI architecture](architecture/genui-stack.md).
