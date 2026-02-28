# Other MCP Clients

Any MCP client that supports **stdio** transport can use Open Agent Search.

## Generic Configuration

| Setting       | Value                                   |
| ------------- | --------------------------------------- |
| **Command**   | `uvx`                                   |
| **Args**      | `["--from", "open-agent-search", "oas-mcp"]` |
| **Transport** | `stdio`                                 |

## Using a Global Install

If your client doesn't support `uvx`, install the package first:

```bash
uv pip install open-agent-search
# or
pip install open-agent-search
```

Then configure your client with:

| Setting       | Value      |
| ------------- | ---------- |
| **Command**   | `oas-mcp` |
| **Transport** | `stdio`    |

## Using HTTP Transport

If your client supports HTTP/SSE MCP transport, start the HTTP server and point the client at the MCP endpoint:

```bash
uv run open-agent-search
# MCP endpoint → http://localhost:8000/ai/mcp
```

| Setting       | Value                          |
| ------------- | ------------------------------ |
| **URL**       | `http://localhost:8000/ai/mcp` |
| **Transport** | `http` / `sse`                 |

## Available Tools

Once connected, the server exposes **8 tools**. See the [Tools Reference](../api/mcp-tools.md) for full details.
