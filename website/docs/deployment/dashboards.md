---
title: Dashboards
description: Grafana dashboard expectations for Dockprom-AI services.
---

# Dashboards

The architecture anticipates dashboards for host and container health,
Prometheus and OpenTelemetry pipelines, PostgreSQL, and MCP service health.

The current repository does not include dashboard JSON or Grafana provisioning
files. Add them to the core stack and provision stable datasource UIDs before
documenting dashboard-specific links or panels here.

At minimum, monitor:

- request count, latency, and errors for the Ollama gateway;
- Chainlit and Open-Intelligent-UI container availability;
- PostgreSQL connections, query latency, and vector-search failures;
- MCP connection and tool-call errors;
- Prometheus scrape health and OpenTelemetry export failures.
