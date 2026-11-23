# LangChain Deep Agents + Tavily

An agent built with [LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview), `langchain-tavily`, and `ChatNebius` on [Nebius Token Factory](https://tokenfactory.nebius.com/).

Adding web access to a Deep Agent is one argument:

```python
agent = create_deep_agent(model=model, system_prompt=SYSTEM_PROMPT)

web_agent = create_deep_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[TavilySearch(max_results=5, search_depth="advanced"), TavilyExtract()],
)
```

## Files

- **`tavily_agent.ipynb`** — Interactive walkthrough: builds the agent without web access, adds `TavilySearch` + `TavilyExtract`, and runs a multi-step company brief with live tool streaming.
- **`agent.py`** — CLI script and importable `build_agent(with_web=...)` / `ask()` helper with the same live tool-call and truncated JSON result output.

## Setup & run

Requires `NEBIUS_API_KEY` and `TAVILY_API_KEY` in the repo root's `.env`. From the repo root:

```bash
# Interactive notebook
uv run jupyter lab langchain-deepagents/tavily_agent.ipynb

# CLI script
uv run langchain-deepagents/agent.py
uv run langchain-deepagents/agent.py "Write a competitive brief on Palo Alto Networks."
uv run langchain-deepagents/agent.py --no-web
uv run langchain-deepagents/agent.py --model reflection/beam
```

## Notes

- **Nebius Token Factory URL:** `ChatNebius` defaults to the legacy studio endpoint, so both files pass `base_url="https://api.tokenfactory.nebius.com/v1/"` explicitly.
- **Fallback model:** Default is `meta-models/muse-spark-open`. If that endpoint is busy during an event, pass `--model reflection/beam`.
- **More Tavily tools:** `TavilyMap`, `TavilyCrawl`, and `TavilyResearch` live in the same `langchain_tavily` package—see [`../.agents/skills/tavily-sdk/references/integrations.md`](../.agents/skills/tavily-sdk/references/integrations.md).
