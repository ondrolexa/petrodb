#!/bin/sh
set -eu

BACKUP_DIR="${BACKUP_DIR:-/dumps}"
RECENT_DIR="$BACKUP_DIR/recent"
WEEK_DIR="$BACKUP_DIR/last_week"
MONTH_DIR="$BACKUP_DIR/last_month"
YEAR_DIR="$BACKUP_DIR/last_year"

KEEP_RECENT_DAYS="${BACKUP_KEEP_RECENT_DAYS:-7}"
KEEP_WEEKS="${BACKUP_KEEP_WEEKS:-5}"
KEEP_MONTHS="${BACKUP_KEEP_MONTHS:-12}"
KEEP_YEARS="${BACKUP_KEEP_YEARS:-5}"

log() {
    echo "[$(date -Iseconds)] $*"
}

mkdir -p "$RECENT_DIR" "$WEEK_DIR" "$MONTH_DIR" "$YEAR_DIR"

timestamp=$(date +%Y%m%d_%H%M%S)
filename="petrodb_${timestamp}.dump"
tmpfile="$RECENT_DIR/.${filename}.tmp"
destfile="$RECENT_DIR/$filename"

log "Starting backup of database '$DBNAME' on $DBHOST -> $destfile"

PGPASSWORD="$DBPASSWORD" pg_dump -h "$DBHOST" -U "$DBUSER" -d "$DBNAME" -Fc -f "$tmpfile"
# Atomic rename: a failed/killed pg_dump never leaves a half-written file
# masquerading as a complete backup at the final name.
mv "$tmpfile" "$destfile"

log "Backup complete: $destfile ($(du -h "$destfile" | cut -f1))"

# Promote into the weekly/monthly/yearly tiers via hardlink - same inode,
# no extra disk space, all tiers live on the same filesystem under $BACKUP_DIR.
day_of_week=$(date +%u)   # 1=Monday .. 7=Sunday
day_of_month=$(date +%d)
day_of_year=$(date +%j)

if [ "$day_of_week" = "7" ]; then
    ln -f "$destfile" "$WEEK_DIR/$filename"
    log "Promoted to $WEEK_DIR/$filename"
fi
if [ "$day_of_month" = "01" ]; then
    ln -f "$destfile" "$MONTH_DIR/$filename"
    log "Promoted to $MONTH_DIR/$filename"
fi
if [ "$day_of_year" = "001" ]; then
    ln -f "$destfile" "$YEAR_DIR/$filename"
    log "Promoted to $YEAR_DIR/$filename"
fi

# Prune each tier to its retention window.
find "$RECENT_DIR" -maxdepth 1 -name 'petrodb_*.dump' -mtime "+${KEEP_RECENT_DAYS}" -delete
find "$WEEK_DIR"   -maxdepth 1 -name 'petrodb_*.dump' -mtime "+$((KEEP_WEEKS * 7))" -delete
find "$MONTH_DIR"  -maxdepth 1 -name 'petrodb_*.dump' -mtime "+$((KEEP_MONTHS * 31))" -delete
find "$YEAR_DIR"   -maxdepth 1 -name 'petrodb_*.dump' -mtime "+$((KEEP_YEARS * 366))" -delete

log "Retention pruning complete (keep: ${KEEP_RECENT_DAYS}d recent, ${KEEP_WEEKS}w weekly, ${KEEP_MONTHS}m monthly, ${KEEP_YEARS}y yearly)."
