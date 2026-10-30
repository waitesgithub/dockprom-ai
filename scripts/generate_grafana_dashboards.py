#!/usr/bin/env python3
"""Generate the provisioned Dockprom-AI Grafana dashboards.

The dashboards intentionally reference a documented metrics contract. Panels
show no data until their corresponding optional exporter or application
instrumentation is enabled.
"""

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "grafana" / "dashboards"


def prometheus_target(expression: str, legend: str = "{{service_name}}") -> dict[str, Any]:
    return {
        "datasource": {"type": "prometheus", "uid": "prometheus"},
        "editorMode": "code",
        "expr": expression,
        "legendFormat": legend,
        "range": True,
        "refId": "A",
    }


def loki_target(expression: str) -> dict[str, Any]:
    return {
        "datasource": {"type": "loki", "uid": "loki"},
        "editorMode": "code",
        "expr": expression,
        "queryType": "range",
        "refId": "A",
    }


def postgres_target(sql: str, table: bool = False) -> dict[str, Any]:
    return {
        "datasource": {"type": "postgres", "uid": "postgres"},
        "editorMode": "code",
        "format": "table" if table else "time_series",
        "rawQuery": True,
        "rawSql": sql,
        "refId": "A",
    }


def tempo_target(query: str) -> dict[str, Any]:
    return {
        "datasource": {"type": "tempo", "uid": "tempo"},
        "query": query,
        "queryType": "traceql",
        "refId": "A",
        "tableType": "traces",
    }


def panel(
    panel_id: int,
    title: str,
    kind: str,
    datasource: str,
    query: str,
    description: str,
    unit: str = "short",
    legend: str = "{{service_name}}",
) -> dict[str, Any]:
    width = 6 if kind == "stat" else 12
    height = 5 if kind == "stat" else 8
    if kind == "logs":
        target = loki_target(query)
    elif datasource == "postgres":
        target = postgres_target(query, table=kind == "table")
    elif datasource == "tempo":
        target = tempo_target(query)
    else:
        target = prometheus_target(query, legend)

    result: dict[str, Any] = {
        "datasource": {"type": datasource, "uid": datasource},
        "description": description,
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "palette-classic"},
                "custom": {},
                "mappings": [],
                "thresholds": {
                    "mode": "absolute",
                    "steps": [
                        {"color": "green", "value": None},
                        {"color": "yellow", "value": 0.8},
                        {"color": "red", "value": 0.95},
                    ],
                },
                "unit": unit,
            },
            "overrides": [],
        },
        "gridPos": {"h": height, "w": width, "x": 0, "y": 0},
        "id": panel_id,
        "options": {},
        "targets": [target],
        "title": title,
        "type": kind,
    }
    if kind == "stat":
        result["options"] = {
            "colorMode": "value",
            "graphMode": "area",
            "justifyMode": "auto",
            "orientation": "auto",
            "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
            "textMode": "auto",
        }
    elif kind == "timeseries":
        result["options"] = {
            "legend": {"calcs": ["lastNotNull"], "displayMode": "table", "placement": "bottom"},
            "tooltip": {"mode": "multi", "sort": "desc"},
        }
    elif kind == "logs":
        result["options"] = {
            "dedupStrategy": "none",
            "enableLogDetails": True,
            "prettifyLogMessage": True,
            "showCommonLabels": False,
            "showLabels": False,
            "showTime": True,
            "sortOrder": "Descending",
            "wrapLogMessage": True,
        }
    elif kind == "table":
        result["options"] = {"cellHeight": "sm", "showHeader": True}
    return result


def layout(panels: list[dict[str, Any]]) -> None:
    x = 0
    y = 0
    row_height = 0
    for item in panels:
        width = item["gridPos"]["w"]
        height = item["gridPos"]["h"]
        if x + width > 24:
            x = 0
            y += row_height
            row_height = 0
        item["gridPos"].update({"x": x, "y": y})
        x += width
        row_height = max(row_height, height)


def dashboard(uid: str, title: str, tags: list[str], specs: list[tuple[Any, ...]]) -> dict[str, Any]:
    panels = [panel(index, *spec) for index, spec in enumerate(specs, start=1)]
    layout(panels)
    return {
        "annotations": {
            "list": [
                {
                    "builtIn": 1,
                    "datasource": {"type": "grafana", "uid": "-- Grafana --"},
                    "enable": True,
                    "hide": True,
                    "iconColor": "rgba(0, 211, 255, 1)",
                    "name": "Annotations & Alerts",
                    "type": "dashboard",
                }
            ]
        },
        "description": f"Dockprom-AI: {title}. Placeholder panels follow the documented telemetry contract.",
        "editable": False,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 1,
        "id": None,
        "links": [],
        "liveNow": False,
        "panels": panels,
        "refresh": "30s",
        "schemaVersion": 42,
        "tags": ["dockprom-ai", *tags],
        "templating": {"list": []},
        "time": {"from": "now-6h", "to": "now"},
        "timepicker": {},
        "timezone": "browser",
        "title": title,
        "uid": uid,
        "version": 1,
        "weekStart": "",
    }


DASHBOARDS: dict[str, dict[str, Any]] = {
    "ai-operations-command-center.json": dashboard(
        "dockprom-ai-command",
        "AI Operations Command Center",
        ["overview", "slo"],
        [
            ("Service availability", "stat", "prometheus", 'avg(up{stack="dockprom-ai"})', "Availability across Dockprom-AI scrape targets.", "percentunit"),
            ("AI workflow success rate", "stat", "prometheus", "sum(rate(dockprom_ai_workflow_total{outcome=\"success\"}[5m])) / clamp_min(sum(rate(dockprom_ai_workflow_total[5m])), 1)", "Completed AI workflows divided by all workflows.", "percentunit"),
            ("End-to-end p95 latency", "stat", "prometheus", "histogram_quantile(0.95, sum by (le) (rate(dockprom_ai_workflow_duration_seconds_bucket[5m])))", "User-perceived workflow latency.", "s"),
            ("RAG retrieval success", "stat", "prometheus", "sum(rate(dockprom_ai_rag_retrieval_total{outcome=\"success\"}[5m])) / clamp_min(sum(rate(dockprom_ai_rag_retrieval_total[5m])), 1)", "Successful runbook retrieval rate.", "percentunit"),
            ("Workflow rate by stage", "timeseries", "prometheus", "sum by (stage) (rate(dockprom_ai_workflow_stage_total[5m]))", "Throughput through each workflow stage.", "ops", "{{stage}}"),
            ("Error rate by service", "timeseries", "prometheus", "sum by (service_name) (rate(dockprom_ai_errors_total[5m]))", "Application errors grouped by service.", "ops"),
            ("Firing alerts", "table", "prometheus", 'ALERTS{alertstate="firing"}', "Currently firing Prometheus alerts.", "short", "{{alertname}}"),
            ("Slow AI traces", "table", "tempo", '{ resource.service.name =~ "chainlit-genui|ollama-gateway|open-intelligent-ui" && duration > 5s }', "TraceQL view of slow AI workflows."),
        ],
    ),
    "ollama-inference-model-performance.json": dashboard(
        "dockprom-ollama-inference",
        "Ollama Inference and Model Performance",
        ["ollama", "genai"],
        [
            ("Request rate", "stat", "prometheus", 'sum(rate(gen_ai_client_operation_duration_seconds_count{gen_ai_system="ollama"}[5m]))', "OpenTelemetry GenAI client operation rate.", "reqps"),
            ("p95 operation latency", "stat", "prometheus", 'histogram_quantile(0.95, sum by (le) (rate(gen_ai_client_operation_duration_seconds_bucket{gen_ai_system="ollama"}[5m])))', "OpenTelemetry GenAI operation duration.", "s"),
            ("p95 time to first token", "stat", "prometheus", "histogram_quantile(0.95, sum by (le) (rate(dockprom_ai_genai_time_to_first_token_seconds_bucket[5m])))", "Time until the first streamed token.", "s"),
            ("Output tokens per second", "stat", "prometheus", 'sum(rate(gen_ai_client_token_usage_total{gen_ai_token_type="output"}[5m]))', "Generated token throughput.", "ops"),
            ("Latency by model", "timeseries", "prometheus", "histogram_quantile(0.95, sum by (le, gen_ai_request_model) (rate(gen_ai_client_operation_duration_seconds_bucket[5m])))", "p95 operation latency by requested model.", "s", "{{gen_ai_request_model}}"),
            ("Input and output token usage", "timeseries", "prometheus", "sum by (gen_ai_token_type, gen_ai_request_model) (rate(gen_ai_client_token_usage_total[5m]))", "OpenTelemetry GenAI token usage by type and model.", "ops", "{{gen_ai_request_model}} {{gen_ai_token_type}}"),
            ("Context-window utilization", "timeseries", "prometheus", "max by (gen_ai_request_model) (dockprom_ai_genai_context_utilization_ratio)", "Used tokens divided by configured context window.", "percentunit", "{{gen_ai_request_model}}"),
            ("Queue depth", "timeseries", "prometheus", "sum by (gen_ai_request_model) (dockprom_ai_genai_queue_depth)", "Waiting inference operations.", "short", "{{gen_ai_request_model}}"),
            ("Model load duration", "timeseries", "prometheus", "histogram_quantile(0.95, sum by (le, gen_ai_request_model) (rate(dockprom_ai_genai_model_load_duration_seconds_bucket[15m])))", "Cold-start and model-load latency.", "s", "{{gen_ai_request_model}}"),
            ("Inference errors", "logs", "loki", '{service_name=~"ollama-gateway|chainlit-genui"} | json | level=~"error|critical"', "Inference errors with trace correlation."),
        ],
    ),
    "genui-end-to-end-experience.json": dashboard(
        "dockprom-genui-e2e",
        "GenUI End-to-End Experience",
        ["genui", "chainlit", "openui"],
        [
            ("Active conversations", "stat", "prometheus", "sum(dockprom_ai_chainlit_active_sessions)", "Current Chainlit sessions."),
            ("Completion rate", "stat", "prometheus", 'sum(rate(dockprom_ai_workflow_total{outcome="success"}[5m])) / clamp_min(sum(rate(dockprom_ai_workflow_total[5m])), 1)', "Successful conversation workflows.", "percentunit"),
            ("p95 end-to-end latency", "stat", "prometheus", "histogram_quantile(0.95, sum by (le) (rate(dockprom_ai_workflow_duration_seconds_bucket[5m])))", "Message receipt through response completion.", "s"),
            ("Streaming interruption rate", "stat", "prometheus", 'sum(rate(dockprom_ai_stream_total{outcome="interrupted"}[5m]))', "Interrupted streaming responses.", "ops"),
            ("Stage latency", "timeseries", "prometheus", "histogram_quantile(0.95, sum by (le, stage) (rate(dockprom_ai_workflow_stage_duration_seconds_bucket[5m])))", "Embedding, retrieval, first-token and render-stage latency.", "s", "{{stage}}"),
            ("Widget-intent detections", "timeseries", "prometheus", "sum by (component_type) (rate(dockprom_ai_genui_component_intent_total[5m]))", "Responses that request a GenUI component.", "ops", "{{component_type}}"),
            ("OpenUI navigation rate", "timeseries", "prometheus", "sum(rate(dockprom_ai_openui_navigation_total[5m]))", "Users following the OpenUI link.", "ops"),
            ("Workflow errors by stage", "timeseries", "prometheus", "sum by (stage, error_type) (rate(dockprom_ai_workflow_errors_total[5m]))", "Errors grouped by workflow stage.", "ops", "{{stage}} {{error_type}}"),
            ("Slow GenUI traces", "table", "tempo", '{ resource.service.name =~ "chainlit-genui|open-intelligent-ui" && duration > 3s }', "Slow end-to-end user journeys."),
        ],
    ),
    "rag-pgvector-quality.json": dashboard(
        "dockprom-rag-quality",
        "RAG and pgvector Quality",
        ["rag", "pgvector"],
        [
            ("Retrieval success rate", "stat", "prometheus", 'sum(rate(dockprom_ai_rag_retrieval_total{outcome="success"}[5m])) / clamp_min(sum(rate(dockprom_ai_rag_retrieval_total[5m])), 1)', "Successful retrievals.", "percentunit"),
            ("Empty-result rate", "stat", "prometheus", 'sum(rate(dockprom_ai_rag_retrieval_total{outcome="empty"}[5m])) / clamp_min(sum(rate(dockprom_ai_rag_retrieval_total[5m])), 1)', "Queries with no matching runbook.", "percentunit"),
            ("p95 retrieval latency", "stat", "prometheus", "histogram_quantile(0.95, sum by (le) (rate(dockprom_ai_rag_retrieval_duration_seconds_bucket[5m])))", "Embedding plus vector search latency.", "s"),
            ("Runbook corpus size", "stat", "postgres", "SELECT count(*) AS value FROM operational_runbooks;", "Number of indexed runbooks."),
            ("Similarity-score distribution", "timeseries", "prometheus", "histogram_quantile(0.5, sum by (le, service) (rate(dockprom_ai_rag_similarity_score_bucket[15m])))", "Median retrieved similarity without exposing document content.", "short", "{{service}}"),
            ("Low-confidence retrievals", "timeseries", "prometheus", 'sum by (service) (rate(dockprom_ai_rag_retrieval_total{outcome="below_threshold"}[5m]))', "Retrievals below the configured relevance threshold.", "ops", "{{service}}"),
            ("Runbooks by service", "table", "postgres", "SELECT service, count(*) AS runbooks, max(updated_at) AS newest FROM operational_runbooks GROUP BY service ORDER BY runbooks DESC;", "Corpus coverage and freshness."),
            ("Database connections", "timeseries", "prometheus", 'sum by (datname, state) (pg_stat_activity_count{datname="rag_storage"})', "Connections to the RAG database.", "short", "{{state}}"),
            ("Vector-search failures", "logs", "loki", '{service_name="chainlit-genui"} | json | event_action="rag.retrieve" | event_outcome="failure"', "Structured RAG failures."),
        ],
    ),
    "ai-security-detection-center.json": dashboard(
        "dockprom-ai-security",
        "AI Security Detection Center",
        ["security", "genai"],
        [
            ("Critical detections", "stat", "prometheus", 'sum(increase(dockprom_ai_security_detection_total{security_severity="critical"}[24h]))', "Critical AI security detections in the last day."),
            ("Blocked requests", "stat", "prometheus", 'sum(rate(dockprom_ai_security_detection_total{policy_action="block"}[5m]))', "Requests blocked by AI policy.", "ops"),
            ("Prompt injection attempts", "timeseries", "prometheus", 'sum by (security_severity) (rate(dockprom_ai_security_detection_total{security_detection_type="prompt_injection"}[5m]))', "Prompt-injection detections by severity.", "ops", "{{security_severity}}"),
            ("Jailbreak attempts", "timeseries", "prometheus", 'sum by (security_severity) (rate(dockprom_ai_security_detection_total{security_detection_type="jailbreak"}[5m]))', "Jailbreak detections.", "ops", "{{security_severity}}"),
            ("Sensitive-data leakage", "timeseries", "prometheus", 'sum by (security_detection_type) (rate(dockprom_ai_security_detection_total{security_detection_type=~"secret_leakage|pii_leakage"}[5m]))', "Secret or PII leakage detections.", "ops", "{{security_detection_type}}"),
            ("Detections by policy and action", "timeseries", "prometheus", "sum by (policy_name, policy_action) (rate(dockprom_ai_security_detection_total[5m]))", "Policy decision activity.", "ops", "{{policy_name}} {{policy_action}}"),
            ("Suspicious AI events", "logs", "loki", '{job="ai-security"} | json | security_severity=~"high|critical"', "Structured events should include event.action, event.outcome, security.detection.type, security.severity, gen_ai.operation.name, gen_ai.request.model, session.id_hash, user.id_hash, source.ip, tool.name, tool.risk, policy.name, policy.action and trace_id."),
            ("AI attack traces", "table", "tempo", '{ span.security.severity =~ "high|critical" }', "Trace-correlated high-severity detections."),
        ],
    ),
    "mcp-tool-security-audit.json": dashboard(
        "dockprom-mcp-security",
        "MCP Tool Security and Audit",
        ["mcp", "security"],
        [
            ("Tool invocation rate", "stat", "prometheus", "sum(rate(dockprom_ai_mcp_tool_invocation_total[5m]))", "All MCP tool calls.", "ops"),
            ("Denied tool calls", "stat", "prometheus", 'sum(rate(dockprom_ai_mcp_tool_invocation_total{outcome="denied"}[5m]))', "Policy-denied calls.", "ops"),
            ("Confirmation rejection rate", "stat", "prometheus", 'sum(rate(dockprom_ai_mcp_confirmation_total{decision="rejected"}[5m])) / clamp_min(sum(rate(dockprom_ai_mcp_confirmation_total[5m])), 1)', "Operator rejection rate.", "percentunit"),
            ("High-risk tool attempts", "stat", "prometheus", 'sum(rate(dockprom_ai_mcp_tool_invocation_total{tool_risk=~"high|critical"}[5m]))', "High-risk tool invocation attempts.", "ops"),
            ("Tool latency", "timeseries", "prometheus", "histogram_quantile(0.95, sum by (le, server_name, tool_name) (rate(dockprom_ai_mcp_tool_duration_seconds_bucket[5m])))", "p95 duration by MCP tool.", "s", "{{server_name}} {{tool_name}}"),
            ("Outcome by tool", "timeseries", "prometheus", "sum by (tool_name, outcome) (rate(dockprom_ai_mcp_tool_invocation_total[5m]))", "Successful, failed, denied and timed-out calls.", "ops", "{{tool_name}} {{outcome}}"),
            ("JSON-RPC errors", "timeseries", "prometheus", "sum by (rpc_code) (rate(dockprom_ai_mcp_jsonrpc_error_total[5m]))", "JSON-RPC protocol errors.", "ops", "{{rpc_code}}"),
            ("MCP audit events", "logs", "loki", '{job="mcp-audit"} | json', "Prompt-to-tool-to-result audit trail with pseudonymous identities."),
            ("Tool execution traces", "table", "tempo", '{ span.mcp.tool.name != nil }', "MCP tool execution traces."),
        ],
    ),
    "postgresql-pgvector-operations.json": dashboard(
        "dockprom-postgres-pgvector",
        "PostgreSQL and pgvector Operations",
        ["postgresql", "pgvector"],
        [
            ("PostgreSQL availability", "stat", "prometheus", "pg_up", "Postgres exporter availability."),
            ("Active connections", "stat", "prometheus", "sum(pg_stat_activity_count)", "Current database connections."),
            ("Cache hit ratio", "stat", "prometheus", "sum(rate(pg_stat_database_blks_hit[5m])) / clamp_min(sum(rate(pg_stat_database_blks_hit[5m]) + rate(pg_stat_database_blks_read[5m])), 1)", "Buffer cache effectiveness.", "percentunit"),
            ("Deadlocks", "stat", "prometheus", "sum(increase(pg_stat_database_deadlocks[1h]))", "Deadlocks in the last hour."),
            ("Transactions", "timeseries", "prometheus", "sum by (datname) (rate(pg_stat_database_xact_commit[5m]) + rate(pg_stat_database_xact_rollback[5m]))", "Transaction throughput.", "ops", "{{datname}}"),
            ("Database size", "timeseries", "prometheus", "pg_database_size_bytes", "Database storage consumption.", "bytes", "{{datname}}"),
            ("Long-running queries", "table", "postgres", "SELECT pid, datname, usename, now() - query_start AS duration, left(query, 180) AS query FROM pg_stat_activity WHERE state <> 'idle' AND query_start < now() - interval '30 seconds' ORDER BY query_start;", "Queries running longer than 30 seconds."),
            ("Largest indexes", "table", "postgres", "SELECT schemaname, relname, indexrelname, pg_size_pretty(pg_relation_size(indexrelid)) AS size FROM pg_stat_user_indexes ORDER BY pg_relation_size(indexrelid) DESC LIMIT 20;", "Largest indexes, including vector indexes."),
            ("Autovacuum activity", "timeseries", "prometheus", "sum by (datname) (pg_stat_database_tup_updated + pg_stat_database_tup_deleted)", "Tuple churn requiring vacuum attention.", "short", "{{datname}}"),
        ],
    ),
    "edge-auth-api-security.json": dashboard(
        "dockprom-edge-security",
        "Edge Authentication and API Security",
        ["caddy", "security"],
        [
            ("Request rate", "stat", "prometheus", "sum(rate(caddy_http_requests_total[5m]))", "Caddy ingress request rate.", "reqps"),
            ("Authentication failures", "stat", "prometheus", 'sum(rate(caddy_http_requests_total{code=~"401|403"}[5m]))', "Unauthorized and forbidden requests.", "reqps"),
            ("Upstream 5xx rate", "stat", "prometheus", 'sum(rate(caddy_http_requests_total{code=~"5.."}[5m]))', "Ingress server errors.", "reqps"),
            ("TLS certificate expiry", "stat", "prometheus", "min(caddy_tls_certificate_expiration_timestamp_seconds - time())", "Minimum remaining certificate lifetime.", "s"),
            ("Responses by route and status", "timeseries", "prometheus", "sum by (handler, code) (rate(caddy_http_requests_total[5m]))", "Request outcomes by route.", "reqps", "{{handler}} {{code}}"),
            ("Authentication failures by source", "logs", "loki", '{service_name="caddy"} | json | status=~"401|403"', "Repeated failures and brute-force candidates."),
            ("Path scanning", "logs", "loki", '{service_name="caddy"} | json | status="404"', "Repeated 404 requests and suspicious paths."),
            ("Unexpected public bind", "stat", "prometheus", 'max(dockprom_ai_service_public_bind{service_name=~"chainlit-genui|open-intelligent-ui"})', "One indicates an AI UI service is exposed beyond loopback."),
        ],
    ),
    "incident-response-effectiveness.json": dashboard(
        "dockprom-incident-response",
        "Incident Response Effectiveness",
        ["keep", "alertmanager", "mattermost"],
        [
            ("Firing alerts", "stat", "prometheus", 'count(ALERTS{alertstate="firing"})', "Currently firing alerts."),
            ("Incidents opened", "stat", "prometheus", "sum(increase(dockprom_ai_incident_total[24h]))", "Incidents created in 24 hours."),
            ("Median time to acknowledge", "stat", "prometheus", "histogram_quantile(0.5, sum by (le) (rate(dockprom_ai_incident_acknowledge_duration_seconds_bucket[24h])))", "MTTA.", "s"),
            ("Median time to resolve", "stat", "prometheus", "histogram_quantile(0.5, sum by (le) (rate(dockprom_ai_incident_resolution_duration_seconds_bucket[24h])))", "MTTR.", "s"),
            ("Alert outcomes", "timeseries", "prometheus", "sum by (outcome) (rate(dockprom_ai_alert_processing_total[5m]))", "Grouped, inhibited, correlated and notified alerts.", "ops", "{{outcome}}"),
            ("Incidents by severity", "timeseries", "prometheus", "sum by (severity) (increase(dockprom_ai_incident_total[1h]))", "Incident creation by severity.", "short", "{{severity}}"),
            ("Notification failures", "timeseries", "prometheus", 'sum by (destination) (rate(dockprom_ai_notification_total{outcome="failure"}[5m]))', "Mattermost and other notification failures.", "ops", "{{destination}}"),
            ("Alerts without runbooks", "stat", "prometheus", 'sum(dockprom_ai_alert_runbook_mapping{mapped="false"})', "Active alert types lacking a runbook."),
            ("Incident timeline", "logs", "loki", '{job=~"keep|alertmanager|mattermost"} | json | event_action=~"incident.*|alert.*|notification.*"', "Cross-system incident timeline."),
        ],
    ),
    "opentelemetry-signal-quality.json": dashboard(
        "dockprom-otel-quality",
        "OpenTelemetry Signal Quality",
        ["opentelemetry", "quality"],
        [
            ("Accepted telemetry", "stat", "prometheus", "sum(rate(otelcol_receiver_accepted_spans[5m]) + rate(otelcol_receiver_accepted_metric_points[5m]) + rate(otelcol_receiver_accepted_log_records[5m]))", "Accepted signals across receivers.", "ops"),
            ("Refused telemetry", "stat", "prometheus", "sum(rate(otelcol_receiver_refused_spans[5m]) + rate(otelcol_receiver_refused_metric_points[5m]) + rate(otelcol_receiver_refused_log_records[5m]))", "Receiver-refused telemetry.", "ops"),
            ("Export failures", "stat", "prometheus", "sum(rate(otelcol_exporter_send_failed_spans[5m]) + rate(otelcol_exporter_send_failed_metric_points[5m]) + rate(otelcol_exporter_send_failed_log_records[5m]))", "Failed export operations.", "ops"),
            ("Queue utilization", "stat", "prometheus", "max(otelcol_exporter_queue_size / clamp_min(otelcol_exporter_queue_capacity, 1))", "Highest exporter queue utilization.", "percentunit"),
            ("Signal throughput", "timeseries", "prometheus", "sum by (receiver) (rate(otelcol_receiver_accepted_spans[5m]))", "Span throughput by receiver.", "ops", "{{receiver}}"),
            ("Dropped telemetry", "timeseries", "prometheus", "sum by (exporter) (rate(otelcol_exporter_send_failed_spans[5m]))", "Dropped spans by exporter.", "ops", "{{exporter}}"),
            ("Missing service.name", "timeseries", "prometheus", 'sum(rate(dockprom_ai_telemetry_quality_total{issue="missing_service_name"}[5m]))', "Telemetry without service identity.", "ops"),
            ("High-cardinality attributes", "table", "prometheus", "topk(20, dockprom_ai_telemetry_attribute_cardinality)", "Attributes contributing the most series cardinality.", "short", "{{attribute_name}}"),
            ("Orphan and incomplete traces", "timeseries", "prometheus", "sum by (issue) (rate(dockprom_ai_trace_quality_total[5m]))", "Orphan spans, missing parents and errors without logs.", "ops", "{{issue}}"),
        ],
    ),
    "gpu-model-capacity.json": dashboard(
        "dockprom-gpu-capacity",
        "GPU and Model Capacity",
        ["gpu", "capacity"],
        [
            ("GPU utilization", "stat", "prometheus", "avg(DCGM_FI_DEV_GPU_UTIL) / 100", "Average NVIDIA GPU utilization; use vendor-equivalent metrics for AMD or Intel.", "percentunit"),
            ("Framebuffer utilization", "stat", "prometheus", "sum(DCGM_FI_DEV_FB_USED) / clamp_min(sum(DCGM_FI_DEV_FB_USED + DCGM_FI_DEV_FB_FREE), 1)", "GPU memory utilization.", "percentunit"),
            ("Maximum temperature", "stat", "prometheus", "max(DCGM_FI_DEV_GPU_TEMP)", "Maximum GPU temperature.", "celsius"),
            ("Power draw", "stat", "prometheus", "sum(DCGM_FI_DEV_POWER_USAGE)", "Total GPU power.", "watt"),
            ("GPU utilization by device", "timeseries", "prometheus", "DCGM_FI_DEV_GPU_UTIL / 100", "Utilization by GPU.", "percentunit", "GPU {{gpu}}"),
            ("Memory by device", "timeseries", "prometheus", "DCGM_FI_DEV_FB_USED * 1024 * 1024", "Used framebuffer memory.", "bytes", "GPU {{gpu}}"),
            ("Thermal and power throttling", "timeseries", "prometheus", "increase(DCGM_FI_DEV_XID_ERRORS[5m])", "Hardware error/throttling indicators.", "short", "GPU {{gpu}}"),
            ("Queue depth versus GPU saturation", "timeseries", "prometheus", "sum(dockprom_ai_genai_queue_depth)", "Inference backlog for capacity correlation.", "short", "Queue"),
            ("Tokens per second", "timeseries", "prometheus", 'sum by (gen_ai_request_model) (rate(gen_ai_client_token_usage_total{gen_ai_token_type="output"}[5m]))', "Model throughput for capacity planning.", "ops", "{{gen_ai_request_model}}"),
        ],
    ),
    "agent-harness-security-operations.json": dashboard(
        "dockprom-agent-harness",
        "Agent Harness Security and Operations",
        ["agents", "owasp", "security"],
        [
            ("Agent run rate", "stat", "prometheus", "sum(rate(dockprom_ai_agent_run_total[5m]))", "Agent runs across all bounded agent types.", "ops"),
            ("Agent success rate", "stat", "prometheus", 'sum(rate(dockprom_ai_agent_run_total{outcome="success"}[5m])) / clamp_min(sum(rate(dockprom_ai_agent_run_total[5m])), 1)', "Verified successful runs divided by all runs.", "percentunit"),
            ("Goal-drift detections", "stat", "prometheus", 'sum(rate(dockprom_ai_agent_security_event_total{event_type="goal_drift"}[5m]))', "Runs terminated for leaving the declared objective.", "ops"),
            ("Policy denials", "stat", "prometheus", 'sum(rate(dockprom_ai_agent_policy_decision_total{decision="deny"}[5m]))', "Tool or plan decisions denied by deterministic policy.", "ops"),
            ("Runs by agent and outcome", "timeseries", "prometheus", "sum by (agent_name, outcome) (rate(dockprom_ai_agent_run_total[5m]))", "Agent run outcomes by bounded agent identity.", "ops", "{{agent_name}} {{outcome}}"),
            ("Tool outcomes by agent", "timeseries", "prometheus", "sum by (agent_name, tool_name, outcome) (rate(dockprom_ai_agent_tool_call_total[5m]))", "Successful, failed, denied, and timed-out tool calls.", "ops", "{{agent_name}} {{tool_name}} {{outcome}}"),
            ("Approval decisions", "timeseries", "prometheus", "sum by (agent_name, decision) (rate(dockprom_ai_agent_approval_total[5m]))", "Accepted, rejected, expired, and replay-blocked approvals.", "ops", "{{agent_name}} {{decision}}"),
            ("Delegation depth", "timeseries", "prometheus", "max by (agent_name) (dockprom_ai_agent_delegation_depth)", "Maximum inter-agent delegation depth.", "short", "{{agent_name}}"),
            ("Budget exhaustion", "timeseries", "prometheus", "sum by (agent_name, budget_type) (rate(dockprom_ai_agent_budget_exhausted_total[5m]))", "Step, tool, token, retry, duration, or cost limits reached.", "ops", "{{agent_name}} {{budget_type}}"),
            ("Circuit breakers and rollbacks", "timeseries", "prometheus", "sum by (agent_name, action) (rate(dockprom_ai_agent_safety_action_total[5m]))", "Kill-switch, circuit-breaker, rollback, and quarantine activity.", "ops", "{{agent_name}} {{action}}"),
            ("Agent security events", "logs", "loki", '{job="agent-audit"} | json | security_severity=~"medium|high|critical"', "Redacted, structured harness events mapped to OWASP agentic risks."),
            ("Agent execution traces", "table", "tempo", '{ span.agent.name != nil }', "Agent, policy, approval, tool, verification, and rollback traces."),
        ],
    ),
    "runtime-supply-chain-security.json": dashboard(
        "dockprom-runtime-security",
        "Runtime and Supply-Chain Security",
        ["falco", "trivy", "security"],
        [
            ("Critical runtime detections", "stat", "prometheus", 'sum(rate(falcosecurity_falcosidekick_falco_events_total{priority="Critical"}[5m]))', "Critical Falco events.", "ops"),
            ("Critical vulnerabilities", "stat", "prometheus", 'sum(trivy_image_vulnerabilities{severity="Critical"})', "Critical image vulnerabilities from a Trivy metrics adapter or generated textfile metrics."),
            ("Unsigned images", "stat", "prometheus", 'sum(dockprom_ai_image_compliance{signed="false"})', "Images failing signature policy."),
            ("Root containers", "stat", "prometheus", 'sum(dockprom_ai_container_compliance{runs_as_root="true"})', "Containers running as root."),
            ("Falco events by rule", "timeseries", "prometheus", "sum by (rule, priority) (rate(falcosecurity_falcosidekick_falco_events_total[5m]))", "Runtime detections by rule and priority.", "ops", "{{priority}} {{rule}}"),
            ("Vulnerabilities by severity", "timeseries", "prometheus", "sum by (severity) (trivy_image_vulnerabilities)", "Current image vulnerability inventory.", "short", "{{severity}}"),
            ("Runtime security events", "logs", "loki", '{job="falco"} | json', "Falco events shipped to Loki through stdout or Falcosidekick."),
            ("Supply-chain scan events", "logs", "loki", '{job="trivy"} | json', "Trivy JSON scan summaries shipped to Loki."),
        ],
    ),
}


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    expected = set(DASHBOARDS)
    for existing in OUTPUT.glob("*.json"):
        if existing.name not in expected:
            existing.unlink()
    for filename, content in DASHBOARDS.items():
        path = OUTPUT / filename
        path.write_text(json.dumps(content, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(DASHBOARDS)} dashboards in {OUTPUT}")


if __name__ == "__main__":
    main()
