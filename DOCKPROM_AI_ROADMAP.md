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

## Implementation status

This status reflects the repository contents, not only the intended
architecture. A provisioned dashboard is considered complete as a dashboard
artifact, but it is not considered operational until its telemetry producer is
connected and emitting the documented contract.

| Area | Status | Remaining work |
| --- | --- | --- |
| Grafana 13.3.0 configuration | Partial | Compose uses `grafana/grafana:13.3.0`; rerun dashboard provisioning tests against that exact image. |
| Dashboard JSON | Complete | Thirteen dashboard files exist with Grafana 13 `schemaVersion: 42`. Maintain compatibility tests when Grafana changes. |
| Grafana provisioning | Complete | Dashboard and datasource provisioning files exist. Validate them during CI and container startup. |
| Prometheus configuration | Partial | Scrape jobs exist, but several referenced services are not provided by the current Compose files. |
| Core exporters | Partial | Node Exporter and PostgreSQL Exporter are defined; NVIDIA DCGM Exporter is optional and host-specific exporters still require selection. |
| Recording and alerting rules | Not started | Add Prometheus recording rules, SLO rules, and alert rules. |
| Application telemetry | Not started | Chainlit, OpenUI, RAG, MCP, and AI security signals still use a placeholder telemetry contract. |
| OpenTelemetry integration | Partial | Datasource and contract documentation exist; add and configure the Collector and instrument the applications. |
| MCP execution | Not started | Chainlit has MCP endpoint configuration but does not invoke MCP tools. |
| Runtime and supply-chain security | Documentation only | Falco and Trivy installation guidance exists; operational ingestion and dashboards need live events. |
| PydanticAI agents | In progress | Five read-only Python agents exist locally under `agents/`; complete testing, harness integration, documentation, and repository commit. |
| Custom agent harness | Not complete | Centralize policy, budgets, audit metadata, model execution, tool authorization, and containment for every agent. |

### Unresolved scrape targets

Prometheus currently declares jobs for the following services, but the current
`compose.yaml` and `compose-genui.yaml` do not define all of them. Each target
must either gain a Compose service, be configured as an external deployment, or
be removed or disabled until available:

- OpenTelemetry Collector;
- Envoy/Ollama gateway;
- Ollama exporter;
- Grafana MCP server;
- Prometheus MCP server;
- Caddy;
- Alertmanager;
- Loki;
- Tempo;
- Keep;
- Falco.

## Remaining observability work

Complete this work in the following order so dashboards become operational
without inventing telemetry:

1. Pull `grafana/grafana:13.3.0`, start a disposable Grafana instance, and
   verify that all provisioned datasources and thirteen dashboards load without
   migration or plugin errors.
2. Add CI validation for dashboard JSON, provisioning YAML, Prometheus
   configuration, Compose interpolation, and Grafana startup provisioning.
3. Add Prometheus recording rules for availability, request and error rates,
   latency percentiles, saturation, AI workflow success, and SLO/error-budget
   calculations.
4. Add alert rules for service failure, elevated AI latency, RAG failures,
   telemetry loss, PostgreSQL saturation, GPU pressure, and high-severity AI or
   runtime-security events.
5. Define or connect the missing Loki, Tempo, Alertmanager, OpenTelemetry
   Collector, edge, incident-management, MCP, Ollama, and security services.
6. Instrument Chainlit message receipt, embedding, retrieval, generation,
   first-token, streaming, completion, and error stages using OpenTelemetry
   Generative AI semantic conventions.
7. Instrument OpenUI navigation, component generation, render success, render
   failure, abandonment, and client-perceived latency.
8. Propagate trace context across Chainlit, pgvector, Envoy/Ollama, MCP tools,
   and OpenUI so dashboards can correlate metrics, logs, and traces.
9. Emit low-cardinality RAG quality metrics for empty results, similarity
   thresholds, result ranking, corpus coverage, freshness, and retrieval
   latency without exposing document content.
10. Emit structured AI security events for prompt injection, jailbreak,
    leakage, policy decisions, suspicious retrieval, and model or tool abuse.
11. Implement MCP tool execution with strict schemas, per-call authorization,
    explicit confirmation for risky actions, bounded results, and correlated
    audit events.
12. Export Falco detections and Trivy scan summaries into the observability
    pipeline while keeping raw sensitive findings in restricted storage.
13. Add host-appropriate GPU telemetry and correlate model queueing, token
    throughput, memory pressure, temperature, power, and CPU fallback.
14. Create operational runbooks and dashboard links for every actionable alert.

## Remaining agent work

Use PydanticAI as the only agent framework. All agents must be Python based and
live under the repository's separate `agents/` package. The initial portfolio
contains the Observability Triage, LLM Performance, RAG Quality, AI Security,
and Capacity Planning agents. Before that package is production-ready:

1. Implement one custom PydanticAI harness as the mandatory execution boundary
   for every agent; agents must not invoke models or tools around the harness.
2. Make the harness responsible for agent lookup, typed input/output
   validation, immutable system instructions, dependency construction, model
   invocation, and normalized structured errors.
3. Enforce per-agent allowlists and authorize every tool call outside model
   reasoning. Deny calls with missing identity, scope, or policy context.
4. Enforce budgets for wall-clock duration, model requests, tokens, retries,
   tool calls, concurrency, delegation depth, and tool-result size.
5. Generate immutable agent-run and trace identifiers and emit structured audit
   events for run start, model operation, policy decision, tool call, denial,
   failure, and completion.
6. Add global and per-agent kill switches, circuit breakers, bounded retries,
   and safe failure behavior when model, telemetry, or policy services are
   unavailable.
7. Redact credentials, authentication headers, PII, raw prompts, raw model
   responses, and sensitive tool content before telemetry or audit emission.
8. Keep endpoint origins operator-configured, reject embedded credentials,
   disable redirects, validate queries and trace identifiers, and retain strict
   response-size and timeout limits.
9. Add unit tests for settings, schemas, registry selection, tool allowlists,
   dependency injection, structured output, and all harness budget failures.
10. Add adversarial tests for direct and indirect prompt injection, SSRF,
    command injection, path traversal, tool-result spoofing, confused-deputy
    behavior, goal drift, and hallucinated success.
11. Add security tests for cross-tenant isolation, memory poisoning, approval
    replay, parameter substitution, privilege escalation, retry storms, and
    audit completeness.
12. Use PydanticAI's deterministic test model for unit tests; tests must not
    contact Ollama or production observability services.
13. Add OpenTelemetry spans and metrics for agent runs, model calls, tool calls,
    policy denials, retries, budget exhaustion, circuit breakers, and run
    outcomes without recording chain-of-thought.
14. Document installation, environment configuration, agent selection, example
    read-only runs, security boundaries, and troubleshooting.
15. Run the complete Python test suite, type and import checks, dependency scan,
    secret scan, and container/repository security checks before committing the
    package.
16. Update `docs/AGENT_ROADMAP.md` and the Docusaurus secure-agent documentation
    to distinguish implemented agents from planned agents.
17. Commit the `agents/` package only after the harness and its security tests
    pass, then add it to CI as an independently testable Python project.

Later agent phases remain intentionally unimplemented: Runbook Recommendation,
MCP Tool Policy, Incident Correlation, Runtime and Supply-Chain, Telemetry
Engineering, Remediation Planner, Runbook Curator, Post-Incident Review, and the
approval-gated Change Executor. Do not implement write-capable execution until
the identity, policy, approval, verification, rollback, audit, adversarial-test,
shadow-mode, and canary gates in `docs/AGENT_ROADMAP.md` are satisfied.

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
