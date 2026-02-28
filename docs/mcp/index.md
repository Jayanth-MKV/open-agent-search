# MCP Integration

DDGS Server provides a full [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server with **8 search tools**. It works in two modes:

| Mode      | Command       | Transport       | Use case                              |
| --------- | ------------- | --------------- | ------------------------------------- |
| **HTTP**  | `ddgs-server` | Streamable HTTP | Deployed API — MCP at `/ai/mcp`       |
| **stdio** | `ddgs-mcp`    | Standard I/O    | Local tool — wire into any MCP client |

## Zero-Install

!!! success "No clone, no pip install needed"
Just point your MCP client to:
`     uvx --from ddgs-server ddgs-mcp
    `
This uses [`uvx`](https://docs.astral.sh/uv/concepts/tools/) to run the server directly from PyPI.

## Choose Your Client

<div class="grid cards" markdown>

- :simple-anthropic:{ .lg .middle } **Claude Desktop**

  ***

  [:octicons-arrow-right-24: Setup guide](claude-desktop.md)

- :octicons-terminal-16:{ .lg .middle } **Claude Code**

  ***

  [:octicons-arrow-right-24: Setup guide](claude-code.md)

- :material-cursor-default-click:{ .lg .middle } **Cursor**

  ***

  [:octicons-arrow-right-24: Setup guide](cursor.md)

- :material-microsoft-visual-studio-code:{ .lg .middle } **VS Code / Copilot**

  ***

  [:octicons-arrow-right-24: Setup guide](vscode.md)

- :material-weather-windy:{ .lg .middle } **Windsurf**

  ***

  [:octicons-arrow-right-24: Setup guide](windsurf.md)

- :material-dots-horizontal:{ .lg .middle } **Other Clients**

  ***

  [:octicons-arrow-right-24: Generic guide](other-clients.md)

</div>

## Config File Locations

| Client         | Config file                                                               |
| -------------- | ------------------------------------------------------------------------- |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) |
|                | `%APPDATA%\Claude\claude_desktop_config.json` (Windows)                   |
| Claude Code    | No file — use `claude mcp add` CLI                                        |
| Cursor         | `~/.cursor/mcp.json`                                                      |
| VS Code        | `.vscode/mcp.json` (per project)                                          |
| Windsurf       | `~/.codeium/windsurf/mcp_config.json`                                     |

## Available Tools

All 8 tools are exposed in both HTTP and stdio modes:

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

!!! info "Tool details"
See the [MCP Tools reference](../api/mcp-tools.md) for full parameter docs.
