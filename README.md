# Tavily agent starter

A starter pack for building agents that can use the web.

The notebook builds one agent twice: first without web access, then with [Tavily](https://tavily.com). The difference is one line.

```python
agent = create_deep_agent(model=model, system_prompt=SYSTEM_PROMPT)

web_agent = create_deep_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[TavilySearch(max_results=5), TavilyExtract()],
)
```

## Quickstart

You need [uv](https://docs.astral.sh/uv/) and two API keys:

- `NEBIUS_API_KEY` from [Nebius Token Factory](https://tokenfactory.nebius.com/) for model inference
- `TAVILY_API_KEY` from [Tavily](https://app.tavily.com/) for the web

```bash
cp .env.example .env    # then fill in both keys
uv sync
uv run jupyter lab langchain-deepagents/tavily_agent.ipynb
```

## What's in the repo

| Path | What it is |
|---|---|
| `langchain-deepagents/tavily_agent.ipynb` | The agent with and without Tavily, plus one use case, built on LangChain Deep Agents |
| `.agents/skills/` | [Tavily skills](https://skills.tavily.com) for your coding agent |
| `.mcp.json` | The hosted Tavily MCP server |
| `AGENTS.md` | Instructions that tell a coding agent when and how to use Tavily here |

## Use Tavily from your coding agent

The skills and MCP config in this repo work with any coding agent that reads `.agents/skills/`, `.mcp.json` or `AGENTS.md`.

To set up Tavily for your agent outside this repo, run the guided installer. It installs the `tvly` CLI, signs you in, and adds the skills and MCP server to the agents it finds:

```bash
npx @tavily/cli init
```

To install only the skills:

```bash
npx skills add https://github.com/tavily-ai/skills
```

To restore the skills pinned in `skills-lock.json`:

```bash
npx skills experimental_install
```

## Ideas to build

Each idea starts from the notebook's `web_agent` and leans on a different Tavily tool.

1. **Fresh-facts assistant.** Answer questions about this week's events with cited sources. Uses search.
2. **Docs-grounded coding agent.** Read a library's current docs before writing code against it. Uses map and crawl.
3. **Account or lead enrichment.** Turn a list of company names into filled-in records. Uses search and extract.
4. **Competitor monitor.** Report what changed at three competitors since yesterday. Uses search with a time range.
5. **Deep research report.** Produce a long, cited report on a market or technology. Uses research.
6. **Fact-checker.** Take a draft and mark each claim as supported, contradicted or unverified. Uses search and extract.

## Links

- Tavily docs: https://docs.tavily.com
- Tavily skills: https://skills.tavily.com
- Deep Agents docs: https://docs.langchain.com/oss/python/deepagents/overview
