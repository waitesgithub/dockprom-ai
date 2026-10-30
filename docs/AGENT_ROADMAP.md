# Dockprom-AI Secure Agent Roadmap

MCP servers expose tools; they are not autonomous agents. Dockprom-AI should
add agents only where a bounded goal, explicit identity, restricted tool set,
and measurable outcome provide value beyond a direct MCP call.

This roadmap treats every agent and skill as untrusted orchestration code. The
harness must address the OWASP Agentic Security Initiative risks: goal
hijacking, tool misuse, identity and privilege abuse, supply-chain compromise,
unexpected code execution, memory poisoning, insecure inter-agent messages,
cascading failures, human-trust exploitation, and rogue-agent behavior.

The normative OWASP and MITRE references and control traceability matrix are in
[`SECURITY_CONTROL_REFERENCES.md`](SECURITY_CONTROL_REFERENCES.md). They apply
to every agent, skill, MCP server, RAG pipeline, telemetry path, model release,
and execution container.

## Recommended agent portfolio

| Agent | Mission | Default tools | Write authority | Risk |
| --- | --- | --- | --- | --- |
| Observability Triage Agent | Correlate alerts, metrics, logs, and traces into an evidence-backed incident summary. | Prometheus query, Loki query, Tempo search, Grafana read | None | Low |
| AI/LLM Performance Agent | Diagnose Ollama latency, TTFT, token throughput, context pressure, queues, and GPU saturation. | Prometheus query, Tempo search, model inventory read | None | Low |
| RAG Quality Agent | Evaluate retrieval latency, empty results, similarity distributions, corpus coverage, and runbook freshness. | PostgreSQL read-only, Prometheus query | None | Medium |
| AI Security Detection Agent | Detect prompt injection, jailbreaks, leakage, anomalous retrieval, and model/tool abuse. | Loki query, Tempo search, Prometheus query, policy read | None | Medium |
| MCP Tool Policy Agent | Classify tool risk, validate parameters, and produce allow, deny, or require-approval decisions. | Tool registry read, OPA decision API | Policy decision only | High |
| Incident Correlation Agent | Group related alerts and assemble a candidate incident timeline. | Alertmanager read, Keep read, Loki/Tempo query | Create draft incident only | Medium |
| Runbook Recommendation Agent | Retrieve and rank relevant runbooks with citations and freshness warnings. | pgvector read-only | None | Low |
| Runbook Curator Agent | Identify stale, duplicate, missing, or poorly grounded operational knowledge. | pgvector read, Git read | Pull-request draft only | Medium |
| Capacity Planning Agent | Forecast host, storage, database, telemetry, GPU, and model capacity. | Prometheus range query, PostgreSQL read-only | None | Low |
| Remediation Planner Agent | Propose reversible remediation steps, blast radius, validation, and rollback. | All observability read tools, runbooks | None | High |
| Change Executor Agent | Execute one approved, predeclared remediation and verify its result. | Narrow action-specific tool allowlist | Approval-gated | Critical |
| Runtime and Supply-Chain Agent | Correlate Falco events, Trivy findings, image provenance, and container posture. | Falco/Loki read, Trivy report read, Git read | Pull-request draft only | Medium |
| Telemetry Engineering Agent | Detect missing instrumentation, broken correlations, cardinality growth, and dashboard drift. | Prometheus/Loki/Tempo/Grafana read, repository read | Pull-request draft only | Medium |
| Post-Incident Review Agent | Build a cited timeline, contributing factors, and follow-up drafts after closure. | Incident, chat, metrics, logs, traces read | Postmortem draft only | Medium |

## Recommended implementation order

### Phase 1: read-only agents

1. Observability Triage Agent.
2. AI/LLM Performance Agent.
3. Runbook Recommendation Agent.
4. Capacity Planning Agent.

These agents provide immediate operational value and can be constrained to
read-only MCP tools. They establish the harness, audit, evaluation, and
telemetry patterns without creating production mutations.

### Phase 2: detection and governance agents

1. AI Security Detection Agent.
2. RAG Quality Agent.
3. MCP Tool Policy Agent.
4. Runtime and Supply-Chain Agent.
5. Telemetry Engineering Agent.

These agents consume structured security and quality events. Policy decisions
must be deterministic, explainable, and enforced outside the model by the
harness or an open-source policy engine such as Open Policy Agent.

### Phase 3: workflow agents

1. Incident Correlation Agent.
2. Remediation Planner Agent.
3. Runbook Curator Agent.
4. Post-Incident Review Agent.

Outputs remain drafts. Humans approve incident creation, repository changes,
and remediation plans.

### Phase 4: approval-gated execution

Add the Change Executor Agent only after the other phases have demonstrated:

- reliable identity and authorization;
- complete tool audit trails;
- deterministic policy enforcement;
- rollback-capable runbooks;
- adversarial-test coverage;
- circuit breakers and rate limits;
- successful shadow-mode and canary evaluations.

Do not give a general-purpose shell, unrestricted Docker socket, database write
credential, or arbitrary HTTP client to an execution agent.

## Secure agent harness requirements

### Identity and authorization

- Assign a unique workload identity to each agent instance.
- Use separate service accounts for read, draft, approval, and execution roles.
- Authorize every tool call outside the model.
- Enforce least privilege with explicit tool and resource allowlists.
- Bind approval tokens to the actor, action, parameters, target, expiry, and
  trace ID so approval cannot be replayed for another action.
- Deny by default when identity, policy context, or target classification is
  missing.

### Goal and prompt integrity

- Store the system goal and immutable safety constraints outside user-controlled
  context.
- Delimit system instructions, retrieved documents, tool output, and user input.
- Treat retrieved runbooks, logs, webpages, tickets, and chat messages as
  untrusted data that can contain indirect prompt injection.
- Reject instructions found inside tool output or retrieved content unless the
  harness explicitly promotes them through policy.
- Detect goal drift and terminate when an agent leaves its declared objective.

### Tool safety

- Define every tool with strict JSON Schema inputs and bounded outputs.
- Validate types, formats, enum values, length, resource identifiers, and target
  scope before execution.
- Separate read tools from mutation tools.
- Require human approval for destructive, externally visible, privileged, or
  high-blast-radius operations.
- Apply timeouts, rate limits, concurrency limits, idempotency keys, and result
  size limits.
- Return structured errors; never let the model infer that an action succeeded.
- Prevent command concatenation, shell interpolation, path traversal, SSRF, and
  unrestricted URL fetching.
- For MCP, authenticate both endpoints, validate origins, bind authorization to
  the active session, prevent confused-deputy behavior, and re-authorize every
  call instead of trusting capability discovery.

### Planner/executor isolation

- The planner produces a typed action plan but has no mutation credentials.
- The policy layer validates the plan against current state and allowed targets.
- The approval layer captures an accountable human decision.
- The executor receives only the approved action, not the full conversation.
- The verifier independently checks success criteria and rollback conditions.
- A rollback handler runs from a predefined, tested procedure—not generated
  shell text.

### Memory and RAG security

- Namespace memory by tenant, user, agent, purpose, and environment.
- Attach provenance, author, creation time, classification, and expiry to every
  memory item.
- Never persist secrets, credentials, raw authentication headers, or unrestricted
  prompt/response content.
- Scan documents for prompt injection and sensitive content before indexing.
- Require citations and relevance thresholds for retrieved evidence.
- Prevent one user or environment from poisoning another user's memory.
- Support quarantine, revocation, and re-embedding of compromised knowledge.
- Authorize retrieval before vector search so filtering cannot leak document
  existence or metadata across tenants.
- Keep an ingestion manifest with document hash, source, parser, scanner,
  embedding model, index version, and policy decision.

### Inter-agent communication

- Use authenticated, schema-validated messages rather than free-form prompt
  forwarding.
- Include sender, recipient, purpose, trace ID, expiry, data classification, and
  allowed next actions.
- Reject recursive delegation outside a bounded depth and agent allowlist.
- Prevent agents from granting privileges or tools to other agents.
- Record the full delegation graph for investigation.

### Execution isolation

- Run agents and tools as non-root containers with read-only filesystems where
  practical.
- Drop Linux capabilities, apply seccomp/AppArmor profiles, and limit CPU,
  memory, process count, and network egress.
- Use short-lived credentials injected directly into the tool process, never
  exposed to the model context.
- Prohibit arbitrary code execution. If a narrowly scoped code sandbox is
  essential, isolate it from production networks and secrets and destroy it
  after each task.

### Supply-chain security

- Pin agent, model, MCP server, skill, exporter, and container versions.
- Generate SBOMs and scan artifacts with the open-source Trivy CLI.
- Verify release checksums/signatures and container provenance.
- Require code review for agent prompts, policies, tool schemas, and skills.
- Record the hash/version of the agent, system prompt, policy, skill, model, and
  tool registry in every execution trace.
- Disable dynamically downloaded skills or tools in production.

### Observability and audit

- Emit OpenTelemetry spans for agent runs, model operations, retrieval, policy
  decisions, tool calls, approvals, execution, verification, and rollback.
- Record metrics for success, latency, token use, tool outcomes, denials,
  confirmation decisions, retries, circuit-breaker trips, and goal-drift events.
- Write append-only structured audit events with pseudonymous actor/session IDs.
- Redact prompts, responses, tool payloads, credentials, PII, and sensitive
  runbook content before logging.
- Correlate all signals using a trace ID and immutable agent-run ID.
- Follow MITRE ATLAS AML.M0024 by monitoring model, agent, retrieval, policy,
  tool, approval, execution, verification, and rollback activity as one trace.

### Resilience and containment

- Set maximum steps, tool calls, tokens, wall-clock duration, retries, cost, and
  delegation depth per run.
- Stop cascading failures with circuit breakers and per-service budgets.
- Add global and per-agent kill switches.
- Use shadow mode before enabling production recommendations or actions.
- Require canaries for high-risk changes.
- Fall back to human-operated runbooks when telemetry or policy services fail.

### Human factors

- Clearly label agent-generated conclusions and uncertainty.
- Present evidence, alternatives, blast radius, and rollback before approval.
- Never use urgency, authority claims, or hidden defaults to pressure approval.
- Make reject and request-more-evidence actions as easy as approve.
- Require a second approver for critical production changes.

## Secure skill contract

Every skill should have a machine-readable manifest containing at least:

```yaml
name: string
version: semver
owner: team-or-person
description: bounded purpose
inputs_schema: path-or-inline-json-schema
outputs_schema: path-or-inline-json-schema
allowed_tools: []
allowed_resources: []
network_egress: []
data_classifications: []
required_identity_role: string
approval_policy: none-or-policy-id
side_effects: none-read-draft-write-destructive
max_steps: integer
max_tool_calls: integer
timeout_seconds: integer
audit_event_types: []
rollback_runbook: null-or-path
sbom: path
source_digest: sha256
```

Skills must not:

- embed credentials or tokens;
- broaden their own tool permissions;
- install packages or fetch code at runtime;
- accept unvalidated free-form shell commands;
- write outside declared resources;
- suppress tool failures or claim unverified success;
- persist unredacted model or tool content;
- delegate to undeclared agents.

## Agent evaluation gates

Before an agent enters production, require:

- unit tests for input/output and tool schemas;
- policy allow/deny tests;
- prompt-injection and indirect-injection tests;
- memory-poisoning and cross-tenant isolation tests;
- SSRF, command-injection, path-traversal, and privilege-escalation tests;
- tool-result spoofing and confused-deputy tests;
- approval replay and parameter-substitution tests;
- cascading-failure and retry-storm tests;
- hallucinated-success and missing-evidence tests;
- telemetry redaction and audit-completeness tests;
- rollback and kill-switch exercises.

Open-source CLI candidates include `promptfoo` and `garak` for adversarial model
testing, `opa` for deterministic policy tests, `trivy` for supply-chain scanning,
and `falco` for runtime detections. Pin and scan each tool before use.

## Agent observability dashboards

Extend the existing dashboards with:

- Agent runs by type, version, model, and outcome.
- Goal-drift and policy-denial rates.
- Tool calls, latency, retries, and denied calls per agent.
- Approval acceptance, rejection, expiry, and replay attempts.
- Planner versus executor outcomes.
- Delegation graph depth and fan-out.
- Memory retrieval by source classification and relevance.
- Agent cost/token budgets and exhaustion.
- Circuit-breaker, kill-switch, and rollback activity.
- Security detections mapped to the relevant OWASP agentic risk.

Do not expose chain-of-thought. Store concise decision summaries, policy
outcomes, evidence references, and tool results instead.
