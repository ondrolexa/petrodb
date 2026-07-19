#!/bin/sh
set -eu

SCHEDULE="${BACKUP_SCHEDULE:-0 3 * * *}"

# root's crontab (busybox crond's standard location). Job output is
# redirected to PID 1's own stdout/stderr so it lands in `docker logs`
# instead of being discarded.
echo "$SCHEDULE su-exec backup /usr/local/bin/backup.sh >>/proc/1/fd/1 2>>/proc/1/fd/2" \
    > /etc/crontabs/root

echo "Backup schedule: $SCHEDULE"

exec crond -f -l 8
