from __future__ import annotations

from pathlib import Path
from typing import Any

import toml


class FileHandler:
    def __init__(self, filepath: Path) -> None:
        self._filepath = filepath
        self._ensure_dir()
        self._last_modified_time = None

    def source_exists(self) -> bool:
        """Check if the file exists."""
        return self._filepath.exists()

    def source_is_modified(self) -> bool:
        """Check if the source file has been modified since the last check."""
        last_modified_time = self._last_modified_time
        current_modified_time = self._get_modified_time()

        return last_modified_time is None or current_modified_time != last_modified_time, current_modified_time

    def load(self) -> dict[str, Any]:
        """Load the settings from the file."""
        self._last_modified_time = self._get_modified_time()
        with Path.open(self._filepath, mode="r", encoding="utf-8") as f:
            return toml.load(f)

    def save(self, data: dict) -> None:
        """Save the settings to the file and update the updated timestamp."""
        with Path.open(self._filepath, mode="w", encoding="utf-8") as f:
            toml.dump(data, f)
        self._last_modified_time = self._get_modified_time()

    def _get_modified_time(self) -> float:
        """Get the last modified time of the file."""
        return self._filepath.stat().st_mtime

    def _ensure_dir(self) -> None:
        """Ensure the directory for the file path exists."""
        self._filepath.parent.mkdir(parents=True, exist_ok=True)
