#!/bin/sh
set -eu

BACKUP_DIR="${BACKUP_DIR:-/dumps}"

if [ -z "${1:-}" ]; then
    echo "Usage: restore.sh <path-to-dump-file>" >&2
    echo "" >&2
    echo "Available backups:" >&2
    find "$BACKUP_DIR" -name 'petrodb_*.dump' | sort >&2
    exit 1
fi

DUMP_FILE="$1"
if [ ! -f "$DUMP_FILE" ]; then
    echo "File not found: $DUMP_FILE" >&2
    exit 1
fi

echo "WARNING: this will DROP and recreate objects in database '$DBNAME' on $DBHOST."
echo "Restoring from: $DUMP_FILE"
printf "Type 'yes' to continue: "
read -r confirm
if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

# --clean --if-exists: drop existing objects before recreating them.
# --single-transaction: all-or-nothing - a failure rolls back completely
# instead of leaving the database half-restored.
PGPASSWORD="$DBPASSWORD" pg_restore -h "$DBHOST" -U "$DBUSER" -d "$DBNAME" \
    --clean --if-exists --no-owner --no-privileges --single-transaction \
    "$DUMP_FILE"

echo "Restore complete."
