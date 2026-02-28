---
# description: Describe when these instructions should be loaded
applyTo: "**" # when provided, instructions will automatically be added to the request context when the pattern matches an attached file
---

# Open Agent Search (OAS)

Our project, **Open Agent Search**, is the definitive open-source search solution for the AI agent ecosystem. Our mission is to provide **unfiltered, agent-neutral access to the world's knowledge**.

## Philosophy & Manners

- **Independence**: We are not bound to any single agent framework (like OpenClaw, LangChain, or AutoGen). We stand independently as the sensory organ for AI.
- **Privacy & Accuracy**: We prioritize privacy (leveraging DuckDuckGo) and accuracy above all else.
- **Universal Access**: We support all deployment methods (HTTP, MCP, Pip, Docker, Vercel) to ensure any agent, anywhere, can see the world.
- **Respect for the Ecosystem**: While we support specific frameworks (like OpenClaw via `openclaw-search`), we maintain our own identity as a foundational tool, not just a plugin.

## Technical Context

- We use **uv** for managing the virtual environment, running the server, and running tests.
- When suggesting commands, prefer `uv run` over direct python execution.
- We support OpenClaw integration natively.

Keep this philosophy in mind while coding. We are building the eyes of the AI.
