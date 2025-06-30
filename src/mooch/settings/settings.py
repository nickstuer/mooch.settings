from __future__ import annotations

from pathlib import Path
from typing import Any

from mooch.settings.filehandler import FileHandler
from mooch.settings.utils import get_nested, set_nested


class Settings:
    def __init__(
        self,
        settings_filepath: Path,
        default_settings: dict | None = None,
        *,
        dynamic_reload: bool = True,
    ) -> None:
        if not isinstance(settings_filepath, Path):
            error_message = "settings_filepath must be a Path object"
            raise TypeError(error_message)
        if not isinstance(default_settings, dict) and default_settings is not None:
            error_message = "default_settings must be a dictionary or None"
            raise TypeError(error_message)

        self._settings_filepath = settings_filepath
        self._file = FileHandler(self._settings_filepath)
        self.dynamic_reload = dynamic_reload

        self._data = self._file.load()

        if default_settings:
            self._set_defaults(default_settings)
            self._file.save(self._data)

    def get(self, key: str) -> Any | None:  # noqa: ANN401
        """Return a value from the configuration by key.

        Args:
        key (str): The key to return a value from.

        Returns:
        Any | None: The value associated with the key, or None if the key does not exist.

        """
        if self.dynamic_reload:
            self._data = self._file.load()
        return get_nested(self._data, key)

    def set(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Set a value in the configuration by key.

        Args:
        key (str): The key to store the value under.
        value (Any): The value to set for the key.

        Returns:
        None

        """
        set_nested(self._data, key, value)
        self._file.save(self._data)

    def __getitem__(self, key: str) -> Any | None:  # noqa: ANN401
        """Get an item from the configuration by key."""
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Set an item in the configuration by key."""
        self.set(key, value)

    def _set_defaults(self, d: dict, parent_key: str = "") -> None:
        for k, v in d.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            if self.get(full_key) is None:
                self.set(full_key, v)

            elif isinstance(v, dict):
                self._set_defaults(v, full_key)

    def __repr__(self) -> str:  # noqa: D105
        return f"Settings Stored at: {self._settings_filepath}"
