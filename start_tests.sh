#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/crawler"
STOP_SCRIPT="$SCRIPT_DIR/stop_service.sh"
TIMESTAMP="$(date '+%Y%m%d-%H%M%S')"
TEST_ARTIFACTS_ROOT="${KP_CRAWLER_TEST_ARTIFACTS_ROOT:-$PROJECT_DIR/data/test-runs/$TIMESTAMP}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found" >&2
  exit 1
fi

cleanup() {
  "$STOP_SCRIPT" >/dev/null 2>&1 || true
}

trap cleanup EXIT

export PYTHONPATH="$PROJECT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"
export KP_CRAWLER_TEST_ARTIFACTS_ROOT="$TEST_ARTIFACTS_ROOT"
mkdir -p "$KP_CRAWLER_TEST_ARTIFACTS_ROOT"

cd "$PROJECT_DIR"

TEST_EXIT_CODE=0
if [ "$#" -gt 0 ]; then
  python3 -m unittest "$@" || TEST_EXIT_CODE=$?
else
  python3 -m unittest discover -s tests -v || TEST_EXIT_CODE=$?
fi

echo "test artifacts: $KP_CRAWLER_TEST_ARTIFACTS_ROOT"
exit "$TEST_EXIT_CODE"
