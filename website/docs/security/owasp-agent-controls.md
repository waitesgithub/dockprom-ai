---
id: owasp-agent-controls
title: OWASP Agent, MCP, and RAG Controls
---

# OWASP agent, MCP, and RAG controls

All Dockprom-AI agents, skills, MCP servers, RAG pipelines, and execution
containers must follow these references:

- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)
- [OWASP RAG Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [OWASP Secure AI Model Ops — Monitoring and Logging](https://cheatsheetseries.owasp.org/cheatsheets/Secure_AI_Model_Ops_Cheat_Sheet.html#7-monitoring-logging)
- [MITRE ATLAS AML.M0024 — AI Telemetry Logging and Monitoring](https://atlas.mitre.org/mitigations/AML.M0024)
- [MITRE ATLAS official dataset](https://github.com/mitre-atlas/atlas-data/blob/main/dist/ATLAS-latest.yaml)

The MITRE webpage returned HTTP 404 during repository validation on 2026-10-30;
the official ATLAS dataset remains the fallback source for AML.M0024.

## Minimum controls

| Component | Minimum controls |
| --- | --- |
| Agent | Bounded immutable goal, unique identity, least privilege, budgets, goal-drift detection, kill switch. |
| Skill | Versioned manifest, strict schemas, declared tools/resources/egress, no embedded secrets, SBOM and digest. |
| MCP server | Authenticated transport, origin/session binding, tool allowlist, parameter validation, authorization per call, complete audit. |
| RAG | Trusted ingestion, provenance, tenant isolation, poisoning/injection scanning, relevance threshold, citations, revocation. |
| Logging | Structured sanitized events, trace correlation, time sync, access control, retention, no secret or prompt leakage. |
| Container | Non-root, least capabilities, read-only filesystem, resource limits, restricted egress, no unrestricted Docker socket. |
| Model operations | Pinned model/prompt/policy versions, evaluation gates, telemetry, canary deployment, rollback. |

## Required security telemetry

Every agent run must correlate:

```text
agent.run
  -> model.operation
  -> rag.retrieve
  -> policy.decision
  -> mcp.tool.call
  -> human.approval
  -> action.execute
  -> action.verify
  -> rollback or completion
```

Record decision summaries and evidence references, not hidden chain-of-thought.
Redact credentials, PII, prompt/response content, tool payloads, and sensitive
retrieved text before telemetry leaves the process.

The complete control matrix and release checklist are maintained in
[`docs/SECURITY_CONTROL_REFERENCES.md`](https://github.com/waitesgithub/dockprom-ai/blob/main/docs/SECURITY_CONTROL_REFERENCES.md).
