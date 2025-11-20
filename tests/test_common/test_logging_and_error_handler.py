# TODO: revisit test for this
# from __future__ import annotations

# import asyncio
# import logging
# from pathlib import Path
# from typing import Any,  Coroutine, TypeVar

# import pytest
# from _pytest.logging import LogCaptureFixture
# from logging.handlers import RotatingFileHandler

# from src.common.error_handler import BaseErrorHandler
# from src.common.logging import setup_logger

# T = TypeVar("T")


# # ---------------------------------------------------------------------------
# # Helpers
# # ---------------------------------------------------------------------------


# def _reset_logger(component_name: str) -> None:
#     """Remove all handlers for a named logger (to avoid cross-test leakage)."""
#     logger = logging.getLogger(component_name)
#     for handler in list(logger.handlers):
#         logger.removeHandler(handler)
#         handler.close()
#     logger.handlers.clear()


# def _run(coro: Coroutine[Any, Any, T]) -> T:
#     """Run an async coroutine using asyncio.run with a clear return type."""
#     return asyncio.run(coro)


# # def _flush_logger(logger: logging.Logger) -> None:
# #     """Flush all handlers on a logger."""
# #     for handler in logger.handlers:
# #         handler.flush()


# # ---------------------------------------------------------------------------
# # Fixtures
# # ---------------------------------------------------------------------------


# @pytest.fixture()
# def component_name() -> str:
#     return "TestComponent"


# @pytest.fixture()
# def log_dir(tmp_path: Path) -> Path:
#     # We create a dedicated directory per test run
#     return tmp_path / "logs"


# # ---------------------------------------------------------------------------
# # setup_logger tests
# # ---------------------------------------------------------------------------


# # def test_setup_logger_accepts_str_log_level(
# #     log_dir: Path,
# #     component_name: str,
# # ) -> None:
# #     """
# #     setup_logger should accept a string log level and configure handlers correctly.
# #     """
# #     _reset_logger(component_name)

# #     logger = setup_logger(
# #         component=component_name,
# #         log_dir=log_dir,
# #         log_level="DEBUG",
# #     )

# #     # Logger level is taken from the string value
# #     assert logger.level == logging.DEBUG

# #     # We expect 2 RotatingFileHandlers: main + error
# #     file_handlers = [
# #         h for h in logger.handlers if isinstance(h, RotatingFileHandler)
# #     ]
# #     assert len(file_handlers) == 2

# #     main_handler = next(
# #         h for h in file_handlers if not h.baseFilename.endswith(".error.log")
# #     )
# #     error_handler = next(
# #         h for h in file_handlers if h.baseFilename.endswith(".error.log")
# #     )

# #     # Paths are configured under the provided log_dir
# #     assert Path(main_handler.baseFilename).parent == log_dir
# #     assert Path(main_handler.baseFilename).name == f"{component_name}.log"

# #     assert Path(error_handler.baseFilename).parent == log_dir / "error"
# #     assert Path(error_handler.baseFilename).name == f"{component_name}.error.log"

# #     # Levels: main handler uses the effective level; error handler logs ERROR only
# #     assert main_handler.level == logging.DEBUG
# #     assert error_handler.level == logging.ERROR

# #     # No propagation to root logger
# #     assert logger.propagate is False


# # def test_setup_logger_accepts_int_log_level(
# #     log_dir: Path,
# #     component_name: str,
# # ) -> None:
# #     """
# #     setup_logger should accept an int log level and configure handlers correctly.
# #     """
# #     _reset_logger(component_name)

# #     int_level = logging.WARNING

# #     logger = setup_logger(
# #         component=component_name,
# #         log_dir=log_dir,
# #         log_level=int_level,
# #     )

# #     # Logger level directly equals the int level
# #     assert logger.level == int_level

# #     # We expect 2 RotatingFileHandlers: main + error
# #     file_handlers = [
# #         h for h in logger.handlers if isinstance(h, RotatingFileHandler)
# #     ]
# #     assert len(file_handlers) == 2

# #     main_handler = next(
# #         h for h in file_handlers if not h.baseFilename.endswith(".error.log")
# #     )
# #     error_handler = next(
# #         h for h in file_handlers if h.baseFilename.endswith(".error.log")
# #     )

# #     # Paths are configured under the provided log_dir
# #     assert Path(main_handler.baseFilename).parent == log_dir
# #     assert Path(main_handler.baseFilename).name == f"{component_name}.log"

# #     assert Path(error_handler.baseFilename).parent == log_dir / "error"
# #     assert Path(error_handler.baseFilename).name == f"{component_name}.error.log"

# #     # Levels: main handler uses the int level; error handler logs ERROR only
# #     assert main_handler.level == int_level
# #     assert error_handler.level == logging.ERROR

# #     # No propagation to root logger
# #     assert logger.propagate is False


# # ---------------------------------------------------------------------------
# # BaseErrorHandler.handle tests (sync)
# # ---------------------------------------------------------------------------


# def test_handle_success_returns_value_and_logs_nothing(
#     log_dir: Path,
#     component_name: str,
#     caplog: LogCaptureFixture,
# ) -> None:
#     """handle() should return the function result and not log errors on success."""
#     _reset_logger(component_name)
#     logger = setup_logger(component=component_name, log_dir=log_dir)
#     handler = BaseErrorHandler(component_name=component_name)

#     def add(x: int, y: int) -> int:
#         return x + y

#     with caplog.at_level(logging.ERROR, logger=logger.name):
#         result = handler.handle(add, 3, 7)

#     assert result == 10
#     assert caplog.records == []


# # def test_handle_logs_error_and_does_not_exit_when_exit_on_error_false(
# #     log_dir: Path,
# #     component_name: str,
# #     caplog: LogCaptureFixture,
# # ) -> None:
# #     """
# #     handle() should log errors and NOT raise SystemExit when exit_on_error=False.
# #     """
# #     _reset_logger(component_name)
# #     logger = setup_logger(component=component_name, log_dir=log_dir)
# #     handler = BaseErrorHandler(component_name=component_name, exit_on_error=False)

# #     def boom() -> None:
# #         raise ValueError("bad value")

# #     with caplog.at_level(logging.ERROR, logger=logger.name):
# #         result = handler.handle(boom)

# #     assert result is None

# #     messages = [record.getMessage() for record in caplog.records]
# #     assert any("ValueError" in msg for msg in messages)
# #     assert any("bad value" in msg for msg in messages)


# # ---------------------------------------------------------------------------
# # BaseErrorHandler.handle_async tests
# # ---------------------------------------------------------------------------


# async def _async_ok(value: int) -> int:
#     """Small async helper returning value * 2."""
#     await asyncio.sleep(0)
#     return value * 2


# async def _async_fail_runtime() -> None:
#     """Async helper that always raises RuntimeError."""
#     await asyncio.sleep(0)
#     raise RuntimeError("async boom")


# def test_handle_async_success_returns_value_and_logs_nothing(
#     log_dir: Path,
#     component_name: str,
#     caplog: LogCaptureFixture,
# ) -> None:
#     """
#     handle_async() should return the coroutine result and not log errors on success.
#     """
#     _reset_logger(component_name)
#     logger = setup_logger(component=component_name, log_dir=log_dir)
#     handler = BaseErrorHandler(component_name=component_name)

#     with caplog.at_level(logging.ERROR, logger=logger.name):
#         result = _run(handler.handle_async(_async_ok, 5))

#     assert result == 10
#     assert caplog.records == []


# # def test_handle_async_logs_error_and_does_not_exit_when_exit_on_error_false(
# #     log_dir: Path,
# #     component_name: str,
# #     caplog: LogCaptureFixture,
# # ) -> None:
# #     """
# #     handle_async() should log errors and NOT raise SystemExit when exit_on_error=False.
# #     """
# #     _reset_logger(component_name)
# #     logger = setup_logger(component=component_name, log_dir=log_dir)
# #     handler = BaseErrorHandler(component_name=component_name, exit_on_error=False)

# #     # We expect no SystemExit here; if BaseErrorHandler._exit() is called
# #     # with exit_on_error=False, it should *not* call sys.exit().
# #     with caplog.at_level(logging.ERROR, logger=logger.name):
# #         result = _run(handler.handle_async(_async_fail_runtime))

# #     assert result is None

# #     messages = [record.getMessage() for record in caplog.records]
# #     # Your implementation prefixes with an error type; we just assert the
# #     # important parts are present.
# #     assert any("UnexpectedError" in msg or "RuntimeError" in msg for msg in messages)
# #     assert any("async boom" in msg for msg in messages)
