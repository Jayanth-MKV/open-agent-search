# Contributing

Thanks for your interest in contributing to DDGS Server! This guide will get you up and running.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Jayanth-MKV/ddgs-server.git
cd ddgs-server

# Install uv (if you haven't already)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync all dependencies (including dev tools)
uv sync --dev
```

## Running the Server

```bash
# HTTP API + MCP
uv run ddgs-server

# With hot reload
uv run uvicorn ddgs_server.app:app --reload --host 0.0.0.0 --port 8000

# Standalone MCP (stdio)
uv run ddgs-mcp
```

## Running Tests

```bash
uv run pytest
```

## Code Style

We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
uv run ruff check .
uv run ruff format .
```

Follow [PEP 8](https://peps.python.org/pep-0008/) conventions and use type hints for all function signatures.

## Adding Dependencies

```bash
# Runtime dependency
uv add <package>

# Dev-only dependency
uv add --group dev <package>
```

## Pull Request Process

1. Fork the repo and create your branch from `main`.
2. Add or update tests for any new functionality.
3. Ensure `uv run ruff check .` and `uv run pytest` pass.
4. Update documentation if you changed any public API or behaviour.
5. Open a pull request with a clear description of your changes.

## Reporting Issues

Use [GitHub Issues](https://github.com/Jayanth-MKV/ddgs-server/issues). Include:

- Steps to reproduce
- Expected vs actual behaviour
- Python version and OS

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](https://github.com/Jayanth-MKV/ddgs-server/blob/main/LICENSE).
