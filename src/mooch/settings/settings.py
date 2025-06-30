from __future__ import annotations

from pathlib import Path
from typing import Any

from mooch.settings.file import File
from mooch.settings.utils import get_nested, set_nested


class Settings:
    def __init__(
        self,
        settings_filepath: Path,
        default_settings: dict | None = None,
    ) -> None:
        self._file = File(settings_filepath)
        self.dynamic_reload = True

        self._data = self._file.load()

        if default_settings:
            self._set_defaults(default_settings)
            self._file.save(self._data)

    @staticmethod
    def home_directory() -> Path:
        """Return the path to the home directory.

        Returns: Path
        """
        return Path.home()

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
