---
id: telemetry-contract
title: AI Telemetry Contract
---

# AI telemetry contract

The custom dashboards use this placeholder contract. Applications must emit
these metrics before the corresponding panels populate.

## OpenTelemetry Generative AI

Instrument model operations with the pinned version of the
[OpenTelemetry Generative AI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/).
The Prometheus exporter typically translates dotted OpenTelemetry metric names
to underscore-separated names.

Expected metrics include:

- `gen_ai_client_operation_duration_seconds`
- `gen_ai_client_token_usage_total`
- `dockprom_ai_genai_time_to_first_token_seconds`
- `dockprom_ai_genai_context_utilization_ratio`
- `dockprom_ai_genai_queue_depth`
- `dockprom_ai_genai_model_load_duration_seconds`

Expected bounded attributes include model, operation, token type, error type,
and service. Do not attach prompt or response content.

## Workflow and RAG metrics

- `dockprom_ai_workflow_total{outcome}`
- `dockprom_ai_workflow_duration_seconds`
- `dockprom_ai_workflow_stage_total{stage}`
- `dockprom_ai_workflow_stage_duration_seconds{stage}`
- `dockprom_ai_workflow_errors_total{stage,error_type}`
- `dockprom_ai_chainlit_active_sessions`
- `dockprom_ai_stream_total{outcome}`
- `dockprom_ai_genui_component_intent_total{component_type}`
- `dockprom_ai_openui_navigation_total`
- `dockprom_ai_rag_retrieval_total{outcome,service}`
- `dockprom_ai_rag_retrieval_duration_seconds`
- `dockprom_ai_rag_similarity_score{service}`

## Security and MCP metrics

- `dockprom_ai_security_detection_total`
- `dockprom_ai_mcp_tool_invocation_total`
- `dockprom_ai_mcp_tool_duration_seconds`
- `dockprom_ai_mcp_confirmation_total`
- `dockprom_ai_mcp_jsonrpc_error_total`
- `dockprom_ai_service_public_bind`
- `dockprom_ai_agent_run_total`
- `dockprom_ai_agent_tool_call_total`
- `dockprom_ai_agent_policy_decision_total`
- `dockprom_ai_agent_approval_total`
- `dockprom_ai_agent_delegation_depth`
- `dockprom_ai_agent_budget_exhausted_total`
- `dockprom_ai_agent_safety_action_total`
- `dockprom_ai_agent_security_event_total`

Use bounded labels such as detection type, severity, policy action, tool name,
tool risk, outcome, and error code. User/session identity belongs in restricted
structured events as a hash, not in Prometheus.

## Structured security event fields

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

Raw prompts, responses, runbook content, credentials, and PII must not be
included unless an explicitly approved, access-controlled redaction and
retention policy is in place.
