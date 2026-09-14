FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /uvx /usr/local/bin/

WORKDIR /app

# Dependencies first — this layer is cached until the lockfile changes.
# README.md is required: pyproject declares readme = "README.md".
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev
