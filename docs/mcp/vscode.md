# VS Code / GitHub Copilot

## Setup

Add a `.vscode/mcp.json` file in your project root:

```json
{
  "servers": {
    "oas": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "open-agent-search", "oas-mcp"]
    }
  }
}
```

!!! warning "Different format"
VS Code uses `"servers"` (not `"mcpServers"`) and requires a `"type"` field. This is different from Claude Desktop and Cursor.

## Global Configuration

To make it available across all VS Code workspaces, add it to your **User Settings** (`settings.json`):

```json
{
  "mcp": {
    "servers": {
      "oas": {
        "type": "stdio",
        "command": "uvx",
        "args": ["--from", "open-agent-search", "oas-mcp"]
      }
    }
  }
}
```

## Verify

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Run **MCP: List Servers**
3. You should see `oas` listed

## Using a Remote Server

For a deployed Open Agent Search instance:

```json
{
  "servers": {
    "oas-remote": {
      "type": "http",
      "url": "https://your-instance.vercel.app/ai/mcp"
    }
  }
}
```
