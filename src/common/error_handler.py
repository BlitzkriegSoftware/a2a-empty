from __future__ import annotations

import inspect
import logging
import sys
import traceback
from typing import Awaitable, Callable, Optional, ParamSpec, TypeVar, overload

P = ParamSpec("P")
T = TypeVar("T")


class BaseErrorHandler:
    """
    Reusable error handling utility for A2A components.
    Provides:
    - handle():     runs synchronous callables and handles exceptions.
    - handle_async(): runs async or sync callables and handles exceptions.
    - structured logging via component-specific loggers.
    """

    def __init__(
        self,
        component_name: str,
        *,
        exit_on_error: bool = True,
        trace_printer: Callable[[], None] | None = None,
    ) -> None:
        self.component_name = component_name
        self.exit_on_error = exit_on_error
        self._logger = logging.getLogger(component_name)
        self._trace_printer = trace_printer or self._default_trace_printer

    # ======================================================================
    # SYNC HANDLER
    # ======================================================================

    def handle(
        self,
        func: Callable[P, T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Optional[T]:
        """Execute a synchronous callable and handle any exceptions."""
        try:
            return func(*args, **kwargs)
        except ImportError as exc:
            self._log_error("ImportError", f"Missing dependency or bad import: {exc}")
        except ValueError as exc:
            self._log_error("ValueError", str(exc))
        except Exception as exc:  # noqa: BLE001
            self._log_error("UnexpectedError", f"{type(exc).__name__}: {exc}")

        self._trace_printer()
        self._exit(1)
        return None

    # ======================================================================
    # ASYNC HANDLER (supports async & sync callables)
    # ======================================================================

    @overload
    async def handle_async(
        self,
        func: Callable[P, T],  # sync function
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Optional[T]: ...

    @overload
    async def handle_async(
        self,
        func: Callable[P, "Awaitable[T]"],  # async function
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Optional[T]: ...

    async def handle_async(
        self,
        func: Callable[P, T] | Callable[P, "Awaitable[T]"],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Optional[T]:
        """Execute an async or sync callable and handle exceptions."""
        try:
            # async callable case
            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
                return result

            # sync callable case
            result = func(*args, **kwargs)
            return result  # type: ignore

        except ImportError as exc:
            self._log_error("ImportError", f"Missing dependency or bad import: {exc}")
        except ValueError as exc:
            self._log_error("ValueError", str(exc))
        except Exception as exc:  # noqa: BLE001
            self._log_error("UnexpectedError", f"{type(exc).__name__}: {exc}")

        self._trace_printer()
        self._exit(1)
        return None

    # ======================================================================
    # INTERNAL HELPERS
    # ======================================================================

    def _log_error(self, error_type: str, message: str) -> None:
        """Log the error using the component logger with a consistent prefix."""
        full_message = f"[{error_type}] {message}"
        if self._logger.handlers:
            self._logger.error(full_message)
        else:
            # fallback when logger not configured
            print(f"[{self.component_name}] {full_message}")

    def _default_trace_printer(self) -> None:
        traceback.print_exc()

    def _exit(self, code: int) -> None:
        if self.exit_on_error:
            sys.exit(code)
