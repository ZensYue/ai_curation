#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/crawler"
PID_FILE="$SCRIPT_DIR/.kp_crawler.pid"
LOG_FILE="$SCRIPT_DIR/.kp_crawler.log"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found" >&2
  exit 1
fi

if [ -f "$PID_FILE" ]; then
  EXISTING_PID="$(cat "$PID_FILE")"
  if kill -0 "$EXISTING_PID" >/dev/null 2>&1; then
    echo "service already running with pid $EXISTING_PID"
    echo "log file: $LOG_FILE"
    exit 0
  fi
  rm -f "$PID_FILE"
fi

export PYTHONPATH="$PROJECT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"
cd "$PROJECT_DIR"

if [ "$#" -gt 0 ]; then
  CLI_ARGS=("$@")
else
  HOST="${KP_CRAWLER_HOST:-127.0.0.1}"
  PORT="${KP_CRAWLER_PORT:-8080}"
  LOG_LEVEL="${KP_CRAWLER_LOG_LEVEL:-INFO}"
  CLI_ARGS=(serve --host "$HOST" --port "$PORT" --log-level "$LOG_LEVEL")
fi

: >"$LOG_FILE"
nohup python3 -c 'from kp_crawler.cli import main; main()' "${CLI_ARGS[@]}" >"$LOG_FILE" 2>&1 &
SERVICE_PID=$!
echo "$SERVICE_PID" >"$PID_FILE"

sleep 1
if ! kill -0 "$SERVICE_PID" >/dev/null 2>&1; then
  rm -f "$PID_FILE"
  echo "service failed to start" >&2
  if grep -q "Address already in use" "$LOG_FILE"; then
    echo "port is already in use; try ./start_service.sh serve --host 127.0.0.1 --port 18080" >&2
  fi
  tail -n 20 "$LOG_FILE" >&2 || true
  exit 1
fi

echo "service started with pid $SERVICE_PID"
echo "pid file: $PID_FILE"
echo "log file: $LOG_FILE"
