---
title: Prometheus MCP
description: PromQL tool access through the Prometheus MCP SSE endpoint.
---

# Prometheus MCP

The GenUI container receives the Prometheus MCP endpoint as:

```text
PROMETHEUS_MCP_URL=http://prometheus-mcp:8080/sse
```

Expose read-only PromQL tools wherever possible. Validate query ranges,
timeouts, and result-size limits at the MCP boundary so generated requests
cannot overload Prometheus.

## GenUI status

The endpoint is configured but not consumed by `genui/chainlit/app.py`. Until an
MCP client is implemented, Chainlit answers use pgvector evidence and Ollama
generation only.
