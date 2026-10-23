#!/usr/bin/env bash
# Verify all 7 services are healthy.
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
require_tools curl jq
TIMEOUT="${HEALTH_TIMEOUT:-120}"

echo "== Prometheus (9090)"
wait_for "health endpoint /-/healthy" "$TIMEOUT" http_ok "$PROMETHEUS_URL/-/healthy"
wait_for "ready endpoint /-/ready" "$TIMEOUT" http_ok "$PROMETHEUS_URL/-/ready"
check "has active scrape targets" bash -c \
  "curl -fsS '$PROMETHEUS_URL/api/v1/targets' | jq -e '.data.activeTargets | length > 0'"

echo "== Grafana (3000)"
wait_for "health endpoint /api/health" "$TIMEOUT" http_ok "$GRAFANA_URL/api/health"
check "login works" http_ok -u "$GRAFANA_USER:$GRAFANA_PASSWORD" "$GRAFANA_URL/api/user"
check "datasource API reachable" http_ok -u "$GRAFANA_USER:$GRAFANA_PASSWORD" "$GRAFANA_URL/api/datasources"

echo "== Loki (3100)"
wait_for "ready endpoint /ready" "$TIMEOUT" http_ok "$LOKI_URL/ready"
check "label API (ingestion path) responds" http_ok "$LOKI_URL/loki/api/v1/labels"

echo "== Tempo (3200, 4317)"
wait_for "ready endpoint /ready" "$TIMEOUT" http_ok "$TEMPO_URL/ready"
check "echo endpoint responds" http_ok "$TEMPO_URL/api/echo"

echo "== AlertManager (9093)"
wait_for "health endpoint /-/healthy" "$TIMEOUT" http_ok "$ALERTMANAGER_URL/-/healthy"
check "configuration loaded" bash -c \
  "curl -fsS '$ALERTMANAGER_URL/api/v2/status' | jq -e '.config.original | length > 0'"

echo "== Node Exporter (9100)"
wait_for "metrics endpoint" "$TIMEOUT" http_ok "$NODE_EXPORTER_URL/metrics"
check "exposes node_ metrics" bash -c \
  "curl -fsS '$NODE_EXPORTER_URL/metrics' | grep -q '^node_cpu_seconds_total'"

echo "== OTEL Collector (4317, 4318)"
wait_for "health_check extension (13133)" "$TIMEOUT" http_ok "$OTEL_HEALTH_URL"
check "OTLP/HTTP receiver active (4318)" bash -c \
  "[ \"\$(curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' -d '{}' '$OTEL_HTTP_URL/v1/traces')\" = 200 ]"
check "OTLP/gRPC receiver listening (4317)" bash -c "timeout 5 bash -c '</dev/tcp/localhost/4317'"

summary
