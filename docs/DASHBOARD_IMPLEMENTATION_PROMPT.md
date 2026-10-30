# Dockprom-AI Dashboard Implementation Prompt

Use this prompt for future repository updates:

```text
Act as a Grafana engineer, AI observability engineer, and AI security detection
engineer. Work directly in the dockprom-ai repository.

Maintain the open-source-only observability stack. Use CLI-driven installation
and validation. Do not introduce proprietary SaaS dependencies.

Requirements:
1. Preserve compose.yaml, Prometheus scrape configuration, Grafana datasource
   provisioning, and dashboard file provisioning.
2. Keep all provisioned dashboards compatible with the current Grafana file
   provisioning schema and validate every JSON file.
3. Regenerate dashboard JSON with scripts/generate_grafana_dashboards.py after
   changing dashboard definitions.
4. Maintain dashboards for AI operations, Ollama inference, GenUI end-to-end
   experience, RAG/pgvector quality, AI security detections, MCP tool security,
   PostgreSQL, edge authentication, incident response, OpenTelemetry signal
   quality, GPU capacity, and runtime/supply-chain security.
   Include Agent Harness Security and Operations when agents are present.
5. Use a pinned OpenTelemetry Generative AI semantic-convention version for LLM
   spans and metrics.
6. Never place prompts, responses, secrets, PII, user IDs, session IDs, source
   IPs, document content, or unbounded values in Prometheus labels.
7. Emit structured AI security events with event.action, event.outcome,
   security.detection.type, security.severity, gen_ai.operation.name,
   gen_ai.request.model, session.id_hash, user.id_hash, source.ip, tool.name,
   tool.risk, policy.name, policy.action, and trace_id.
8. Require explicit operator confirmation and audit events for mutating MCP
   tools.
9. Keep Grafana PostgreSQL access read-only and load all credentials from
   environment variables or secret managers.
10. Document and validate open-source exporter choices for NVIDIA, AMD, Intel,
    CPU-only inference, PostgreSQL, Caddy, OpenTelemetry, Falco, and Trivy CLI.
11. Treat unavailable metrics as explicit telemetry TODOs; never fabricate
    dashboard data.
12. Run Compose validation, promtool validation, YAML parsing, JSON parsing,
    dashboard-generation drift checks, Docusaurus build, and git diff --check.
13. Preserve unrelated user changes, use conventional commits, and publish only
    after all applicable tests pass.
14. Apply the OWASP-aligned identity, goal integrity, tool validation,
    planner/executor separation, memory isolation, inter-agent authentication,
    sandboxing, supply-chain, audit, resilience, and human-approval controls in
    docs/AGENT_ROADMAP.md to every agent and skill.
15. Use docs/SECURITY_CONTROL_REFERENCES.md as the mandatory release checklist
    for every agent, skill, MCP server, RAG pipeline, logging path, container,
    and model-operations change.
```
