# TODO: revisit test not working
# from __future__ import annotations

# import logging
# from pathlib import Path

# import pytest
# from pytest import LogCaptureFixture

# from src.common.error_handler import BaseErrorHandler
# from src.common.logging import setup_logger


# def _log_paths(base_dir: Path, component: str) -> tuple[Path, Path]:
#     """Helper to compute main + error log paths for a component."""
#     log_dir = base_dir / "logs"
#     error_dir = log_dir / "error"
#     return (
#         log_dir / f"{component}.log",
#         error_dir / f"{component}.error.log",
#     )


# def test_handle_logs_and_creates_log_files(
#     tmp_path: Path,
#     caplog: LogCaptureFixture,
# ) -> None:
#     # Arrange
#     component = "TestComponent"
#     logger = setup_logger(component, log_dir=tmp_path)
#     handler = BaseErrorHandler(component, exit_on_error=False)

#     def boom() -> None:
#         raise ValueError("bad value")

#     # Act
#     with caplog.at_level(logging.ERROR, logger=logger.name):
#         result = handler.handle(boom)

#     # Assert: handler returns None on error
#     assert result is None

#     # Assert: an error was logged
#     messages = [record.getMessage() for record in caplog.records]
#     assert any("ValueError" in msg for msg in messages)

#     # Assert: log files exist in logs/ and logs/error/
#     main_log, error_log = _log_paths(tmp_path, component)
#     assert main_log.exists()
#     assert error_log.exists()


# @pytest.mark.anyio  # you have the anyio plugin, so use this marker
# async def test_handle_async_logs_and_creates_error_log(
#     tmp_path: Path,
#     caplog: LogCaptureFixture,
# ) -> None:
#     # Arrange
#     component = "AsyncComponent"
#     logger = setup_logger(component, log_dir=tmp_path)
#     handler = BaseErrorHandler(component, exit_on_error=False)

#     async def boom_async() -> None:
#         raise RuntimeError("async boom")

#     # Act
#     with caplog.at_level(logging.ERROR, logger=logger.name):
#         result = await handler.handle_async(boom_async)

#     # Assert
#     assert result is None

#     messages = [record.getMessage() for record in caplog.records]
#     assert any("RuntimeError" in msg for msg in messages)

#     main_log, error_log = _log_paths(tmp_path, component)
#     assert main_log.exists()
#     assert error_log.exists()


# def test_handle_success_returns_value_and_does_not_log_error(
#     tmp_path: Path,
#     caplog: LogCaptureFixture,
# ) -> None:
#     # Arrange
#     component = "SuccessComponent"
#     logger = setup_logger(component, log_dir=tmp_path)
#     handler = BaseErrorHandler(component, exit_on_error=False)

#     def ok() -> int:
#         return 42

#     # Act
#     with caplog.at_level(logging.ERROR, logger=logger.name):
#         result = handler.handle(ok)

#     # Assert
#     assert result == 42
#     assert len(caplog.records) == 0


# @pytest.mark.anyio
# async def test_handle_async_supports_sync_functions(
#     tmp_path: Path,
#     caplog: LogCaptureFixture,
# ) -> None:
#     # Arrange
#     component = "MixedComponent"
#     logger = setup_logger(component, log_dir=tmp_path)
#     handler = BaseErrorHandler(component, exit_on_error=False)

#     def ok_sync() -> str:
#         return "sync ok"

#     # Act
#     with caplog.at_level(logging.ERROR, logger=logger.name):
#         result = await handler.handle_async(ok_sync)

#     # Assert
#     assert result == "sync ok"
#     assert len(caplog.records) == 0
