#!/usr/bin/env bash
# Validate metrics, logs and traces flow end-to-end via the OTEL Collector.
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
require_tools curl jq
FIX="$TESTS_DIR/fixtures"
RUN_ID="$(date +%s)$RANDOM"

otlp_post() { # signal file
  curl -fsS --max-time 10 -X POST -H 'Content-Type: application/json' \
    --data-binary @"$2" "$OTEL_HTTP_URL/v1/$1"
}
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

echo "== Metrics: OTEL -> Prometheus"
sed "s/__NOW__/$(now_ns)/" "$FIX/test-metric.json" > "$TMP/m.json"
check "send test metric" otlp_post metrics "$TMP/m.json"
metric_in_prom() {
  curl -fsS -G "$PROMETHEUS_URL/api/v1/query" --data-urlencode 'query=integration_test_gauge' \
    | jq -e '.data.result | length > 0'
}
# the collector's prometheus exporter only holds data for a limited time, so keep re-sending
metric_loop() { otlp_post metrics "$TMP/m.json" >/dev/null; metric_in_prom; }
wait_for "metric visible in Prometheus" 90 metric_loop

echo "== Logs: OTEL -> Loki"
MARKER="integration-test-log-$RUN_ID"
sed -e "s/__NOW__/$(now_ns)/" -e "s/__MARKER__/$MARKER/" "$FIX/test-log.json" > "$TMP/l.json"
check "send test log" otlp_post logs "$TMP/l.json"
log_in_loki() {
  curl -fsS -G "$LOKI_URL/loki/api/v1/query_range" \
    --data-urlencode "query={service_name=\"integration-test\"} |= \"$MARKER\"" \
    --data-urlencode "start=$(( $(date +%s) - 600 ))000000000" \
    | jq -e '.data.result | length > 0'
}
wait_for "log found in Loki via LogQL" 60 log_in_loki

echo "== Traces: OTEL -> Tempo"
TRACE_ID="$(printf '%016x%016x' "$(date +%s)" "$RANDOM$RANDOM")"
START="$(now_ns)"
sed -e "s/__TRACE_ID__/$TRACE_ID/" -e "s/__START__/$START/" -e "s/__END__/$(( $(date +%s) + 1 ))000000000/" \
  "$FIX/test-trace.json" > "$TMP/t.json"
check "send test trace" otlp_post traces "$TMP/t.json"
wait_for "trace $TRACE_ID found in Tempo" 60 http_ok "$TEMPO_URL/api/traces/$TRACE_ID"

summary
