# Installation

## Prerequisites

- **Python 3.12+**
- [**uv**](https://docs.astral.sh/uv/getting-started/installation/) — the fast Python package & project manager

Install `uv`:

=== "macOS / Linux"

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Windows"

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

## Install Methods

### Zero-install with `uvx` (recommended)

No clone, no install — run the MCP server directly:

```bash
uvx --from ddgs-server ddgs-mcp
```

### Install from PyPI

```bash
uv pip install ddgs-server
# or with pip:
pip install ddgs-server
```

After installing, two CLI commands are available:

| Command       | Description                             |
| ------------- | --------------------------------------- |
| `ddgs-server` | Start the HTTP API + MCP server         |
| `ddgs-mcp`    | Start the standalone MCP server (stdio) |

### From Source

```bash
git clone https://github.com/Jayanth-MKV/ddgs-server.git
cd ddgs-server
uv sync            # installs all deps + creates .venv automatically
uv sync --dev      # include dev tools (pytest, ruff, locust)
```

## Verify Installation

```bash
# Check the HTTP API
uv run ddgs-server
# Visit http://localhost:8000/docs for Swagger UI

# Check the MCP server
uv run ddgs-mcp
# The server will start in stdio mode — press Ctrl+C to exit
```
