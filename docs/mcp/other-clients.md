# Other MCP Clients

Any MCP client that supports **stdio** transport can use DDGS Server.

## Generic Configuration

| Setting       | Value                                   |
| ------------- | --------------------------------------- |
| **Command**   | `uvx`                                   |
| **Args**      | `["--from", "ddgs-server", "ddgs-mcp"]` |
| **Transport** | `stdio`                                 |

## Using a Global Install

If your client doesn't support `uvx`, install the package first:

```bash
uv pip install ddgs-server
# or
pip install ddgs-server
```

Then configure your client with:

| Setting       | Value      |
| ------------- | ---------- |
| **Command**   | `ddgs-mcp` |
| **Transport** | `stdio`    |

## Using HTTP Transport

If your client supports HTTP/SSE MCP transport, start the HTTP server and point the client at the MCP endpoint:

```bash
uv run ddgs-server
# MCP endpoint → http://localhost:8000/ai/mcp
```

| Setting       | Value                          |
| ------------- | ------------------------------ |
| **URL**       | `http://localhost:8000/ai/mcp` |
| **Transport** | `http` / `sse`                 |

## Available Tools

Once connected, the server exposes **8 tools**. See the [Tools Reference](../api/mcp-tools.md) for full details.
