import logging
import os


# --- Environment Detection ---
def get_env_stage() -> str:
    """Returns the current environment stage: dev or prod (default: dev)."""
    return os.getenv("ENV_STAGE", "dev").strip().lower()


# --- Config Loader ---
def get_config() -> dict:
    """Returns validated configuration dictionary based on environment stage."""
    stage = get_env_stage()

    config = {
        "agent_api_key": os.getenv(
            "AGENT_API_KEY" if stage == "prod" else "AGENT_API_KEY_DEV"
        ),
        "log_level": "INFO" if stage == "prod" else "DEBUG",
        "timeout": 30 if stage == "prod" else 10,
        "debug_mode": stage != "prod",
    }

    validate_config(config)
    return config


# --- Config Validation ---
def validate_config(config: dict):
    """Ensures required config keys are present and non-empty."""
    required_keys = ["agent_api_key"]
    missing = [key for key in required_keys if not config.get(key)]
    if missing:
        raise RuntimeError(f"Missing required config keys: {', '.join(missing)}")


# --- Logging Setup ---
def setup_logging(log_level: str):
    """Initializes logging with fallback for Cloud Run environments."""
    try:
        level = getattr(logging, log_level.upper())
    except AttributeError:
        level = logging.INFO
        logging.warning(f"Invalid log level '{log_level}', defaulting to INFO.")

    # Avoid duplicate handlers in Cloud Run or preconfigured environments
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )
