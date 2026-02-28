# Contributing to Open Agent Search

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Jayanth-MKV/open-agent-search.git
cd open-agent-search

# Install uv (if you haven't already)
# https://docs.astral.sh/uv/getting-started/installation/
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync all dependencies (including dev tools)
uv sync --dev
```

## Running the Server

```bash
uv run open-agent-search

# With hot reload for development
uv run uvicorn open_agent_search.app:app --reload --host 0.0.0.0 --port 8000
```

## Running Tests

```bash
uv run pytest
```

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) conventions.
- Use type hints for all function signatures.
- Format code with [Ruff](https://docs.astral.sh/ruff/):

```bash
uv run ruff check .
uv run ruff format .
```

## Pull Request Process

1. Fork the repo and create your branch from `main`.
2. Add or update tests for any new functionality.
3. Make sure `uv run ruff check .` and `uv run pytest` pass.
4. Update the README if you changed any public API or behaviour.
5. Open a pull request with a clear description of your changes.

## Adding Dependencies

```bash
# Add a runtime dependency
uv add <package>

# Add a dev-only dependency
uv add --group dev <package>
```

## Reporting Issues

- Use [GitHub Issues](https://github.com/Jayanth-MKV/open-agent-search/issues).
- Include steps to reproduce, expected behaviour, and actual behaviour.
- Mention your Python version and OS.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
