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

You need [uv](https://docs.astral.sh/uv/), a [Tavily API key](https://app.tavily.com/) (`TAVILY_API_KEY`), and an API key for whichever model provider you're using:

- `ANTHROPIC_API_KEY` from [Anthropic Console](https://console.anthropic.com/) for `quickstart/claude.py`
- `NEBIUS_API_KEY` from [Nebius Token Factory](https://tokenfactory.nebius.com/) for `quickstart/agent.py` and `langchain-deepagents/`

```bash
cp .env.example .env    # fill in TAVILY_API_KEY + ANTHROPIC_API_KEY or NEBIUS_API_KEY
uv sync
```

Pick how you want to run or fork it:

```bash
# 1. Zero-framework Claude script (Anthropic SDK + TavilyClient)
uv run quickstart/claude.py --compare
uv run quickstart/claude.py "What does PANW do?"

# 2. Zero-framework Nebius script (OpenAI SDK + TavilyClient)
uv run quickstart/agent.py --compare
uv run quickstart/agent.py "What shipped in the latest FastAPI release?"

# 3. Interactive notebook (LangChain Deep Agents — best for walkthroughs)
uv run jupyter lab langchain-deepagents/tavily_agent.ipynb

# 4. Deep Agents CLI script (planning + multi-step tool calling)
uv run langchain-deepagents/agent.py
uv run langchain-deepagents/agent.py --no-web
```

## What's in the repo

| Path | What it is |
|---|---|
| `quickstart/claude.py` | Minimal tool-calling loop using `anthropic` + `tavily-python` |
| `quickstart/agent.py` | Minimal tool-calling loop using `openai` (Nebius Token Factory) + `tavily-python` |
| `langchain-deepagents/tavily_agent.ipynb` | Interactive notebook: agent without vs. with Tavily, plus a competitor-brief use case |
| `langchain-deepagents/agent.py` | Script & importable `build_agent()` version of the Deep Agents starter |
| `.agents/skills/` | [Tavily skills](https://skills.tavily.com) (`tavily-search`, `tavily-sdk`, `tavily-research`, `tavily-entity`, `tavily-list`, `tavily-monitor`) |
| `.mcp.json` | Hosted Tavily MCP server config for coding agents |
| `AGENTS.md` / `CLAUDE.md` | Repo context + Tavily guidelines for coding agents |

## Use Tavily from your coding agent

This repo already includes `.agents/skills/`, `.mcp.json`, and `AGENTS.md` (`CLAUDE.md`) so coding agents have live web access and up-to-date Tavily SDK docs while you build.

**Guided setup (Claude Code, Cursor, Codex)** — installs `tvly`, signs in, configures skills + MCP, and verifies a live search:

```bash
npx @tavily/cli init

# On a remote/SSH VM without a local browser (use SSH port forwarding or set TAVILY_API_KEY):
npx @tavily/cli init --no-browser
```

**Claude Code plugin** — adds the Tavily skills, hosted MCP server, and session hook directly inside Claude Code:

```text
/plugin install tavily --marketplace tavily-ai/skills
```

Or from the official Anthropic marketplace: `claude plugin install tavily@claude-plugins-official`.

**Skills only** — install the core skills or add ready-made workflow skills from [skills.tavily.com](https://skills.tavily.com) (`tavily-lead-gen`, `tavily-competitor-analysis`, `tavily-due-diligence`, `tavily-market-research`, `tavily-meeting-prep`, `tavily-literature-review`):

```bash
npx skills add tavily-ai/skills -y
npx skills add tavily-ai/official-workflows --skill tavily-competitor-analysis -y
```

*Curious how Tavily compares to Claude's built-in web search? See [Tavily vs. Claude Web Search](https://www.tavily.com/blog/tavily-vs-claude-web-search-when-native-search-isn-t-enough).*

## Ideas to build

Each idea maps to specific Tavily endpoints and a reference skill in `.agents/skills/`. Paste any starter prompt into your coding agent inside this repo to scaffold it.

1. **Fresh-facts assistant** (`search` with `search_depth="advanced"`, `time_range`)
   Answer questions about this week's launches, funding, or live events with inline source citations.
   > *Prompt:* `"Using quickstart/claude.py as a base, build a FastAPI endpoint that answers questions about tech news from the past 7 days with verified source URLs."`

2. **Docs-grounded coding helper** (`map` + `crawl` with `instructions`, `select_paths`)
   Map a library's docs site and crawl the relevant pages before generating code against newly released APIs.
   > *Prompt:* `"Read .agents/skills/tavily-sdk/references/crawl.md and build a CLI tool that maps and crawls a documentation URL, then answers code questions grounded in those pages."`

3. **Account & lead enrichment** (`search` + `extract` · pairs with `tavily-entity` / `tavily-lead-gen`)
   Take a CSV or list of company names, disambiguate each entity, and return structured JSON records (product, pricing model, recent news, HQ) from official pages.
   > *Prompt:* `"Read .agents/skills/tavily-entity/SKILL.md and .agents/skills/tavily-sdk/SKILL.md, then build a script that enriches a list of company names into structured Pydantic records."`

4. **Competitor & changelog monitor** (`search` with `time_range="day"` / `include_domains` · pairs with `tavily-monitor` / `tavily-competitor-analysis`)
   Track pricing pages, changelogs, and announcements across a list of competitors and report only what changed since the last run.
   > *Prompt:* `"Read .agents/skills/tavily-monitor/SKILL.md and build a competitor monitor on langchain-deepagents/agent.py that diffs new pricing and changelog updates against a local JSON baseline."`

5. **Deep research report generator** (`research` with `model="pro"` / `output_schema`, or parallel `SubAgent`s · pairs with `tavily-research`)
   Produce a cited, decision-grade market or technical report—either via `TavilyClient().research()` or by dispatching specialist sub-agents in Deep Agents.
   > *Prompt:* `"Read .agents/skills/tavily-sdk/references/research.md and build an app that runs Tavily research with a structured output_schema and renders a cited markdown report."`

6. **Draft fact-checker** (`search` + `extract`)
   Break a blog post or memo into discrete claims, verify each claim against primary sources, and flag `supported`, `contradicted`, or `unverified` with quotes.
   > *Prompt:* `"Using quickstart/claude.py, build a CLI fact-checker that extracts claims from a markdown file, checks each one with Tavily search + extract, and outputs a cited verification table."`

## Links

- Tavily docs: https://docs.tavily.com
- Tavily skills & workflows: https://skills.tavily.com
- Tavily vs. Claude Web Search: https://www.tavily.com/blog/tavily-vs-claude-web-search-when-native-search-isn-t-enough
- Anthropic Console: https://console.anthropic.com
- Nebius Token Factory: https://tokenfactory.nebius.com
- Deep Agents docs: https://docs.langchain.com/oss/python/deepagents/overview
