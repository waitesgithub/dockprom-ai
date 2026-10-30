# AI, Agent, MCP, RAG, and Runtime Security References

These sources are normative security references for Dockprom-AI agent, skill,
MCP, RAG, observability, container, and model-operations design. A change that
affects these components must document the applicable controls and verification
evidence during review.

## Required references

1. [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
2. [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)
3. [OWASP RAG Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html)
4. [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
5. [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
6. [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
7. [OWASP Secure AI Model Ops Cheat Sheet — Monitoring and Logging](https://cheatsheetseries.owasp.org/cheatsheets/Secure_AI_Model_Ops_Cheat_Sheet.html#7-monitoring-logging)
8. [MITRE ATLAS AML.M0024 — AI Telemetry Logging and Monitoring](https://atlas.mitre.org/mitigations/AML.M0024)
9. [MITRE ATLAS official data repository](https://github.com/mitre-atlas/atlas-data/blob/main/dist/ATLAS-latest.yaml)

The supplied MITRE ATLAS webpage returned HTTP 404 during validation on
2026-10-30, while the official ATLAS changelog and dataset still identify
AML.M0024 as **AI Telemetry Logging and Monitoring**. The canonical link is kept
for when the website route is restored; the official dataset is the fallback.

## Control traceability matrix

| Area | Required controls | Primary references | Verification evidence |
| --- | --- | --- | --- |
| Agent goals | Immutable bounded goal, prompt/data separation, goal-drift detection, maximum steps | AI Agent Security; Prompt Injection Prevention | Goal hash, drift event, termination test |
| Agent identity | Unique workload identity, least privilege, deny-by-default authorization | AI Agent Security; MCP Security | Identity claim, policy decision, denied-call test |
| Tool execution | Strict schemas, allowlists, parameter validation, timeouts, rate limits, approval binding | MCP Security; AI Agent Security | Tool schema tests, OPA tests, approval replay test |
| MCP transport | Authenticated clients/servers, TLS, origin validation, session binding, SSRF protection | MCP Security | Transport tests, endpoint policy, connection audit |
| MCP lifecycle | Server/tool inventory, version pinning, capability review, revocation, audit | MCP Security; Secure AI Model Ops | Registry digest, SBOM, review record |
| RAG ingestion | Provenance, classification, malware/injection scanning, quarantine, trusted sources | RAG Security; Prompt Injection Prevention | Ingestion decision, source hash, quarantine test |
| RAG retrieval | Tenant isolation, authorization before retrieval, relevance thresholds, citations | RAG Security | Cross-tenant test, retrieval trace, citation check |
| RAG output | Treat documents as data, block embedded instructions, redact sensitive context | RAG Security; Prompt Injection Prevention | Injection corpus tests, redaction tests |
| Memory | Namespace, provenance, classification, expiry, revocation, poisoning detection | AI Agent Security; RAG Security | Isolation tests, memory lineage, revocation exercise |
| Inter-agent messages | Mutual authentication, typed schema, expiry, delegation limits, no privilege transfer | AI Agent Security | Message validation tests, delegation graph |
| Container isolation | Non-root, least capabilities, read-only filesystem, resource limits, restricted socket/egress | Docker Security | Compose policy checks, runtime security scan |
| Model lifecycle | Version/digest pinning, provenance, evaluation, rollback, access control | Secure AI Model Ops | Model card, digest, evaluation and rollback evidence |
| Logging | Structured security events, time sync, sanitization, access controls, retention, availability | Logging; Secure AI Model Ops; AML.M0024 | Log schema tests, redaction tests, retention policy |
| AI telemetry | Agent/model/tool/policy/approval/verification spans and bounded metrics | Secure AI Model Ops; AML.M0024 | Trace completeness and dashboard tests |
| Sensitive data | No secrets/PII in prompts, labels, logs, traces, memory, or tool errors | Logging; RAG Security; Prompt Injection Prevention | Secret scan, redaction and negative tests |
| Supply chain | Pin dependencies, SBOM, signature/checksum validation, vulnerability scans | Secure AI Model Ops; Docker Security | Trivy results, SBOM, provenance record |
| Human approval | Evidence, uncertainty, blast radius, parameter-bound approval, reject path | AI Agent Security; MCP Security | Approval UX test, replay/substitution tests |
| Resilience | Budgets, circuit breakers, kill switches, canaries, independent verification, rollback | AI Agent Security; Secure AI Model Ops | Failure injection, kill-switch, rollback exercise |

## Mandatory review checklist

An agent, skill, or MCP server must not be approved unless all applicable items
are satisfied:

- Purpose and goals are narrow, documented, and immutable during a run.
- Identity and tool permissions are unique and least-privileged.
- Inputs, tool parameters, outputs, and inter-agent messages have strict schemas.
- Untrusted prompts, retrieved documents, logs, tool output, and webpages are
  treated as data rather than instructions.
- Read and write capabilities are separated.
- High-risk and mutating calls require parameter-bound human approval.
- MCP transport and sessions are authenticated, encrypted, origin-checked, and
  protected from SSRF and confused-deputy behavior.
- Memory and RAG are tenant-isolated, provenance-aware, revocable, and scanned
  for poisoning and indirect prompt injection.
- Containers run non-root without unrestricted Docker socket access or broad
  network egress.
- Models, prompts, policies, skills, MCP servers, and tools are versioned and
  recorded in telemetry.
- Logs are structured, sanitized, access-controlled, time-synchronized, and
  retained according to classification.
- Secrets, PII, prompts, responses, and retrieved content are not placed in
  Prometheus labels or unrestricted logs.
- Every run has correlated agent, model, retrieval, policy, tool, approval,
  verification, and rollback telemetry.
- Step, tool, token, retry, time, cost, and delegation budgets are enforced.
- Kill switch, circuit breaker, rollback, and incident-response procedures are
  tested.
- Adversarial, authorization, isolation, replay, injection, and failure tests
  pass before release.
