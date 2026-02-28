# Quick Start

## Run as HTTP API

```bash
# Via CLI entry point
uv run open-agent-search

# Or via uvicorn directly (with hot reload for development)
uv run uvicorn open_agent_search.app:app --reload --host 0.0.0.0 --port 8000

# Or via python -m
uv run python -m open_agent_search
```

The API is now running at `http://localhost:8000`.

| URL                                                          | Description  |
| ------------------------------------------------------------ | ------------ |
| [http://localhost:8000/docs](http://localhost:8000/docs)     | Swagger UI   |
| [http://localhost:8000/redoc](http://localhost:8000/redoc)   | ReDoc        |
| [http://localhost:8000/health](http://localhost:8000/health) | Health check |
| [http://localhost:8000/ai/mcp](http://localhost:8000/ai/mcp) | MCP endpoint |

## Try a Search

```bash
# Text search
curl "http://localhost:8000/api/search/text?q=python+programming&max_results=5"

# Image search with filters
curl "http://localhost:8000/api/search/images?q=sunset&size=Large&color=Orange"

# News from the last week
curl "http://localhost:8000/api/search/news?q=AI&timelimit=w&max_results=10"

# Fetch content from a URL
curl "http://localhost:8000/api/content/fetch?url=https://example.com"

# Fetch multiple URLs
curl -X POST "http://localhost:8000/api/content/fetch-multiple" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com", "https://example.org"]}'
```

## Run as MCP Server

For local MCP clients (Claude Desktop, Cursor, VS Code, etc.):

```bash
uv run oas-mcp
```

Or run directly via `uvx` (no install needed):

```bash
uvx --from open-agent-search oas-mcp
```

!!! tip "Next steps"
Head to the [MCP Integration](../mcp/index.md) section for step-by-step guides on connecting to your favourite MCP client.

## Configuration

Copy the example environment file and edit as needed:

```bash
cp .env.example .env
```

| Variable       | Default      | Description                                         |
| -------------- | ------------ | --------------------------------------------------- |
| `APP_ENV`      | `production` | `development` or `production` (changes rate limits) |
| `HOST`         | `0.0.0.0`    | Server bind address                                 |
| `PORT`         | `8000`       | Server port                                         |
| `DDGS_TIMEOUT` | `10`         | Search request timeout (seconds)                    |
| `DDGS_PROXY`   | —            | Optional SOCKS5 proxy URL                           |
