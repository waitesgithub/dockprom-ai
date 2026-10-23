#!/usr/bin/env bash
# Validate configuration files (syntax + key settings).
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
require_tools python3
cd "$REPO_ROOT" || exit 2

yaml_ok() { python3 -c 'import sys,yaml; list(yaml.safe_load_all(open(sys.argv[1])))' "$1"; }
python3 -c 'import yaml' 2>/dev/null || { echo "Missing python module: pyyaml"; exit 2; }

for f in docker-compose.yaml prometheus.yml alert-rules.yml alert-config.yaml tempo.yaml loki-config.yaml otel-collector-config.yaml; do
  [ -f "$f" ] && check "$f is valid YAML" yaml_ok "$f" || fail "$f missing"
done
[ -f alert-email-template.tmpl ] && pass "alert-email-template.tmpl exists" || fail "alert-email-template.tmpl missing"

check "prometheus.yml has scrape_configs" grep -q '^scrape_configs:' prometheus.yml
check "prometheus.yml references alert-rules.yml" grep -q 'alert-rules.yml' prometheus.yml
check "alert-config.yaml has route and receivers" bash -c "grep -q '^route:' alert-config.yaml && grep -q '^receivers:' alert-config.yaml"
check "otel config has otlp receiver" grep -q 'otlp:' otel-collector-config.yaml
check "otel config defines metrics/logs/traces pipelines" bash -c \
  "grep -q 'metrics:' otel-collector-config.yaml && grep -q 'logs:' otel-collector-config.yaml && grep -q 'traces:' otel-collector-config.yaml"
check "tempo.yaml has otlp receiver" grep -q 'otlp:' tempo.yaml
check "loki-config.yaml sets http_listen_port 3100" grep -q 'http_listen_port: 3100' loki-config.yaml

if command -v promtool >/dev/null 2>&1; then
  check "promtool check config" promtool check config prometheus.yml
fi
for f in tests/fixtures/*.json; do check "$f is valid JSON" python3 -m json.tool "$f"; done

summary
