# VS Code / GitHub Copilot

## Setup

Add a `.vscode/mcp.json` file in your project root:

```json
{
  "servers": {
    "ddgs": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "ddgs-server", "ddgs-mcp"]
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
      "ddgs": {
        "type": "stdio",
        "command": "uvx",
        "args": ["--from", "ddgs-server", "ddgs-mcp"]
      }
    }
  }
}
```

## Verify

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Run **MCP: List Servers**
3. You should see `ddgs` listed

## Using a Remote Server

For a deployed DDGS Server instance:

```json
{
  "servers": {
    "ddgs-remote": {
      "type": "http",
      "url": "https://your-instance.vercel.app/ai/mcp"
    }
  }
}
```
