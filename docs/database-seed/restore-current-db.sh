#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
BACKEND_DIR="${BACKEND_DIR:-${PROJECT_ROOT}/backend}"

MODE="${1:-full}"

DB_HOST="${DB_HOST:-127.0.0.1}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-relief_db}"
DB_USER="${DB_USER:-relief_user}"
DB_PASSWORD="${DB_PASSWORD:-relief_pass}"

FULL_DUMP="${SCRIPT_DIR}/opengrc-current-full.sql"
DATA_DUMP="${SCRIPT_DIR}/opengrc-current-data.sql"
FIXTURE_FILE="${SCRIPT_DIR}/opengrc-current-data.json"
RESET_SQL="${SCRIPT_DIR}/opengrc-reset-sequences.sql"
COUNTS_FILE="${SCRIPT_DIR}/opengrc-current-data.counts.txt"

usage() {
  cat <<'EOF'
Usage:
  ./restore-current-db.sh [full|data-only|fixture]

Modes:
  full
    Restore the full PostgreSQL dump (schema + data).
    Recommended for a fresh Docker/PostgreSQL database.

  data-only
    Restore only the SQL data dump into an already migrated schema.
    Less reliable because of circular constraint warnings in the dump.

  fixture
    Run Django migrations, load the JSON fixture, then reset PostgreSQL sequences.

Optional environment variables:
  DB_HOST       Default: 127.0.0.1
  DB_PORT       Default: 5432
  DB_NAME       Default: relief_db
  DB_USER       Default: relief_user
  DB_PASSWORD   Default: relief_pass
  BACKEND_DIR   Default: ../../backend from this script

Examples:
  ./restore-current-db.sh
  ./restore-current-db.sh full
  DB_NAME=mydb DB_USER=myuser DB_PASSWORD=secret ./restore-current-db.sh fixture
EOF
}

require_file() {
  local target="$1"
  if [[ ! -f "${target}" ]]; then
    echo "Missing required file: ${target}" >&2
    exit 1
  fi
}

run_psql_file() {
  local sql_file="$1"
  require_file "${sql_file}"
  echo "Restoring ${sql_file##*/} into ${DB_NAME} on ${DB_HOST}:${DB_PORT}..."
  PGPASSWORD="${DB_PASSWORD}" psql \
    -h "${DB_HOST}" \
    -p "${DB_PORT}" \
    -U "${DB_USER}" \
    -d "${DB_NAME}" \
    -v ON_ERROR_STOP=1 \
    -f "${sql_file}"
}

run_fixture_restore() {
  require_file "${FIXTURE_FILE}"
  require_file "${RESET_SQL}"

  if [[ ! -d "${BACKEND_DIR}" ]]; then
    echo "Backend directory not found: ${BACKEND_DIR}" >&2
    exit 1
  fi

  if [[ ! -f "${BACKEND_DIR}/manage.py" ]]; then
    echo "manage.py not found in ${BACKEND_DIR}" >&2
    exit 1
  fi

  if [[ ! -f "${BACKEND_DIR}/.venv/bin/activate" ]]; then
    echo "Python virtualenv not found in ${BACKEND_DIR}/.venv" >&2
    echo "Create it first or set BACKEND_DIR to the correct backend path." >&2
    exit 1
  fi

  echo "Running Django migrations..."
  (
    cd "${BACKEND_DIR}"
    # shellcheck disable=SC1091
    source .venv/bin/activate
    export DB_HOST DB_PORT DB_NAME DB_USER DB_PASSWORD
    python manage.py migrate
    echo "Loading JSON fixture..."
    python manage.py loaddata "${FIXTURE_FILE}"
  )

  echo "Resetting PostgreSQL sequences..."
  run_psql_file "${RESET_SQL}"
}

case "${MODE}" in
  full)
    run_psql_file "${FULL_DUMP}"
    ;;
  data-only)
    echo "Warning: the data-only dump had circular constraint warnings during export."
    echo "Use this mode only if the schema already exists and you accept that risk."
    run_psql_file "${DATA_DUMP}"
    ;;
  fixture)
    run_fixture_restore
    ;;
  -h|--help|help)
    usage
    exit 0
    ;;
  *)
    echo "Unknown mode: ${MODE}" >&2
    echo >&2
    usage
    exit 1
    ;;
esac

echo
echo "Restore completed."
echo "Recommended verification:"
echo "  - compare row counts with ${COUNTS_FILE}"
echo "  - start the backend and frontend, then spot-check key Cyber GRC modules"
