# Claude Desktop

## Setup

**1.** Open your Claude Desktop config file:

| OS      | Path                                                              |
| ------- | ----------------------------------------------------------------- |
| macOS   | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json`                     |

**2.** Add the DDGS server:

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

**3.** Restart Claude Desktop.

!!! tip "Prerequisites"
You need [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed. The `uvx` command comes with it automatically.

## Verify

After restarting, you should see a hammer icon (:material-hammer:) in the Claude Desktop chat input. Click it to see the 8 DDGS tools available.

## Using a Deployed Server (HTTP)

If you have a remote DDGS Server instance running (e.g. on Vercel or Docker), you can connect via HTTP instead:

```json
{
  "mcpServers": {
    "ddgs-remote": {
      "url": "https://your-deployed-instance.vercel.app/ai/mcp"
    }
  }
}
```
