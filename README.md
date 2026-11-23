# Tavily agent starter

A starter pack for building AI agents that can search, read, crawl, and research the live web with [Tavily](https://tavily.com).

Every example builds the same agent twice: **without web access**, then **with Tavily**. Adding web access is one argument:

```python
agent = create_deep_agent(model=model, system_prompt=SYSTEM_PROMPT)

web_agent = create_deep_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[TavilySearch(max_results=5, search_depth="advanced"), TavilyExtract()],
)
```

## Quickstart

You need [uv](https://docs.astral.sh/uv/) and two API keys:

- `NEBIUS_API_KEY` from [Nebius Token Factory](https://tokenfactory.nebius.com/) for model inference
- `TAVILY_API_KEY` from [Tavily](https://app.tavily.com/) for web access

```bash
cp .env.example .env    # fill in NEBIUS_API_KEY and TAVILY_API_KEY
uv sync
```

Pick how you want to run or fork it:

```bash
# 1. Interactive notebook (LangChain Deep Agents — best for walkthroughs)
uv run jupyter lab langchain-deepagents/tavily_agent.ipynb

# 2. Zero-framework Python script (OpenAI SDK + TavilyClient — best to drop into an app)
uv run quickstart/agent.py --compare
uv run quickstart/agent.py "What shipped in the latest FastAPI release?"

# 3. Deep Agents CLI script (planning + multi-step tool calling)
uv run langchain-deepagents/agent.py --compare
```

## What's in the repo

| Path | What it is |
|---|---|
| `quickstart/agent.py` | Minimal ~120-line tool-calling loop using only `openai` + `tavily-python` |
| `langchain-deepagents/tavily_agent.ipynb` | Interactive notebook: agent without vs. with Tavily, plus a competitor-brief use case |
| `langchain-deepagents/agent.py` | Script & importable `build_agent()` version of the Deep Agents starter |
| `.agents/skills/` | [Tavily skills](https://skills.tavily.com) (`tavily-search`, `tavily-sdk`, `tavily-research`, `tavily-entity`, `tavily-list`, `tavily-monitor`) |
| `.mcp.json` | Hosted Tavily MCP server config for coding agents |
| `AGENTS.md` | Repo context + Tavily guidelines for coding agents |

## Use Tavily from your coding agent

This repo already includes `.agents/skills/`, `.mcp.json`, and `AGENTS.md` so coding agents have live web access and up-to-date Tavily SDK docs while you build.

To install Tavily globally across your coding agents ( installs `tvly`, signs in, and configures skills + MCP):

```bash
npx @tavily/cli init

# On a remote/SSH VM without a local browser (use SSH port forwarding or set TAVILY_API_KEY):
npx @tavily/cli init --no-browser
```

To install only the skills, or restore the exact versions pinned in `skills-lock.json`:

```bash
npx skills add https://github.com/tavily-ai/skills
npx skills experimental_install
```

## Ideas to build

Each idea maps to specific Tavily endpoints and a reference skill in `.agents/skills/`. Paste any starter prompt into your coding agent inside this repo to scaffold it.

1. **Fresh-facts assistant** (`search` with `search_depth="advanced"`, `time_range`)
   Answer questions about this week's launches, funding, or live events with inline source citations.
   > *Prompt:* `"Using quickstart/agent.py as a base, build a FastAPI endpoint that answers questions about tech news from the past 7 days with verified source URLs."`

2. **Docs-grounded coding helper** (`map` + `crawl` with `instructions`, `select_paths`)
   Map a library's docs site and crawl the relevant pages before generating code against newly released APIs.
   > *Prompt:* `"Read .agents/skills/tavily-sdk/references/crawl.md and build a CLI tool that maps and crawls a documentation URL, then answers code questions grounded in those pages."`

3. **Account & lead enrichment** (`search` + `extract` · pairs with `tavily-entity`)
   Take a CSV or list of company names, disambiguate each entity, and return structured JSON records (product, pricing model, recent news, HQ) from official pages.
   > *Prompt:* `"Read .agents/skills/tavily-entity/SKILL.md and .agents/skills/tavily-sdk/SKILL.md, then build a script that enriches a list of company names into structured Pydantic records."`

4. **Competitor & changelog monitor** (`search` with `time_range="day"` / `include_domains` · pairs with `tavily-monitor`)
   Track pricing pages, changelogs, and announcements across a list of competitors and report only what changed since the last run.
   > *Prompt:* `"Read .agents/skills/tavily-monitor/SKILL.md and build a competitor monitor on langchain-deepagents/agent.py that diffs new pricing and changelog updates against a local JSON baseline."`

5. **Deep research report generator** (`research` with `model="pro"` / `output_schema`, or parallel `SubAgent`s · pairs with `tavily-research`)
   Produce a cited, decision-grade market or technical report—either via `TavilyClient().research()` or by dispatching specialist sub-agents in Deep Agents.
   > *Prompt:* `"Read .agents/skills/tavily-sdk/references/research.md and build an app that runs Tavily research with a structured output_schema and renders a cited markdown report."`

6. **Draft fact-checker** (`search` + `extract`)
   Break a blog post or memo into discrete claims, verify each claim against primary sources, and flag `supported`, `contradicted`, or `unverified` with quotes.
   > *Prompt:* `"Using quickstart/agent.py, build a CLI fact-checker that extracts claims from a markdown file, checks each one with Tavily search + extract, and outputs a cited verification table."`

## Links

- Tavily docs: https://docs.tavily.com
- Tavily skills: https://skills.tavily.com
- Nebius Token Factory: https://tokenfactory.nebius.com
- Deep Agents docs: https://docs.langchain.com/oss/python/deepagents/overview
