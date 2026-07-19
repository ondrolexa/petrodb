FROM postgres:18-alpine

# su-exec: drops from root to the unprivileged 'backup' user before running
# the actual backup/restore scripts (see entrypoint.sh). crond itself stays
# root - see docker-compose.yml / README for why that's a deliberate,
# narrow exception to this project's usual non-root posture.
# uid/gid 1000 matches the host user that owns the bind-mounted ./backups
# directory (same convention already used by the petrodb service).
RUN apk add --no-cache su-exec \
 && addgroup -S -g 1000 backup \
 && adduser -S -G backup -u 1000 -h /home/backup backup

WORKDIR /usr/local/bin

COPY entrypoint.sh backup.sh restore.sh ./
RUN chmod +x entrypoint.sh backup.sh restore.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
