# Vercel

Deploy DDGS Server to [Vercel](https://vercel.com) with one click — no server management required.

## One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FJayanth-MKV%2Fddgs-server&project-name=ddgs-server&repository-name=ddgs-server)

Click the button above to:

1. Fork the repository into your GitHub account
2. Create a new Vercel project linked to the fork
3. Deploy automatically

## How It Works

Vercel uses the `@vercel/python` builder to serve the FastAPI app as a serverless function. The included `vercel.json` handles routing:

```json
{
  "builds": [
    {
      "src": "ddgs_server/app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "ddgs_server/app.py"
    }
  ]
}
```

All requests are routed to the FastAPI application, including:

- REST API endpoints (`/api/search/*`, `/api/content/*`)
- MCP server (`/ai/mcp`)
- Interactive docs (`/docs`, `/redoc`)

## Environment Variables

Set environment variables in **Vercel → Project → Settings → Environment Variables**:

| Variable       | Recommended Value | Description            |
| -------------- | ----------------- | ---------------------- |
| `APP_ENV`      | `production`      | Enables stricter rate limits |

## Using the Deployed Instance

Once deployed, your instance is available at `https://<your-project>.vercel.app`:

```bash
# REST API
curl "https://your-project.vercel.app/api/search/text?q=hello"

# MCP endpoint
# Point MCP clients to: https://your-project.vercel.app/ai/mcp
```

### Connect MCP Clients to Your Deployment

=== "Claude Code"

    ```bash
    claude mcp add --transport http ddgs-remote https://your-project.vercel.app/ai/mcp
    ```

=== "Cursor (via mcp-remote)"

    ```json
    {
      "mcpServers": {
        "ddgs-remote": {
          "command": "npx",
          "args": ["-y", "mcp-remote", "https://your-project.vercel.app/ai/mcp"]
        }
      }
    }
    ```

## Limitations

- Vercel serverless functions have a **10 s** default timeout (30 s on Pro). Unified search with many results may hit this limit.
- Cold starts add ~1–2 s on the first request after idle time.
- In-memory rate limiting resets per invocation. For persistent rate limits, use a Redis-backed deployment (e.g., Docker).
