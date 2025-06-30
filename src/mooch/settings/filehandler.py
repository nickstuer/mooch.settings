from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import toml

from mooch.settings.utils import set_nested

NOTICE_KEY = "metadata.notice"
NOTICE = "This file was created by mooch.settings."
CREATED_KEY = "metadata.created"
UPDATED_KEY = "metadata.updated"


class FileHandler:
    def __init__(self, settings_filepath: Path) -> None:
        self._filepath = settings_filepath
        if not self._filepath.exists():
            self.create_file_and_directories()

    def create_file_and_directories(self) -> None:
        """Create the settings file and directories."""
        # Ensure the parent directory exists
        self._filepath.parent.mkdir(parents=True, exist_ok=True)
        data = {}
        set_nested(data, NOTICE_KEY, NOTICE)
        set_nested(data, CREATED_KEY, datetime.now(tz=timezone.utc).isoformat())
        set_nested(data, UPDATED_KEY, datetime.now(tz=timezone.utc).isoformat())

        self.save(data)

    def load(self) -> dict[str, Any]:
        """Load the settings from the file."""
        with Path.open(self._filepath, mode="r", encoding="utf-8") as f:
            return toml.load(f)

    def save(self, data: dict) -> None:
        """Save the settings to the file and update the updated timestamp."""
        set_nested(data, UPDATED_KEY, datetime.now(tz=timezone.utc).isoformat())
        with Path.open(self._filepath, mode="w", encoding="utf-8") as f:
            toml.dump(data, f)
