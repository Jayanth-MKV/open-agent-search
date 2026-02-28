# Developer TLDR

Quick reference for repo owner commands. No fluff.

---

## Setup

```bash
uv sync --dev --group docs   # everything: runtime + dev + docs
```

---

## Day-to-Day

```bash
# Run server (pick one)
uv run ddgs-server                                              # production
uv run uvicorn ddgs_server.app:app --reload --host 0.0.0.0 --port 8000  # dev w/ hot reload
uv run ddgs-mcp                                                 # MCP stdio only

# Lint & format
uv run ruff check .              # lint
uv run ruff check --fix .        # lint + auto-fix
uv run ruff format .             # format
uv run ruff format --check .     # format dry-run (CI uses this)

# Tests
uv run pytest -v                 # unit tests
uv run pytest -x                 # stop on first failure

# Load tests
uv run locust -f tests/locustfile.py --host=http://localhost:8000              # interactive UI
uv run locust -f tests/locustfile.py --host=http://localhost:8000 \
  --users 50 --spawn-rate 5 --run-time 2m --headless                           # headless
```

---

## Docs (GitHub Pages)

Site: `https://jayanth-mkv.github.io/ddgs-server/`

```bash
# Install docs deps (first time)
uv sync --group docs

# Local preview (live reload at http://127.0.0.1:8000)
uv run mkdocs serve

# Build (output → site/)
uv run mkdocs build

# Manual deploy to gh-pages branch
uv run mkdocs gh-deploy --force
```

**Auto-deploy:** pushing to `main` with changes in `docs/` or `mkdocs.yml` triggers the `Deploy Docs` workflow. It builds and pushes to the `gh-pages` branch automatically.

**First-time GitHub Pages setup:**

1. Go to repo **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: **gh-pages** / `/(root)`
4. Save

---

## CI Workflows

### `ci.yml` — Lint + Test

| Trigger      | `push` / `pull_request` to `main`                          |
| ------------ | ---------------------------------------------------------- |
| **lint** job | `ruff check .` + `ruff format --check .`                   |
| **test** job | `pytest -v` on Python 3.12 & 3.13 (runs after lint passes) |

### `docs.yml` — Deploy Docs

| Trigger        | `push` to `main` (only `docs/**`, `mkdocs.yml`) + manual `workflow_dispatch` |
| -------------- | ---------------------------------------------------------------------------- |
| **deploy** job | `mkdocs gh-deploy --force` → pushes built site to `gh-pages` branch          |

---

## Docker

```bash
docker compose up -d             # build + run
docker compose logs -f           # tail logs
docker compose down              # stop
docker compose watch             # dev mode (live sync)
docker build -t ddgs-server .    # manual build
```

---

## Dependencies

```bash
uv add <pkg>               # add runtime dep
uv add --group dev <pkg>   # add dev dep
uv add --group docs <pkg>  # add docs dep
uv lock                    # regenerate lockfile
uv sync --locked           # install from lockfile (CI mode)
```

---

## Publish to PyPI

```bash
uv build                        # builds wheel + sdist → dist/
uv publish                      # upload to PyPI (needs token)
```

---

## Key URLs (local)

| URL                          | What                        |
| ---------------------------- | --------------------------- |
| http://localhost:8000        | API root                    |
| http://localhost:8000/docs   | Swagger UI                  |
| http://localhost:8000/redoc  | ReDoc                       |
| http://localhost:8000/health | Health check                |
| http://localhost:8000/ai/mcp | MCP endpoint                |
| http://127.0.0.1:8000        | mkdocs serve (docs preview) |
