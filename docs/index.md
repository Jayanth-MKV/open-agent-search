---
hide:
  - navigation
  - toc
---

# DDGS Server

<div style="text-align: center; margin: 2rem 0;">
<p style="font-size: 1.4rem; color: var(--md-default-fg-color--light);">
A production-ready metasearch REST API and MCP server powered by DuckDuckGo Search.
</p>

<p>
<a href="https://github.com/Jayanth-MKV/ddgs-server/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.12%2B-blue.svg" alt="Python 3.12+"></a>
<a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.121+-green.svg" alt="FastAPI"></a>
<a href="https://modelcontextprotocol.io/"><img src="https://img.shields.io/badge/MCP-Compatible-purple.svg" alt="MCP Compatible"></a>
</p>
</div>

---

<div class="grid cards" markdown>

- :material-download:{ .lg .middle } **Install in 30 seconds**

  ***

  Zero-install with `uvx` — wire into any MCP client instantly.

  ```bash
  uvx --from ddgs-server ddgs-mcp
  ```

  [:octicons-arrow-right-24: Getting started](getting-started/installation.md)

- :material-api:{ .lg .middle } **Full REST API**

  ***

  Search text, images, videos, news, books — all from one API with Swagger docs.

  [:octicons-arrow-right-24: API reference](api/endpoints.md)

- :material-robot:{ .lg .middle } **MCP Server**

  ***

  8 tools for Claude Desktop, Claude Code, Cursor, VS Code, Windsurf & more.

  [:octicons-arrow-right-24: MCP setup guides](mcp/index.md)

- :material-rocket-launch:{ .lg .middle } **One-Click Deploy**

  ***

  Deploy to Vercel or Docker in seconds.

  [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FJayanth-MKV%2Fddgs-server&project-name=ddgs-server&repository-name=ddgs-server)

  [:octicons-arrow-right-24: Deployment guide](deployment/vercel.md)

</div>

---

## Why DDGS Server?

| Feature             | Description                                                              |
| ------------------- | ------------------------------------------------------------------------ |
| **Dual-mode MCP**   | HTTP transport (`/ai/mcp`) for deployed servers + stdio for local tools  |
| **8 search tools**  | Web, images, videos, news, books, unified search, URL content extraction |
| **Rate limiting**   | Built-in per-IP rate limiting with configurable thresholds               |
| **SSRF protection** | URL validator blocks private/internal network requests                   |
| **Zero-install**    | Run via `uvx` — no clone, no pip install needed                          |
| **Docker ready**    | Multi-stage build, < 100 MB image, health checks included                |
| **Vercel deploy**   | One-click deploy button for serverless hosting                           |

## Quick Example

=== "MCP (Claude Desktop)"

    ```json
    {
      "mcpServers": {
        "ddgs": {
          "command": "uvx",
          "args": ["--from", "ddgs-server", "ddgs-mcp"]
        }
      }
    }
    ```

=== "REST API"

    ```bash
    curl "http://localhost:8000/api/search/text?q=python+programming&max_results=5"
    ```

=== "Claude Code"

    ```bash
    claude mcp add ddgs -- uvx --from ddgs-server ddgs-mcp
    ```
