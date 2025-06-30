from __future__ import annotations

from typing import Any


def set_nested(d: dict, key: str, value: Any, sep: str = ".") -> None:  # noqa: ANN401
    """Set a nested value in a dictionary by key."""
    keys = key.split(sep)
    for k in keys[:-1]:
        if k not in d or not isinstance(d[k], dict):
            d[k] = {}
        d = d[k]
    d[keys[-1]] = value


def get_nested(d: dict, key: str, sep: str = ".") -> Any | None:  # noqa: ANN401
    """Get a nested value from a dictionary by key."""
    keys = key.split(sep)
    for k in keys:
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            return None
    return d
