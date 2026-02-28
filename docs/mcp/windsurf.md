# Windsurf

## Setup

**1.** Edit `~/.codeium/windsurf/mcp_config.json`:

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

**2.** Restart Windsurf to activate the server.

## Verify

Open Windsurf's MCP panel to confirm the `ddgs` server is connected and showing 8 tools.
