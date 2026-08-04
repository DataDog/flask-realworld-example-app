#!/usr/bin/env bash
set -euo pipefail

# run_ops.sh — 简单的运维 helper：构建、迁移、启动并做基本 smoke checks
# Usage: ./run_ops.sh [up|build|migrate|down|smoke]
# Default: up

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# load .env if exists
if [ -f "${ROOT_DIR}/.env" ]; then
  # shellcheck disable=SC1090
  set -a
  # shellcheck source=/dev/null
  . "${ROOT_DIR}/.env"
  set +a
fi

COMPOSE_FILE="${ROOT_DIR}/docker-compose.yml"

wait_for_postgres() {
  host=${1:-db}
  port=${2:-5432}
  timeout=${3:-60}
  echo "Waiting for Postgres at ${host}:${port} (timeout ${timeout}s)..."
  start_ts=$(date +%s)
  while ! nc -z "$host" "$port"; do
    sleep 1
    now=$(date +%s)
    if [ $((now - start_ts)) -ge "$timeout" ]; then
      echo "Timeout waiting for Postgres"
      return 1
    fi
  done
  echo "Postgres is available"
  return 0
}

smoke_check() {
  echo "Running smoke checks..."
  if command -v curl >/dev/null 2>&1; then
    echo "Checking /health..."
    curl -fsS http://localhost:8080/health || { echo "/health failed"; return 1; }
    echo "Checking /metrics..."
    curl -fsS http://localhost:8080/metrics || echo "/metrics unavailable (optional)"
    echo "Smoke checks passed"
  else
    echo "curl not installed; skipping HTTP checks"
  fi
}

case "${1:-up}" in
  build)
    docker-compose -f "$COMPOSE_FILE" build --pull --no-cache
    ;;

  migrate)
    docker-compose -f "$COMPOSE_FILE" up -d db
    wait_for_postgres "${DATABASE_HOST:-db}" "${DATABASE_PORT:-5432}" 60
    docker-compose -f "$COMPOSE_FILE" run --rm web flask db upgrade
    ;;

  up)
    docker-compose -f "$COMPOSE_FILE" build
    docker-compose -f "$COMPOSE_FILE" up -d
    printf "\n==> Waiting for DB and applying migrations...\n"
    wait_for_postgres "${DATABASE_HOST:-db}" "${DATABASE_PORT:-5432}" 60
    docker-compose -f "$COMPOSE_FILE" run --rm web flask db upgrade || true
    sleep 2
    smoke_check
    ;;

  down)
    docker-compose -f "$COMPOSE_FILE" down
    ;;

  smoke)
    smoke_check
    ;;

  *)
    echo "Usage: $0 [up|build|migrate|down|smoke]"
    exit 2
    ;;
esac
