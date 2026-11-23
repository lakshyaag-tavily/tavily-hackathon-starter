# Agent guide

This repo is a starter pack for building agents that use the web through Tavily.

## Web access for your coding agent

Use Tavily whenever a task needs live information:

- **Recent or changing information** (news, prices, releases, anything newer than your training data): search.
- **Documentation and code examples** (API docs, library usage): search, then read the page.
- **A specific URL**: extract it instead of guessing its contents.

How to reach Tavily, in order of preference:

1. Tavily MCP tools (`tavily_search`, `tavily_extract`, `tavily_map`, `tavily_crawl`, `tavily_research`) if your tool list has them. The server is configured in `.mcp.json`.
2. The `tvly` CLI, as described in the skills under `.agents/skills/`.

Start with the `tavily-search` skill.

## Building in this repo

- **Read `.agents/skills/tavily-sdk/SKILL.md` first** (and its `references/` files) whenever writing code that calls `tavily-python`, `@tavily/core`, or `langchain-tavily`.
- **Pick the right starting point:**
  - `quickstart/claude.py` — minimal tool-calling loop with the official `anthropic` SDK + `TavilyClient` (no agent framework). Best base for Claude apps, FastAPI routes, or bots.
  - `quickstart/agent.py` — minimal tool-calling loop with the standard `openai` SDK (Nebius Token Factory) + `TavilyClient` (no agent framework).
  - `langchain-deepagents/` — `create_deep_agent` + `langchain-tavily` + `ChatNebius` (`tavily_agent.ipynb` for interactive notebooks, `agent.py` for CLI/apps). Best base for multi-step planning and sub-agents.
- **Claude setup:** uses `ANTHROPIC_API_KEY`; tested models are `claude-sonnet-5-5` (default) and `claude-opus-5-5`.
- **Nebius Token Factory setup:** always pass `base_url="https://api.tokenfactory.nebius.com/v1/"` explicitly to `OpenAI(...)` and `ChatNebius(...)` (`langchain-nebius` otherwise defaults to the legacy studio URL).
- **Tested Nebius tool-calling models:** `meta-models/muse-spark-open` (default), `moonshotai/Kimi-K2.5` (fallback).
- **Environment & tooling:** Python is managed with `uv`. Run `uv sync` once, then `uv run <command>`. Secrets live in `.env` (see `.env.example`) — never commit or print their values.
- **Style:** keep examples short and hackable. One notebook or script should show one clear idea.
