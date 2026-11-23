"""LangChain Deep Agents + Tavily CLI and importable agent builder.

Run:
    uv run langchain-deepagents/agent.py
    uv run langchain-deepagents/agent.py "Write a competitive brief on Tavily."
    uv run langchain-deepagents/agent.py --no-web
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

from deepagents import create_deep_agent
from dotenv import find_dotenv, load_dotenv
from langchain_core.messages import AIMessage, ToolMessage
from langchain_nebius import ChatNebius
from langchain_tavily import TavilyExtract, TavilySearch
from rich.console import Console
from rich.markdown import Markdown
from rich.markup import escape
from rich.panel import Panel

TOKEN_FACTORY_URL = "https://api.tokenfactory.nebius.com/v1/"
DEFAULT_MODEL = "meta-models/muse-spark-open"  # Fallback: "reflection/beam"
DEFAULT_QUESTION = (
    "What are the three newest models on Nebius Token Factory, and when was each one added?"
)

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


def build_agent(*, with_web: bool = True, model_name: str = DEFAULT_MODEL):
    """Build the Deep Agent, toggling web access with the `tools` argument."""
    model = ChatNebius(model=model_name, base_url=TOKEN_FACTORY_URL)
    system_prompt = (
        f"Today is {time.strftime('%Y-%m-%d')}. You are a helpful assistant.\n"
        "Answer the question directly. Cite a source URL for every fact you look up."
    )
    tools = (
        [TavilySearch(max_results=5, search_depth="advanced"), TavilyExtract()]
        if with_web
        else []
    )
    return create_deep_agent(model=model, system_prompt=system_prompt, tools=tools)


def _truncate(value, max_chars: int = 60):
    if isinstance(value, str):
        text = " ".join(value.split())
        return text if len(text) <= max_chars else text[: max_chars - 1] + "…"
    if isinstance(value, dict):
        return {k: _truncate(v, max_chars) for k, v in value.items() if v not in (None, [], "")}
    if isinstance(value, list):
        return [_truncate(v, max_chars) for v in value]
    return value


def _print_tool_result(name: str, content, indent: str = "") -> None:
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            line = _truncate(content, 160)
            console.print(f"{indent}[dim]← {name} {escape(line)}[/dim]", no_wrap=True, overflow="ellipsis")
            return
    data = content.get("results", content) if isinstance(content, dict) else content
    line = json.dumps(_truncate(data), ensure_ascii=False)
    console.print(f"{indent}[dim]← {name} {escape(line)}[/dim]", no_wrap=True, overflow="ellipsis")


def ask(agent, question: str, *, title: str = "Agent") -> str:
    """Stream the agent run, printing each tool call and result live."""
    started = time.time()
    tool_calls = 0
    answer = ""

    stream = agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="updates",
        subgraphs=True,
    )
    for namespace, update in stream:
        indent = "  " if namespace else ""
        for partial in (update or {}).values():
            if not isinstance(partial, dict):
                continue
            for msg in partial.get("messages") or []:
                if isinstance(msg, AIMessage):
                    for call in msg.tool_calls or []:
                        tool_calls += 1
                        args_str = json.dumps(call.get("args", {}), default=str)
                        console.print(f"{indent}[cyan]→ {call['name']}[/cyan] [dim]{args_str}[/dim]")
                    if not namespace and not msg.tool_calls and msg.text.strip():
                        answer = msg.text
                elif isinstance(msg, ToolMessage):
                    _print_tool_result(msg.name or "tool", msg.content, indent=indent)

    elapsed = time.time() - started
    console.print(
        Panel(
            Markdown(answer or "_No answer returned._"),
            title=title,
            subtitle=f"{tool_calls} tool calls · {elapsed:.1f}s",
            border_style="green" if tool_calls else "yellow",
        )
    )
    return answer


def main() -> None:
    parser = argparse.ArgumentParser(description="LangChain Deep Agents + Tavily starter.")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("--no-web", action="store_true", help="Disable Tavily web tools.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Nebius Token Factory model ID.")
    args = parser.parse_args()

    load_dotenv(find_dotenv())
    with_web = not args.no_web
    check_env(require_tavily=with_web)

    console.print(f"[bold]Question:[/] {args.question}\n")
    agent = build_agent(with_web=with_web, model_name=args.model)
    label = "With Tavily" if with_web else "Without Tavily"
    ask(agent, args.question, title=f"{label} · {args.model}")


if __name__ == "__main__":
    main()
