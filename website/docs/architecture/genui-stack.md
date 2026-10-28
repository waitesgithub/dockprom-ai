---
title: GenUI Stack
description: Chainlit, Open-Intelligent-UI, Ollama, and pgvector data flow.
---

import GenuiArchitecture from '@site/static/img/architecture-genui.svg';

# Generative UI and copilot stack

The GenUI stack is defined in `compose-genui.yaml` and contains two services:
the Chainlit copilot and Open-Intelligent-UI.

<p align="center">
  <GenuiArchitecture
    role="img"
    aria-label="Animated Dockprom-AI Generative UI and AIOps copilot architecture"
    style={{width: '100%', height: 'auto'}}
  />
</p>

## Request flow

1. An operator submits a question to Chainlit on port `8050`.
2. Chainlit asks Ollama to embed the question.
3. The embedding is compared with `operational_runbooks` in pgvector.
4. Chainlit sends the retrieved evidence and question to the configured Ollama model.
5. The streamed response appears in Chainlit, with a link to Open-Intelligent-UI when UI-oriented content is detected.

## Current integration boundary

The Compose service provides Grafana and Prometheus MCP endpoint variables, but
`genui/chainlit/app.py` does not yet invoke MCP tools. Live telemetry retrieval
must be implemented and tested before responses can claim to include current
Grafana or Prometheus data.

See [`README_GENUI.md`](https://github.com/waitesgithub/dockprom-ai/blob/main/README_GENUI.md)
for the deployment procedure and security notes.
