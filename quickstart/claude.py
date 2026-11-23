"""Minimal web-connected agent using the Anthropic SDK + Tavily (no agent framework).

Run:
    uv run quickstart/claude.py
    uv run quickstart/claude.py "What does PANW do?"
    uv run quickstart/claude.py --compare
    uv run quickstart/claude.py --no-web
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

from anthropic import Anthropic
from dotenv import find_dotenv, load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.markup import escape
from rich.panel import Panel
from tavily import TavilyClient

DEFAULT_MODEL = "claude-sonnet-5-5"  # Fallback: "claude-opus-5-5"
DEFAULT_QUESTION = "What does PANW do?"

TOOLS = [
    {
        "name": "tavily_search",
        "description": (
            "Search the live web for current facts, news, docs, or URLs. "
            "Supports recency and domain filters."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Focused search-engine query (keep concise).",
                },
                "time_range": {
                    "type": "string",
                    "enum": ["day", "week", "month", "year"],
                    "description": "Optional recency filter for recent events or news.",
                },
                "include_domains": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of domains to restrict search to.",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "tavily_extract",
        "description": "Read the full markdown content of one or more specific URLs.",
        "input_schema": {
            "type": "object",
            "properties": {
                "urls": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "URLs to extract in full (max 20).",
                },
            },
            "required": ["urls"],
        },
    },
]

console = Console()


def check_env(require_tavily: bool = True) -> None:
    needed = ["ANTHROPIC_API_KEY"] + (["TAVILY_API_KEY"] if require_tavily else [])
    missing = [key for key in needed if not os.getenv(key)]
    if missing:
        console.print(
            Panel(
                f"Missing env var(s): [bold red]{', '.join(missing)}[/]\n\n"
                "Copy [cyan].env.example[/] to [cyan].env[/] and add your keys:\n"
                "• ANTHROPIC_API_KEY → https://console.anthropic.com/\n"
                "• TAVILY_API_KEY → https://app.tavily.com/",
                title="Setup required",
                border_style="red",
            )
        )
        sys.exit(1)


def _truncate(value, max_chars: int = 60):
    if isinstance(value, str):
        text = " ".join(value.split())
        return text if len(text) <= max_chars else text[: max_chars - 1] + "…"
    if isinstance(value, dict):
        return {k: _truncate(v, max_chars) for k, v in value.items() if v not in (None, [], "")}
    if isinstance(value, list):
        return [_truncate(v, max_chars) for v in value]
    return value


def _print_tool_result(name: str, result) -> None:
    data = result.get("results", result) if isinstance(result, dict) else result
    line = json.dumps(_truncate(data), ensure_ascii=False)
    console.print(f"[dim]← {name} {escape(line)}[/dim]", no_wrap=True, overflow="ellipsis")


def run_tool(tavily: TavilyClient, name: str, args: dict) -> dict:
    if name == "tavily_search":
        kwargs: dict = {
            "query": args["query"],
            "search_depth": "advanced",
            "max_results": 5,
        }
        if args.get("time_range"):
            kwargs["time_range"] = args["time_range"]
        if args.get("include_domains"):
            kwargs["include_domains"] = args["include_domains"]
        return tavily.search(**kwargs)
    if name == "tavily_extract":
        urls = args["urls"]
        return tavily.extract(urls=[urls] if isinstance(urls, str) else urls)
    return {"error": f"Unknown tool: {name}"}


def ask(
    question: str,
    *,
    with_web: bool = True,
    model: str = DEFAULT_MODEL,
    max_turns: int = 6,
) -> str:
    """Run a tool-calling loop with Claude, with or without Tavily."""
    client = Anthropic()
    tavily = TavilyClient() if with_web else None

    system_prompt = (
        f"Today is {time.strftime('%Y-%m-%d')}. You are a helpful assistant. "
        "Answer the question directly. Cite a source URL for every fact you look up."
    )
    messages: list = [{"role": "user", "content": question}]

    started = time.time()
    tool_calls = 0
    answer = ""

    for turn in range(max_turns):
        use_tools = with_web and turn < max_turns - 1
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_prompt,
            messages=messages,
            **({"tools": TOOLS} if use_tools else {}),
        )
        messages.append({"role": "assistant", "content": response.content})

        tool_uses = [block for block in response.content if block.type == "tool_use"]
        if not tool_uses:
            answer = "\n".join(
                block.text for block in response.content if block.type == "text"
            ).strip()
            break

        tool_results = []
        for block in tool_uses:
            tool_calls += 1
            args_str = json.dumps(block.input, ensure_ascii=False)
            console.print(f"[cyan]→ {block.name}[/cyan] [dim]{escape(args_str)}[/dim]")
            assert tavily is not None
            result = run_tool(tavily, block.name, block.input)
            _print_tool_result(block.name, result)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                }
            )
        messages.append({"role": "user", "content": tool_results})

    elapsed = time.time() - started
    title = "With Tavily" if with_web else "Without Tavily"
    console.print(
        Panel(
            Markdown(answer or "_No answer returned._"),
            title=f"{title} · {model}",
            subtitle=f"{tool_calls} tool calls · {elapsed:.1f}s",
            border_style="green" if with_web else "yellow",
        )
    )
    return answer


def main() -> None:
    parser = argparse.ArgumentParser(description="Anthropic SDK + Tavily quickstart agent.")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("--no-web", action="store_true", help="Disable Tavily web tools.")
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Run the same question first without Tavily, then with Tavily.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Anthropic model ID.")
    args = parser.parse_args()

    load_dotenv(find_dotenv())
    check_env(require_tavily=args.compare or not args.no_web)

    console.print(f"[bold]Question:[/] {args.question}\n")
    if args.compare:
        ask(args.question, with_web=False, model=args.model)
        console.print()
        ask(args.question, with_web=True, model=args.model)
    else:
        ask(args.question, with_web=not args.no_web, model=args.model)


if __name__ == "__main__":
    main()
