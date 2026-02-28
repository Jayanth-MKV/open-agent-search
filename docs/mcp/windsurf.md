# Windsurf

## Setup

**1.** Edit `~/.codeium/windsurf/mcp_config.json`:

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

**2.** Restart Windsurf to activate the server.

## Verify

Open Windsurf's MCP panel to confirm the `ddgs` server is connected and showing 8 tools.
