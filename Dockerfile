FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Enable bytecode compilation for faster startup
ENV UV_COMPILE_BYTECODE=1
# Use copy mode (cache mount is on a separate filesystem)
ENV UV_LINK_MODE=copy

# Install dependencies first (better layer caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copy the project into the image
COPY . /app

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

# --- Runtime stage ---
FROM python:3.12-slim

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Place the venv on PATH so entry points are available
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["clawsearch"]
