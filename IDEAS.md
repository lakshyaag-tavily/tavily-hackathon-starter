# Project Ideas

Six concrete starting points for a hackathon or build day. Each one exercises a different part of the [Tavily API](https://docs.tavily.com) and pairs with the skills already bundled in [`.agents/skills/`](.agents/skills/).

If you're using Claude Code, Cursor, or another coding agent inside this repo, you can paste any of the starter prompts below directly to scaffold a first version.

## 1. Fresh-facts assistant

**Tavily endpoints:** `search` (`search_depth="advanced"`, `time_range`)

Answer questions about this week's product launches, funding rounds, or live events with inline source citations that point back to primary reporting.

> **Starter prompt:** `"Using quickstart/claude.py as a base, build a FastAPI endpoint that answers questions about tech news from the past 7 days with verified source URLs."`

## 2. Docs-grounded coding helper

**Tavily endpoints:** `map` + `crawl` (`instructions`, `select_paths`)

Map a library's documentation site, crawl the relevant pages, and answer code questions grounded in the latest release instead of stale training data.

> **Starter prompt:** `"Read .agents/skills/tavily-sdk/references/crawl.md and build a CLI tool that maps and crawls a documentation URL, then answers code questions grounded in those pages."`

## 3. Account & lead enrichment

**Tavily endpoints:** `search` + `extract` · **Skill:** `tavily-entity`

Take a CSV or list of company names, disambiguate each one, and return structured records (what they sell, pricing model, recent news, HQ) pulled from official pages.

> **Starter prompt:** `"Read .agents/skills/tavily-entity/SKILL.md and .agents/skills/tavily-sdk/SKILL.md, then build a script that enriches a list of company names into structured Pydantic records."`

## 4. Competitor & changelog monitor

**Tavily endpoints:** `search` (`time_range="day"`, `include_domains`) + `extract` · **Skill:** `tavily-monitor`

Watch pricing pages, changelogs, and release blogs across a list of competitors and report only what changed since the last run.

> **Starter prompt:** `"Read .agents/skills/tavily-monitor/SKILL.md and build a competitor monitor on langchain-deepagents/agent.py that diffs new pricing and changelog updates against a local JSON baseline."`

## 5. Deep research report generator

**Tavily endpoints:** `research` (`model="pro"`, `output_schema`) or parallel sub-agents · **Skill:** `tavily-research`

Generate a cited market or technical report—either directly via `TavilyClient().research()` with a structured schema, or by fanning out specialist sub-agents in Deep Agents.

> **Starter prompt:** `"Read .agents/skills/tavily-sdk/references/research.md and build an app that runs Tavily research with a structured output_schema and renders a cited markdown report."`

## 6. Draft fact-checker

**Tavily endpoints:** `search` + `extract`

Break a blog post, memo, or pitch deck into discrete claims, verify each claim against primary sources, and flag it as `supported`, `contradicted`, or `unverified` with supporting quotes.

> **Starter prompt:** `"Using quickstart/claude.py, build a CLI fact-checker that extracts claims from a markdown file, checks each one with Tavily search + extract, and outputs a cited verification table."`

---

## Ready-made workflow skills

If you'd rather start from a complete workflow inside your coding agent, [skills.tavily.com](https://skills.tavily.com) also publishes six ready-to-install workflows (`tavily-lead-gen`, `tavily-competitor-analysis`, `tavily-due-diligence`, `tavily-market-research`, `tavily-meeting-prep`, `tavily-literature-review`):

```bash
npx skills add tavily-ai/official-workflows --skill tavily-lead-gen -y
```
