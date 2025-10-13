# petrodb

API to PostgreSQL based petrological database

## Run

Copy `.env.sample` to `.env` and modify. For testing you can use
`docker-compose.yml` to run postgresql database.

Run API:
```
uv run uvicorn petroapi:app --reload
```

## Docs

http://localhost:8000/docs
