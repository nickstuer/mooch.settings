from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def is_valid_key(key: str) -> bool:
    # Bare keys: a-z, A-Z, 0-9, _, -, no quotes or spaces
    # No support for keys with nested quotes
    return bool(re.fullmatch(r"[A-Za-z0-9_-]+", key))


def set_nested(d: dict, key: str, value: Any, sep: str = ".") -> None:  # noqa: ANN401
    """Set a nested value in a dictionary by key."""
    keys = key.split(sep)
    for k in keys[:-1]:
        if not is_valid_key(k):
            error_msg = (
                f"Invalid key: '{k}'. "
                "Keys must be alphanumeric, underscores, or dashes, "
                "and cannot contain spaces or quotes."
            )
            raise ValueError(error_msg)

        if k not in d or not isinstance(d[k], dict):
            d[k] = {}
        d = d[k]
    if not is_valid_key(keys[-1]):
        error_msg = (
            f"Invalid key: '{keys[-1]}'. "
            "Keys must be alphanumeric, underscores, or dashes, "
            "and cannot contain spaces or quotes."
        )
        raise ValueError(error_msg)
    d[keys[-1]] = value


def get_nested(d: dict, key: str, sep: str = ".") -> Any | None:  # noqa: ANN401
    """Get a nested value from a dictionary by key."""
    keys = key.split(sep)
    for k in keys:
        if not is_valid_key(k):
            error_msg = (
                f"Invalid key: '{k}'. "
                "Keys must be alphanumeric, underscores, or dashes, "
                "and cannot contain spaces or quotes."
            )
            raise ValueError(error_msg)
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            return None
    return d


def has_file_changed(filepath: Path, last_modified_time: float | None = None) -> tuple[bool, float]:
    current_modified_time = Path(filepath).stat().st_mtime

    return last_modified_time is None or current_modified_time != last_modified_time, current_modified_time
