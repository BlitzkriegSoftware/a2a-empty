import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(component: str, log_level: str = "INFO") -> logging.Logger:
    """
    Create or return a reusable logger for any component (good, bad, evil).
    Writes:
      - all logs to logs/<component>.log
      - errors only to logs/error/<component>.error.log
      - also logs to console
    """

    logger = logging.getLogger(component)
    logger.setLevel(log_level.upper())
    logger.propagate = False  # don't duplicate logs to root logger

    # If already configured, just return it
    if logger.handlers:
        return logger

    # -----------------------------
    # Paths
    # -----------------------------
    log_dir = Path("logs")
    error_dir = log_dir / "error"
    log_dir.mkdir(exist_ok=True)
    error_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # Formatter
    # -----------------------------
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # -----------------------------
    # Console handler
    # -----------------------------
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # -----------------------------
    # Main log file (all levels)
    # -----------------------------
    file_handler = RotatingFileHandler(
        filename=log_dir / f"{component}.log",
        maxBytes=5_000_000,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(log_level.upper())
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # -----------------------------
    # Error-only log file
    # -----------------------------
    error_file_handler = RotatingFileHandler(
        filename=error_dir / f"{component}.error.log",
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    logger.addHandler(error_file_handler)

    return logger
