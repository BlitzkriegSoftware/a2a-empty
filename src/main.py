# """
# Entry launcher for A2A agents.

# Usage:
#     # run GOOD (default)
#     python -m src.main

#     # run BAD
#     A2A_AGENT=bad python -m src.main

#     # run EVIL
#     A2A_AGENT=evil python -m src.main
# """

import os

from src.common.error_handler import BaseErrorHandler
from src.common.logging import setup_logger


def run_good() -> None:
    from src.good.a2a_server.main import main as good_main

    good_main()


def run_bad() -> None:
    from src.bad.a2a_server.main import main as bad_main

    bad_main()


def run_evil() -> None:
    from src.evil.a2a_server.main import main as evil_main

    evil_main()


def main() -> None:
    agent = os.getenv("A2A_AGENT", "good").lower()
    error_handler = BaseErrorHandler(component_name="A2ALauncher", exit_on_error=True)
    log_handler = setup_logger("A2ALauncher")

    log_handler.info(f"[A2A Launcher] Starting agent: {agent}")

    def _start():
        if agent == "good":
            run_good()
        elif agent == "bad":
            run_bad()
        elif agent == "evil":
            run_evil()
        else:
            raise ValueError(f"Unknown agent '{agent}'. Use one of: good, bad, evil.")

    error_handler.handle(_start)

    # If we ever return here, the agent was stopped manually
    log_handler.info(f"[A2A Launcher] Agent '{agent}' stopped normally.")


if __name__ == "__main__":
    main()
