import inspect
import sys
import traceback
from typing import Any, Callable, Optional


class BaseErrorHandler:
    """Reusable error handling utility for A2A components."""

    def __init__(
        self, component_name: str = "A2AComponent", exit_on_error: bool = True
    ):
        self.component_name = component_name
        self.exit_on_error = exit_on_error

    # ---------- SYNC handler (for launcher, server startup) ----------

    def handle(
        self, func: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Optional[Any]:
        """Handle errors for synchronous functions."""
        try:
            return func(*args, **kwargs)
        except ImportError as e:
            self._log_error("ImportError", f"Missing dependency or bad import: {e}")
            self._print_trace()
            self._exit(2)
        except ValueError as e:
            self._log_error("ValueError", str(e))
            self._exit(3)
        except Exception as e:
            self._log_error("UnexpectedError", f"{type(e).__name__}: {e}")
            self._print_trace()
            self._exit(1)

    # ---------- ASYNC handler (for executors, async clients) ----------

    async def handle_async(
        self, func: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Optional[Any]:
        """Handle errors for asynchronous functions (or sync if passed)."""
        try:
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        except ImportError as e:
            self._log_error("ImportError", f"Missing dependency or bad import: {e}")
            self._print_trace()
            self._exit(2)
        except ValueError as e:
            self._log_error("ValueError", str(e))
            self._exit(3)
        except Exception as e:
            self._log_error("UnexpectedError", f"{type(e).__name__}: {e}")
            self._print_trace()
            self._exit(1)

    # ---------- internals ----------

    def _log_error(self, error_type: str, message: str) -> None:
        print(f"[{self.component_name}:{error_type}] {message}")

    def _print_trace(self) -> None:
        traceback.print_exc()

    def _exit(self, code: int) -> None:
        if self.exit_on_error:
            sys.exit(code)
