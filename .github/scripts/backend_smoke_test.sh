#!/usr/bin/env bash
# Starts the FastAPI backend the same way Railway does and checks that it is healthy.
# Run from the repository root. Uses PYTHON (default: python) to launch uvicorn.
set -euo pipefail

PYTHON="${PYTHON:-python}"
PORT="${PORT:-8000}"
BASE="http://127.0.0.1:${PORT}"
LOG="$(mktemp)"

cd backend
"${PYTHON}" -m uvicorn app.main:app --host 127.0.0.1 --port "${PORT}" >"${LOG}" 2>&1 &
SERVER_PID=$!
trap 'kill "${SERVER_PID}" 2>/dev/null || true' EXIT

echo "Waiting for ${BASE}/health ..."
for i in $(seq 1 30); do
  if curl -fsS "${BASE}/health" >/dev/null 2>&1; then
    break
  fi
  if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
    echo "::error::Backend exited during startup"
    cat "${LOG}"
    exit 1
  fi
  sleep 2
done

echo "--- /health"
curl -fsS "${BASE}/health" | tee /dev/stderr | grep -q '"status":"ok"' || {
  echo "::error::/health did not report status ok"
  cat "${LOG}"
  exit 1
}
echo

echo "--- /study-areas"
curl -fsS "${BASE}/study-areas" | grep -q '"areas"' || {
  echo "::error::/study-areas did not return an areas list"
  cat "${LOG}"
  exit 1
}

echo "Backend smoke test passed"
