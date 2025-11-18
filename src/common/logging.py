from __future__ import annotations

import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_MAX_BYTES: Final[int] = 5 * 1024 * 1024  # 5 MB
DEFAULT_BACKUP_COUNT: Final[int] = 3

_LEVEL_NAMES: Final[dict[str, int]] = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _to_log_level(level: str | int) -> int:
    """Convert a logging level string or int to a numeric level.

    Falls back to logging.INFO for unknown values.
    """
    if isinstance(level, int):
        return level

    numeric = _LEVEL_NAMES.get(level.upper())
    if numeric is None:
        return logging.INFO
    return numeric


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def setup_logger(
    component: str,
    log_level: str | int = "INFO",
    *,
    log_dir: Path | None = None,
    max_bytes: int = DEFAULT_MAX_BYTES,
    backup_count: int = DEFAULT_BACKUP_COUNT,
) -> Logger:
    """Create or return a reusable logger for a component.

    - All messages -> logs/<component>.log
    - Error messages -> logs/error/<component>.error.log
    - Also logs to console.

    The same logger instance is reused if it already exists.
    """
    base_log_dir = log_dir or Path("logs")
    error_dir = base_log_dir / "error"

    base_log_dir.mkdir(parents=True, exist_ok=True)
    error_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(component)
    effective_level = _to_log_level(log_level)
    logger.setLevel(effective_level)
    logger.propagate = False  # don't duplicate to root logger

    # If already configured, just reuse it
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Main log file (all levels)
    main_log_file = base_log_dir / f"{component}.log"
    file_handler = RotatingFileHandler(
        main_log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Error-only log file
    error_log_file = error_dir / f"{component}.error.log"
    error_file_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    logger.addHandler(error_file_handler)

    return logger
