import shutil
from pathlib import Path

import pytest
import toml

from mooch.settings.filehandler import CREATED_KEY, NOTICE, UPDATED_KEY, FileHandler


@pytest.fixture
def temp_settings_file(tmp_path):
    file_path = tmp_path / "settings.toml"
    yield file_path
    if file_path.exists():
        file_path.unlink()
    shutil.rmtree(tmp_path, ignore_errors=True)


def test_create_file_if_not_exists_creates_file_with_metadata(temp_settings_file):
    file = FileHandler(temp_settings_file)
    assert temp_settings_file.exists()
    data = toml.load(temp_settings_file)
    assert data["metadata"]["notice"] == NOTICE
    assert CREATED_KEY.split(".", 1)[1] in data["metadata"]
    assert UPDATED_KEY.split(".", 1)[1] in data["metadata"]


def test_load_returns_correct_data(temp_settings_file):
    file = FileHandler(temp_settings_file)
    # Write some data
    data = {"foo": {"bar": 123}}
    file.save(data)
    loaded = file.load()
    assert loaded["foo"]["bar"] == 123
    assert "metadata" in loaded


def test_save_updates_updated_timestamp(temp_settings_file):
    file = FileHandler(temp_settings_file)
    data = file.load()
    old_updated = data["metadata"]["updated"]
    # Wait a moment to ensure timestamp changes
    import time

    time.sleep(0.01)
    file.save(data)
    new_data = file.load()
    assert new_data["metadata"]["updated"] != old_updated


def test_save_and_load_roundtrip(temp_settings_file):
    file = FileHandler(temp_settings_file)
    data = {"alpha": 1, "beta": {"gamma": 2}}
    file.save(data)
    loaded = file.load()
    assert loaded["alpha"] == 1
    assert loaded["beta"]["gamma"] == 2
    assert "metadata" in loaded


def test_create_file_if_not_exists_does_not_overwrite_existing(temp_settings_file):
    # Create file manually
    with Path.open(temp_settings_file, "w", encoding="utf-8") as f:
        f.write('[custom]\nkey="value"\n')
    file = FileHandler(temp_settings_file)
    data = file.load()
    assert "custom" in data
    assert data["custom"]["key"] == "value"
