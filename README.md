# petrodb

API to PostgreSQL based petrological database

## Run

Copy `.env.sample` to `.env` and modify. For testing you can use
`docker-compose.yml` to run postgresql database.

## Create venv
```
uv sync
```

## Database Migrations

Schema changes are managed with [Alembic](https://alembic.sqlalchemy.org/) —
the database connection is read from the same `.env`-backed settings the app
uses (`petroapi.settings.get_settings`), not from `alembic.ini`.

Apply all pending migrations (required before first run, and after pulling
any change that touches `src/petroapi/models.py`):
```
uv run alembic upgrade head
```

After changing `src/petroapi/models.py`, generate a migration for the diff
and review the generated file before committing it:
```
uv run alembic revision --autogenerate -m "describe the change"
```

Other useful commands:
```
uv run alembic current    # show the DB's current revision
uv run alembic history    # list all revisions
uv run alembic downgrade -1   # roll back one revision
```

The Docker image runs `alembic upgrade head` automatically on container
start (see `entrypoint.sh`), so no manual step is needed when running via
`docker-compose.yml`.

## Run API
```
uv run uvicorn petroapi:app --reload
```

## API Docs

http://localhost:8000/docs

## Backups

`docker-compose.yml` runs a `petrodb-backup` service alongside the database.
It's a cron job (default: daily at 03:00, via `BACKUP_SCHEDULE`) that
`pg_dump`s the database and keeps the dumps in four retention tiers under
the bind-mounted `./dumps` directory:

```
dumps/
  recent/      # every daily dump - kept BACKUP_KEEP_RECENT_DAYS days (default 7)
  last_week/   # Sunday's dump    - kept BACKUP_KEEP_WEEKS weeks     (default 5)
  last_month/  # 1st-of-month dump - kept BACKUP_KEEP_MONTHS months  (default 12)
  last_year/   # Jan 1st dump      - kept BACKUP_KEEP_YEARS years    (default 5)
```

A dump promoted into a tier is hardlinked (not copied) from `recent/`, so it
costs no extra disk space. All four retention windows and the cron schedule
can be overridden via `.env` (`BACKUP_SCHEDULE`, `BACKUP_KEEP_RECENT_DAYS`,
`BACKUP_KEEP_WEEKS`, `BACKUP_KEEP_MONTHS`, `BACKUP_KEEP_YEARS`).

Trigger a backup immediately, without waiting for the schedule:
```
docker compose exec petrodb-backup su-exec backup /usr/local/bin/backup.sh
```

Restore a dump into the running database (interactive - prompts for
confirmation, since it drops and recreates existing objects):
```
docker compose exec -it petrodb-backup /usr/local/bin/restore.sh /dumps/recent/<file>.dump
```
Run it with no argument to list the available dumps.

### Bootstrapping a new deployment from an existing backup

If `./dumps/recent/` already has a dump when `petrodb` starts against a
**fresh, empty** data directory (e.g. first deploy on a new host), it
restores that most recent dump automatically before the database comes up
(`backup/restore-on-init.sh`, wired in via the official Postgres image's
`docker-entrypoint-initdb.d` mechanism). This only ever runs on that
first-time initialization — an existing, already-initialized `postgres-data`
volume is never touched by it, so it's safe to leave in place permanently.
If no backup exists yet, the database just starts empty as before.

Backups currently reuse the app's own database role (`DBUSER`/`DBPASSWORD`);
a dedicated read-only role for the backup job would be a reasonable future
hardening step.
