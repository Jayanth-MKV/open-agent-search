# Claude Code

[Claude Code](https://code.claude.com/) is Anthropic's CLI tool for Claude. No config file needed — use the `claude mcp add` command.

## Setup (stdio — local)

```bash
claude mcp add oas -- uvx --from open-agent-search oas-mcp
```

## Setup (HTTP — remote)

If you have a deployed Open Agent Search instance:

```bash
claude mcp add --transport http oas-remote https://your-instance.vercel.app/ai/mcp
```

Or connect to a local running server:

```bash
claude mcp add --transport http oas-local http://localhost:8000/ai/mcp
```

## Manage

```bash
# List all configured servers
claude mcp list

# Get details for the Open Agent Search
claude mcp get oas

# Remove the server
claude mcp remove oas

# Check server status (within Claude Code)
/mcp
```

## Scopes

Use `--scope` to control where the config is stored:

| Scope             | Description                                             |
| ----------------- | ------------------------------------------------------- |
| `local` (default) | Available only to you in the current project            |
| `project`         | Shared with everyone via `.mcp.json` (committed to git) |
| `user`            | Available to you across all projects                    |

```bash
# Make it available across all your projects
claude mcp add --scope user oas -- uvx --from open-agent-search oas-mcp
```
