---
id: secure-agents
title: Secure Agent Architecture
---

# Secure agent architecture

MCP servers expose bounded tools. Agents combine a goal, model, memory, policy,
and tools into a workflow. Dockprom-AI should begin with read-only diagnostic
agents and add mutation only after approval, isolation, audit, and rollback
controls have been proven.

## Recommended first agents

1. **Observability Triage Agent:** correlates alerts, metrics, logs, and traces.
2. **AI/LLM Performance Agent:** diagnoses Ollama, token, context, queue, and GPU behavior.
3. **Runbook Recommendation Agent:** retrieves cited operational guidance.
4. **AI Security Detection Agent:** identifies injection, leakage, abuse, and anomalous tool activity.
5. **RAG Quality Agent:** monitors retrieval relevance, coverage, and freshness.
6. **MCP Tool Policy Agent:** makes deterministic allow, deny, or approval-required decisions.
7. **Incident Correlation Agent:** produces a draft incident and evidence timeline.
8. **Remediation Planner Agent:** proposes bounded, reversible steps without executing them.

The approval-gated Change Executor Agent should be last. It must never have a
general-purpose shell or unrestricted Docker socket.

## Harness flow

```text
Untrusted input
  -> input classification and injection checks
  -> bounded agent goal
  -> read-only evidence collection
  -> typed plan
  -> deterministic OPA policy decision
  -> human approval when required
  -> narrowly scoped executor
  -> independent verification
  -> rollback or completion
  -> immutable audit event and OpenTelemetry trace
```

## OWASP-aligned controls

- Immutable agent goals and prompt/data separation.
- Unique agent identity and least-privilege tool authorization.
- Strict JSON Schema validation for every tool and inter-agent message.
- Planner, policy, approval, executor, and verifier separation.
- Tenant-isolated memory with provenance, classification, expiry, and quarantine.
- Sandboxed non-root execution with restricted egress and short-lived credentials.
- Signed/pinned agent, skill, MCP, model, and container dependencies.
- Maximum steps, tools, tokens, retries, duration, and delegation depth.
- Kill switches, circuit breakers, canaries, and tested rollback procedures.
- Redacted OpenTelemetry traces and append-only structured audit events.
- Human-facing evidence, uncertainty, blast radius, and rollback before approval.

The complete agent portfolio, secure skill contract, evaluation gates, and
implementation phases are maintained in
[`docs/AGENT_ROADMAP.md`](https://github.com/waitesgithub/dockprom-ai/blob/main/docs/AGENT_ROADMAP.md).
Use the [OWASP agent, MCP, and RAG controls](../security/owasp-agent-controls.md)
as the mandatory design and release checklist.
