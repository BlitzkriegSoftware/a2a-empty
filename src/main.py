from __future__ import annotations

import argparse
import asyncio
import os
from collections.abc import Sequence
from typing import Optional

from src.common.error_handler import BaseErrorHandler
from src.common.logging import setup_logger


def _build_parser() -> argparse.ArgumentParser:
    """Create the top-level CLI parser."""
    parser = argparse.ArgumentParser(
        prog="a2a",
        description="A2A demo launcher for agents and client.",
    )

    parser.add_argument(
        "command",
        nargs="?",
        choices=("server", "client"),
        default="server",
        help="What to run: 'server' (default) or 'client'.",
    )

    parser.add_argument(
        "--agent",
        choices=("good", "bad", "evil"),
        default=os.getenv("A2A_AGENT", "good").lower(),
        help="Agent to run. Defaults to env A2A_AGENT or 'good'.",
    )

    return parser


def _ensure_valid_agent(agent: str) -> str:
    """Validate and normalize the agent name."""
    normalized = agent.lower()
    if normalized not in {"good", "bad", "evil"}:
        raise ValueError(f"Unknown agent {agent!r}. Use one of 'good', 'bad', 'evil'.")
    return normalized


def run_server(agent: str) -> int:
    """
    Run the selected agent server.

    This is a synchronous entrypoint so it can be safely used from the CLI.
    """
    agent_name = _ensure_valid_agent(agent)
    logger = setup_logger("A2ALauncher")
    error_handler = BaseErrorHandler(
        component_name="A2ALauncherServer", exit_on_error=True
    )

    logger.info("[A2ALauncher] Starting command=server agent=%s", agent_name)

    def _runner() -> None:
        if agent_name == "good":
            from src.good.a2a_server.main import main as good_main

            good_main()
        elif agent_name == "bad":
            from src.bad.a2a_server.main import main as bad_main

            bad_main()
        else:  # agent_name == "evil"
            from src.evil.a2a_server.main import main as evil_main

            evil_main()

    error_handler.handle(_runner)

    logger.info("[A2ALauncher] Finished command=server agent=%s", agent_name)
    return 0


def run_client(agent: str) -> int:
    """
    Run the selected agent client.

    The underlying client is async, so we bridge it using asyncio.run().
    """
    agent_name = _ensure_valid_agent(agent)
    logger = setup_logger("A2ALauncher")
    error_handler = BaseErrorHandler(
        component_name="A2ALauncherClient", exit_on_error=True
    )

    logger.info("[A2ALauncher] Starting command=client agent=%s", agent_name)

    async def _runner() -> None:
        if agent_name == "good":
            # NOTE: test_client.main is async
            from src.good.a2a_server.test_client import main as good_client_main

            await good_client_main()
        elif agent_name == "bad":
            from src.bad.a2a_server.test_client import main as bad_client_main

            await bad_client_main()
        else:  # agent_name == "evil"
            from src.evil.a2a_server.test_client import main as evil_client_main

            await evil_client_main()

    # Ensure the coroutine is awaited exactly once
    asyncio.run(error_handler.handle_async(_runner))

    logger.info("[A2ALauncher] Finished command=client agent=%s", agent_name)
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    """
    CLI entrypoint.

    Example:
        python -m src.main server --agent good
        python -m src.main client --agent good
    """
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    command: str = args.command
    agent: str = args.agent

    if command == "server":
        return run_server(agent)

    if command == "client":
        return run_client(agent)

    # Argparse should prevent us from ever getting here.
    raise ValueError(f"Unexpected command {command!r}.")


if __name__ == "__main__":
    raise SystemExit(main())
