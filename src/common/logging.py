import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(component: str, log_level: str = "INFO") -> logging.Logger:
    """
    Creates a reusable logger for any component (good, bad, evil).
    """

    logger = logging.getLogger(component)
    logger.setLevel(log_level.upper())

    # Prevent duplicate handlers if logger is already configured
    if logger.handlers:
        return logger

    # -----------------------------
    # Format
    # -----------------------------
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # -----------------------------
    # Console handler
    # -----------------------------
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # -----------------------------
    # File handler (rotating)
    # logs/<component>.log
    # -----------------------------
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    file_handler = RotatingFileHandler(
        filename=log_dir / f"{component}.log",
        maxBytes=5_000_000,  # 5 MB
        backupCount=3,  # keep 3 old log files
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
