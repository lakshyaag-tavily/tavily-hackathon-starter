# Agent guide

This repo is a starter pack for building agents that use the web through Tavily.

## Web access

Use Tavily whenever a task needs live information:

- **Recent or changing information** (news, prices, releases, anything newer than your training data): search.
- **Documentation and code examples** (API docs, library usage): search, then read the page.
- **A specific URL**: extract it instead of guessing its contents.

How to reach Tavily, in order of preference:

1. Tavily MCP tools (`tavily_search`, `tavily_extract`, `tavily_map`, `tavily_crawl`, `tavily_research`) if your tool list has them. The server is configured in `.mcp.json`.
2. The `tvly` CLI, as described in the skills under `.agents/skills/`.

Start with the `tavily-search` skill. Use `tavily-sdk` when writing code that calls Tavily.

## Working in this repo

- Python is managed with `uv`. Run `uv sync` once, then `uv run <command>`.
- Secrets live in `.env` (see `.env.example`). Never commit it or print its values.
- Each agent framework has its own top-level folder, for example `langchain-deepagents/`.
- Keep examples short. One notebook should show one idea.
