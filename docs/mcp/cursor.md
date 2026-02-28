# Cursor

## Setup

**1.** Edit `~/.cursor/mcp.json` (create it if it doesn't exist):

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

**2.** Restart Cursor to activate the server.

## Verify

Open Cursor Settings → MCP. You should see `oas` listed with a green status indicator.

## Using a Remote Server

If you have a deployed Open Agent Search instance, you can connect via HTTP using `mcp-remote`:

```json
{
  "mcpServers": {
    "oas-remote": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://your-instance.vercel.app/ai/mcp"]
    }
  }
}
```

!!! note
Remote HTTP support varies by Cursor version. The `mcp-remote` proxy is a reliable fallback.
