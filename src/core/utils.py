import json
from datetime import datetime
from typing import Any, Dict
from loguru import logger


def safe_json_dumps(data: Dict[str, Any]) -> str:
    """
    Safely converts a Python dict into a pretty JSON string.
    Useful for logging, MCP responses, and debugging.
    """
    try:
        return json.dumps(data, indent=4, sort_keys=True)
    except Exception as e:
        logger.error(f"[utils] JSON serialization failed: {e}")
        return "{}"


def timestamp() -> str:
    """Returns the current timestamp in ISO format."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def validate_id(id_str: str) -> bool:
    """
    Validates whether a string looks like a UUID.
    Does not guarantee correctness but filters out obvious invalid cases.
    """
    if not isinstance(id_str, str):
        return False
    return len(id_str) >= 8  # light validation for simplicity


def pretty_print(obj: Any) -> None:
    """Prints objects with loguru formatting."""
    logger.info(f"\n{str(obj)}\n")
