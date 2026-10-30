# Dockprom-AI Observability and Security Roadmap

This roadmap turns the architecture described in `README.md` and
`README_GENUI.md` into a measurable, security-aware operations platform. It
prioritizes end-to-end AI workflows over adding more isolated backend screens.

## Current foundation

This repository now includes placeholder infrastructure for:

- Docker Compose startup for Grafana, Prometheus, Node Exporter, PostgreSQL
  Exporter, and an optional NVIDIA DCGM Exporter profile.
- Prometheus scrape targets for the core, GenUI, MCP, database, edge, incident,
  GPU, and runtime-security services described by the project.
- Provisioned Prometheus, Loki, Tempo, and PostgreSQL datasources.
- Thirteen provisioned Grafana dashboards generated as JSON with Grafana 13's
  `schemaVersion: 42`.
- A metrics and structured-event contract for application instrumentation.
- Open-source exporter and security CLI installation references.

The placeholder panels intentionally display **No data** until their exporter
or application instrumentation is enabled. They do not manufacture values.

## Guiding principles

1. Measure user-impacting workflows from prompt receipt through retrieval,
   generation, tool use, and UI presentation.
2. Use OpenTelemetry Generative AI semantic conventions for model operations.
3. Keep high-cardinality or sensitive values out of Prometheus labels.
4. Never place raw prompts, model responses, secrets, PII, or retrieved runbook
   text on broadly accessible dashboards.
5. Correlate metrics, logs, and traces through `trace_id` and stable service
   identity.
6. Use pseudonymous hashes for users and sessions in security telemetry.
7. Require explicit operator confirmation for disruptive MCP tool actions.
8. Use only open-source integrations and CLI-driven installation workflows.

## Priority 0: operational readiness

### AI Operations Command Center

Purpose: provide one landing view for the Dockprom-AI service graph and user
experience.

Recommended panels:

- Service availability across all scrape targets.
- AI workflow success rate.
- End-to-end p95 response latency.
- RAG retrieval success rate.
- Workflow rate and latency by stage.
- Error rate by service.
- Firing alerts by severity.
- Slow AI traces with drilldowns.
- Error-budget consumption once SLO recording rules are defined.

### Ollama Inference and Model Performance

Purpose: explain inference latency, throughput, saturation, and model capacity.

Recommended panels:

- Request rate and success rate.
- p50/p95/p99 model-operation latency.
- Time to first token.
- Input and output token usage.
- Output tokens per second.
- Latency by requested model and operation.
- Context-window utilization.
- Inference queue depth.
- Model cold-start and load duration.
- Client cancellations, timeouts, and upstream failures.
- Model-specific traces and correlated errors.

Instrumentation should use OpenTelemetry attributes and metrics derived from
the Generative AI semantic conventions, including `gen_ai.system`,
`gen_ai.operation.name`, `gen_ai.request.model`, token type, response model, and
error type. Pin the OpenTelemetry semantic-convention version used by the
application because the GenAI conventions may evolve.

### GenUI End-to-End Experience

Purpose: measure the complete Chainlit, RAG, Ollama, and OpenUI user journey.

Recommended panels:

- Active and completed conversations.
- Conversation completion and abandonment rates.
- End-to-end response duration.
- Embedding-generation duration.
- pgvector retrieval duration.
- Time to first model token.
- Streaming interruptions.
- Widget/component intent detections.
- OpenUI navigation and render errors.
- Errors grouped by workflow stage.
- Slowest GenUI traces.

Required trace stages:

```text
user.message
  -> gen_ai.embeddings
  -> rag.retrieve
  -> gen_ai.chat
  -> gen_ai.first_token
  -> response.complete
  -> openui.navigate/render
```

### RAG and pgvector Quality

Purpose: determine whether retrieval is timely, relevant, and sufficiently
grounded—not merely whether PostgreSQL is available.

Recommended panels:

- Retrieval success and empty-result rates.
- Retrieval p50/p95/p99 latency.
- Similarity-score distribution.
- Results below the configured relevance threshold.
- Top-1 versus top-2 similarity delta.
- Runbook count, ownership, service coverage, and freshness.
- Missing or invalid embeddings.
- Vector index size and utilization.
- Sequential scans versus index scans.
- Connection saturation and slow vector queries.
- Retrieval failures correlated to traces.

### AI Security Detection Center

Purpose: centralize AI-specific abuse, leakage, and policy detections.

Recommended panels:

- Prompt-injection and jailbreak attempts.
- System-prompt extraction attempts.
- Secret, credential, and PII leakage detections.
- Suspicious encoded or obfuscated inputs.
- Requests or responses exceeding policy size thresholds.
- RAG documents containing instruction-like payloads.
- Retrieval of unusually sensitive runbooks.
- Repeated policy violations by pseudonymous session or user.
- Blocked versus allowed requests.
- Detections by severity, model, operation, and policy.
- High-severity events linked to traces.

Structured security events should include:

```text
event.action
event.outcome
security.detection.type
security.severity
gen_ai.operation.name
gen_ai.request.model
session.id_hash
user.id_hash
source.ip
tool.name
tool.risk
policy.name
policy.action
trace_id
```

Do not include raw prompts or responses as metric labels. If content retention
is explicitly approved, store redacted content in a restricted log tenant with
a short retention period.

### MCP Tool Security and Audit

Purpose: measure tool reliability while enforcing confirmation and least
privilege.

Recommended panels:

- Invocations by MCP server and tool.
- Successful, failed, denied, and timed-out calls.
- High-risk or mutating tool attempts.
- Operator confirmations accepted and rejected.
- JSON-RPC errors and invalid parameters.
- Tool latency and result size.
- Unusual tool volume per session.
- Read-only versus mutating calls.
- Prompt-to-tool-to-result audit logs.
- Tool execution traces.

The current Chainlit application exposes MCP endpoint environment variables but
does not yet invoke MCP tools. Instrumentation and the audit contract must be
implemented alongside tool execution.

## Priority 1: platform depth

### PostgreSQL and pgvector Operations

Recommended panels:

- Availability, connection saturation, and connection state.
- Transactions, rollbacks, locks, and deadlocks.
- Cache-hit ratio, checkpoints, WAL, and temporary files.
- Database, table, and index growth.
- Autovacuum health and tuple churn.
- Long-running and expensive `pg_stat_statements` queries.
- Vector index size and vector-query latency.
- `rag_storage`, Keep, and Mattermost database breakdowns.

Grafana must use a read-only database role. Do not reuse application credentials
for the provisioned PostgreSQL datasource.

### Edge Authentication and API Security

Recommended panels:

- Request rate by host, route, method, and status.
- Authentication failures and repeated source failures.
- 404 scanning activity and suspicious paths.
- Oversized requests and request-rate anomalies.
- Upstream 5xx responses and latency.
- Long-lived SSE connections.
- TLS version and certificate expiry.
- Unexpected public binds for Chainlit or OpenUI.

### Incident Response Effectiveness

Recommended panels:

- Alerts received, grouped, inhibited, silenced, and correlated.
- Incidents opened, assigned, mitigated, resolved, and reopened.
- Mean or median time to acknowledge and resolve.
- Duplicate/noisy alert ratio.
- Mattermost and other notification failures.
- Alerts without runbooks.
- AI recommendations accepted or rejected.
- Cross-system incident timeline.

### OpenTelemetry Signal Quality

Recommended panels:

- Accepted, refused, and exported spans, metrics, and logs.
- Export failures, retries, and queue utilization.
- Missing `service.name` and correlation attributes.
- Orphan spans and broken parent relationships.
- Errors without correlated logs.
- AI operations missing token or model attributes.
- High-cardinality attributes and top contributors.
- Sampling ratios and storage-growth estimates.

### GPU and Model Capacity

Recommended panels:

- Accelerator utilization and memory consumption.
- Temperature, power, and hardware errors.
- Thermal or power throttling.
- Model memory footprint and concurrent model residency.
- Queue depth correlated with accelerator saturation.
- Tokens per second versus accelerator utilization.
- CPU fallback activity.
- Capacity trend and forecast.

Use the exporter appropriate for the host:

- NVIDIA: DCGM Exporter.
- AMD: AMD SMI Exporter or ROCm SMI CLI plus Prometheus textfile output.
- Intel: Intel Device Plugins GPU exporter/telemetry tooling.
- CPU-only Ollama: Node Exporter process and host metrics.

## Priority 2: runtime and supply-chain security

### Runtime and Supply-Chain Security

Recommended panels:

- Falco detections by rule, priority, container, and namespace.
- Shell execution and sensitive file access in containers.
- Privilege escalation and unexpected outbound connections.
- Critical/high vulnerabilities by image.
- Vulnerability age and stale base images.
- Unsigned or unverified images.
- Containers running as root.
- Excessive capabilities and writable root filesystems.
- Scan and runtime events linked to the affected workload.

Use Falco for runtime detections and the Trivy CLI for repository, filesystem,
configuration, secret, and image scanning. Their CLI installation and export
patterns are documented in
`website/docs/deployment/exporters-security-tools.md`.

## Delivery phases

### Phase 1: provisioning foundation

- Validate `compose.yaml` with placeholder secrets.
- Validate Prometheus configuration with `promtool`.
- Validate datasource and dashboard provisioning YAML.
- Validate every generated dashboard as JSON.
- Start Grafana and verify all dashboards load without migration errors.

### Phase 2: core exporter integration

- Enable Node Exporter and PostgreSQL Exporter.
- Connect Envoy/Ollama and OpenTelemetry Collector metrics.
- Select and enable the host-specific GPU exporter.
- Add recording rules for common SLO and latency calculations.

### Phase 3: application instrumentation

- Instrument Chainlit message, embedding, retrieval, stream, and completion
  stages with OpenTelemetry and Prometheus.
- Instrument OpenUI navigation and render outcomes.
- Implement trace propagation through Envoy/Ollama.
- Emit low-cardinality RAG quality metrics.

### Phase 4: security telemetry

- Emit structured AI policy-decision events.
- Add prompt-injection, leakage, and abuse detection hooks.
- Implement MCP tool execution with explicit confirmation and audit events.
- Ship Falco events and Trivy scan summaries to Loki.

### Phase 5: alerting and operationalization

- Define SLOs and multi-window burn-rate alerts.
- Add alerts for AI workflow failures, RAG empty-result spikes, security
  detections, MCP denials, telemetry loss, database saturation, and GPU
  throttling.
- Link alerts to runbooks and dashboard panels.
- Test incident routing through Keep and Mattermost.

## Acceptance criteria

- All provisioning files parse successfully.
- Grafana starts with no dashboard or datasource provisioning errors.
- All twelve dashboards appear in the `Dockprom-AI` folder.
- Every panel documents its telemetry dependency.
- Metrics use bounded-cardinality labels.
- Logs and traces carry `service.name`, environment, and `trace_id`.
- AI spans follow the pinned OpenTelemetry GenAI semantic-convention version.
- No secrets, raw credentials, raw prompts, or raw model responses appear in
  dashboard JSON, metric labels, or committed configuration.
- Security events contain the structured fields defined above.
- MCP mutating tools require confirmation and produce an audit event.
- Falco and Trivy integrations use open-source CLI workflows.
- Dashboard generation is deterministic and `git diff --check` passes.

## Dashboard inventory

| Dashboard | Provisioned JSON |
| --- | --- |
| AI Operations Command Center | `ai-operations-command-center.json` |
| Ollama Inference and Model Performance | `ollama-inference-model-performance.json` |
| GenUI End-to-End Experience | `genui-end-to-end-experience.json` |
| RAG and pgvector Quality | `rag-pgvector-quality.json` |
| AI Security Detection Center | `ai-security-detection-center.json` |
| MCP Tool Security and Audit | `mcp-tool-security-audit.json` |
| PostgreSQL and pgvector Operations | `postgresql-pgvector-operations.json` |
| Edge Authentication and API Security | `edge-auth-api-security.json` |
| Incident Response Effectiveness | `incident-response-effectiveness.json` |
| OpenTelemetry Signal Quality | `opentelemetry-signal-quality.json` |
| GPU and Model Capacity | `gpu-model-capacity.json` |
| Agent Harness Security and Operations | `agent-harness-security-operations.json` |
| Runtime and Supply-Chain Security | `runtime-supply-chain-security.json` |

## Secure agent program

MCP servers are tool providers, not agents. The recommended agent portfolio,
OWASP-aligned harness controls, secure skill manifest, evaluation gates, and
phased rollout are defined in [`docs/AGENT_ROADMAP.md`](docs/AGENT_ROADMAP.md).
The normative OWASP/MITRE reference list and control matrix are in
[`docs/SECURITY_CONTROL_REFERENCES.md`](docs/SECURITY_CONTROL_REFERENCES.md).

Begin with read-only observability, LLM performance, runbook recommendation,
and capacity agents. Add security/policy and workflow agents after the telemetry
contract is operational. An approval-gated Change Executor Agent is the final
phase and must never receive a general-purpose shell or unrestricted Docker
socket.
