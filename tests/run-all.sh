#!/usr/bin/env bash
# Run the full suite. Usage: tests/run-all.sh [--no-stack]  (static tests only with --no-stack)
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 2
SCRIPTS=(config-validation.sh docker-compose-validation.sh)
[ "${1:-}" != "--no-stack" ] && SCRIPTS+=(health-checks.sh service-connectivity.sh data-flow.sh)
rc=0
for s in "${SCRIPTS[@]}"; do
  echo; echo "######## $s"
  bash "./$s" || rc=1
done
[ "$rc" -eq 0 ] && echo "ALL TESTS PASSED" || echo "SOME TESTS FAILED"
exit $rc
