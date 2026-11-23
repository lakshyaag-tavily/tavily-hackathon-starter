# Quickstart (no framework)

Minimal Python tool-calling loops using only the model provider's official SDK and `tavily-python`. Pick whichever script matches your API key and copy `ask()` / `run_tool()` straight into a FastAPI route, bot, or CLI.

| File | Provider & SDK | Default model | Required keys |
|---|---|---|---|
| `claude.py` | Anthropic (`anthropic`) | `claude-sonnet-5-5` | `ANTHROPIC_API_KEY`, `TAVILY_API_KEY` |
| `agent.py` | Nebius Token Factory (`openai`) | `meta-models/muse-spark-open` | `NEBIUS_API_KEY`, `TAVILY_API_KEY` |

Both scripts expose the same two tools (`tavily_search` with `time_range` and `include_domains`, plus `tavily_extract`) and print every tool call and a compact preview of each result live.

## Run

From the repo root (after `uv sync` and setting up `.env`):

```bash
# Anthropic Claude
uv run quickstart/claude.py --compare
uv run quickstart/claude.py "What does PANW do?"
uv run quickstart/claude.py --no-web
uv run quickstart/claude.py --model claude-opus-5-5

# Nebius Token Factory (OpenAI-compatible)
uv run quickstart/agent.py --compare
uv run quickstart/agent.py "What shipped in the latest FastAPI release?"
uv run quickstart/agent.py --no-web
uv run quickstart/agent.py --model reflection/beam
```

## Extending it

- **Add more Tavily tools:** `TavilyClient` also supports `map()`, `crawl()`, and `research()`. See [`../.agents/skills/tavily-sdk/`](../.agents/skills/tavily-sdk/) for parameter references and examples.
- **Swap the model:** Pass `--model <id>` on the CLI or change `DEFAULT_MODEL` at the top of either file.
- **Embed in an app:** Import `ask` directly (`ask("...", with_web=True)`) and return the string response from your web handler or workflow.
