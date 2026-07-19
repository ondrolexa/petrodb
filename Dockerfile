FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install dependencies first, in their own layer, so app-code changes
# below never invalidate this (slow) layer's cache.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

# Now bring in the application source and install the project itself.
COPY src ./src
COPY LICENSE README.md ./
RUN uv sync --locked --no-dev

# Migration tooling (alembic.ini, alembic/) and the startup entrypoint,
# carried through to the final stage by the /app copy below.
COPY alembic.ini ./
COPY alembic ./alembic
COPY entrypoint.sh ./


# Final stage: minimal runtime image, no uv, no build toolchain.
FROM python:3.14-slim-bookworm

# Non-interactive, headless-friendly runtime behavior.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="/app/.venv/bin:$PATH"

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy the application (venv + source + migrations + entrypoint) from the
# builder stage.
COPY --from=builder --chown=nonroot:nonroot /app /app
RUN chmod +x /app/entrypoint.sh

USER nonroot
WORKDIR /app

# Unprivileged port: lets the non-root user bind without any Linux
# capabilities, so the container can run with cap_drop: ALL.
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8080/', timeout=2).status == 200 else 1)"

# entrypoint.sh runs `alembic upgrade head` before exec'ing the CMD below,
# so the schema is always brought up to date before uvicorn starts.
ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "petroapi:app", "--host", "0.0.0.0", "--port", "8080"]
