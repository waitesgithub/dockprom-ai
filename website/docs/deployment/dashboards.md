---
title: Dashboards
description: Grafana dashboard expectations for Dockprom-AI services.
---

# Dashboards

Grafana file provisioning loads the JSON dashboards from `grafana/dashboards`
into the `Dockprom-AI` folder. Stable datasource UIDs are defined in
`grafana/provisioning/datasources/datasources.yml`.

## Provisioned dashboards

| Dashboard | Focus |
| --- | --- |
| AI Operations Command Center | Cross-stack health, workflow SLOs, alerts, and traces. |
| Ollama Inference and Model Performance | OpenTelemetry GenAI latency, TTFT, tokens, queueing, and model loading. |
| GenUI End-to-End Experience | Chainlit, RAG, Ollama, stream, and OpenUI stages. |
| RAG and pgvector Quality | Retrieval latency, relevance, runbook coverage, and database behavior. |
| AI Security Detection Center | Injection, jailbreak, leakage, abuse, and policy decisions. |
| MCP Tool Security and Audit | Tool outcomes, risk, confirmations, JSON-RPC errors, and audit trails. |
| PostgreSQL and pgvector Operations | Connections, transactions, cache, deadlocks, growth, and indexes. |
| Edge Authentication and API Security | Authentication failures, scanning, TLS, and upstream errors. |
| Incident Response Effectiveness | Alert outcomes, MTTA, MTTR, notification delivery, and runbooks. |
| OpenTelemetry Signal Quality | Signal acceptance, refusal, export failure, queues, and cardinality. |
| GPU and Model Capacity | Accelerator utilization, memory, thermal state, queueing, and throughput. |
| Agent Harness Security and Operations | Agent outcomes, policy denials, approvals, delegation, budgets, and safety actions. |
| Runtime and Supply-Chain Security | Falco events, Trivy summaries, image policy, and container compliance. |

## Regenerate dashboards

```bash
python3 scripts/generate_grafana_dashboards.py
find grafana/dashboards -name '*.json' -print0 | xargs -0 -n1 jq empty
```

The dashboards use a placeholder telemetry contract and display no data until
the corresponding exporter or application instrumentation is enabled. See the
[AI telemetry contract](telemetry-contract.md) and
[exporter/security tool reference](exporters-security-tools.md).
