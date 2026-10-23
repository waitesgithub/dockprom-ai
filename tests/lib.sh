#!/usr/bin/env bash
# Shared helpers for integration tests.

PROMETHEUS_URL="${PROMETHEUS_URL:-http://localhost:9090}"
GRAFANA_URL="${GRAFANA_URL:-http://localhost:3000}"
GRAFANA_USER="${GRAFANA_USER:-admin}"
GRAFANA_PASSWORD="${GRAFANA_PASSWORD:-admin}"
LOKI_URL="${LOKI_URL:-http://localhost:3100}"
TEMPO_URL="${TEMPO_URL:-http://localhost:3200}"
ALERTMANAGER_URL="${ALERTMANAGER_URL:-http://localhost:9093}"
NODE_EXPORTER_URL="${NODE_EXPORTER_URL:-http://localhost:9100}"
OTEL_HTTP_URL="${OTEL_HTTP_URL:-http://localhost:4318}"
OTEL_HEALTH_URL="${OTEL_HEALTH_URL:-http://localhost:13133}"

TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$TESTS_DIR")"
PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); echo "  [PASS] $1"; }
fail() { FAIL=$((FAIL + 1)); echo "  [FAIL] $1"; [ -n "${2:-}" ] && echo "         $2"; return 0; }

# check "description" command [args...]
check() {
  local desc="$1"; shift
  local out
  if out=$("$@" 2>&1); then pass "$desc"; else fail "$desc" "$(echo "$out" | head -n 3)"; fi
}

# wait_for "description" timeout_seconds command [args...]
wait_for() {
  local desc="$1" timeout="$2"; shift 2
  local end=$((SECONDS + timeout))
  while [ "$SECONDS" -lt "$end" ]; do
    if "$@" >/dev/null 2>&1; then pass "$desc"; return 0; fi
    sleep 3
  done
  fail "$desc" "timed out after ${timeout}s"
}

http_ok() { curl -fsS --max-time 10 "$@" >/dev/null; }

require_tools() {
  local t
  for t in "$@"; do
    command -v "$t" >/dev/null 2>&1 || { echo "Missing required tool: $t"; exit 2; }
  done
}

summary() {
  echo
  echo "Results: $PASS passed, $FAIL failed"
  [ "$FAIL" -eq 0 ]
}

now_ns() { echo "$(date +%s)000000000"; }
