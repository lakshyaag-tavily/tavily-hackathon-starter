# Tavily Agent Starter

A minimal starter repo for building AI agents with live web access via [Tavily](https://tavily.com).

Every example runs the same agent two ways: without web access, then with Tavily search and extract tools wired in. The whole point is to give you a clean base you can clone, run in two minutes, and fork into whatever you're building.

## Setup

You'll need [uv](https://docs.astral.sh/uv/), a [Tavily API key](https://app.tavily.com/), and an API key for whichever model provider you want to use:

- **Claude (`quickstart/claude.py`):** `ANTHROPIC_API_KEY` from [Anthropic Console](https://console.anthropic.com/)
- **Nebius Token Factory (`quickstart/agent.py`, `langchain-deepagents/`):** `NEBIUS_API_KEY` from [Nebius Token Factory](https://tokenfactory.nebius.com/)

```bash
cp .env.example .env    # add TAVILY_API_KEY + your model key
uv sync
```

## Where to start

| Folder / File | What's inside | Best for |
|---|---|---|
| [`quickstart/`](quickstart/) | Plain Python tool-calling loops using `anthropic` (`claude.py`) or `openai` (`agent.py`) + `tavily-python` | Dropping into FastAPI, Slack/Discord bots, or custom scripts without an agent framework |
| [`langchain-deepagents/`](langchain-deepagents/) | Interactive Jupyter notebook (`tavily_agent.ipynb`) and CLI script (`agent.py`) built on [LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview) | Multi-step planning, sub-agents, and live walkthroughs |
| [`IDEAS.md`](IDEAS.md) | 6 concrete project ideas paired with Tavily endpoints and starter prompts | Picking a build track and scaffolding fast with your coding agent |

Quick smoke test once `.env` is ready:

```bash
# Claude + Tavily (runs without web, then with Tavily)
uv run quickstart/claude.py --compare

# Nebius Token Factory + Tavily
uv run quickstart/agent.py --compare

# LangChain Deep Agents notebook
uv run jupyter lab langchain-deepagents/tavily_agent.ipynb
```

## Using Tavily in your coding agent

This repo ships with [`.agents/skills/`](.agents/skills/), [`.mcp.json`](.mcp.json), [`AGENTS.md`](AGENTS.md), and [`CLAUDE.md`](CLAUDE.md), so coding agents already have Tavily SDK docs and MCP config when you open the project.

If you want Tavily set up globally across your coding agents (Claude Code, Cursor, Codex):

```bash
npx @tavily/cli init

# On a remote/SSH VM without a local browser (use SSH port forwarding or set TAVILY_API_KEY):
npx @tavily/cli init --no-browser
```

**Using Claude Code?** You can also install the official plugin directly inside a session to get the skills, hosted MCP server, and session hook together:

```text
/plugin install tavily --marketplace tavily-ai/skills
```

Or from the Anthropic marketplace: `claude plugin install tavily@claude-plugins-official`.

**Want just the skills (or ready-made workflows)?** Browse [skills.tavily.com](https://skills.tavily.com) or install from the CLI:

```bash
npx skills add tavily-ai/skills -y
npx skills add tavily-ai/official-workflows --skill tavily-competitor-analysis -y
```

Curious how Tavily stacks up against Claude's built-in web search? Read [Tavily vs. Claude Web Search](https://www.tavily.com/blog/tavily-vs-claude-web-search-when-native-search-isn-t-enough).

## License

[MIT](LICENSE)
