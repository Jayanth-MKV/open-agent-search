# Open Agent Search (OAS)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121+-green.svg)](https://fastapi.tiangolo.com/)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://jayanth-mkv.github.io/open-agent-search/)

The **sensory organ** for the AI agent ecosystem. An independent, privacy-first search layer providing unfiltered access to the world's knowledge via [MCP](https://modelcontextprotocol.io/) and HTTP API.

> **Open Agent Search is an independent foundational tool.** We are not bound to any single agent framework but support them all (including OpenClaw via `openclaw-search`). Our mission is accuracy, speed, and universal access.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FJayanth-MKV%2Fopen-agent-search&project-name=open-agent-search&repository-name=open-agent-search)

> **[Read the full documentation →](https://jayanth-mkv.github.io/open-agent-search/)**

---

## Quick Start

### Zero-install (MCP)

```bash
# Works instantly — no clone or install needed
uvx --from open-agent-search oas-mcp
```

### Install & Run

```bash
# Install from PyPI
uv pip install open-agent-search

# Start the HTTP API + MCP server
open-agent-search
# → http://localhost:8000 (API)
# → http://localhost:8000/ai/mcp (MCP)
```

### From Source

```bash
git clone https://github.com/Jayanth-MKV/open-agent-search.git
cd open-agent-search
uv sync
uv run open-agent-search
```

### Docker

```bash
docker compose up -d
```

---

## What's Included

| Feature                 | Description                                                                    |
| ----------------------- | ------------------------------------------------------------------------------ |
| **REST API**            | 8 search endpoints (text, images, videos, news, books, unified, content fetch) |
| **MCP Server**          | 8 tools accessible via stdio or HTTP — works with every major AI coding client |
| **OpenClaw Compatible** | Works as an OpenClaw skill via stdio MCP transport                             |
| **Rate Limiting**       | Per-IP rate limits with configurable dev/prod profiles                         |
| **One-Click Deploy**    | Deploy to Vercel in seconds                                                    |
| **Docker**              | Multi-stage Dockerfile + Compose with health checks                            |

---

## MCP Client Setup

> **[Full setup guides →](https://jayanth-mkv.github.io/open-agent-search/mcp/)**

Add to any MCP client with `uvx` — zero install:

```json
{
  "mcpServers": {
    "open-agent-search": {
      "command": "uvx",
      "args": ["--from", "open-agent-search", "oas-mcp"]
    }
  }
}
```

Guides available for: **Claude Desktop** · **Claude Code** · **Cursor** · **VS Code** · **Windsurf** · **OpenClaw** · [and more](https://jayanth-mkv.github.io/open-agent-search/mcp/other-clients/)

---

## API Endpoints

| Endpoint                      | Method | Description                        |
| ----------------------------- | ------ | ---------------------------------- |
| `/api/search/text`            | GET    | Web / text search                  |
| `/api/search/images`          | GET    | Image search                       |
| `/api/search/videos`          | GET    | Video search                       |
| `/api/search/news`            | GET    | News search                        |
| `/api/search/books`           | GET    | Book search                        |
| `/api/search/all`             | GET    | Unified parallel search            |
| `/api/content/fetch`          | GET    | Fetch & extract content from a URL |
| `/api/content/fetch-multiple` | POST   | Fetch content from multiple URLs   |
| `/ai/mcp`                     | —      | MCP server endpoint                |

> **[Full API reference →](https://jayanth-mkv.github.io/open-agent-search/api/endpoints/)**

---

## Documentation

- [Installation](https://jayanth-mkv.github.io/open-agent-search/getting-started/installation/)
- [Quick Start](https://jayanth-mkv.github.io/open-agent-search/getting-started/quickstart/)
- [MCP Integration](https://jayanth-mkv.github.io/open-agent-search/mcp/)
- [API Reference](https://jayanth-mkv.github.io/open-agent-search/api/endpoints/)
- [Docker Deployment](https://jayanth-mkv.github.io/open-agent-search/deployment/docker/)
- [Vercel Deployment](https://jayanth-mkv.github.io/open-agent-search/deployment/vercel/)
- [Contributing](https://jayanth-mkv.github.io/open-agent-search/contributing/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
