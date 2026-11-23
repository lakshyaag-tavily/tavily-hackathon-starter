"""Minimal web-connected agent using the OpenAI SDK + Tavily (no agent framework).

Run:
    uv run quickstart/agent.py
    uv run quickstart/agent.py "What shipped in Python 3.14?"
    uv run quickstart/agent.py --compare
    uv run quickstart/agent.py --no-web
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.markup import escape
from rich.panel import Panel
from tavily import TavilyClient

TOKEN_FACTORY_URL = "https://api.tokenfactory.nebius.com/v1/"
DEFAULT_MODEL = "meta-models/muse-spark-open"
DEFAULT_QUESTION = (
    "What are the three newest models on Nebius Token Factory, and when was each one added?"
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "tavily_search",
            "description": (
                "Search the live web for current facts, news, docs, or URLs. "
                "Supports recency and domain filters."
            ),
            "parameters": {
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
    },
    {
        "type": "function",
        "function": {
            "name": "tavily_extract",
            "description": "Read the full markdown content of one or more specific URLs.",
            "parameters": {
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
    },
]

console = Console()


def check_env(require_tavily: bool = True) -> None:
    needed = ["NEBIUS_API_KEY"] + (["TAVILY_API_KEY"] if require_tavily else [])
    missing = [key for key in needed if not os.getenv(key)]
    if missing:
        console.print(
            Panel(
                f"Missing env var(s): [bold red]{', '.join(missing)}[/]\n\n"
                "Copy [cyan].env.example[/] to [cyan].env[/] and add your keys:\n"
                "• NEBIUS_API_KEY → https://tokenfactory.nebius.com/\n"
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


def run_tool(tavily: TavilyClient, name: str, raw_args: str) -> dict:
    args = json.loads(raw_args or "{}")
    if name == "tavily_search":
        kwargs: dict = {
            "query": args["query"],
            "search_depth": "fast",
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
    """Run a tool-calling loop against Nebius Token Factory, with or without Tavily."""
    client = OpenAI(base_url=TOKEN_FACTORY_URL, api_key=os.environ["NEBIUS_API_KEY"])
    tavily = TavilyClient() if with_web else None

    system_prompt = (
        f"Today is {time.strftime('%Y-%m-%d')}. You are a helpful assistant. "
        "Answer the question directly. Cite a source URL for every fact you look up."
    )
    messages: list = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    started = time.time()
    tool_calls = 0
    answer = ""

    for turn in range(max_turns):
        use_tools = with_web and turn < max_turns - 1
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            **({"tools": TOOLS} if use_tools else {}),
        )
        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            answer = msg.content or ""
            break

        for call in msg.tool_calls:
            tool_calls += 1
            console.print(
                f"[cyan]→ {call.function.name}[/cyan] [dim]{call.function.arguments}[/dim]"
            )
            assert tavily is not None
            result = run_tool(tavily, call.function.name, call.function.arguments)
            _print_tool_result(call.function.name, result)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result),
                }
            )

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
    parser = argparse.ArgumentParser(description="OpenAI SDK + Tavily quickstart agent.")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("--no-web", action="store_true", help="Disable Tavily web tools.")
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Run the same question first without Tavily, then with Tavily.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Nebius Token Factory model ID.")
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
