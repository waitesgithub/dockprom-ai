#!/usr/bin/env bash
# Validate docker-compose.yaml (no running stack needed).
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
require_tools docker jq
cd "$REPO_ROOT" || exit 2
EXPECTED="prometheus grafana node-exporter alertmanager tempo loki otel-collector"

check "docker compose config is valid" docker compose -f docker-compose.yaml config -q
CONFIG="$(docker compose -f docker-compose.yaml config --format json 2>/dev/null)"

actual="$(echo "$CONFIG" | jq -r '.services | keys[]' | sort | tr '\n' ' ')"
expected="$(echo "$EXPECTED" | tr ' ' '\n' | sort | tr '\n' ' ')"
if [ "$actual" = "$expected" ]; then pass "defines exactly the 7 expected services"; else fail "service list mismatch" "got: $actual"; fi

for svc in $EXPECTED; do
  check "$svc has image" bash -c "echo '$CONFIG' | jq -e '.services[\"$svc\"].image'"
  check "$svc on monitoring network" bash -c "echo '$CONFIG' | jq -e '.services[\"$svc\"].networks | has(\"monitoring\")'"
done

# every bind-mounted local file must exist
while read -r src; do
  [ -e "$src" ] && pass "bind mount source exists: ${src#"$REPO_ROOT"/}" || fail "missing bind mount source: ${src#"$REPO_ROOT"/}"
done < <(echo "$CONFIG" | jq -r --arg r "$REPO_ROOT" \
  '.services[].volumes[]? | select(.type=="bind") | .source | select(startswith($r))' | sort -u)

summary
