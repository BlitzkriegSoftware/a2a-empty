import logging
from pathlib import Path

import pytest
from pytest import LogCaptureFixture

from src.common.error_handler import BaseErrorHandler
from src.common.logging import setup_logger


def test_handle_logs_and_creates_log_files(
    temp_cwd: Path, caplog: LogCaptureFixture
) -> None:
    # Arrange
    logger = setup_logger("TestComponent")
    handler = BaseErrorHandler("TestComponent", exit_on_error=False)

    def boom():
        raise ValueError("bad value")

    # Act
    with caplog.at_level(logging.ERROR, logger=logger.name):
        result = handler.handle(boom)

    # Assert: handler returns None on error
    assert result is None

    # Assert: an error was logged
    messages = [record.getMessage() for record in caplog.records]
    assert any("ValueError" in m for m in messages)

    # Assert: log files exist in logs/ and logs/error/
    log_dir = temp_cwd / "logs"
    main_log = log_dir / "TestComponent.log"
    error_log = log_dir / "error" / "TestComponent.error.log"

    assert main_log.exists(), f"Expected main log file at {main_log}"
    assert error_log.exists(), f"Expected error log file at {error_log}"


@pytest.mark.asyncio
async def test_handle_async_logs_and_creates_error_log(
    temp_cwd: Path, caplog: LogCaptureFixture
) -> None:
    # Arrange
    logger = setup_logger("AsyncComponent")
    handler = BaseErrorHandler("AsyncComponent", exit_on_error=False)

    async def boom_async():
        raise RuntimeError("async boom")

    # Act
    with caplog.at_level(logging.ERROR, logger=logger.name):
        result = await handler.handle_async(boom_async)

    # Assert
    assert result is None
    messages = [record.getMessage() for record in caplog.records]
    assert any("RuntimeError" in m for m in messages)

    log_dir = temp_cwd / "logs"
    main_log = log_dir / "AsyncComponent.log"
    error_log = log_dir / "error" / "AsyncComponent.error.log"

    assert main_log.exists()
    assert error_log.exists()


def test_handle_success_returns_value_and_does_not_log_error(
    temp_cwd: Path, caplog: LogCaptureFixture
) -> None:
    # Arrange
    logger = setup_logger("SuccessComponent")
    handler = BaseErrorHandler("SuccessComponent", exit_on_error=True)

    def ok():
        return 42

    # Act
    with caplog.at_level(logging.ERROR, logger=logger.name):
        result = handler.handle(ok)

    # Assert
    assert result == 42
    # No errors should have been logged
    assert len(caplog.records) == 0


@pytest.mark.asyncio
async def test_handle_async_supports_sync_functions(
    temp_cwd: Path, caplog: LogCaptureFixture
) -> None:
    # Arrange
    logger = setup_logger("MixedComponent")
    handler = BaseErrorHandler("MixedComponent", exit_on_error=False)

    def ok_sync():
        return "sync-ok"

    # Act
    with caplog.at_level(logging.ERROR, logger=logger.name):
        result = await handler.handle_async(ok_sync)

    # Assert: returns the sync result and no errors
    assert result == "sync-ok"
    assert len(caplog.records) == 0
