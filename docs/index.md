---
hide:
  - navigation
  - toc
---

<style>
  .md-typeset h1 { display: none; }
  .hero { text-align: center; padding: 2rem 1rem 1rem; }
  .hero__tagline { font-size: 1.5rem; font-weight: 300; color: var(--md-default-fg-color--light); max-width: 640px; margin: 0.5rem auto 1.5rem; line-height: 1.5; }
  .hero__title { font-size: 2.6rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 0.25rem; }
  .hero__subtitle { font-size: 1.1rem; color: var(--md-default-fg-color--lighter); margin-bottom: 1.5rem; }
  .hero__badges { margin-bottom: 2rem; }
  .hero__badges img { margin: 0 0.15rem; }
  .hero__cta { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 2rem; }
  .hero__cta a { padding: 0.75rem 1.75rem; border-radius: 8px; font-weight: 600; text-decoration: none; font-size: 0.95rem; transition: transform 0.15s ease, box-shadow 0.15s ease; }
  .hero__cta a:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
  .hero__cta-primary { background: var(--md-primary-fg-color); color: var(--md-primary-bg-color) !important; }
  .hero__cta-secondary { border: 2px solid var(--md-primary-fg-color); color: var(--md-primary-fg-color) !important; background: transparent; }
  .hero__install { background: var(--md-code-bg-color); border-radius: 8px; padding: 0.75rem 1.5rem; display: inline-block; font-family: var(--md-code-font-family); font-size: 0.9rem; margin: 1rem auto 0; }
  .features-section { margin-top: 2rem; }
  .stats { display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; margin: 2rem 0; padding: 1.5rem 0; border-top: 1px solid var(--md-default-fg-color--lightest); border-bottom: 1px solid var(--md-default-fg-color--lightest); }
  .stats__item { text-align: center; }
  .stats__number { font-size: 2rem; font-weight: 800; color: var(--md-primary-fg-color); }
  .stats__label { font-size: 0.85rem; color: var(--md-default-fg-color--light); text-transform: uppercase; letter-spacing: 0.05em; }
  .clients-grid { display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin: 1.5rem 0; }
  .clients-grid span { background: var(--md-code-bg-color); padding: 0.4rem 0.9rem; border-radius: 20px; font-size: 0.85rem; font-weight: 500; }
</style>

# Open Agent Search

<div class="hero" markdown>

<div class="hero__title">Open Agent Search</div>
<div class="hero__subtitle">The Eyes of the AI Agent Ecosystem</div>
<p class="hero__tagline">
Privacy-first, unfiltered search for every AI agent. 8 search tools accessible via MCP and REST API — powered by DuckDuckGo.
</p>

<div class="hero__badges">
<a href="https://github.com/Jayanth-MKV/open-agent-search/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.12%2B-blue.svg" alt="Python 3.12+"></a>
<a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.121+-green.svg" alt="FastAPI"></a>
<a href="https://modelcontextprotocol.io/"><img src="https://img.shields.io/badge/MCP-Compatible-purple.svg" alt="MCP Compatible"></a>
</div>

<div class="hero__cta">
<a href="getting-started/installation/" class="hero__cta-primary">Get Started</a>
<a href="api/endpoints/" class="hero__cta-secondary">API Reference</a>
</div>

<div class="hero__install">uvx --from open-agent-search oas-mcp</div>
<br>
<small style="color: var(--md-default-fg-color--lighter);">Zero-install — runs directly from PyPI, no clone needed</small>

</div>

<div class="stats">
  <div class="stats__item">
    <div class="stats__number">8</div>
    <div class="stats__label">Search Tools</div>
  </div>
  <div class="stats__item">
    <div class="stats__number">2</div>
    <div class="stats__label">Transports</div>
  </div>
  <div class="stats__item">
    <div class="stats__number">7+</div>
    <div class="stats__label">MCP Clients</div>
  </div>
  <div class="stats__item">
    <div class="stats__number">&lt;100MB</div>
    <div class="stats__label">Docker Image</div>
  </div>
</div>

---

## :material-lightning-bolt: Works Everywhere { .features-section }

Plug Open Agent Search into any MCP-compatible client — or call the REST API directly.

<div class="clients-grid" markdown>
  <span markdown="span">:simple-anthropic: Claude Desktop</span>
  <span markdown="span">:octicons-terminal-16: Claude Code</span>
  <span markdown="span">:material-cursor-default-click: Cursor</span>
  <span markdown="span">:material-microsoft-visual-studio-code: VS Code</span>
  <span markdown="span">:material-weather-windy: Windsurf</span>
  <span markdown="span">:material-hook: OpenClaw</span>
  <span markdown="span">:material-dots-horizontal: Any MCP Client</span>
</div>

[:octicons-arrow-right-24: See all MCP setup guides](mcp/index.md){ .md-button }

---

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } **Install in 30 Seconds**

    ---

    Zero-install with `uvx` — wire into any MCP client instantly. No clone, no pip install.

    [:octicons-arrow-right-24: Getting started](getting-started/installation.md)

-   :material-api:{ .lg .middle } **Full REST API**

    ---

    Search text, images, videos, news, books — all from one API with interactive Swagger docs.

    [:octicons-arrow-right-24: API reference](api/endpoints.md)

-   :material-robot:{ .lg .middle } **MCP Server**

    ---

    8 tools for Claude Desktop, Claude Code, Cursor, VS Code, Windsurf, OpenClaw & more.

    [:octicons-arrow-right-24: MCP setup guides](mcp/index.md)

-   :material-rocket-launch:{ .lg .middle } **One-Click Deploy**

    ---

    Deploy to Vercel or Docker in seconds. Production-ready out of the box.

    [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FJayanth-MKV%2Fopen-agent-search&project-name=open-agent-search&repository-name=open-agent-search)

    [:octicons-arrow-right-24: Deployment guide](deployment/vercel.md)

-   :material-shield-check:{ .lg .middle } **Privacy First**

    ---

    Powered by DuckDuckGo. No tracking, no API keys required, no data collection. SSRF protection built-in.

    [:octicons-arrow-right-24: Learn more](getting-started/quickstart.md)

-   :material-hook:{ .lg .middle } **OpenClaw Compatible**

    ---

    Works as an OpenClaw skill — give your lobster assistant the power of search.

    [:octicons-arrow-right-24: OpenClaw guide](mcp/openclaw.md)

</div>

---

## Why Open Agent Search?

> _We are building the eyes of the AI._ Independent, agent-neutral access to the world's knowledge.

| Feature             | Description                                                              |
| ------------------- | ------------------------------------------------------------------------ |
| **Dual-mode MCP**   | HTTP transport (`/ai/mcp`) for deployed servers + stdio for local tools  |
| **8 search tools**  | Web, images, videos, news, books, unified search, URL content extraction |
| **Agent-neutral**   | Not bound to any single framework — supports them all                    |
| **Rate limiting**   | Built-in per-IP rate limiting with configurable thresholds               |
| **SSRF protection** | URL validator blocks private/internal network requests                   |
| **Zero-install**    | Run via `uvx` — no clone, no pip install needed                          |
| **Docker ready**    | Multi-stage build, < 100 MB image, health checks included                |
| **Vercel deploy**   | One-click deploy button for serverless hosting                           |
| **OpenClaw native** | Works as an OpenClaw skill via stdio MCP transport                       |

---

## Quick Example

=== "MCP (Claude Desktop)"

    ```json
    {
      "mcpServers": {
        "oas": {
          "command": "uvx",
          "args": ["--from", "open-agent-search", "oas-mcp"]
        }
      }
    }
    ```

=== "REST API"

    ```bash
    curl "http://localhost:8000/api/search/text?q=python+programming&max_results=5"
    ```

=== "OpenClaw Skill"

    ```bash
    # Create the skill directory
    mkdir -p ~/.openclaw/workspace/skills/open-agent-search

    # Create SKILL.md (see OpenClaw guide for full content)
    cat > ~/.openclaw/workspace/skills/open-agent-search/SKILL.md << 'EOF'
    ---
    name: open-agent-search
    description: Search the web via Open Agent Search MCP. Privacy-first, powered by DuckDuckGo.
    metadata: {"openclaw": {"requires": {"bins": ["uvx"]}, "emoji": "🔍"}}
    ---
    # Open Agent Search
    Use `uvx --from open-agent-search oas-mcp` to search the web.
    EOF
    ```

=== "Docker"

    ```bash
    docker compose up -d
    # API → http://localhost:8000
    # MCP → http://localhost:8000/ai/mcp
    ```

=== "Claude Code"

    ```bash
    claude mcp add oas -- uvx --from open-agent-search oas-mcp
    ```
