---
title: Grafana MCP
description: Configure the Grafana MCP SSE endpoint and service-account token.
---

# Grafana MCP

The GenUI container receives the Grafana MCP endpoint as:

```text
GRAFANA_MCP_URL=http://mcp-grafana:8000/sse
```

## Token provisioning

1. Create a dedicated Grafana service account for MCP access.
2. Grant only the datasource and dashboard permissions required for investigation.
3. Create a service-account token.
4. Store the token in the core stack's secret mechanism; never commit it to Compose or `.env` files.
5. Restart the MCP service and verify its health from inside `monitor-net`.

## GenUI status

The endpoint is reserved in `compose-genui.yaml`, but the current Chainlit code
does not open an MCP session or call Grafana tools. Treat this page as the
connection contract for the future integration.
