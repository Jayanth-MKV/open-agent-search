# Docker

Run Open Agent Search in a container with zero local setup.

## Quick Start

```bash
# Build and run with Docker Compose
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

## Manual Build

```bash
docker build -t open-agent-search .
docker run -p 8000:8000 open-agent-search
```

The server is available at `http://localhost:8000`.

## Environment Variables

Pass environment variables with `-e` or via a `.env` file:

```bash
docker run -p 8000:8000 \
  -e APP_ENV=production \
  -e DDGS_TIMEOUT=15 \
  open-agent-search
```

See [Configuration](../getting-started/quickstart.md#configuration) for all variables.

## Docker Compose

The included `docker-compose.yml` provides:

- **Health checks** — automatic restart on failure
- **Watch mode** — live reload during development (`docker compose watch`)
- **Production defaults** — `APP_ENV=production`, `restart: unless-stopped`

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=production
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c",
             "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
```

## Dockerfile

The Dockerfile uses a **multi-stage build** for a minimal production image:

1. **Builder stage** — installs uv, syncs dependencies, compiles bytecode
2. **Runtime stage** — copies only the virtual environment (~slim image)

```
python:3.12-slim (builder) → uv sync → python:3.12-slim (runtime)
```

No source code is included in the final image — only the installed package and its dependencies.
