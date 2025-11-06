# Environment detection (ENV_STAGE)
# Secret loading via environment variables (injected by Cloud Run)
# Logging setup
# Config validation


import os
import logging

def get_env_stage():
    """Returns the current environment stage: dev or prod (default: dev)."""
    return os.getenv("ENV_STAGE", "dev")

def get_config():
    """Returns environment-specific configuration dictionary."""
    stage = get_env_stage()

    if stage == "prod":
        return {
            "agent_api_key": os.getenv("AGENT_API_KEY"),
            "log_level": "INFO",
            "timeout": 30,
            "debug_mode": False,
        }
    else:
        return {
            "agent_api_key": os.getenv("AGENT_API_KEY_DEV"),
            "log_level": "DEBUG",
            "timeout": 10,
            "debug_mode": True,
        }

def validate_config(config):
    """Ensures required keys are present and not empty."""
    required_keys = ["agent_api_key"]
    for key in required_keys:
        if not config.get(key):
            raise ValueError(f"Missing required config: {key}")

def setup_logging(log_level):
    """Configures logging based on environment."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
