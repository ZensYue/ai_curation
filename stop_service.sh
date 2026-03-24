#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.kp_crawler.pid"
PROJECT_DIR="$SCRIPT_DIR/crawler"

stop_pid() {
  local service_pid="$1"

  if ! kill -0 "$service_pid" >/dev/null 2>&1; then
    return 1
  fi

  kill "$service_pid"

  for _ in 1 2 3 4 5; do
    if ! kill -0 "$service_pid" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done

  kill -9 "$service_pid"
}

if [ -f "$PID_FILE" ]; then
  SERVICE_PID="$(cat "$PID_FILE")"
  if stop_pid "$SERVICE_PID"; then
    rm -f "$PID_FILE"
    echo "service stopped"
    exit 0
  fi
  rm -f "$PID_FILE"
fi

MATCHED_PIDS="$(pgrep -f "$PROJECT_DIR/.*/kp-crawler serve|$PROJECT_DIR/.venv/bin/kp-crawler serve|kp_crawler.cli serve" || true)"

if [ -z "$MATCHED_PIDS" ]; then
  echo "service is not running"
  exit 0
fi

STOPPED_ANY=0
for SERVICE_PID in $MATCHED_PIDS; do
  if stop_pid "$SERVICE_PID"; then
    STOPPED_ANY=1
  fi
done

rm -f "$PID_FILE"

if [ "$STOPPED_ANY" -eq 1 ]; then
  echo "service stopped"
  exit 0
fi

echo "service is not running"
