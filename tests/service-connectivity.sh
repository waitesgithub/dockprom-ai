#!/usr/bin/env bash
# Test inter-service communication.
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
require_tools curl jq
G="$GRAFANA_URL/api"
AUTH="$GRAFANA_USER:$GRAFANA_PASSWORD"

echo "== Prometheus -> scrape targets"
wait_for "all scrape targets are up" 120 bash -c \
  "curl -fsS '$PROMETHEUS_URL/api/v1/targets' | jq -e '[.data.activeTargets[].health] | all(. == \"up\")'"
for job in prometheus node-exporter alertmanager otel-collector; do
  check "job '$job' has a target" bash -c \
    "curl -fsS '$PROMETHEUS_URL/api/v1/targets' | jq -e --arg j $job '[.data.activeTargets[] | select(.labels.job == \$j)] | length > 0'"
done

echo "== Prometheus -> AlertManager"
check "alertmanager discovered by Prometheus" bash -c \
  "curl -fsS '$PROMETHEUS_URL/api/v1/alertmanagers' | jq -e '.data.activeAlertmanagers | length > 0'"
check "alert rules loaded" bash -c \
  "curl -fsS '$PROMETHEUS_URL/api/v1/rules' | jq -e '.data.groups | length > 0'"

echo "== Grafana -> datasources"
declare -A DS=(
  [it-prometheus]="prometheus|http://prometheus:9090"
  [it-loki]="loki|http://loki:3100"
  [it-tempo]="tempo|http://tempo:3200"
)
for uid in "${!DS[@]}"; do
  type="${DS[$uid]%%|*}"; url="${DS[$uid]##*|}"
  curl -fsS -u "$AUTH" -X DELETE "$G/datasources/uid/$uid" >/dev/null 2>&1 || true
  body=$(jq -n --arg n "$uid" --arg t "$type" --arg u "$url" \
    '{name:$n,uid:$n,type:$t,url:$u,access:"proxy"}')
  if curl -fsS -u "$AUTH" -H 'Content-Type: application/json' -d "$body" "$G/datasources" >/dev/null; then
    wait_for "Grafana -> $type ($url)" 60 curl -fsS -u "$AUTH" "$G/datasources/uid/$uid/health"
    curl -fsS -u "$AUTH" -X DELETE "$G/datasources/uid/$uid" >/dev/null 2>&1 || true
  else
    fail "create Grafana $type datasource"
  fi
done

echo "== OTEL Collector"
check "collector healthy" http_ok "$OTEL_HEALTH_URL"
check "collector metrics exporter (8889) reachable" http_ok "http://localhost:8889/metrics"

summary
