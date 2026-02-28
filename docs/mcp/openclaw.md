# OpenClaw

[OpenClaw](https://openclaw.ai/) is a self-hosted personal AI assistant that connects to WhatsApp, Telegram, Discord, Slack, Signal, iMessage, and more. It uses **skills** — markdown-based instruction files — to teach the agent how to use tools.

Open Agent Search integrates with OpenClaw as a **skill**, giving your lobster assistant the ability to search the web, images, videos, news, books, and extract content from URLs.

---

## Method 1: Skill File (Recommended)

OpenClaw skills live in your workspace. Create a skill folder and `SKILL.md` file:

**1.** Create the skill directory:

```bash
mkdir -p ~/.openclaw/workspace/skills/open-agent-search
```

**2.** Create `~/.openclaw/workspace/skills/open-agent-search/SKILL.md`:

```markdown
---
name: open-agent-search
description: Search the web, images, videos, news, and books via Open Agent Search MCP server. Privacy-first, powered by DuckDuckGo.
metadata: {"openclaw": {"requires": {"bins": ["uvx"]}, "emoji": "🔍"}}
---

# Open Agent Search

You have access to a powerful search MCP server called Open Agent Search.

## Starting the server

Run the MCP server via stdio:

```bash
uvx --from open-agent-search oas-mcp
```

## Available tools

- **search_web** — Text / web search
- **search_images** — Image search with size & colour filters
- **search_videos** — Video search with resolution & duration filters
- **search_news** — News search with time-limit filter
- **search_books** — Book search
- **search_everything** — Parallel search across all sources
- **fetch_content** — Extract content from a single URL
- **fetch_multiple_contents** — Extract content from multiple URLs (max 10)

## Usage

When the user asks you to search for something, use these tools. Prefer `search_web` for general queries and `search_everything` for comprehensive research.
```

**3.** Restart your OpenClaw gateway or start a new session. The skill will be picked up automatically.

!!! tip "Prerequisites"
    You need [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed. The `uvx` command comes with it.

---

## Method 2: MCP Server in `openclaw.json`

You can also wire Open Agent Search as an MCP tool server directly in your OpenClaw configuration.

**1.** Edit `~/.openclaw/openclaw.json`:

```json
{
  "tools": {
    "mcp": {
      "open-agent-search": {
        "command": "uvx",
        "args": ["--from", "open-agent-search", "oas-mcp"],
        "transport": "stdio"
      }
    }
  }
}
```

**2.** Restart the OpenClaw gateway:

```bash
openclaw gateway --port 18789
```

All 8 search tools will be available to your OpenClaw assistant.

---

## Method 3: Remote HTTP Server

If you have a deployed Open Agent Search instance (e.g. on Vercel or Docker), point OpenClaw at the HTTP MCP endpoint:

```json
{
  "tools": {
    "mcp": {
      "open-agent-search": {
        "url": "https://your-instance.vercel.app/ai/mcp",
        "transport": "http"
      }
    }
  }
}
```

This is useful when your OpenClaw runs on a different machine from your search server, or when you want to share a single deployed instance.

---

## Install via ClawHub

If the skill is published on [ClawHub](https://clawhub.com/), you can install it directly:

```bash
clawhub install open-agent-search
```

This downloads the skill into your workspace automatically.

---

## Verify

Once configured, talk to your OpenClaw assistant:

> "Search the web for the latest news about open source AI agents"

Your assistant should use the `search_web` or `search_news` tool from Open Agent Search and return results.

You can also check the OpenClaw Control UI at [http://127.0.0.1:18789](http://127.0.0.1:18789) to see the skill listed under your active skills.

## Available Tools

Once connected, the server exposes **8 tools**. See the [Tools Reference](../api/mcp-tools.md) for full parameter documentation.

| Tool                      | Description                                     |
| ------------------------- | ----------------------------------------------- |
| `search_web`              | Text / web search                               |
| `search_images`           | Image search with size & colour filters         |
| `search_videos`           | Video search with resolution & duration filters |
| `search_news`             | News search with time-limit filter              |
| `search_books`            | Book search                                     |
| `search_everything`       | Parallel search across all sources              |
| `fetch_content`           | Extract content from a single URL               |
| `fetch_multiple_contents` | Extract content from multiple URLs (max 10)     |
