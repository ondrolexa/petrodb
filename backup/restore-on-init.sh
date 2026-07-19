#!/bin/sh
set -eu

# Runs via the official postgres image's /docker-entrypoint-initdb.d/
# mechanism - only executed once, when the data directory is being
# initialized for the first time. Never runs against an already-existing
# database, so this can't clobber live data on a normal restart.

RECENT_DIR="/dumps/recent"

LATEST=$(find "$RECENT_DIR" -maxdepth 1 -name 'petrodb_*.dump' 2>/dev/null | sort | tail -n1 || true)

if [ -z "$LATEST" ]; then
    echo "restore-on-init: no backup found under $RECENT_DIR - starting with an empty database."
    exit 0
fi

echo "restore-on-init: restoring database '$POSTGRES_DB' from backup: $LATEST"
pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner --no-privileges "$LATEST"
echo "restore-on-init: restore complete."
