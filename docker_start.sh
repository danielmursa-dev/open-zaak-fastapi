#!/bin/sh

set -ex

# Wait for the database container
# See: https://docs.docker.com/compose/startup-order/
export PGHOST=${DB_HOST:-db}
export PGPORT=${DB_PORT:-5432}

uwsgi_port=${UWSGI_PORT:-8000}
uwsgi_processes=${UWSGI_PROCESSES:-2}
uwsgi_threads=${UWSGI_THREADS:-2}

mountpoint=${SUBPATH:-/}

# wait for required services
${SCRIPTPATH}/wait_for_db.sh

# Start server
>&2 echo "Starting server"
exec uvicorn src.main:app --host 0.0.0.0 --port "${UVICORN_PORT:-8000}" --workers "${UVICORN_WORKERS:-4}"
